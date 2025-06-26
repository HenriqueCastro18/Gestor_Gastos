import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from models import listar_gastos, remover_gasto, editar_gasto, adicionar_gasto
from tkcalendar import DateEntry

# Janela de formulário para adicionar um novo gasto
def janela_adicionar(db_file):
    win = tk.Toplevel(bg="#2e2e2e")
    win.title("Adicionar Gasto")
    win.geometry("350x400")
    win.resizable(False, False)

    # Estilos visuais
    estilo_label = {"bg": "#2e2e2e", "fg": "white", "font": ("Helvetica", 10, "bold")}
    estilo_entry = {"bg": "white", "fg": "black", "insertbackground": "black", "relief": "flat"}

    container = tk.Frame(win, bg="#2e2e2e")
    container.pack(padx=20, pady=20)

    # Campo de valor
    tk.Label(container, text="Valor:", **estilo_label).grid(row=0, column=0, sticky="w", pady=(0, 2))
    valor_entry = tk.Entry(container, **estilo_entry)
    valor_entry.grid(row=1, column=0, sticky="we", pady=(0, 10))

    # Campo de data (com calendário)
    tk.Label(container, text="Data:", **estilo_label).grid(row=2, column=0, sticky="w", pady=(0, 2))
    data_entry = DateEntry(
        container,
        date_pattern="dd/MM/yyyy",
        background="white",
        foreground="black",
        borderwidth=1,
        headersbackground="#2e2e2e",
        normalbackground="#f5f5f5",
        weekendbackground="#2e2e2e",
        headersforeground="white",
        normalforeground="black",
        weekendforeground="white",
        selectbackground="#4CAF50",
        selectforeground="white"
    )
    data_entry.grid(row=3, column=0, sticky="we", pady=(0, 10))

    # Campo de descrição
    tk.Label(container, text="Descrição:", **estilo_label).grid(row=4, column=0, sticky="w", pady=(0, 2))
    desc_entry = tk.Entry(container, **estilo_entry)
    desc_entry.grid(row=5, column=0, sticky="we", pady=(0, 10))

    # Área de parcelas (inicialmente escondida)
    frame_parcelas = tk.Frame(container, bg="#2e2e2e")
    lbl_parcelas = tk.Label(frame_parcelas, text="Qtd de parcelas:", **estilo_label)
    entry_parcelas = tk.Entry(frame_parcelas, width=5, **estilo_entry)
    lbl_parcelas.pack(side="left")
    entry_parcelas.pack(side="left", padx=5)
    frame_parcelas.grid(row=6, column=0, sticky="w", pady=(0, 10))
    frame_parcelas.grid_remove()

    # Checkbox de parcelado
    parcela_var = tk.IntVar()

    def toggle_parcelas():
        if parcela_var.get():
            frame_parcelas.grid()
        else:
            frame_parcelas.grid_remove()

    tk.Checkbutton(container, text="É parcelado?", variable=parcela_var,
                   bg="#2e2e2e", fg="white", selectcolor="#2e2e2e",
                   activebackground="#2e2e2e", activeforeground="white",
                   command=toggle_parcelas).grid(row=7, column=0, sticky="w", pady=(0, 20))

    # Botões de ação (Salvar / Cancelar)
    def salvar():
        try:
            valor = float(valor_entry.get())
            data = data_entry.get_date().isoformat()
            desc = desc_entry.get().strip()
            parcelas = int(entry_parcelas.get()) if parcela_var.get() else 1
            adicionar_gasto(valor, data, desc, parcelas, db_file)
            messagebox.showinfo("Sucesso", "Gasto adicionado!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Verifique os dados inseridos.\n{e}")

    btn_frame = tk.Frame(container, bg="#2e2e2e")
    btn_frame.grid(row=8, column=0)

    tk.Button(btn_frame, text="Salvar", bg="#4CAF50", fg="white",
              font=("Helvetica", 10, "bold"), command=salvar).pack(side="left", padx=5)

    tk.Button(btn_frame, text="Cancelar", bg="#F44336", fg="white",
              font=("Helvetica", 10, "bold"), command=win.destroy).pack(side="left", padx=5)



# Janela para consultar, editar ou remover gastos
def janela_consultar(db_file):
    win = tk.Toplevel(bg="#2e2e2e")
    win.title("Consultar Gastos")
    win.geometry("800x500")

    # Configuração da tabela visual (Treeview)
    tree = ttk.Treeview(win, columns=("ID", "Gasto", "Data", "Descrição", "Parcelas"), show="headings")
    tree.heading("ID", text="ID")
    tree.column("ID", width=50, anchor="center")
    tree.heading("Gasto", text="Gasto")
    tree.column("Gasto", width=100, anchor="center")
    tree.heading("Data", text="Data")
    tree.column("Data", width=100, anchor="center")
    tree.heading("Descrição", text="Descrição")
    tree.column("Descrição", width=300, anchor="w")
    tree.heading("Parcelas", text="Parcelas")
    tree.column("Parcelas", width=80, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Exibe o total calculado dos gastos
    lbl_total = tk.Label(win, bg="#2e2e2e", fg="white", font=("Helvetica", 12, "bold"))
    lbl_total.pack(pady=(5, 20))

    btn_frame = tk.Frame(win, bg="#2e2e2e")
    btn_frame.pack(pady=(0, 30))

    # Atualiza a lista de gastos e o total
    def atualizar():
        for i in tree.get_children():
            tree.delete(i)
        dados = listar_gastos(db_file)
        total = 0
        for id_g, v, d, desc, p in dados:
            total += v
            data_fmt = datetime.datetime.strptime(d, "%Y-%m-%d").strftime("%d/%m/%Y")
            tree.insert("", "end", values=(id_g, f"R$ {v:.2f}", data_fmt, desc, f"{p}x"))
        lbl_total.config(text=f"TOTAL DOS GASTOS: R$ {total:.2f}")

    # Remove um gasto selecionado
    def remover():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um gasto.")
            return
        id_g = int(tree.item(sel[0])["values"][0])
        remover_gasto(id_g, db_file)
        atualizar()
        messagebox.showinfo("Sucesso", "Gasto removido.")

    # Abre janela para editar um gasto
    def editar():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um gasto.")
            return
        valores = tree.item(sel[0])["values"]
        abrir_janela_editar(valores, atualizar, db_file)

    # Botões de ação
    tk.Button(btn_frame, text="Remover Gasto", bg="#F44336", fg="white", width=15, command=remover).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Editar Gasto", bg="#2196F3", fg="white", width=15, command=editar).pack(side="left", padx=5)

    tk.Button(win, text="Voltar", bg="#555555", fg="white", width=10, command=win.destroy).place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    atualizar()


# Janela de edição de um gasto existente
def abrir_janela_editar(valores, atualizar_callback, db_file):
    id_gasto = int(valores[0])
    win = tk.Toplevel(bg="#2e2e2e")
    win.title("Editar Gasto")
    win.geometry("320x360")
    win.resizable(False, False)

    # Entrada para valor
    tk.Label(win, text="Valor:", bg="#2e2e2e", fg="white").pack()
    valor_entry = tk.Entry(win, bg="#3c3c3c", fg="white", insertbackground="white")
    valor_entry.pack()
    valor_entry.insert(0, valores[1].replace("R$ ", ""))

    # Entrada para data (formato texto)
    tk.Label(win, text="Data (DD/MM/AAAA):", bg="#2e2e2e", fg="white").pack()
    data_entry = tk.Entry(win, bg="#3c3c3c", fg="white", insertbackground="white")
    data_entry.pack()
    data_entry.insert(0, valores[2])

    # Entrada para descrição
    tk.Label(win, text="Descrição:", bg="#2e2e2e", fg="white").pack()
    desc_entry = tk.Entry(win, bg="#3c3c3c", fg="white", insertbackground="white")
    desc_entry.pack()
    desc_entry.insert(0, valores[3])

    # Define se gasto é parcelado
    parcela_var = tk.IntVar()
    qtd = int(valores[4].replace("x", ""))
    if qtd > 1:
        parcela_var.set(1)

    # Checkbox de parcelado
    tk.Checkbutton(win, text="É parcelado?", variable=parcela_var, bg="#2e2e2e", fg="white",
                   command=lambda: toggle()).pack()

    # Entrada de número de parcelas
    frame = tk.Frame(win, bg="#2e2e2e")
    lbl = tk.Label(frame, text="Qtd de parcelas:", bg="#2e2e2e", fg="white")
    ent = tk.Entry(frame, width=5, bg="#3c3c3c", fg="white", insertbackground="white")
    ent.insert(0, str(qtd))

    def toggle():
        if parcela_var.get():
            frame.pack()
            lbl.pack(side="left")
            ent.pack(side="left")
        else:
            frame.pack_forget()

    if parcela_var.get():
        toggle()

    # Botão para salvar alterações
    def salvar():
        try:
            valor = float(valor_entry.get())
            data = datetime.datetime.strptime(data_entry.get(), "%d/%m/%Y").date().isoformat()
            desc = desc_entry.get().strip()
            parc = int(ent.get()) if parcela_var.get() else 1
            editar_gasto(id_gasto, valor, data, desc, parc, db_file)
            messagebox.showinfo("Sucesso", "Gasto atualizado!")
            atualizar_callback()
            win.destroy()
        except:
            messagebox.showerror("Erro", "Verifique os dados.")

    tk.Button(win, text="Salvar", bg="#4CAF50", fg="white", command=salvar).pack(pady=5)
    tk.Button(win, text="Cancelar", bg="#F44336", fg="white", command=win.destroy).pack()
