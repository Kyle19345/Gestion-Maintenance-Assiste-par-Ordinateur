import customtkinter as ctk

class InterventionView(ctk.CTkToplevel):
    def __init__(self,master,ajouter = None,on_suppr = None):
        super().__init__(master)
        self.title("Editer Intervention")
        self.on_suppr = on_suppr
        self.resizable(False, False)   
        self.transient(master)               # Reste au-dessus du parent
        self.grab_set()    

        self.frame_container = ctk.CTkFrame(self,corner_radius=12,border_width=1)
        self.frame_container.pack(expand ="True",fill="both",padx=15,pady=15)

        ctk.CTkLabel(self.frame_container,text = "Intervention",font=("Poppins",18,"bold")).grid(row=0,column=0,pady=10)

        self.labels = ["Référence","Date d'intervention","Durée","Machine","Outils","Exécutant"]
        placeholder = ["Ex : INT-2025-001","JJ/MM/AAAA","","Ex : MCH-001","EX : Clé dynamométrique, tournevis","Ex : Rakoto Jean"]
        self.entries = {}

        for i,label in enumerate(self.labels):
            ctk.CTkLabel(self.frame_container,text = label,font=("Poppins",13)).grid(row=i+1,column=0,pady = 8,padx=30,sticky="e")
            entry = ctk.CTkEntry(self.frame_container,width=300,placeholder_text=placeholder[i])
            entry.grid(row = i+1,column=1,pady=8,padx=30)
            self.entries[label.replace(" ","_")] = entry

        ctk.CTkLabel(self.frame_container,text = "Description",font=("Poppins",13)).grid(row=len(self.labels)+3,column=0,padx=30,sticky="e")
        self.description = ctk.CTkTextbox(self.frame_container,height=75,width=300)
        self.description.grid(row=len(self.labels)+3,column =1,padx=30,pady=8)

        ctk.CTkButton(self.frame_container,text="Enregistrer",command = ajouter,width=170,height=35,font=("Poppins",14)).grid(row=len(self.labels)+4,column=1,pady=20,padx=20,sticky="e")

       
    def afficher(self,intervention):
        lbl_statut = ctk.CTkLabel(self.frame_container,text="Statut",font=("Poppins",13))
        lbl_statut.grid(row=len(self.labels)+2,column=0,padx=30,pady=8)

        self.statut = ctk.CTkComboBox(self.frame_container,width=300,values=["Planifié","En cours","Réalisé"],state="readonly")
        self.statut.set("planifié")
        self.statut.grid(row=len(self.labels)+2,column=1,padx=30,pady=8)

        ctk.CTkButton(self.frame_container,text="Supprimer",fg_color="#BE7272",hover_color="red",command = self.on_suppr,width=170,height=35,font=("Poppins",14)).grid(row=len(self.labels)+4,column=0,pady=20,padx=20)

        self.suppression_champ()
        self.entries["Référence"].insert(0,intervention.ref)
        self.entries["Référence"].configure(state = "readonly")
        self.entries["Date_d'intervention"].insert(0,intervention.date_intervention)
        self.entries["Durée"].insert(0,intervention.dure)
        self.entries["Outils"].insert(0,intervention.outils)
        self.entries["Machine"].insert(0,intervention.machine)
        self.entries["Machine"].configure(state = "readonly")
        self.entries["Exécutant"].insert(0,intervention.executant)
        self.description.insert("1.0",intervention.description)
    

 

    def get_entre_with_statut(self):
        return{
            'ref' : self.entries["Référence"].get().strip(),
            "date": self.entries["Date_d'intervention"].get().strip(),
            "dure": self.entries["Durée"].get().strip(),
            "outils":self.entries["Outils"].get().strip(),
            "machine": self.entries["Machine"].get().strip(),
            "executant": self.entries["Exécutant"].get().strip(),
            "description": self.description.get("1.0","end").strip(),
            "statut": self.statut.get().strip()
            }
    
    def get_entre(self):
        return{
            'ref' : self.entries["Référence"].get().strip(),
            "date": self.entries["Date_d'intervention"].get().strip(),
            "dure": self.entries["Durée"].get().strip(),
            "outils":self.entries["Outils"].get().strip(),
            "machine": self.entries["Machine"].get().strip(),
            "executant": self.entries["Exécutant"].get().strip(),
            "description": self.description.get("1.0","end").strip()
            }

    
    def suppression_champ(self):
        self.entries["Référence"].delete("0","end")
        self.entries["Date_d'intervention"].delete("0","end")
        self.entries["Durée"].delete("0","end")
        self.entries["Outils"].delete("0","end")
        self.entries["Machine"].delete("0","end")
        self.entries["Exécutant"].delete("0","end")
        self.description.delete("1.0","end")
    
    def suppr_selected(self):
        return self.entries["Référence"].get()
    


if __name__ == "__main__":
    root = ctk.CTk()
    app = InterventionView(root)
    root.mainloop()
            