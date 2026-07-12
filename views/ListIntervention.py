#list intervention

import customtkinter as ctk
from tkinter import ttk,font


def ellipsize_for_width(text, avail_px, tkfont):
    if tkfont.measure(text) <= avail_px:
        return text
    ell = "…"
    lo, hi = 0, len(text)
    while lo < hi:
        mid = (lo + hi) // 2
        candidate = text[:mid].rstrip() + ell
        if tkfont.measure(candidate) <= avail_px:
            lo = mid + 1
        else:
            hi = mid
    return text[:max(0, lo-1)].rstrip() + ell

class ListIntervention(ctk.CTkFrame):
    def __init__(self, master, on_select = None,on_search = None,width=1000,height = 450):
        super().__init__(master,width=width,height=height,corner_radius= 8)
        self.width = width
        self.height = height

        self.on_select = on_select
        
        self.column_headers = ["Référence","Description","Date d'intervention","Dure","Machine","Outils","Executant","statut"]
        self.column_attrs = ["ref","description","date_intervention","dure","machine","outils","executant","statut"]

        self.head_font = font.Font(family="Poppins", size=11, weight="bold")
        self.cell_font = font.Font(family="Poppins", size=10)

        frame = ctk.CTkFrame(self)
        frame.pack(fill = "both",expand = True,pady=20,padx=20)
        lbl = ctk.CTkLabel(frame, text="📋 Liste des interventions", font= ("Poppins",18,"bold"))
        lbl.grid(row=0,column=0,pady=20,padx=20,sticky="w")

        self.barre_recherche = ctk.CTkEntry(frame,width=400)
        self.barre_recherche.grid(row=1,column=0,pady=20,padx=20)
        self.bouton_rechercher = ctk.CTkButton(frame,text = "Rechercher 🔍",width=170,command=on_search,height=35,font=("Poppins",14))
        self.bouton_rechercher.grid(sticky="w",row=1,column=1,pady=20)

        container = ctk.CTkScrollableFrame(self, width=950, height=370)
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        bg_color = "#2b2b2b"
        even_color = "#333333"
        odd_color = "#3a3a3a"
        text_color = "#f2f2f2"
        select_bg = "#3C4577"
        hover_color = "#3C4577"
        
    
        container.configure(fg_color=bg_color)

       
        style = ttk.Style()
        try:
            style.theme_use('clam')  
        except Exception:
            pass

       
        tree_style_name = "Custom.Treeview"

       
        style.configure(tree_style_name,
                        background=bg_color,
                        fieldbackground=bg_color,
                        foreground=text_color,
                        rowheight=26,
                        font=self.cell_font,
                        borderwidth=0,
                        relief="flat",
                        lightcolor=bg_color,
                        darkcolor=bg_color,
                        bordercolor=bg_color)
        
        style.layout("Treeview", [
    ("Treeview.treearea", {"sticky": "nswe"}) 
])
        style.configure(tree_style_name + ".Heading",
                        font=self.head_font,
                        foreground=text_color,
                        background=even_color,
                        bordercolor=bg_color,
                        relief="flat")

        style.map("Treeview.Heading",
                background=[("active", hover_color)],  
                relief=[("active", "flat")]          
)

        # --- Création du Treeview en précisant le style personnalisé ---
        self.tree = ttk.Treeview(container, columns=self.column_attrs, show="headings", height=13,
                                 style=tree_style_name)
        self.tree.pack(fill="both", expand=True, pady=5, padx=5)

        total = self.width - 60
        weights = [10,20,15,10,10,12,10,8]
        s = sum(weights[:len(self.column_attrs)])
        pix = [max(60, int(total * w / s)) for w in weights[:len(self.column_attrs)]]

        for header, attr, w in zip(self.column_headers, self.column_attrs, pix):
            self.tree.heading(attr, text=header, anchor="w")
            self.tree.column(attr, width=w, anchor="w", stretch=False)

        # tags pour alternance de lignes
        self.tree.tag_configure("odd", background=odd_color)
        self.tree.tag_configure("even", background=even_color)

        self.tree.bind("<Double-1>", self._on_double_click)
        self._donnees = []
    
    def _normalize_row(self, intervention):
        return [getattr(intervention, attr, "") for attr in self.column_attrs]

    def afficher(self, donne):
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
            
    def search_get(self):
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
    app = ListIntervention(root,on_select)
    app.pack()  
    inter =[
        Intervention(1,"gf","gmfj","mlgjd","gfmj","gmfj","lgm","gmfj")
        
    ]
    app.afficher(inter)
    root.mainloop()

    