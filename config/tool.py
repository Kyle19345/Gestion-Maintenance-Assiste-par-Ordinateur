from datetime import datetime
from typing import Dict


def check_date_valide(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    
    except:
        return False

def check_champ_vide(donnes: Dict[str, str]) -> bool:
    for donne in donnes.values():
        if not donne:
            return False

    return True

def check_number(n) -> bool:
    try:
        number = int(n)
        return True

    except (TypeError, ValueError):
        return False


