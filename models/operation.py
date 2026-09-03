"""
Ce module decrit les operations a effectué dans un OT
"""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Operation:
    operation_id: str = field(default_factory=lambda: str(uuid4()))
    description: str = ""
    sous_operation: str = ""
    personnel_id: str = None
    outillage_id: str = None
    date_intervention: str = ""
    date_fin_prevue: str = ""


if __name__ == "__main__":
    operation = Operation()
    print(operation.operation_id)
