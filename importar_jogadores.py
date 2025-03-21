import sqlite3

import numpy as np
import pandas as pd

# 📌 Caminhos do banco de dados e do CSV
DB_PATH = "data/dados.db"
CSV_PATH = "data/jogadores.csv"

# 📌 Conectar ao banco de dados
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 📌 Carregar os dados do CSV
df = pd.read_csv(CSV_PATH)

# 📌 Padronizar nomes das colunas para o formato do banco de dados
df.rename(
    columns={
        "Jogador": "nome",
        "Pos1": "posicao_primaria",
        "Pos2": "posicao_secundaria",
        "Físico": "fisico",
        "Defesa": "defesa",
        "Tática": "tatica",
        "Velocidade": "velocidade",
        "Técnica": "tecnica",
        "Ataque": "ataque",
    },
    inplace=True,
)

# 📌 Remover colunas desnecessárias
df = df[
    [
        "nome",
        "posicao_primaria",
        "posicao_secundaria",
        "fisico",
        "defesa",
        "tatica",
        "velocidade",
        "tecnica",
        "ataque",
    ]
]

# 📌 Converter valores decimais para inteiros (arredondando)
for col in ["fisico", "defesa", "tatica", "velocidade", "tecnica", "ataque"]:
    df[col] = df[col].apply(
        lambda x: int(round(x))
    )  # Arredonda e converte para inteiro

# 📌 Substituir valores NaN em `posicao_secundaria` por NULL
df["posicao_secundaria"].replace("", None, inplace=True)

# 📌 Inserir os jogadores no banco de dados
for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO jogadores (nome, posicao_primaria, posicao_secundaria, fisico, defesa, tatica, velocidade, tecnica, ataque)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(nome) DO UPDATE SET
            posicao_primaria = excluded.posicao_primaria,
            posicao_secundaria = excluded.posicao_secundaria,
            fisico = excluded.fisico,
            defesa = excluded.defesa,
            tatica = excluded.tatica,
            velocidade = excluded.velocidade,
            tecnica = excluded.tecnica,
            ataque = excluded.ataque
    """,
        tuple(row),
    )

# 📌 Fechar conexão
conn.commit()
conn.close()

print("📌 Jogadores importados com sucesso do CSV para o banco de dados!")
