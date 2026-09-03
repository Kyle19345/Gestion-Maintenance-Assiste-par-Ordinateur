from abc import ABC, abstractmethod
from typing import Dict

from views.messageView import MessageBox
from config.tool import check_date_valide, check_champ_vide, check_number


class BaseController(ABC):
    def __init__(self, master, database):
        self.master = master
        self.database = database

    def check_data(
            self,
            data: Dict[str, str],
            date: str,
            number: str
    ) -> bool:
        if not check_champ_vide(data):
            MessageBox(
                self.master,
                "Veuillez remplir tous les champs",
                type="error"
            )
            return False

        if not check_date_valide(date):
            MessageBox(
                self.master,
                "La date saisie est invalide",
                type="error"
            )
            return False

        if not check_number(number):
            MessageBox(
                self.master,
                "Veuillez saisir un nombre entier",
                type="error"
            )
            return False
        return True
