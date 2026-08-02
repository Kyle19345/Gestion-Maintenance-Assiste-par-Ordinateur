import pytest

from models.database import BaseDeDonne
from models.intervention import Intervention
from models.machine import Machine
import sqlite3

@pytest.fixture
def db():
    database = BaseDeDonne(":memory:")
    yield database
    database.close()


def test_add_machine(db):
    machine = Machine(
        ref = "MCH-001",
        nom = "Test_machine",
        categorie = "Test",
        date_service = "02/08/2026",
        fabricant = "Toyota",
        etat = "En maintenance",
        compteur = "4J"
    )

    db.add_machine(machine=machine)
    machines = db.get_all_machine()

    assert machines[0].ref == "MCH-001"
    assert machines[0].nom == "Test_machine"

def test_add_multiple_machine(db):
    machine = Machine(
        nom = "Test_machine_1",
        categorie = "Test",
        date_service = "01/08/2026"
    )

    machine2 = Machine(
        nom = "Test_machine_2",
        categorie = "Test",
        date_service = "01/08/2026",
        etat = "En maintenance"
    )

    db.add_machine(machine=machine)
    db.add_machine(machine=machine2) 
    machines = db.get_all_machine()

    assert len(machines) == 2
    assert machines[0].machine_id != machines[1].machine_id
    assert machines[1].etat == "En maintenance"

def test_exception_id_machine(db):
    machine1 = Machine(
        machine_id = "m1"
    )
    machine2 = Machine(
        machine_id = "m1"
    )

    db.add_machine(machine=machine1)
    with pytest.raises(sqlite3.IntegrityError):
        db.add_machine(machine=machine2)

    machines = db.get_all_machine()

    assert len(machines) == 1
    assert machines[0].machine_id == "m1"

def test_delete_machine(db):
    machine = Machine(
        machine_id = "m1"
    )
    db.add_machine(machine=machine)
    db.delete_machine("m1")
    result = db.get_all_machine()

    assert len(result) == 0

def test_update_machine(db):
    machine = Machine(
        machine_id = "m1",
        nom = "test_machine_1"
    )

    machine2 = Machine(
        machine_id = "m1",
        nom = "test_update_machine_1"
    )

    machine3 = Machine(
        machine_id = "inconnu"
    )
    db.add_machine(machine=machine)
    db.update_machine(machine=machine2)
    db.update_machine(machine=machine3)

    result = db.get_all_machine()

    assert len(result) == 1
    assert result[0].nom == "test_update_machine_1"


def test_add_planing(db):
    machine = Machine(
        machine_id = "mch-01"
    )

    intervention = Intervention(
        ref = "IN-001",
        description = "Test_add_intervention",
        machine_id = "mch-01"
    )

    db.add_machine(machine = machine)
    db.add_intervention(intervention = intervention)

    results = db.get_planing()

    assert len(results) == 1
    assert results[0].machine_id == "mch-01"

def test_add_planing_with_no_machine(db):
    intervention = Intervention(
            ref = "IN-001",
            description = "Test_add_intervention",
            machine_id = "mch-01"
        )
    with pytest.raises(sqlite3.IntegrityError):
        db.add_intervention(intervention = intervention)

    results = db.get_planing()
    assert(len(results)) == 0

def test_add_multiples_planing(db):
    machine = Machine(
        machine_id = "m-01"
    )
    intervention = Intervention(
        ref = "IN-01",
        machine_id = "m-01"
    )

    intervention2 = Intervention(
        ref = "IN-02",
        machine_id = "m-01"
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    db.add_intervention(intervention=intervention2)
    results = db.get_planing()

    assert len(results) == 2
    assert results[0].machine_id == "m-01"
    assert results[1].machine_id == "m-01"
    assert results[0].ref != results[1].ref

def test_add_intervention(db):
    machine = Machine(
        machine_id = "m-01"
    )

    intervention = Intervention(
        machine_id = "m-01",
        statut = "Réalisé"
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)

    results = db.get_all_intervention()

    assert len(results) == 1
    assert results[0].statut == "Réalisé"

def test_delete_intervention(db):
    machine = Machine(
        machine_id = "m-01"
    )

    intervention = Intervention(
        ref = "IN-01",
        machine_id = "m-01"
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    results = db.get_planing()
    machines = db.get_all_machine()

    db.delete_intervention(intervention_id="IN-01")
    result2= db.get_planing()
    machines2 = db.get_all_machine()

    assert len(results) == 1
    assert len(machines) == 1
    assert len(results) != len(result2)
    assert len(machines2) == 1

def test_update_intervention(db):
    machine = Machine(
        machine_id = "m-01"
    )
    
    intervention = Intervention(
        ref = "IN-01",
        machine_id = "m-01",
        statut = "Réalisé"
    )

    intervention_maj = Intervention(
        intervention_id = intervention.intervention_id,
        ref = "IN-01",
        machine_id = "m-01",
        statut = "Planifié",
        outils = "Tourne Vis"
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    results = db.get_every_intervention()
    
    db.update_intervention(intervention=intervention_maj)
    results2 = db.get_every_intervention()
    results_maj = db.get_planing()

    assert len(results) == 1
    assert results[0].outils == ""
    assert len(results2) == 1
    assert results_maj[0].statut == "Planifié"
    assert results_maj[0].outils == "Tourne Vis"

def test_delete_cascade(db):
    machine = Machine(
        machine_id = "mch-01"
    )
    intervention =  Intervention(
        ref = "IN-01",
        machine_id = "mch-01"
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    db.delete_machine(machine_id="mch-01")
    machines = db.get_all_machine()
    interventions = db.get_all_intervention()

    assert len(machines) == 0
    assert len(interventions) == 0

def test_get_every_intervention(db):
    machine = Machine(
        machine_id = "mch-01"
    )

    intervention =  Intervention(
        ref = "IN-01",
        machine_id = "mch-01"
    )

    intervention2 = Intervention(
        ref = "IN-02",
        machine_id = "mch-01",
        statut = "Réalisé"
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    db.add_intervention(intervention=intervention2)

    results = db.get_every_intervention()

    assert len(results) == 2
