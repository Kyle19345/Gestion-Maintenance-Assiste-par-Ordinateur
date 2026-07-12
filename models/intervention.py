"""
Ce module représente une Intervention assigné
à une machine.
"""

from dataclasses import dataclass


@dataclass
class Intervention:
    """Intervention assigné à une machine"""
    ref: str
    description: str
    date_intervention: str
    machine: str
    dure: int
    outils: str
    executant: str
    statut: str="Planifié"

