import sqlite3

DB_FILE = "Gastos.db"

# Retorna uma conexão com o banco de dados
def conectar(db_file=DB_FILE):
    return sqlite3.connect(db_file)

# Cria a tabela 'Gastos' se ela não existir
def criar_tabela(db_file=DB_FILE):
    conn = conectar(db_file)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            parcelas INTEGER NOT NULL,
            ultima_atualizacao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
