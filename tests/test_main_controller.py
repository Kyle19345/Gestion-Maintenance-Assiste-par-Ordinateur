from controller.main_controller import MainController
from unittest.mock import Mock, patch


def test_show_machine():
    machine = Mock()
    intervention = Mock()
    master = Mock()
    database = Mock()

    with patch("controller.main_controller.Sidebar"), \
         patch("controller.main_controller.Header"), \
         patch("controller.main_controller.InterventionController"), \
         patch("controller.main_controller.MachineController"):
        controller = MainController(master, database)
        controller.intervention = intervention(master, database)
        controller.machine = machine(master, database)

        controller.show_machine()

    controller.intervention.planing.grid_forget.assert_called_once()
    controller.intervention.list_intervention.grid_forget.assert_called_once()
    controller.machine.list_machine.grid.assert_called_once_with(
        row=1,
        column=1,
        padx=(0, 10),
        pady=(0, 10),
        sticky="nsew"
    )

    controller.machine.afficher_machine.assert_called_once()

def test_show_intervention():
    machine = Mock()
    intervention = Mock()
    master = Mock()
    database = Mock()

    with patch("controller.main_controller.Sidebar"), \
            patch("controller.main_controller.Header"), \
            patch("controller.main_controller.InterventionController"), \
            patch("controller.main_controller.MachineController"):
        controller = MainController(master, database)
        controller.intervention = intervention(master, database)
        controller.machine = machine(master, database)

        controller.show_intervention()

    controller.intervention.planing.grid_forget.assert_called_once()
    controller.machine.list_machine.grid_forget.assert_called_once()
    controller.intervention.list_intervention.grid.assert_called_once_with(
        row=1,
        column=1,
        padx=(0, 10),
        pady=(0, 10),
        sticky="nsew"
    )

    controller.intervention.afficher_intervention.assert_called_once()

def test_show_planing():
    machine = Mock()
    intervention = Mock()
    master = Mock()
    database = Mock()

    with patch("controller.main_controller.Sidebar"), \
            patch("controller.main_controller.Header"), \
            patch("controller.main_controller.InterventionController"), \
            patch("controller.main_controller.MachineController"):
        controller = MainController(master, database)
        controller.intervention = intervention(master, database)
        controller.machine = machine(master, database)

        controller.show_planing()

    controller.machine.list_machine.grid_forget.assert_called_once()
    controller.intervention.list_intervention.grid_forget.assert_called_once()
    controller.intervention.planing.grid.assert_called_once_with(
        row=1,
        column=1,
        padx=(0, 10),
        pady=(0, 10),
        sticky="nsew"
    )
    controller.intervention.afficher_planing.assert_called_once()
