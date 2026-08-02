"""
Ce Module sert d'interface pour afficher les différents
interventions avec le statut non réalisé dans la base de donné.
"""


import customtkinter as ctk
from typing import Callable, List

from models.intervention import Intervention
from views.base_view import BaseFrame
from views._ui_utils import ellipsize_for_width, create_button, create_label


class Planing(BaseFrame):
    """Permet de créer une vue des interventions à réaliser."""
    def __init__(
            self,
            master: ctk.CTk,
            on_select: Callable = None,
            on_add: Callable = None
    ):
        super().__init__(master)
        self.on_select = on_select
        
        # Headers Treeview
        self.column_headers = ["Date d'intervention","Référence","Description","Machine","Dure","Outils","Executant","Statut"]
        self.column_attrs = ["date_intervention","ref","description","machine","dure","outils","executant","statut"]
        
        # Conteneur Fenetre Ajout
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, pady=20, padx=20)
        lbl = create_label(
            master=frame,
            text="📋 Planing",
            font=("Poppins", 18, "bold")
        )
        lbl.grid(row=0, column=0, pady=20, padx=20, sticky="w")

        bouton_ajouter = create_button(
            master=frame,
            text="➕ Ajouter Intervention",
            command=on_add,
            width=170,
            height=35,
            font=("Poppins", 14)
        )
        bouton_ajouter.grid(row=1, column=0, pady=20, padx=20)

        # Conteneur fentre treeview
        container = ctk.CTkScrollableFrame(self, width=950, height=370)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        container.configure(fg_color="#2b2b2b")

        weights = [20, 12, 18, 15, 12, 15, 15, 8]
        self.tree = self.create_treeview(
            container,
            self.column_attrs,
            self.column_headers,
            weights=weights,
            height=13
        )
        self.tree.pack(fill="both", expand=True, pady=5, padx=5)

        # tags pour alternance de lignes
        self.tree.tag_configure("odd", background="#3a3a3a")
        self.tree.tag_configure("even", background="#333333")

        self.tree.bind("<Double-1>", self._on_double_click)
        self._donnees = []
    
    def _normalize_row(self, intervention: Intervention) -> List:
        """
        Récupère les attributs de l'objet intervention.
        """
        return [getattr(intervention, attr, "") for attr in self.column_attrs]

    def afficher(self, donne: List[Intervention]) -> None:
        """Insert les les interventions non réalisé."""
        self._donnees = donne
        for i in self.tree.get_children():
            self.tree.delete(i)

        col_px = {attr: self.tree.column(attr, option="width") for attr in self.column_attrs}

        for i, intervention in enumerate(donne):
            row = self._normalize_row(intervention)
            disp = []
            for attr, cell in zip(self.column_attrs, row):
                text = str(cell)
                avail = max(30, col_px[attr] - 12)
                short = ellipsize_for_width(text, avail, self.cell_font)
                disp.append(short)
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=disp, tags=(tag,))
    
    def _on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            index = self.tree.index(item_id)
            if 0 <= index < len(self._donnees) and self.on_select:
                self.on_select(self._donnees[index])


if __name__ == "__main__":
    root = ctk.CTk()
    app = Planing(root)
    app.pack()
    root.mainloop()