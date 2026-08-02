"""
Ce module represente l'objet machine
"""

# TODO:
# Ajouter d'autre données dans machine

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Machine:
    """Objet Machine"""
    machine_id: str = field(default_factory=lambda: str(uuid4()))
    ref: str = ""
    nom: str = ""
    categorie: str = ""
    date_service: str = ""
    fabricant: str = ""
    etat: str = "Actif"
    compteur: int = 0

if __name__ == "__main__":
    machine1 = Machine()
    machine2 = Machine

    print(machine1.machine_id)
    print(machine2.machine_id)