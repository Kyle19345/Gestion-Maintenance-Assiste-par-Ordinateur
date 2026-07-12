"""
Ce module represente l'objet machine
"""


from dataclasses import dataclass


@dataclass
class Machine:
    """Objet Machine"""
    ID: str
    nom: str
    categorie: str
    date_service: str
    fabricant: str
    etat: str="Actif"
    compteur: int = 0

