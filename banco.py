import sqlite3
import os

# 📌 Criar a pasta 'data' se não existir
if not os.path.exists("data"):
    os.makedirs("data")

# 📌 Caminho do banco de dados dentro da pasta 'data'
db_path = "data/dados.db"

# 📌 Criar conexão com SQLite no novo caminho
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 📌 Criar tabela de Jogos (times, placar e artilheiros)
cursor.execute("""
CREATE TABLE IF NOT EXISTS jogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    time1 TEXT,
    gols_time1 INTEGER,
    time2 TEXT,
    gols_time2 INTEGER,
    artilheiros TEXT,
    num_times INTEGER DEFAULT 2,
    pontos_vitoria INTEGER DEFAULT 3,
    pontos_empate INTEGER DEFAULT 1
)
""")

# 📌 Adicionar colunas se não existirem
try:
    cursor.execute("ALTER TABLE jogos ADD COLUMN num_times INTEGER DEFAULT 2")
    cursor.execute("ALTER TABLE jogos ADD COLUMN pontos_vitoria INTEGER DEFAULT 3")
    cursor.execute("ALTER TABLE jogos ADD COLUMN pontos_empate INTEGER DEFAULT 1")
except sqlite3.OperationalError:
    pass  # Se as colunas já existem, continuar normalmente

# 📌 Criar tabela de Rankings (jogadores, vitórias, empates, derrotas, pontos, gols)
cursor.execute("""
CREATE TABLE IF NOT EXISTS rankings (
    jogador TEXT PRIMARY KEY,
    vitorias INTEGER DEFAULT 0,
    empates INTEGER DEFAULT 0,
    derrotas INTEGER DEFAULT 0,
    pontos INTEGER DEFAULT 0,
    gols INTEGER DEFAULT 0
)
""")

# 📌 Salvar e fechar conexão
conn.commit()
conn.close()

print("📌 Banco de Dados Atualizado com Sucesso!")
