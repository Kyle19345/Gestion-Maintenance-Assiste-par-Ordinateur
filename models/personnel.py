"""
Ce module decrit l'ensemble des personnels.
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Personnel:
    personnel_id: str = field(default_factory = lambda: str(uuid4()))
    matricule: str = ""
    nom: str = ""
    prenom: str = ""
    num_securite_social: str = ""
    competences: str = ""


if __name__ == "__main__":
    personnel = Personnel()
    print(personnel.personnel_id)
