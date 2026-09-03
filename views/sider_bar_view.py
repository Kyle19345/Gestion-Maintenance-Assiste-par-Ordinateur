"""
Ce module regroupe les interfaces Header et Sider
"""
import customtkinter as ctk

from views._ui_utils import create_button, create_label



class Sidebar(ctk.CTkFrame):
    def __init__(
            self,
            master: ctk.CTk,
            controller,
            width: int=220,
            height: int=500
        ):
        super().__init__(
            master,
            width=width,
            height=height
            )

        self.controller = controller
       
        bouton_machine = create_button(
            self,
            text="Machine",
            font=("Poppins", 14),
            command=self.controller.show_machine,
            height=35
        )
        bouton_machine.grid(
            row=1,
            column=0,
            pady=(40, 12),
            padx=20,
            sticky="ew"
        )

        bouton_intervention = create_button(
            self,
            text="Intervention",
            font=("Poppins", 14),
            command=self.controller.show_intervention,
            height=35
        )
        
        bouton_intervention.grid(
            row=3,
            column=0,
            pady=12,
            padx=20,
            sticky="ew"
        )

        bouton_planing = create_button(
            self,
            text="Planing",
            font=("Poppins", 14),
            command=self.controller.show_planing,
            height=35
        )
        bouton_planing.grid(
            row=2,
            column=0,
            pady=12,
            padx=20,
            sticky="ew"
        )


class Header(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, height: int=100):
        super().__init__(master, height=height)
        self.grid_propagate(False)

        create_label(
            self,
            text="Gestion de Maintenance Assisté par Ordinateur",
            font=("Poppins", 30, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=20
        )


if __name__ == '__main__':
    class controller:
        def show_machine(self):
            pass
        def show_intervention(self):
            pass

    contr = controller()
    root = ctk.CTk()
    app = Sidebar(root, contr)
    app.pack()
    root.mainloop()
