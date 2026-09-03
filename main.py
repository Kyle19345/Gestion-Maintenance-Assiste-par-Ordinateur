"""
Point d'entrée principale du programme.
"""
# TODO: Injection des dépendances


import customtkinter as ctk
from logger_config import setup_logging
import logging

from controller.main_controller import MainController
from models.database import BaseDeDonne
from views.sider_bar_view import Sidebar, Header


DEBUG_MODE = True
setup_logging(debug=DEBUG_MODE)

ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("dark-blue")

logger = logging.getLogger(__name__)
logger.info("Demarrage de l'application")


root = ctk.CTk()
root.title("GMAO")
root.resizable(False, False)

database = BaseDeDonne()

app = MainController(master=root, database=database)

root.protocol("WM_DELETE_WINDOW",app.on_close)

root.mainloop()
