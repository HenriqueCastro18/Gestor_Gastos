from tkinter import ttk

# Configura estilos visuais para Treeview e Scrollbar (modo escuro)
def configurar_estilo():
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("Treeview", background="#3c3c3c", foreground="white", fieldbackground="#3c3c3c", rowheight=25)
    style.map("Treeview", background=[("selected", "#555555")], foreground=[("selected", "white")])
    
    style.configure("Vertical.TScrollbar", background="#555555", troughcolor="#2e2e2e",
                    bordercolor="#2e2e2e", arrowcolor="white")
