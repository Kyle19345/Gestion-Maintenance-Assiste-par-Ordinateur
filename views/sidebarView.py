import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self,master,controller,width=220,height= 500):
        super().__init__(master,width=width,height=height)#,fg_color="#162A43")
       
        bouton_machine = ctk.CTkButton(self,text = "Machine",font=("Poppins",14),command = controller.show_machine,height=35)
        bouton_machine.grid(row=1,column=0,pady=(40,12),padx=20,sticky="ew")

        bouton_intervention = ctk.CTkButton(self,text = "Intervention",font=("Poppins",14),command = controller.show_intervention,height=35)
        bouton_intervention.grid(row=3,column=0,pady=12,padx=20,sticky="ew")

        bouton_planing = ctk.CTkButton(self,text = "Planing",font=("Poppins",14),command = controller.show_planing,height=35)
        bouton_planing.grid(row=2,column=0,pady=12,padx=20,sticky="ew")


class Header(ctk.CTkFrame):
    def __init__(self,master,height = 100):
        super().__init__(master,height=height)#fg_color="#14233A")
        self.grid_propagate(False)

        ctk.CTkLabel(self,text = "Gestion de Maintenance Assisté par Ordinateur",font=("Poppins",30,"bold")).grid(row=0,column=0,sticky="w",padx=20,pady=20)

if __name__ == '__main__':
    class controller:
        def show_machine(self):
            pass
        def show_intervention(self):
            pass
    contr = controller()
    root = ctk.CTk()
    app = Sidebar(root,contr)
    app.pack()
    root.mainloop()