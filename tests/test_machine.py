import pytest
import sqlite3

from models.database import DuplicateReferenceError, PrimaryKeyError
from models.machine import EtatMachine
from confest import db, make_machine


def test_add_machine(db, make_machine):
    machine = make_machine()

    db.add_machine(machine=machine)
    machines = db.get_all_machine()

    assert machines[0].ref == "MCH-001"
    assert machines[0].nom == "Machine_test"

def test_add_multiple_machine(db, make_machine):
    machine = make_machine(
        nom = "Test_machine_1",
        categorie = "Test",
        date_service = "01/08/2026"
    )

    machine2 = make_machine(
        ref = "MCH-002",
        nom = "Test_machine_2",
        categorie = "Test",
        date_service = "01/08/2026",
        etat = EtatMachine.EN_MAINTENANCE
    )

    db.add_machine(machine=machine)
    db.add_machine(machine=machine2) 
    machines = db.get_all_machine()

    noms = {machine.nom for machine in machines}

    machine_maintenance = next(
        machine for machine in machines
        if machine.nom == "Test_machine_2"
    )

    ids = {machine.machine_id for machine in machines}

    assert len(machines) == 2
    assert noms == {"Test_machine_1", "Test_machine_2"}
    assert len(ids) == 2
    assert machine_maintenance.etat == "En maintenance"

def test_exception_id_machine(db, make_machine):
    machine1 = make_machine(
        machine_id = "m1",
        ref = "MCH-01"
    )
    machine2 = make_machine(
        machine_id = "m1",
        ref = "MCH-02"
    )

    db.add_machine(machine=machine1)

    with pytest.raises(PrimaryKeyError):
        db.add_machine(machine=machine2)

    machines = db.get_all_machine()

    assert len(machines) == 1
    assert machines[0].machine_id == "m1"
    assert machines[0].ref == "MCH-01"

def test_exception_ref_machine(db, make_machine):
    machine1 = make_machine(
        ref = "mch01"
    )
    machine2 = make_machine(
        ref = "mch01"
    )

    db.add_machine(machine=machine1)
    with pytest.raises(DuplicateReferenceError):
        db.add_machine(machine=machine2)

    result = db.get_all_machine()

    assert len(result) == 1

def test_delete_machine(db, make_machine):
    machine = make_machine(
        machine_id = "m1"
    )
    db.add_machine(machine=machine)
    db.delete_machine("m1")
    result = db.get_all_machine()

    assert len(result) == 0

def test_delete_none_machine(db):
    result1 = db.get_all_machine()
    db.delete_machine(None)
    result2 = db.get_all_machine()

    assert result1 == result2

def test_update_machine(db, make_machine):
    machine = make_machine(
        machine_id = "m1",
        nom = "test_machine_1"
    )

    machine2 = make_machine(
        machine_id = "m1",
        nom = "test_update_machine_1"
    )

    machine3 = make_machine(
        machine_id = "inconnu"
    )
    db.add_machine(machine=machine)
    db.update_machine(machine=machine2)
    db.update_machine(machine=machine3)

    result = db.get_all_machine()

    assert len(result) == 1
    assert result[0].nom == "test_update_machine_1"

def test_update_machine_error_ref(db, make_machine):
    machine = make_machine(
        machine_id = "m1",
        ref = "mch-01"
    )

    machine2 = make_machine(
        machine_id = "m2",
        ref = "mch"
    )

    machine3 = make_machine(
        machine_id = "m1",
        ref = "mch"
    )

    db.add_machine(machine)
    db.add_machine(machine2)

    with pytest.raises(DuplicateReferenceError):
        db.update_machine(machine=machine3)

    result = db.get_all_machine()

    assert len(result) == 2
    assert result[0].ref == "mch-01"