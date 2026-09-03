import pytest
from models.database import BaseDeDonne
from models.intervention import Intervention, StatutIntervention
from models.machine import Machine, EtatMachine


@pytest.fixture
def db():
    database = BaseDeDonne(":memory:")
    yield database
    database.close()

@pytest.fixture
def make_machine():
    def _make_machine(**kwargs):
        defaults = {
            "ref": "MCH-001",
            "nom": "Machine_test",
            "categorie": "Test",
            "sous_equipement_id": "Moteur A",
            "fiche_technique": "Element de distribution",
            "fabricant": "Toyota",
            "date_service": "2025-01-01",
            "etat": EtatMachine.ACTIF,
            "criticite": "Critique"
        }

        defaults.update(kwargs)

        return Machine(**defaults)

    return _make_machine

@pytest.fixture
def make_intervention():
    def _make_intervention(**kwargs):
        defaults = {
            "ref": "IN-001",
            "description": "Intervention test",
            "date_intervention": "07/08/2026",
            "dure" : "3",
            "statut": StatutIntervention.PLANIFIE
        }

        defaults.update(kwargs)

        return Intervention(**defaults)

    return _make_intervention

@pytest.fixture
def make_data_machine():
    def _make_data_machine(**kwargs):
        defaults = {
            "ref": "MCH-01",
            "nom": "Moteur asynchrone",
            "categorie": "Moteur",
            "sous_equipement_id": "Machine à presse",
            "fiche_technique": "Fihce Moteur asynchrone",
            "fabricant": "Helsinki",
            "etat": EtatMachine.ACTIF.value,
            "compteur": "45",
            "date_service": "12/10/2005",
            "criticite": "critique"
        }

        defaults.update(kwargs)

        return defaults

    return _make_data_machine
