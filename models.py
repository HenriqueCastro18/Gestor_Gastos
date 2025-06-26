import datetime
from database import conectar

# Adiciona um novo gasto na base de dados
def adicionar_gasto(valor, data, descricao, parcelas, db_file):
    conn = conectar(db_file)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Gastos (valor, data, descricao, parcelas, ultima_atualizacao) VALUES (?, ?, ?, ?, ?)",
        (valor, data, descricao, parcelas, datetime.date.today().isoformat())
    )
    conn.commit()
    conn.close()

# Atualiza o número de parcelas conforme o tempo passa.
# Remove gastos finalizados (parcelas <= 0)
def atualizar_parcelas(db_file):
    conn = conectar(db_file)
    cur = conn.cursor()
    cur.execute("SELECT id, descricao, parcelas, ultima_atualizacao FROM Gastos")
    gastos = cur.fetchall()
    hoje = datetime.date.today()
    excluidos = []

    for id_gasto, descricao, parcelas, ultima in gastos:
        ultima_date = datetime.datetime.strptime(ultima, "%Y-%m-%d").date()
        meses_passados = (hoje.year - ultima_date.year) * 12 + (hoje.month - ultima_date.month)
        if meses_passados > 0:
            novas_parcelas = parcelas - meses_passados
            if novas_parcelas <= 0:
                cur.execute("DELETE FROM Gastos WHERE id = ?", (id_gasto,))
                excluidos.append(f"ID {id_gasto} - {descricao}")
            else:
                cur.execute("UPDATE Gastos SET parcelas = ?, ultima_atualizacao = ? WHERE id = ?",
                            (novas_parcelas, hoje.isoformat(), id_gasto))

    conn.commit()
    conn.close()

    # Mostra alerta com os gastos removidos, se houver
    if excluidos:
        from tkinter import messagebox
        messagebox.showinfo("Gastos Excluídos", "Os seguintes gastos foram excluídos automaticamente:\n" + "\n".join(excluidos))

# Retorna todos os gastos registrados
def listar_gastos(db_file):
    conn = conectar(db_file)
    cur = conn.cursor()
    cur.execute("SELECT id, valor, data, descricao, parcelas FROM Gastos")
    dados = cur.fetchall()
    conn.close()
    return dados

# Remove um gasto específico pelo ID
def remover_gasto(id_gasto, db_file):
    conn = conectar(db_file)
    cur = conn.cursor()
    cur.execute("DELETE FROM Gastos WHERE id = ?", (id_gasto,))
    conn.commit()
    conn.close()

# Atualiza os dados de um gasto existente
def editar_gasto(id_gasto, valor, data, descricao, parcelas, db_file):
    conn = conectar(db_file)
    cur = conn.cursor()
    cur.execute("""
        UPDATE Gastos SET valor = ?, data = ?, descricao = ?, parcelas = ?, ultima_atualizacao = ?
        WHERE id = ?
    """, (valor, data, descricao, parcelas, datetime.date.today().isoformat(), id_gasto))
    conn.commit()
    conn.close()
