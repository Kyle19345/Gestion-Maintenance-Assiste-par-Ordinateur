from controller.intervention_controller import InterventionController
from models.intervention import StatutIntervention
from models.database import DuplicateReferenceError, PrimaryKeyError

from unittest.mock import Mock, patch


def test_ajouter_intervention_champ_vide():
    # Arrange
    view = Mock()
    database = Mock()
    master = Mock()

    # Act
    view.get_entre.return_value = {
        "ref": "INT-001",
        "date_intervention": "10/08/2026",
        "dure": "2",
        "outils": "Clé",
        "machine_id": "MCH-001",
        "executant": "Paul",
        "description": ""
    }

    with patch("controller.intervention_controller.ListIntervention"), \
         patch("controller.intervention_controller.Planing"), \
         patch("controller.base_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.add_intervention = view

        controller.ajouter_intervention()

    mock_message.assert_called_once_with(
        master,
        "Veuillez remplir tous les champs",
        type="error"
    )
    database.add_intervention.assert_not_called()

def test_ajouter_intervention_error_dure():
     # Arrange
    view = Mock()
    database = Mock()
    master = Mock()

    # Act
    view.get_entre.return_value = {
        "ref": "INT-001",
        "date_intervention": "10/08/2026",
        "dure": "gdflg",
        "outils": "Clé",
        "machine_id": "MCH-001",
        "executant": "Paul",
        "description": "IN01"
    }

    with patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.base_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.add_intervention = view

        controller.ajouter_intervention()

    mock_message.assert_called_once_with(
        master,
        "Veuillez saisir un nombre entier",
        type="error"
    )
    database.add_intervention.assert_not_called()

def test_ajouter_intervention_date_invalide():
    view = Mock()
    database = Mock()
    master = Mock()

    view.get_entre.return_value = {
        "ref": "INT-001",
        "date_intervention": "invalide",
        "dure": "4",
        "outils": "Clé",
        "machine_id": "MCH-001",
        "executant": "Paul",
        "description": "IN01"
    }

    with patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.base_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.add_intervention = view

        controller.ajouter_intervention()

    mock_message.assert_called_once_with(
        master,
        "La date saisie est invalide",
        type="error"
    )
    database.add_intervention.assert_not_called()

def test_success_ajouter_intervention():
    view = Mock()
    database = Mock()
    master = Mock()

    view.get_entre.return_value = {
        "ref": "INT-001",
        "date_intervention": "12/10/2000",
        "dure": "4",
        "outils": "Clé",
        "machine_id": "mch-546546546",
        "executant": "Paul",
        "description": "IN01"
    }

    with patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.intervention_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.add_intervention = view
        controller.afficher_planing = Mock()

        controller.ajouter_intervention()
        args, kwargs = database.add_intervention.call_args
        intervention = args[0]


    assert intervention.ref == "INT-001"
    assert intervention.date_intervention == "12/10/2000"
    assert intervention.dure == 4
    assert intervention.outils == "Clé"
    assert intervention.machine_id == "mch-546546546"
    assert intervention.executant == "Paul"
    assert intervention.description == "IN01"

    database.add_intervention.assert_called_once()
    controller.afficher_planing.assert_called()
    view.suppression_champ.assert_called()

    mock_message.assert_called_once_with(
        master,
        "Intervention enregistrée",
        type="success"
    )

def test_enregistrer_maj_champ_vide():
    database = Mock()
    view = Mock()
    master = Mock()

    view.get_entre_with_statut.return_value = {
        "ref": "IN_01",
        "date_intervention": "12/12/2000",
        "dure": "3J",
        "Outils": "Tourne Vis",
        "machine_id": "mch-01",
        "executant": "TECH-01",
        "description": "" 
    }

    with patch("controller.intervention_controller.addIntervention"), \
         patch("controller.intervention_controller.ListIntervention"), \
         patch("controller.intervention_controller.Planing"), \
         patch("controller.base_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.update_intervention = view

        controller.enregistrer_maj()

    mock_message.assert_called_once_with(
        master,
        "Veuillez remplir tous les champs",
        type = "error"
    )
    database.update_intervention.assert_not_called()


def test_enregistrer_maj_error_dure():
    database = Mock()
    view = Mock()
    master = Mock()

    view.get_entre_with_statut.return_value = {
        "ref": "IN_01",
        "date_intervention": "12/12/2000",
        "dure": "3J",
        "Outils": "Tourne Vis",
        "machine_id": "mch-01",
        "executant": "TECH-01",
        "description": "Description Intervention01" 
    }

    with patch("controller.intervention_controller.addIntervention"), \
            patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.base_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.update_intervention = view

        controller.enregistrer_maj()

    mock_message.assert_called_once_with(
        master,
        "Veuillez saisir un nombre entier",
        type = "error"
    )
    database.update_intervention.assert_not_called()

def test_enregistrer_date_invalide():
    database = Mock()
    view = Mock()
    master = Mock()

    view.get_entre_with_statut.return_value = {
        "ref": "IN_01",
        "date_intervention": "Date_invalide",
        "dure": "3",
        "Outils": "Tourne Vis",
        "machine_id": "mch-01",
        "executant": "TECH-01",
        "description": "Description Intervention01" 
    }

    with patch("controller.intervention_controller.addIntervention"), \
            patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.base_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.update_intervention = view

        controller.enregistrer_maj()

    mock_message.assert_called_once_with(
        master,
        "La date saisie est invalide",
        type = "error"
    )
    database.update_intervention.assert_not_called()

def test_success_enregistrer_maj():
    database = Mock()
    view = Mock()
    master = Mock()
    
    view.get_entre_with_statut.return_value = {
        "ref": "IN_01",
        "date_intervention": "12/10/2000",
        "dure": "3",
        "outils": "Tourne Vis",
        "machine_id": "mch-01",
        "executant": "TECH-01",
        "description": "Description Intervention01",
        "statut": StatutIntervention.REALISE.value
    }

    with patch("controller.intervention_controller.addIntervention"), \
         patch("controller.intervention_controller.ListIntervention"), \
         patch("controller.intervention_controller.Planing"), \
         patch("controller.intervention_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.update_intervention = view
        controller.afficher_planing = Mock()

        controller.enregistrer_maj()

        args, kwargs = database.update_intervention.call_args
        intervention = args[0]

    assert intervention.ref == "IN_01"
    assert intervention.date_intervention == "12/10/2000"
    assert intervention.dure == 3
    assert intervention.outils == "Tourne Vis"
    assert intervention.machine_id == "mch-01"
    assert intervention.executant == "TECH-01"
    assert intervention.description == "Description Intervention01"
    assert intervention.statut == "Réalisé"

    database.update_intervention.assert_called()

    controller.afficher_planing.assert_called_once()

    mock_message.assert_called_once_with(
        master,
        "Intervention mise à jour",
        type = "success"
    )

def test_suppr_intervention():
    master = Mock()
    database = Mock()

    with patch("controller.intervention_controller.ListIntervention"), \
         patch("controller.intervention_controller.Planing"), \
         patch("controller.intervention_controller.ConfirmationBox") as mock_confirmation:

        controller = InterventionController(master, database)
        controller.suppr_intervention()

    mock_confirmation.assert_called_once_with(
        master,
        on_valid = controller.confirm_delete
    )

def test_confirm_delete():
    master = Mock()
    database = Mock()
    view = Mock()

    view.suppr_selected.return_value = "IN-01"

    with patch("controller.intervention_controller.Planing"), \
         patch("controller.intervention_controller.ListIntervention"), \
         patch("controller.intervention_controller.addIntervention"):
        controller = InterventionController(master, database)

        controller.afficher_planing = Mock()
        controller.update_intervention = view
        controller.confirm_delete()

        args = database.delete_intervention.call_args
        ref_intervention = args[0]

    assert ref_intervention[0] == "IN-01"

    database.delete_intervention.assert_called_once()
    view.destroy.assert_called_once()
    controller.afficher_planing.assert_called_once()

def test_find_intervention():
    view = Mock()
    database = Mock()
    master = Mock()

    view.search_get.return_value = "IN-01"
    database.find_intervention.return_value = "result_IN-01"

    with patch("controller.intervention_controller.ListIntervention"), \
         patch("controller.intervention_controller.Planing"):
        controller = InterventionController(master, database)
        controller.list_intervention = view

        controller.find_intervention()
        args, kwargs = database.find_intervention.call_args
        search_in = args[0]

        args2, kwargs2 = view.afficher.call_args
        result = args2[0]

    assert search_in == "IN-01"
    assert result == "result_IN-01"

    view.grid_forget.assert_called()
    view.grid.assert_called()
    view.afficher.assert_called()

def test_ajouter_intervention_error_ref():
    view = Mock()
    database = Mock()
    master = Mock()

    view.get_entre.return_value = {
        "ref": "INT-001",
        "date_intervention": "12/10/2000",
        "dure": "4",
        "outils": "Clé",
        "machine_id": "mch-546546546",
        "executant": "Paul",
        "description": "IN01"
    }

    with patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.intervention_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.add_intervention = view
        controller.afficher_planing = Mock()
        database.add_intervention.side_effect = DuplicateReferenceError()
        
        controller.ajouter_intervention()
        
    mock_message.assert_called_once_with(
        master,
        "La référence saisie est invalide",
        type="error"
    )
 
    database.add_intervention.assert_called_once()
    controller.afficher_planing.assert_not_called()
    view.suppression_champ.assert_not_called()

def test_ajouter_intervention_error_id():
    view = Mock()
    database = Mock()
    master = Mock()

    view.get_entre.return_value = {
        "ref": "INT-001",
        "date_intervention": "12/10/2000",
        "dure": "4",
        "outils": "Clé",
        "machine_id": "mch-546546546",
        "executant": "Paul",
        "description": "IN01"
    }

    with patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.intervention_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.add_intervention = view
        controller.afficher_planing = Mock()
        database.add_intervention.side_effect = PrimaryKeyError()
        
        controller.ajouter_intervention()
        
    mock_message.assert_called_once_with(
        master,
        "L'id saisie est invalide",
        type="error"
    )
    
    database.add_intervention.assert_called_once()
    controller.afficher_planing.assert_not_called()
    view.suppression_champ.assert_not_called()

def test_enregistrer_maj_error_ref():
    database = Mock()
    view = Mock()
    master = Mock()
    
    view.get_entre_with_statut.return_value = {
        "ref": "IN_01",
        "date_intervention": "12/10/2000",
        "dure": "3",
        "outils": "Tourne Vis",
        "machine_id": "mch-01",
        "executant": "TECH-01",
        "description": "Description Intervention01",
        "statut": StatutIntervention.REALISE.value
    }

    with patch("controller.intervention_controller.addIntervention"), \
            patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.intervention_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.update_intervention = view
        controller.afficher_planing = Mock()
        database.update_intervention.side_effect = DuplicateReferenceError()

        controller.enregistrer_maj()

    database.update_intervention.assert_called()
    mock_message.assert_called_once_with(
        master,
        "La référence saisie est invalide",
        type = "error"
    )

    controller.afficher_planing.assert_not_called()

def test_enregistrer_maj_error_ref():
    database = Mock()
    view = Mock()
    master = Mock()
    
    view.get_entre_with_statut.return_value = {
        "ref": "IN_01",
        "date_intervention": "12/10/2000",
        "dure": "3",
        "outils": "Tourne Vis",
        "machine_id": "mch-01",
        "executant": "TECH-01",
        "description": "Description Intervention01",
        "statut": StatutIntervention.REALISE.value
    }

    with patch("controller.intervention_controller.addIntervention"), \
            patch("controller.intervention_controller.ListIntervention"), \
            patch("controller.intervention_controller.Planing"), \
            patch("controller.intervention_controller.MessageBox") as mock_message:

        controller = InterventionController(master, database)
        controller.update_intervention = view
        controller.afficher_planing = Mock()
        database.update_intervention.side_effect = PrimaryKeyError()

        controller.enregistrer_maj()

    database.update_intervention.assert_called()
    mock_message.assert_called_once_with(
        master,
        "L'id saisie est invalide",
        type = "error"
    )

    controller.afficher_planing.assert_not_called()
