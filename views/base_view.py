"""
Ce Module represente la classe parente de tous les Vues
"""

import customtkinter as ctk
from tkinter import ttk, font
from typing import Callable


WIDTH = 1000
HEIGHT = 550
CORNER_RADIUS = 8


class BaseFrame(ctk.CTkFrame):
    """Base CTkFrame."""
    def __init__(
            self,
            master: ctk.CTk,
            width: int = WIDTH,
            height: int = HEIGHT,
            corner_radius: int = CORNER_RADIUS,
            *args,
            **kwargs
        ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=corner_radius,
            *args,
            **kwargs
        )
        self.width = width
        self.height = height
        self.head_font = font.Font(family="Poppins", size=11, weight="bold")
        self.cell_font = font.Font(family="Poppins", size=10)

    def configure_tree_style(
            self, style_name: str = "Custom.Treeview",
            bg_color="#2b2b2b",
            even_color="#333333",
            text_color="#f2f2f2",
            rowheight: int = 26
    ):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        style.configure(
            style_name,
            background=bg_color,
            fieldbackground=bg_color,
            foreground=text_color,
            rowheight=rowheight,
            font=self.cell_font,
            borderwidth=0,
            relief="flat",
            lightcolor=bg_color,
            darkcolor=bg_color,
            bordercolor=bg_color
        )

        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe"})
        ])

        style.configure(
            style_name + ".Heading",
            font=self.head_font,
            foreground=text_color,
            background=even_color,
            bordercolor=bg_color,
            relief="flat"
        )

        style.map("Treeview.Heading",
                  background=[("active", even_color)],
                  relief=[("active", "flat")])

        return style_name

    def create_treeview(
            self,
            container,
            column_attrs,
            column_headers,
            weights=None, 
            height=13,
            style_name=None
    ) -> ttk.Treeview:
        if style_name is None:
            style_name = self.configure_tree_style()

        tree = ttk.Treeview(container, columns=column_attrs, show="headings", height=height,
                            style=style_name)

        total = self.width - 60
        if weights is None:
            weights = [int(100 / max(1, len(column_attrs))) for _ in column_attrs]
        s = sum(weights[:len(column_attrs)])
        pix = [max(60, int(total * w / s)) for w in weights[:len(column_attrs)]]

        for header, attr, w in zip(column_headers, column_attrs, pix):
            tree.heading(attr, text=header, anchor="w")
            tree.column(attr, width=w, anchor="w", stretch=False)

        return tree

    def _normalize_row(self) -> None:
        """
        Récupère les attributs de l'objet machine.
        """
        pass

    def afficher(self) -> None:
        """
        Insert des données dans le treeview
        """
        pass
   