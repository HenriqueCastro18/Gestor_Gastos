import os
from database import criar_tabela
from models import atualizar_parcelas
import tkinter as tk
from tkinter import ttk, messagebox


# Lista todos os arquivos .db (contas disponíveis)
def listar_contas():
    return [f for f in os.listdir() if f.endswith(".db")]

# Janela para criação de nova conta (novo arquivo .db)
def criar_conta_janela(root, lbl_conta, callback_atualizar):
    win = tk.Toplevel(root)
    win.title("Criar Nova Conta")
    win.geometry("300x150")
    win.configure(bg="#2e2e2e")
    win.resizable(False, False)

    tk.Label(win, text="Nome da nova conta:", bg="#2e2e2e", fg="white").pack(pady=10)
    entry = tk.Entry(win, bg="#3c3c3c", fg="white", insertbackground="white")
    entry.pack()

    def salvar():
        nome = entry.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Nome da conta não pode ser vazio.")
            return
        if not nome.endswith(".db"):
            nome += ".db"
        if os.path.exists(nome):
            messagebox.showerror("Erro", "Conta já existe.")
            return
        criar_tabela(nome)
        atualizar_parcelas(nome)
        lbl_conta.config(text=nome.replace(".db", ""))
        callback_atualizar(nome)
        messagebox.showinfo("Sucesso", f"Conta '{nome}' criada e selecionada.")
        win.destroy()

    tk.Button(win, text="Criar", bg="#4CAF50", fg="white", command=salvar).pack(pady=10)
    tk.Button(win, text="Cancelar", bg="#F44336", fg="white", command=win.destroy).pack()

# Janela para trocar entre contas já criadas
def trocar_conta_janela(root, lbl_conta, callback_atualizar):
    win = tk.Toplevel(root)
    win.title("Trocar Conta")
    win.geometry("300x150")
    win.configure(bg="#2e2e2e")
    win.resizable(False, False)

    tk.Label(win, text="Selecione a conta:", bg="#2e2e2e", fg="white").pack(pady=10)

    contas = listar_contas()
    combo = ttk.Combobox(win, values=contas, state="readonly")
    combo.pack(pady=5)

    def aplicar():
        selecionada = combo.get()
        if not selecionada:
            messagebox.showerror("Erro", "Selecione uma conta.")
            return
        lbl_conta.config(text=selecionada.replace(".db", ""))
        callback_atualizar(selecionada)
        messagebox.showinfo("Sucesso", f"Agora usando: {selecionada}")
        win.destroy()

    tk.Button(win, text="Usar Conta", bg="#2196F3", fg="white", command=aplicar).pack(pady=5)
    tk.Button(win, text="Cancelar", bg="#F44336", fg="white", command=win.destroy).pack()

# Janela para excluir uma conta existente (exceto a ativa)
def excluir_conta_janela(root, conta_ativa):
    win = tk.Toplevel(root)
    win.title("Excluir Conta")
    win.geometry("300x150")
    win.configure(bg="#2e2e2e")
    win.resizable(False, False)

    tk.Label(win, text="Selecione a conta:", bg="#2e2e2e", fg="white").pack(pady=10)

    contas = [c for c in listar_contas() if c != conta_ativa]
    if not contas:
        messagebox.showinfo("Aviso", "Nenhuma conta disponível para exclusão.")
        win.destroy()
        return

    combo = ttk.Combobox(win, values=contas, state="readonly")
    combo.pack(pady=5)

    def excluir():
        selecionada = combo.get()
        if not selecionada:
            messagebox.showerror("Erro", "Selecione uma conta.")
            return
        confirmar = messagebox.askyesno("Confirmar", f"Excluir '{selecionada}'?")
