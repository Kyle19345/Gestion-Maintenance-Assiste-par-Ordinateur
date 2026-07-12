"""
Orchestre l'intervention controller, machine controller
et l'interface principal du programme.
"""
# TODO:
# Injection dépendances
# Meilleur gestion des erreurs


import customtkinter as ctk
import logging

from models.basededonne import BaseDeDonne
from controller.interventioncontroller import InterventionController
from controller.machinecontroller import MachineController

from views.sidebarView import Sidebar,Header


logger = logging.getLogger(__name__)


class MainController:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.database = BaseDeDonne()
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        side = Sidebar(self.master, self)
        side.grid(
            row=1,
            column=0,
            pady=(0, 10),
            padx=(10, 0),
            sticky="nsew"
        )

        head = Header(self.master)
        head.grid(
            row=0,
            columnspan=2,
            padx=10,
            pady=(10, 0),
            sticky="nsew"
        )

        self.intervention = InterventionController(self.master, self.database)
        self.machine = MachineController(self.master, self.database)
        self.show_machine()

        logger.info("Initialisation du controller principal")

    def show_machine(self) -> None:
        """Affiche les machines de la bdd"""
        self.intervention.planing.grid_forget()
        self.intervention.list_intervenetion.grid_forget()
        self.machine.list_machine.grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew"
        )
        self.machine.afficher_machine()

        logger.info("chargement machine efectué")

    def show_intervention(self) -> None:
        """Affiche les intervention de la bdd"""
        self.intervention.planing.grid_forget()
        self.machine.list_machine.grid_forget()
        self.intervention.list_intervenetion.grid(
            row=1,
            column=1,
            padx=(0, 10),
            pady=(0, 10),
            sticky="nsew"
        )
        self.intervention.afficher_intervention()

        logger.info("chargement intervention effectué")

    def show_planing(self) -> None:
        """Affiche les interventions avec le statut non réalisé."""
        self.machine.list_machine.grid_forget()
        self.intervention.list_intervenetion.grid_forget()
        self.intervention.planing.grid(row=1,column=1,padx=(0,10),pady=(0,10),sticky="nsew")
        self.intervention.afficher_planing()

        logger.info("Chargement planing effectué")

    def on_close(self) -> None:
        """Ferme l'interface"""
        try :
            self.database.close()
        except:
            logger.exception("Erreur lors de la fermeture de la DB")
        self.master.destroy()
        logger.info("Fermeture de l'application effectué")
