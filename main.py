"""
Point d'entrée principale du programme.
"""
# TODO: Injection des dépendances


import customtkinter as ctk
from logger_config import setup_logging
import logging

from controller.maincontroller import MainController

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")

DEBUG_MODE = True
setup_logging(debug=DEBUG_MODE)

logger = logging.getLogger(__name__)
logger.info("Demarrage de l'application")

root = ctk.CTk()
root.title("GMAO")
root.resizable(False, False)
app = MainController(root)
root.protocol("WM_DELETE_WINDOW",app.on_close)

root.mainloop()
