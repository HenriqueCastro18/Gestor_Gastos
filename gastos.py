import tkinter as tk
from database import criar_tabela
from models import atualizar_parcelas
from utils import configurar_estilo
from views import janela_adicionar, janela_consultar
from contas import criar_conta_janela, trocar_conta_janela, excluir_conta_janela
import threading
import time

# Conta ativa atual. Pode ser atualizada dinamicamente no app.
conta_ativa = ["Gastos.db"]

# Atualiza a conta em uso, criando a tabela e verificando parcelas vencidas.
def atualizar_conta(nova):
    conta_ativa[0] = nova
    criar_tabela(nova)
    atualizar_parcelas(nova)

# Função principal do app. Configura a UI e inicializa a conta padrão.
def main():
    criar_tabela(conta_ativa[0])
    atualizar_parcelas(conta_ativa[0])

    root = tk.Tk()
    root.title("Gestor de Gastos")
    root.geometry("520x480")
    root.configure(bg="#2e2e2e")
    root.resizable(False, False)

    configurar_estilo()

    lbl_conta = tk.Label(root, text=conta_ativa[0].replace(".db", ""), bg="#2e2e2e", fg="#69F0AE", font=("Helvetica", 18, "bold italic"))
    lbl_conta.place(relx=0.5, y=30, anchor="center")

    frame = tk.Frame(root, bg="#2e2e2e")
    frame.place(relx=0.5, rely=0.35, anchor="center")

    # Estilo padrão dos botões principais
    style_btn = {"fg": "white", "width": 15, "height": 2, "font": ("Helvetica", 10, "bold")}

    # Botão para adicionar um novo gasto
    tk.Button(frame, text="Adicionar Gasto", bg="#43A047", activebackground="#348038",
              command=lambda: janela_adicionar(conta_ativa[0]), **style_btn).pack(side="left", padx=5)

    # Botão para consultar os gastos registrados
    tk.Button(frame, text="Consultar Gastos", bg="#42A5F5", activebackground="#3784C4",
              command=lambda: janela_consultar(conta_ativa[0]), **style_btn).pack(side="left", padx=5)

    bottom_frame = tk.Frame(root, bg="#2e2e2e")
    bottom_frame.place(relx=0.5, rely=0.6, anchor="center")

    # Botão para criar uma nova conta de gastos
    tk.Button(bottom_frame, text="Criar Conta", bg="#8E24AA", activebackground="#611975",
              command=lambda: criar_conta_janela(root, lbl_conta, atualizar_conta), **style_btn).grid(row=0, column=0, padx=5, pady=5)

    # Botão para alternar entre diferentes contas
    tk.Button(bottom_frame, text="Trocar Conta", bg="#FDD835", activebackground="#B69B26",
              command=lambda: trocar_conta_janela(root, lbl_conta, atualizar_conta), **style_btn).grid(row=0, column=1, padx=5, pady=5)

    # Botão para excluir contas existentes (exceto a atual)
    tk.Button(bottom_frame, text="Excluir Conta", bg="#D32F2F", activebackground="#861C1C",
              command=lambda: excluir_conta_janela(root, conta_ativa[0]), **style_btn).grid(row=1, column=0, columnspan=2, pady=(40, 0))

    # Botão para sair do app
    tk.Button(root, text="Sair", bg="#616161", activebackground="#3B3B3B",
              command=root.destroy, **style_btn).place(relx=0.5, rely=1.0, anchor="s", y=-20)

    root.mainloop()

if __name__ == "__main__":
    main()
