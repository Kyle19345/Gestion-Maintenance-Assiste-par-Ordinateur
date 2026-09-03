"""
Ce module sert d'interface pour l'ajout d'intervention.
"""

import customtkinter as ctk

from typing import Callable, Dict

from models.intervention import Intervention
from views._ui_utils import create_button, create_label, create_entry


class addIntervention(ctk.CTkToplevel):
    """Interface d'ajout d'intervention"""
    def __init__(
            self,
            master,
            ajouter: Callable = None,
            on_suppr: Callable = None
    ):
        super().__init__(master)

        self.resizable(False, False)
        self.transient(master) #Permet de rester au dessu du parent
        self.grab_set()
        
        self.title("Editer Intervention")

        self.on_suppr = on_suppr

        # Container principal   
        self.frame_container = ctk.CTkFrame(
            self,
            corner_radius=12,
            border_width=1
        )
        self.frame_container.pack(
            expand="True",
            fill="both",
            padx=15,
            pady=15
        )

        create_label(
            master=self.frame_container,
            text="Intervention",
            font=("Poppins", 18, "bold")
        ).grid(
            row=0,
            column=0,
            pady=10
        )

        self.labels = [
            "Référence", "Date d'intervention", "Durée",
            "Machine", "Outils", "Exécutant"
        ]
        placeholder = [
            "Ex: INT-2025-001", "JJ/MM/AAAA","",
            "Ex: MCH-001", "EX: Clé dynamométrique, tournevis",
            "Ex: Rakoto Jean"
        ]
        self.entries = {}

        for i,label in enumerate(self.labels):
            create_label(
                master=self.frame_container,
                text=label
            ).grid(
                row=i+1,
                column=0,
                pady=8,
                padx=30,
                sticky="e"
            )

            entry = create_entry(
                self.frame_container,
                width=300,
                placeholder_text=placeholder[i]
            )
            entry.grid(row=i+1, column=1, pady=8, padx=30)
            self.entries[label.replace(" ","_")] = entry

        create_label(
            master=self.frame_container,
            text="Description"
        ).grid(
            row=len(self.labels)+3,
            column=0,
            padx=30,
            sticky="e"
        )

        self.description = ctk.CTkTextbox(
            self.frame_container,
            height=75,
            width=300
        )
        self.description.grid(
            row=len(self.labels)+3,
            column=1,
            padx=30,
            pady=8
        )

        create_button(
            master=self.frame_container,
            text="Enregistrer",
            command=ajouter,
            width=170,
            height=35,
            font=("Poppins", 14)
        ).grid(
            row=len(self.labels)+4,
            column=1,
            pady=20,
            padx=20,
            sticky="e"
        )
       
    def afficher(self, intervention: Intervention) -> None:
        """Affiche les données des interventions selectionné."""
        lbl_statut = create_label(
            master=self.frame_container,
            text="Statut"
        )
        lbl_statut.grid(
            row=len(self.labels)+2,
            column=0,
            padx=30,
            pady=8
        )

        self.statut = ctk.CTkComboBox(
            self.frame_container,
            width=300,
            values=["Planifié", "En cours", "Réalisé"],
            state="readonly"
        )
        self.statut.set("planifié")
        self.statut.grid(
            row=len(self.labels)+2,
            column=1,
            padx=30,
            pady=8
        )

        create_button(
            master=self.frame_container,
            text="Supprimer",
            fg_color="#BE7272",
            hover_color="red",
            command=self.on_suppr,
            width=170,
            height=35,
            font=("Poppins", 14)
        ).grid(
            row=len(self.labels)+4,
            column=0,
            pady=20,
            padx=20
        )
        
        self.suppression_champ()
        self.entries["Référence"].insert(0, intervention.ref)
        self.entries["Référence"].configure(state="readonly")
        self.entries["Date_d'intervention"].insert(0, intervention.date_intervention)
        self.entries["Durée"].insert(0, intervention.dure)
        self.entries["Outils"].insert(0, intervention.outils)
        self.entries["Machine"].insert(0, intervention.machine)
        self.entries["Machine"].configure(state="readonly")
        self.entries["Exécutant"].insert(0, intervention.executant)
        self.description.insert("1.0", intervention.description)
    
    def get_entre_with_statut(self) -> Dict[str, str]:
        """
        Récupère les valeurs dans les entry
        avev statut.
        """
        return{
            'ref': self.entries["Référence"].get().strip(),
            "date": self.entries["Date_d'intervention"].get().strip(),
            "dure": self.entries["Durée"].get().strip(),
            "outils": self.entries["Outils"].get().strip(),
            "machine": self.entries["Machine"].get().strip(),
            "executant": self.entries["Exécutant"].get().strip(),
            "description": self.description.get("1.0", "end").strip(),
            "statut": self.statut.get().strip()
        }
    
    def get_entre(self) -> Dict[str, str]:
        """
        Récupère les valeurs dans les entry.
        """
        return{
            'ref': self.entries["Référence"].get().strip(),
            "date": self.entries["Date_d'intervention"].get().strip(),
            "dure": self.entries["Durée"].get().strip(),
            "outils": self.entries["Outils"].get().strip(),
            "machine": self.entries["Machine"].get().strip(),
            "executant": self.entries["Exécutant"].get().strip(),
            "description": self.description.get("1.0", "end").strip()
            }

    def suppression_champ(self) -> None:
        """
        Supprime les données dans tous les champs.
        """
        self.entries["Référence"].delete("0", "end")
        self.entries["Date_d'intervention"].delete("0", "end")
        self.entries["Durée"].delete("0", "end")
        self.entries["Outils"].delete("0", "end")
        self.entries["Machine"].delete("0", "end")
        self.entries["Exécutant"].delete("0", "end")
        self.description.delete("1.0", "end")
    
    def suppr_selected(self) -> str:
        """Supprime une ligne."""
        return self.entries["Référence"].get()


if __name__ == "__main__":
    root = ctk.CTk()
    app = addIntervention(root)
    root.mainloop()
