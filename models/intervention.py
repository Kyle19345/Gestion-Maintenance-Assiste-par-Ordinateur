"""
Ce module représente une Intervention assigné
à une machine.
"""
# TODO: Source de vérité principal

from dataclasses import dataclass, field
from uuid import uuid4, UUID

@dataclass
class Intervention:
    """Intervention assigné à une machine"""
    intervention_id : str = field(default_factory=lambda: str(uuid4()))
    ref: str = ""
    description: str = ""
    date_intervention: str = ""
    machine_id: str = ""
    dure: int = ""
    outils: str = ""
    executant: str = ""
    statut: str = "Planifié"

if __name__ == "__main__":
    intervention = Intervention()
    print(intervention.ref)
