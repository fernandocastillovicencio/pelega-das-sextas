import sqlite3

import pandas as pd

# 📌 Caminho do banco de dados
DB_PATH = "data/dados.db"

# 📌 Conectar ao banco
conn = sqlite3.connect(DB_PATH)

# 📌 Consultar a tabela 'jogadores'
df = pd.read_sql_query("SELECT * FROM jogadores", conn)

# 📌 Fechar conexão
conn.close()

# 📌 Exibir os dados
print(df)
