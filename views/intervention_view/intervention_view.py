"""
Ce module sert d'interface pour afficher les différents interventions
dans la base de donné
"""
# BUG: Uniformiser en .gird() ou en .pack() 
# TODO: Mettre la création des widget dans la classe parente

import customtkinter as ctk

from typing import Callable, List

from models.intervention import Intervention
from views.base_view import BaseFrame
from views._ui_utils import ellipsize_for_width, create_button, create_label, create_entry


class ListIntervention(BaseFrame):
    """
    Fenetre qui liste les différents interventions
    dans la bdd.
    """
    def __init__(
            self,
            master: ctk.CTk,
            on_select: Callable=None,
            on_search: Callable=None
    ):
        super().__init__(master)

        self.on_select = on_select
        self.on_search = on_search

        # Header Treeview
        self.column_headers = ["Référence", "Description", "Date d'intervention", 
                               "Dure", "Machine", "Outils", "Executant", "statut"]
        self.column_attrs = ["ref", "description", "date_intervention", "dure", 
                             "machine", "outils", "executant", "statut"]

        # Conteneur Fenetre recherche   
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, pady=20, padx=20)

        lbl = create_label(
            master=frame,
            text="📋 Liste des interventions",
            font=("Poppins", 18, "bold")
        )
        lbl.grid(row=0, column=0, pady=20, padx=20, sticky="w")

        self.barre_recherche = create_entry(master=frame, width=400)
        self.barre_recherche.grid(row=1, column=0, pady=20, padx=20)

        self.bouton_rechercher = create_button(
            master=frame,
            text="Rechercher 🔍",
            width=170,
            height=35,
            command=on_search
        )
        self.bouton_rechercher.grid(row=1, column=1, sticky="W")

        # Conteneur Treeview
        container = ctk.CTkScrollableFrame(self, width=950, height=370)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        container.configure(fg_color="#2b2b2b")

        weights = [10, 20, 15, 10, 10, 12, 10, 8]
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
        """
        Insert les interventions dans le treeview.
        """
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

    def _on_double_click(self, event) -> None:
        item_id = self.tree.identify_row(event.y)
        if item_id:
            index = self.tree.index(item_id)
            if 0 <= index < len(self._donnees) and self.on_select:
                self.on_select(self._donnees[index])
            
    def search_get(self) -> None:
        "Récupère les donné entré dans la barrre de recherche."
        return self.barre_recherche.get().strip()

    
if __name__ == "__main__":
    from dataclasses import dataclass

    @dataclass
    class Intervention:
        ref : str
        description : str
        date_intervention : str
        machine : str
        dure : int
        outils : str
        executant : str
        statut : str = "planifié"

    def on_select(asset):
        print("Double-cliqué",asset.description)

    root = ctk.CTk()
    app = ListIntervention(root, on_select)
    app.pack()  
    inter =[
        Intervention(1,"gf","gmfj","mlgjd","gfmj","gmfj","lgm","gmfj")
    ]
    app.afficher(inter)
    root.mainloop()
