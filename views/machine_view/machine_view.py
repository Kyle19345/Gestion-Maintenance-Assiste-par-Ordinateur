"""
Ce module permet de lister les machines
dans la base de donné.
"""

import customtkinter as ctk

from typing import Callable, List

from views._ui_utils import ellipsize_for_width, create_button, create_label, create_entry
from views.base_view import BaseFrame
from models.machine import Machine


class ListMachine(BaseFrame):
    def __init__(
            self,
            master: ctk.CTk,
            on_select: Callable = None,
            show_add: Callable = None
    ):
        super().__init__(master)

        self.on_select = on_select
        self.show_add = show_add

        # Header Treeview
        self.column_headers = ["ID", "Nom", "Categorie", "Date de service", 
                               "Fabricant", "etat", "compteur"]
        self.column_attrs = ["ID", "nom", "categorie", "date_service", 
                             "fabricant", "etat", "compteur"]

        # Fenetre Principal
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, pady=20, padx=20)
        
        lbl = create_label(
            master=frame,
            text="📋 Liste des machines"
        )
        lbl.grid(row=0, column=0, pady=20, padx=20)

        bouton_ajouter = create_button(
            frame,
            text="➕ Ajouter machine",
            command=self.show_add,
            width=170,
            height=35
        )
        bouton_ajouter.grid(row=1, column=0, pady=20, padx=20)

        # Fenetre Treeview
        container = ctk.CTkScrollableFrame(self, width=950, height=370)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        container.configure(fg_color="#2b2b2b")

        weights = [8, 20, 15, 20, 12, 18, 12]
        self.tree = self.create_treeview(
            container,
            self.column_attrs,
            self.column_headers,
            weights=weights,
            height=13
        )
        self.tree.pack(fill="both", expand=True, pady=5, padx=5)

        self.tree.tag_configure("odd", background="#3a3a3a")
        self.tree.tag_configure("even", background="#333333")

        self.tree.bind("<Double-1>", self._on_double_click)
        self._donnees = []

    def set_controller(self, controller) -> None:
        """Définit le controller de la vue"""
        self.controller = controller

    def _normalize_row(self, machine: Machine) -> None:
        """
        Récupère les attributs de l'objet machine.
        """
        return [getattr(machine, attr, "") for attr in self.column_attrs]

    def afficher(self, donne: List[Machine]) -> None:
        """
        Insert les informations sur les machines dans
        le treeview.
        """
        self._donnees = donne
        for i in self.tree.get_children():
            self.tree.delete(i)

        col_px = {attr: self.tree.column(attr, option="width") for attr in self.column_attrs}

        for i, machine in enumerate(donne):
            row = self._normalize_row(machine)
            disp = []
            for attr, cell in zip(self.column_attrs, row):
                text = str(cell)
                avail = max(30, col_px[attr] - 12)
                short = ellipsize_for_width(text, avail, self.cell_font)
                disp.append(short)
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=disp, tags=(tag,))

    def _on_double_click(self, event) -> None:
        item_id = self.tree.identify_row(event.y)
        if item_id:
            index = self.tree.index(item_id)
            if 0 <= index < len(self._donnees) and self.on_select:
                self.on_select(self._donnees[index])


if __name__ == "__main__":
    root = ctk.CTk()
    app = ListMachine(root)
    app.pack(fill="both", expand=True)

    class M:
        def __init__(self, **kw):
            for k, v in kw.items():
                setattr(self, k, v)

    sample = [
        M(ID=1, nom="Machine A très longue", categorie="Type 1", date_service="2025-01-01", fabricant="X", etat="OK",
          compteur=123),
        M(ID=2, nom="Machine B", categorie="Type 2", date_service="2024-05-10", fabricant="Y", etat="En panne",
          compteur=456),
        M(ID=3, nom="Machine C", categorie="Type 3", date_service="2023-11-02", fabricant="Z", etat="OK", compteur=789),
    ]
    app.afficher(sample)

    root.mainloop()
