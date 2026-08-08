"""
Ce module représente une Intervention assigné
à une machine.
"""
# TODO: Source de vérité principal

from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum


class StatutIntervention(Enum):
    PLANIFIE = "Planifié"
    EN_COURS = "En cours"
    REALISE = "Réalisé"


@dataclass
class Intervention:
    """Intervention assigné à une machine"""
    intervention_id : str = field(default_factory=lambda: str(uuid4()))
    ref: str = ""
    description: str = ""
    date_intervention: str = ""
    machine_id: str = None
    dure: int = ""
    outils: str = ""
    executant: str = ""
    statut: StatutIntervention = StatutIntervention.PLANIFIE.value


if __name__ == "__main__":
    intervention = Intervention()
    print(intervention.statut)
