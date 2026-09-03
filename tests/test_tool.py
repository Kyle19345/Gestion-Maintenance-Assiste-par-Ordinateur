# Test tool

from confest import make_data_machine

from config.tool import check_date_valide, check_champ_vide, check_number
from models.machine import Machine


def test_est_date_valide_invalide_date():
    date = "01/02/20000"
    date2 = "01/Janvier/2000"
    date3 = "01-01/2000"
    date4 = "01-01-2003"
    date5 = "010/01/2003"

    assert check_date_valide(date) == False
    assert check_date_valide(date2) == False
    assert check_date_valide(date3) == False
    assert check_date_valide(date4) == False
    assert check_date_valide(date5) == False

def test_est_date_valide_date_valide():
    date = "01/01/2003"

    assert check_date_valide(date) == True

def test_check_champ_vide():
    donne = {
        "ref": "INT-001",
        "date": "10/08/2026",
        "dure": "2",
        "outils": "Clé",
        "machine": "MCH-001",
        "executant": "Paul",
        "description": ""
    }

    donne = {
        "ref": "INT-001",
        "date": "10/08/2026",
        "dure": 2,
        "outils": "Clé",
        "machine": "MCH-001",
        "executant": None,
        "description": "Mch"
    }

    assert check_champ_vide(donne) == False
    assert check_champ_vide(donne) == False

def test_check_champ_vide_valide():
    donne = {
        "ref": "INT-001",
        "date": "10/08/2026",
        "dure": "2",
        "outils": "Clé",
        "machine": "MCH-001",
        "executant": "Paul",
        "description": "Interventio, MCH-001"
    }

    assert check_champ_vide(donne) == True

def test_check_number():
    number = "Deux"
    number2 = "2.5"

    assert check_number(number) == False
    assert check_number(number2) == False

def test_check_number_valide():
    number = "2"
    number2 = 2.5

    assert check_number(number) == True
    assert check_number(number2) == True

def test_add_machine():
    data = {
        "ref": "MCH-01",
        "nom": "Verin électrique",
        "categorie": "Distribution",
        "date_service": "10/10/2006",
        "fabricant": "Helsinki",
        "compteur": "4"
    }

    machine = Machine(**data)

    assert machine.ref == "MCH-01"
    assert machine.nom == "Verin électrique"
    assert machine.categorie == "Distribution"
    assert machine.date_service == "10/10/2006"


def test_make_machine(make_data_machine):
    data = make_data_machine(
        ref= "MCH-02"
    )
    assert data == {
            "ref": "MCH-02",
            "nom": "Moteur asynchrone",
            "categorie": "Moteur",
            "sous_equipement_id": "Machine à presse",
            "fiche_technique": "Fihce Moteur asynchrone",
            "fabricant": "Helsinki",
            "etat": "Actif",
            "compteur": "45",
            "date_service": "12/10/2005",
            "criticite": "critique"
        }