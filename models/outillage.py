from dataclasses import dataclass, field
from uuid import uuid4
from enum import Enum


class StatutOutillage(Enum):
    UTILISE = "Utilisé"
    EN_STOCK = "En_stock"


@dataclass
class Outillage:
    outillage_id: str = field(default_factory=lambda: str(uuid4()))
    nom: str = ""
    statut: StatutOutillage = StatutOutillage.EN_STOCK.value
