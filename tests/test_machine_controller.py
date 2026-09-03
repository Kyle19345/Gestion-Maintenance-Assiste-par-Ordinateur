from controller.machine_controller import MachineController
from confest import make_machine, make_data_machine
from models.machine import EtatMachine

from unittest.mock import Mock, patch


def test_check_data(make_data_machine):
    master = Mock()
    database = Mock()

    data = make_data_machine(
        ref="M-01",
        nom="Moteur Asynchrone",
        categorie="",
        date_service="10/10/2000",
        fabricant="Toyota",
        compteur="4",
        etat=EtatMachine.EN_MAINTENANCE.value
    )

    with patch("controller.base_controller.MessageBox") as mock_message, \
         patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        result = controller.check_data(
            data,
            date=data["date_service"],
            number=data["compteur"]
        )

    mock_message.assert_called_with(
        master,
        "Veuillez remplir tous les champs",
        type="error"
    )

    assert result  == False

def test_enregistrer_maj_success(make_data_machine):
    view = Mock()
    database = Mock()
    master = Mock()

    data = make_data_machine(
        ref="M-01",
        nom="Moteur Asynchrone",
        categorie="Moteur",
        date_service="10/10/2000",
        fabricant="Toyota",
        compteur="4",
        etat=EtatMachine.EN_MAINTENANCE.value
    )
    view.get_entre_with_etat.return_value = data

    with patch("controller.machine_controller.ListMachine"), \
         patch("controller.machine_controller.MessageBox") as mock_message:
        controller = MachineController(master, database)
        controller.update_machine = view
        controller.afficher_machine = Mock()

        controller.enregistrer_maj()
        args, kwargs = database.update_machine.call_args
        machine = args[0]

    assert machine.ref == "M-01"
    assert machine.nom == "Moteur Asynchrone"
    assert machine.categorie == "Moteur"
    assert machine.date_service == "10/10/2000"
    assert machine.fabricant == "Toyota"
    assert machine.compteur == 4
    assert machine.etat == "En maintenance"

    database.update_machine.assert_called_once()
    mock_message.assert_called_once_with(
        master,
        "Mise à jour de la machine effectué",
        type="success"
    )
    controller.afficher_machine.assert_called_once()

def test_enregistrer_maj_champ_vide(make_data_machine):
    view = Mock()
    master = Mock()
    database = Mock()

    data = make_data_machine(
        ref="M-01",
        nom="Moteur Asynchrone",
        categorie="",
        date_service="10/10/2000",
        fabricant="Toyota",
        compteur="53",
        etat=EtatMachine.EN_MAINTENANCE.value
    )

    view.get_entre_with_etat.return_value = data

    with patch("controller.base_controller.MessageBox") as mock_message, \
         patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.update_machine = view
        controller.enregistrer_maj()

    mock_message.assert_called_once_with(
        master,
        "Veuillez remplir tous les champs",
        type="error"
    )

    database.update_machine.assert_not_called()

def test_enregistrer_maj_invalid_number(make_data_machine):
    view = Mock()
    master = Mock()
    database = Mock()

    data = make_data_machine(
        ref="M-01",
        nom="Moteur Asynchrone",
        categorie="Moteur",
        date_service="10/10/2000",
        fabricant="Toyota",
        compteur="5J",
        etat=EtatMachine.EN_MAINTENANCE.value
    )

    view.get_entre_with_etat.return_value = data

    with patch("controller.base_controller.MessageBox") as mock_message, \
        patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.update_machine = view
        controller.enregistrer_maj()

    mock_message.assert_called_once_with(
        master,
        "Veuillez saisir un nombre entier",
        type="error"
    )

    database.update_machine.assert_not_called()
    
def test_ajouter_machine(make_data_machine):
    view = Mock()
    database = Mock()
    master = Mock()

    data = make_data_machine(
        ref="MCH-01",
        nom="Verin électrique",
        categorie="Distribution",
        date_service="10/10/2006",
        fabricant="Helsinki",
        compteur="4"
    )

    view.get_entre.return_value = data

    with patch("controller.machine_controller.MessageBox") as mock_message, \
         patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.afficher_machine = Mock()
        controller.add_machine = view

        controller.ajouter_machine()
        args, kwargs = database.add_machine.call_args
        machine = args[0]

    assert machine.ref == "MCH-01"
    assert machine.nom == "Verin électrique"
    assert machine.categorie == "Distribution"
    assert machine.date_service == "10/10/2006"
    assert machine.fabricant == "Helsinki"
    assert machine.compteur == 4

    database.add_machine.assert_called_once()
    
    mock_message.assert_called_once_with(
        master,
        "Machine Enregistrer",
        type="success"
    )

    controller.afficher_machine.assert_called_once()

def test_ajouter_machine_champ_vide(make_data_machine):
    view = Mock()
    database = Mock()
    master = Mock()

    data = make_data_machine(
        ref="MCH-01",
        nom="Verin électrique",
        categorie="Distribution",
        date_service="10/10/2006",
        fabricant="",
        compteur="4"
    )

    view.get_entre.return_value = data

    with patch("controller.base_controller.MessageBox") as mock_message, \
            patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.afficher_machine = Mock()
        controller.add_machine = view

        controller.ajouter_machine()
        
    mock_message.assert_called_once_with(
        master,
        "Veuillez remplir tous les champs",
        type="error"
    )
    database.add_machine.assert_not_called()

def test_ajouter_machine_invalid_number(make_data_machine):
    view = Mock()
    database = Mock()
    master = Mock()

    data = make_data_machine(
        ref="MCH-01",
        nom="Verin électrique",
        categorie="Distribution",
        date_service="10/10/2006",
        fabricant="Helsinki",
        compteur="Quatre"
    )

    view.get_entre.return_value = data

    with patch("controller.base_controller.MessageBox") as mock_message, \
         patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.afficher_machine = Mock()
        controller.add_machine = view

        controller.ajouter_machine()
        
    mock_message.assert_called_once_with(
        master,
        "Veuillez saisir un nombre entier",
        type="error"
    )
    database.add_machine.assert_not_called()

def test_confirm_suppr():
    view = Mock()
    database = Mock()
    master = Mock()

    view.get_machine_delete.return_value = "MCH-01"

    with patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.update_machine = view
        controller.afficher_machine = Mock()

        controller.confirm_suppr()

        args, kwargs = database.delete_machine.call_args
        del_machine = args[0]

    database.delete_machine.assert_called_once()

    assert del_machine == "MCH-01"

    view.destroy.assert_called_once()
    controller.afficher_machine.assert_called_once()

def test_confirm_champ_invalid():
    view = Mock()
    database = Mock()
    master = Mock()

    view.get_machine_delete.return_value = None

    with patch("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.update_machine = view
        controller.afficher_machine = Mock()

        controller.confirm_suppr()

        args, kwargs = database.delete_machine.call_args
        del_machine = args[0]

    database.delete_machine.assert_called_once()

    assert del_machine == None

    view.destroy.assert_called_once()
    controller.afficher_machine.assert_called_once()

def test_show_update(make_machine):
    view = Mock()
    database = Mock()
    master = Mock()

    machine = make_machine()
    database.get_intervention_asset.return_value = ["IN-01", "IN-02", "IN-03"]

    with patch ("controller.machine_controller.addMachine"), \
         patch ("controller.machine_controller.ListMachine"):
        controller = MachineController(master, database)
        controller.update_machine = view
        controller.show_update(machine)

        args, kwargs = controller.update_machine.afficher.call_args
        lst = args[1]
        machine_ref = args[0].ref

    assert lst == ["IN-01", "IN-02", "IN-03"]
    assert machine_ref == "MCH-001"
    controller.update_machine.afficher.assert_called_once()
    