"""
Orchestre les opérations effectués sur les interventions
depuis les interfaces graphiques vers la table intervention.
"""
# TODO:
# Injection des dépendance
# Amélioration des logs et des gestion d'erreurs
# Corriger les fautes d'orthographesi
# Refactorisation du controller

import customtkinter as ctk
import logging

from controller.base_controller import BaseController

from views.intervention_view.add_intervention_view import addIntervention
from views.intervention_view.intervention_view import ListIntervention
from views.intervention_view.planing_view import Planing
from views.messageView import MessageBox, ConfirmationBox

from models.database import BaseDeDonne, DuplicateReferenceError, PrimaryKeyError
from models.intervention import Intervention


logger = logging.getLogger(__name__)


class InterventionController(BaseController):
    def __init__(
            self,
            master: ctk.CTk,
            database: BaseDeDonne
    ):
        super().__init__(master, database)
        self.list_intervention = ListIntervention(
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
        self.update_intervention = addIntervention(
            self.master,
            ajouter=self.enregistrer_maj,
            on_suppr=self.suppr_intervention
        )
        self.update_intervention.afficher(intervention)
        logger.info("Mise à jour intervention afficher")

    def show_add(self) -> addIntervention:
        """Affiche la fenetre pour ajouter une intervention"""
        self.add_intervention = addIntervention(
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
        if not self.check_data(
            data=donne,
            date=donne["date_intervention"],
            number=donne["dure"]
        ):
            return

        intervention = Intervention(**donne)

        try:
            self.database.update_intervention(intervention)
    
        except DuplicateReferenceError:
            MessageBox(
                self.master,
                "La référence saisie est invalide",
                type="error"
            )
            logger.error("Une erreur de la mise a jour des données")
            return

        except PrimaryKeyError:
            MessageBox(
                self.master,
                "L'id saisie est invalide",
                type="error"
            )
            logger.error("Une erreur de la mise a jour des données")
            return
        
        logger.info("Intervention: %s", intervention)
        MessageBox(
            self.master,
            "Intervention mise à jour",
            type='success'
        )
        self.afficher_planing()

    def ajouter_intervention(self) -> None:
        """Ajoute une ligne dans la table intervention"""
        donne = self.add_intervention.get_entre()
        if not self.check_data(
            data=donne,
            date=donne["date_intervention"],
            number=donne["dure"]
        ):
            return

        intervention = Intervention(**donne)

        try:
            self.database.add_intervention(intervention)

        except DuplicateReferenceError:
            MessageBox(
                self.master,
                "La référence saisie est invalide",
                type="error"
            )
            logger.error("Une erreur de la mise a jour des données")
            return

        except PrimaryKeyError:
            MessageBox(
                self.master,
                "L'id saisie est invalide",
                type="error"
            )
            logger.error("Une erreur de la mise a jour des données")
            return

        logger.info("Intervention: %s", intervention)
        self.add_intervention.suppression_champ()

        MessageBox(
            self.master,
            "Intervention enregistrée",
            type="success"
        )
        
        self.afficher_planing()

    def afficher_intervention(self) -> None:
        """Affiche les interventions enregistrés dans la Base de donné."""
        donne = self.database.get_intervention_realise()
        self.list_intervention.afficher(donne)
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
        ref_intervention = self.update_intervention.suppr_selected()
        self.database.delete_intervention(ref_intervention)
        self.update_intervention.destroy()
        self.afficher_planing()
        logger.info(f"Intervention: {ref_intervention} supprimé")

    def find_intervention(self) -> None:
        """
        Recherche une inrevention dans la bas de donné
        et l'affiche dans l'interface.
        """
        inter = self.list_intervention.search_get()
        donne = self.database.find_intervention(inter)
        self.list_intervention.grid_forget()
        self.list_intervention.grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew"
        )
        self.list_intervention.afficher(donne)
        logger.info("Recherche effectué")
