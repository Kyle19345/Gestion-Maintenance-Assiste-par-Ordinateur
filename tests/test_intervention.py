import pytest
import sqlite3

from models.intervention import Intervention, StatutIntervention
from models.machine import Machine

def test_add_planing(db, make_machine, make_intervention):
    machine = make_machine(
        machine_id = "mch-01"
    )

    intervention = make_intervention(
        ref = "IN-001",
        description = "Test_add_intervention",
        machine_id = "mch-01"
    )

    db.add_machine(machine = machine)
    db.add_intervention(intervention = intervention)

    results = db.get_planing()

    assert len(results) == 1
    assert results[0].machine_id == "mch-01"

def test_add_planing_with_no_machine(db, make_intervention):
    intervention = make_intervention(
            ref = "IN-001",
            description = "Test_add_intervention",
            machine_id = "mch-01"
        )
    with pytest.raises(sqlite3.IntegrityError):
        db.add_intervention(intervention = intervention)

    results = db.get_planing()
    assert(len(results)) == 0

def test_add_multiples_planing(db, make_machine, make_intervention):
    machine = make_machine(
        machine_id = "m-01"
    )
    intervention = make_intervention(
        ref = "IN-01",
        machine_id = "m-01"
    )

    intervention2 = make_intervention(
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
        statut = StatutIntervention.REALISE
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)

    results = db.get_all_intervention()

    assert len(results) == 1
    assert results[0].statut == "Réalisé"

def test_add_interveniton_without_machine(db, make_intervention):
    intervention = make_intervention()

    db.add_intervention(intervention=intervention)

    result = db.get_every_intervention()

    assert len(result) == 1
    assert result[0].machine_id is None

def test_delete_intervention(db):
    machine = Machine(
        machine_id = "m-01"
    )

    intervention = Intervention(
        intervention_id = "IN001",
        ref = "IN-01",
        machine_id = "m-01"
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    results = db.get_every_intervention()
    machines = db.get_all_machine()

    db.delete_intervention(intervention_id="IN001")
    result2= db.get_every_intervention()
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
        statut = StatutIntervention.REALISE
    )

    intervention_maj = Intervention(
        intervention_id = intervention.intervention_id,
        ref = "IN-01",
        machine_id = "m-01",
        statut = StatutIntervention.PLANIFIE,
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
        machine_id = machine.machine_id
    )

    intervention2 = Intervention(
        ref = "IN-02",
        machine_id = machine.machine_id
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    db.add_intervention(intervention=intervention2)

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
        statut = StatutIntervention.REALISE
    )

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)
    db.add_intervention(intervention=intervention2)

    results = db.get_every_intervention()

    assert len(results) == 2

def test_find_intervention(db, make_intervention, make_machine):
    machine = make_machine(machine_id = "MCH-01")
    intervention = make_intervention(machine_id = machine.machine_id)

    db.add_machine(machine=machine)
    db.add_intervention(intervention=intervention)

    results = db.find_intervention(intervention_ref = "IN")

    assert len(results) == 1
    assert results[0].description == "Intervention test"

def test_find_multiple_intervention(db, make_intervention, make_machine):
    machine = make_machine(machine_id = "MCH-01")
    intervention1 = make_intervention(ref = "IN01", machine_id = machine.machine_id)
    intervention2 = make_intervention(ref = "IN02", machine_id = machine.machine_id)

    db.add_machine(machine = machine)
    db.add_intervention(intervention = intervention1)
    db.add_intervention(intervention = intervention2)

    results = db.find_intervention(intervention_ref = "IN")

    assert len(results) == 2
    assert results[0].ref == "IN01"
    assert results[1].ref == "IN02"

def test_get_intervention_asset(db, make_intervention, make_machine):
    machine = make_machine(ref="MCH001", machine_id = "MCH-01")
    machine2 = make_machine(ref = "MCH002", machine_id = "MCH-02")

    intervention = make_intervention(
        ref = "IN01",
        machine_id = "MCH-01"
    )

    intervention2 = make_intervention(
        ref = "IN02",
        machine_id = "MCH-01"
    )

    intervention3 = make_intervention(
        ref = "IN03",
        machine_id = machine2.machine_id
    )

    db.add_machine(machine=machine)
    db.add_machine(machine=machine2)

    db.add_intervention(intervention=intervention)
    db.add_intervention(intervention=intervention2)
    db.add_intervention(intervention=intervention3)

    result = db.get_intervention_asset(machine_id = "MCH-01")

    assert len(result) == 2
    assert result[0].ref == "IN01"