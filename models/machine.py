"""
Ce module represente l'objet machine
"""

# TODO:
# Ajouter d'autre données dans machine

from dataclasses import dataclass, field, asdict, fields
from uuid import uuid4
from enum import Enum


class EtatMachine(Enum):
    ACTIF = "Actif"
    EN_MAINTENANCE = "En maintenance"
    EN_PANNE = "En panne"


@dataclass
class Machine:
    """Objet Machine"""
    machine_id: str = field(default_factory=lambda: str(uuid4()))
    ref: str = ""
    nom: str = ""
    categorie: str = ""
    sous_equipement_id: str = None
    fiche_technique: str = ""
    fabricant: str = ""
    etat: EtatMachine = EtatMachine.ACTIF.value
    compteur: int = 0
    date_service: str = ""
    criticite: str = ""

    def __post_init__(self):
        self.compteur = int(self.compteur)


if __name__ == "__main__":
    machine1 = Machine()
    machine2 = Machine()

    print(machine1.machine_id)
    print(machine2.machine_id)

    print(asdict(machine1))


