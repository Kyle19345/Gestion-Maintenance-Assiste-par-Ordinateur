import customtkinter as ctk
from tkinter import ttk

class addMachine(ctk.CTkToplevel):
    def __init__(self,master,on_add = None,on_suppr = None):
        super().__init__(master)   
        self.title("Editer Machine")
        self.on_suppr = on_suppr        # Taille fixe
        self.resizable(False, False)   
        self.transient(master)               # Reste au-dessus du parent
        self.grab_set()    

        self.container = ctk.CTkFrame(self,corner_radius=12,border_width=1)
        self.container.grid(row=0,column=0,padx=15,pady=15,sticky ="nsew")
        ctk.CTkLabel(self.container,text = "Editer Machine",font=("Poppins",18,"bold")).grid(padx=20,pady=10)

        self.labels = ["ID","Nom","Catégorie","Date de service","Fabricant","Compteur"]
        placeholder = ["Ex : MCH-001","Ex: Compresseur d’air principal","Ex : Équipement hydraulique","JJ/MM/AAAA","Ex: Siemens",""]
        self.entries = {}

        for i,label in enumerate(self.labels):
            ctk.CTkLabel(self.container,text = label,font=("Poppins",13)).grid(row = i+1,column=0,pady= 8,padx=30,sticky ="e")
            entry = ctk.CTkEntry(self.container,width=300,placeholder_text=placeholder[i])
            entry.grid(row = i+1,column=1,pady=8,padx=50)
            self.entries[label.replace(" ","_")] = entry
        
        ctk.CTkButton(self.container,text = "Enregistrer",command = on_add,width=170,height=35,font=("Poppins",14)).grid(row=len(self.labels)+4,column =1,pady=20,padx=20,sticky="e")
    
    def afficher(self,machine,list_intervention):
        frame_container = ctk.CTkScrollableFrame(self,corner_radius=12,width=500)
        frame_container.grid(row=0,column=1,padx=(5,15),pady=10,sticky ="nsew")

        ctk.CTkLabel(frame_container,text = " Liste des interventions attribuées à la machine",font=("Poppins",13,"bold")).grid(row=0,column=0,padx=10,pady=10,sticky="w")
        bg_color = "#2b2b2b"       # Fond de la frame
        tree_bg = "#3c3f41"        # Fond du Treeview
        tree_fg = "#ffffff"         # Texte
        select_bg = "#4a90e2"      # Couleur sélection
        hover_color = "#505357"    # Survol de l'en-tête
        font = ("Arial", 10)        # Police pour le texte

        colonnes = ["Référence","Desctiption","Date d'intervention"]
        self.tree = ttk.Treeview(frame_container, columns=colonnes, show="headings", height=15)
        self.tree.grid(row=1,column=0,sticky="nsew", padx=10, pady=5)

        # Configuration des colonnes et en-têtes
        for col in colonnes:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150, anchor="center")

        # Style du Treeview
        style = ttk.Style()

        style.theme_use("clam")  # 'clam' est plus facilement customisable

        style.configure("Treeview",
                background=tree_bg,
                foreground=tree_fg,
                fieldbackground=tree_bg,
                font=font,
                bordercolor=tree_bg,
                rowheight = 25,  
                relief="flat")        

        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe"}) 
        ])

        style.configure("Treeview.Heading",
                        background=tree_bg,
                        foreground=tree_fg,
                        font=("Poppins", 11, "bold"),
                        relief="flat",          
                        bordercolor=tree_bg)   

        style.map("Treeview.Heading",
                background=[("active", hover_color)],
                relief=[("active", "flat")])

        frame_container.grid_columnconfigure(0, weight=1)
        frame_container.grid_rowconfigure(0, weight=1)


        lbl_etat = ctk.CTkLabel(self.container,text="Etat",font=("Poppins",13))
        lbl_etat.grid(row=len(self.labels)+3,column=0,pady = 8,padx=30,sticky ="e")
        self.etat = ctk.CTkComboBox(self.container,width = 300,values=["Actif","En maintenance","En panne"])
        self.etat.set("Actif")
        self.etat.grid(row=len(self.labels)+3,column=1,pady = 8,padx=50,sticky ="e")
        ctk.CTkButton(self.container,text = "Supprimer",fg_color="#BE7272",hover_color="red",command = self.on_suppr,width=170,height=35,font=("Poppins",14)).grid(row=len(self.labels)+4,column=0,pady=20,padx=20,sticky="e")

        for inter in list_intervention:
            self.tree.insert("","end",values=inter) 
            
        self.entries["ID"].insert(0,machine.ID)
        self.entries["ID"].configure(state = "readonly")
        self.entries["Nom"].insert(0,machine.nom)
        self.entries["Catégorie"].insert(0,machine.categorie)
        self.entries["Date_de_service"].insert(0,machine.date_service)
        self.entries["Date_de_service"].configure(state = "readonly")
        self.entries["Fabricant"].insert(0,machine.fabricant)
        self.entries["Compteur"].insert(0,machine.compteur)
    
    def get_entre_with_etat(self):
         return {
            "id" : self.entries["ID"].get().strip(),
            "nom" : self.entries["Nom"].get().strip(),
            "categorie": self.entries["Catégorie"].get().strip(),
            "date": self.entries["Date_de_service"].get().strip(),
            "fabricant" : self.entries["Fabricant"].get().strip(),
            "compteur" : self.entries["Compteur"].get().strip(),
            "etat" : self.etat.get()
        }
    
    def get_entre(self):
        return {
            "id" : self.entries["ID"].get().strip(),
            "nom" : self.entries["Nom"].get().strip(),
            "categorie": self.entries["Catégorie"].get().strip(),
            "date": self.entries["Date_de_service"].get().strip(),
            "fabricant" : self.entries["Fabricant"].get().strip(),
            "compteur" : self.entries["Compteur"].get().strip()
        }
    
    def delete_champ(self):
        self.entries["ID"].delete(0,"end")
        self.entries["Nom"].delete(0,"end")
        self.entries["Categorie"].delete(0,"end")
        self.entries["Date_de_service"].delete(0,"end")
        self.entries["Fabricant"].delete(0,"end")
        self.entries["Compteur"].delete(0,"end")

    def get_machine_delete(self):
        return self.entries["ID"].get()
    
if __name__ == "__main__":
    root = ctk.CTk()
    app = addMachine(root)
    root.mainloop()    

