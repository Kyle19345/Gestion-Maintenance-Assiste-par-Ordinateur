from datetime import datetime

def est_date_valide(date_str):
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except Exception as e:
        return False