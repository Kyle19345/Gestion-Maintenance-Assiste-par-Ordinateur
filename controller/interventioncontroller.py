"""
Orchestre les opérations effectués sur les interventions
depuis les interfaces graphiques vers la table intervention.
"""
# TODO:
# Injection des dépendance
# Amélioration des logs et des gestion d'erreurs


import customtkinter as ctk
import logging

from views.addIntervention import InterventionView
from views.ListIntervention import ListIntervention
from views.planingView import Planing
from views.messageView import MessageBox, ConfirmationBox

from models.basededonne import BaseDeDonne
from models.intervention import Intervention
from config.tool import est_date_valide


logger = logging.getLogger(__name__)


class InterventionController:
    def __init__(self, master: ctk.CTk, database: BaseDeDonne):
        self.master = master
        self.database = database
        self.list_intervenetion = ListIntervention(
            self.master,
            on_search=self.find_intervention
        )
        self.planing = Planing(
            self.master,
            on_select=self.show_update,
            on_add=self.show_add
        )
        logger.info("Initialisation de intervention controller")

    def show_update(self, intervention: Intervention) -> None:
        """Affiche les maj des intervnetions"""
        self.update_intervention = InterventionView(
            self.master,
            ajouter=self.enregistrer_maj,
            on_suppr=self.suppr_intervention
        )
        self.update_intervention.afficher(intervention)
        logger.info("Mise à jour intervention afficher")

    def show_add(self) -> InterventionView:
        """Affiche la fenetre pour ajouter une intervention"""
        self.add_intervention = InterventionView(
            self.master,
            ajouter=self.ajouter_intervention
        )
        logger.info("Fenetre ajout intervention afficher")

    def enregistrer_maj(self) -> None:
        """
        Récupère les informations entrées dans la Vue,
        les vérifies et met à jour la BDD.
        """
        donne = self.update_intervention.get_entre_with_statut()
        for entry in donne.values():
            if not entry:
                MessageBox(
                    self.master,
                    "Veuillez remplir tous les champs",
                    type="error"
                )
                return

        try:
            dure = int(donne.get("dure", 0))

        except (TypeError, ValueError):
            MessageBox(
                self.master,
                "La durée doit etre un nombre entier",
                type="error"
            )
            return

        valide = est_date_valide(donne["date"])

        if not valide:
            MessageBox(
                self.master,
                "La date saisie est invalide",
                type="error"
            )
            return

        intervention = Intervention(
            ref=donne["ref"],
            description=donne["description"],
            date_intervention=donne["date"],
            machine=donne["machine"],
            dure=dure,
            outils=donne["outils"],
            executant=donne["executant"],
            statut=donne["statut"]
        )

        try:
            logger.info("Intervention: %s", intervention)
            self.database.update_intervention(intervention)
            MessageBox(
                self.master,
                "Intervention mise à jour",
                type='success'
            )
            self.afficher_planing()

        except Exception as e:
            MessageBox(
                self.master,
                f"Erreur {e}",
                type="error"
            )
            logger.error(f"Une erreur {e} de la mise a jour des données")

    def ajouter_intervention(self) -> None:
        """Ajoute une ligne dans la table intervention"""
        donne = self.add_intervention.get_entre()
        for entry in donne.values():
            if not entry:
                MessageBox(
                    self.master,
                    "Veuillez remplir tous les champs",
                    type="error"
                )
                return

        try:
            dure = int(donne.get("dure", 0))

        except (TypeError, ValueError):
            MessageBox(
                self.master,
                "La dure doit etre un nombre entier",
                type="error"
            )
            return

        valide = est_date_valide(donne["date"])
        if not valide:
            MessageBox(
                self.master,
                "La date saisie est invalide",
                type="error"
            )
            return

        intervention = Intervention(
            ref=donne["ref"],
            description=donne["description"],
            date_intervention=donne["date"],
            machine=donne["machine"],
            dure=dure,
            outils=donne["outils"],
            executant=donne["executant"]
        )

        try:
            logger.info("Intervention: %s", intervention)
            self.database.add_intervention(intervention)
            self.add_intervention.suppression_champ()
            MessageBox(
                self.master,
                "Intervention enregistrée",
                type="success"
            )
            self.afficher_planing()

        except Exception as e:
            MessageBox(
                self.master,
                "Référence ou machine invalide",
                type="error"
            )
            logger.error(f"Erreur {e} lors de l'ajout de machine.")

    def afficher_intervention(self) -> None:
        """Affiche les interventions enregistrés dans la Base de donné."""
        donne = self.database.get_all_intervention()
        self.list_intervenetion.afficher(donne)
        logger.info("Listes d'intervention chargé")

    def afficher_planing(self) -> None:
        """
        Affcihe les interventions enregistré avec le statut
        non réalisé dans la Base de donné.
        """
        donne = self.database.get_planing()
        self.planing.afficher(donne)
        logger.info("Planing chargé")

    def suppr_intervention(self) -> ConfirmationBox:
        """Affiche une interface pour la suppression d'intervention."""
        ConfirmationBox(self.master, on_valid=self.confirm_delete)
        logger.info("affichage interface suppression intervention")

    def confirm_delete(self) -> None:
        """Supprime l'intervention dans la base de donné"""
        intervention = self.update_intervention.suppr_selected()
        self.database.delete_intervention(intervention)
        self.update_intervention.destroy()
        self.afficher_planing()
        logger.info(f"Intervention: {intervention} supprimé")

    def find_intervention(self) -> None:
        """
        Recherche une inrevention dans la bas de donné
        et l'affiche dans l'interface.
        """
        inter = self.list_intervenetion.search_get()
        donne = self.database.find_intervention(inter)
        self.list_intervenetion.grid_forget()
        self.list_intervenetion.grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew"
        )
        self.list_intervenetion.afficher(donne)
        logger.info("Recherche effectué")
