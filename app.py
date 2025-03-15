import streamlit as st
import sqlite3
import pandas as pd
import os

# 📌 Definir caminho do banco de dados na pasta 'data'
db_path = "data/dados.db"

# 📌 Função para carregar dados do banco
def carregar_dados():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 📌 Carregar ranking completo
    cursor.execute("SELECT * FROM rankings ORDER BY pontos DESC, gols DESC")
    rankings = cursor.fetchall()

    conn.close()
    return rankings

# 📌 Atualizar Ranking Automaticamente
def atualizar_ranking():
    os.system("python atualizar_rankings.py")

# 📌 Interface do Streamlit
st.title("⚽ Gestão da Pelada")

# 📌 Botão para atualizar ranking
if st.button("🔄 Atualizar Rankings"):
    atualizar_ranking()
    st.success("✅ Ranking atualizado!")

# 📌 Carregar dados do ranking
rankings = carregar_dados()

# 📌 Exibir Ranking de Artilheiros (Somente quem marcou gols)
st.subheader("🏆 Ranking de Artilheiros")
df_artilheiros = pd.DataFrame(rankings, columns=["Jogador", "Vitórias", "Empates", "Derrotas", "Pontos", "Gols"])
df_artilheiros = df_artilheiros[df_artilheiros["Gols"] > 0].sort_values(by="Gols", ascending=False)  # Apenas jogadores com gols
st.table(df_artilheiros[["Jogador", "Gols"]])

# 📌 Exibir Ranking de Pontos (Todos os jogadores, ordenado por pontos)
st.subheader("📊 Ranking de Pontos e V/E/D")
df_pontos = pd.DataFrame(rankings, columns=["Jogador", "Vitórias", "Empates", "Derrotas", "Pontos", "Gols"])
df_pontos = df_pontos.sort_values(by="Pontos", ascending=False)
df_pontos["V/E/D"] = df_pontos["Vitórias"].astype(str) + "/" + df_pontos["Empates"].astype(str) + "/" + df_pontos["Derrotas"].astype(str)
st.table(df_pontos[["Jogador", "Pontos", "V/E/D"]])
