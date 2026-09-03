"""
Orchestre les opérations effectués sur les machines
depuis l'interface à la base de donné.
"""
# TODO:
# Injection des dépendances
# Getsion des erreurs
# Refactorisation 
# Utiliser la classe Machine commme source de vérité

import customtkinter as ctk
import logging

from typing import Dict

from controller.base_controller import BaseController

from views.machine_view.machine_view import ListMachine
from views.machine_view.add_machine_view import addMachine
from views.messageView import MessageBox, ConfirmationBox

from models.machine import Machine
from models.database import BaseDeDonne, DuplicateReferenceError, PrimaryKeyError


logger = logging.getLogger(__name__)


class MachineController(BaseController):
    def __init__(
            self,
            master: ctk.CTk,
            database: BaseDeDonne
    ):
        super().__init__(master, database)
        self.list_machine = ListMachine(
            master,
            show_add = self.show_add,
            on_select = self.show_update
        )
        logger.info("Initialisation de machine controller")

    def show_update(self, machine: Machine) -> None:
        """Met à jour une machine"""
        self.update_machine = addMachine(
            self.master,
            on_add=self.enregistrer_maj,
            on_suppr=self.suppr_machine
        )

        list_intervention = self.database.get_intervention_asset(machine.machine_id)
        self.update_machine.afficher(machine, list_intervention)
        logger.info("Maj des informations récupérer et afficher")

    def show_add(self) -> None:
        """Affiche une interface pour ajouter une machine"""
        self.add_machine = addMachine(
            self.master,
            on_add=self.ajouter_machine
        )
        logger.info("Interface ajout machine initialisé")

    def enregistrer_maj(self) -> None:
        """Enregistre les maj de donné de l'interface vers la bdd"""
        donne = self.update_machine.get_entre_with_etat()

        if not self.check_data(
            data=donne,
            date=donne["date_service"],
            number=donne["compteur"]
        ):
            return

        machine = Machine(**donne)

        try:
            self.database.update_machine(machine)

        except DuplicateReferenceError:
            MessageBox(
                self.master,
                "La reference saisie est invalide",
                type="error"
            )
            logger.error("""Erreur lors de la mise à jour de la machine""")

        except PrimaryKeyError:
            MessageBox(
                self.master,
                "L'ID saisie est invalide",
                type="error"
            )
            logger.error("""Erreur lors de la mise à jour de la machine""")

        logger.info("Machine %s", machine)
        MessageBox(
            self.master,
            "Mise à jour de la machine effectué",
            type="success"
        )
        self.afficher_machine()

    def ajouter_machine(self) -> None:
        """
        Ajoute les informations entré dans l'interface vers
        la bdd
        """
        donne = self.add_machine.get_entre()

        if not self.check_data(
            data=donne,
            date=donne["date_service"],
            number=donne["compteur"]
        ):
            return

        machine = Machine(**donne)
        # Attraper l'erreur dans la base de donné
        try:
            self.database.add_machine(machine)
           
        except DuplicateReferenceError:
            MessageBox(
                self.master,
                "La reference saisie est invalide",
                type="error"
            )
            logger.error("""Erreur lors de l'ajout de la machine""")

        except PrimaryKeyError:
            MessageBox(
                self.master,
                "L'ID saisie est invalide",
                type="error"
            )
            logger.error("""Erreur lors de l'ajout de la machine""")
           
        logger.info("Machine %s", machine)
        MessageBox(
            self.master,
            "Machine Enregistrer",
            type="success"
        )
        self.afficher_machine()

    def afficher_machine(self) -> None:
        """
        Récupère les donnés de la table machine et les affiche
        dans l'interface.
        """
        donne = self.database.get_all_machine()
        self.list_machine.afficher(donne)

    def suppr_machine(self) -> ConfirmationBox:
        """
        Affiche l'interface pour la suppression de machine
        """
        ConfirmationBox(self.master, on_valid=self.confirm_suppr)

    def confirm_suppr(self) -> None:
        """Supprime une ligne dans la bdd"""
        machine_id = self.update_machine.get_machine_delete()
        self.database.delete_machine(machine_id)
        self.update_machine.destroy()
        self.afficher_machine()
        logger.info(f"Machine {machine_id} supprimé")
