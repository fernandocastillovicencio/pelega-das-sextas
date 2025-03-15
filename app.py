import sqlite3

import pandas as pd
import streamlit as st

from processar_jogos import (
    atualizar_gols_jogadores,
    atualizar_pontos_jogadores,
    processar_dados,
)

# 📌 Definir caminho do banco de dados na pasta 'data'
db_path = "data/dados.db"

# 📌 Função para carregar dados do ranking
def carregar_dados():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 📌 Verifica se a tabela rankings existe
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='rankings'"
    )
    if not cursor.fetchone():
        st.warning(
            "⚠️ A tabela de rankings ainda não foi criada. Execute o processamento de jogos primeiro."
        )
        return None

    # 📌 Carregar ranking completo
    cursor.execute("SELECT * FROM rankings")
    rankings = cursor.fetchall()

    conn.close()

    # Retorna DataFrame ou None se não houver dados
    if rankings:
        return pd.DataFrame(
            rankings,
            columns=["Jogador", "Vitórias", "Empates", "Derrotas", "Pontos", "Gols"],
        )
    return None


# 📌 Atualizar Ranking Automaticamente
def atualizar_ranking():
    dados_processados = processar_dados()
    atualizar_gols_jogadores(dados_processados)
    atualizar_pontos_jogadores(dados_processados)


# 📌 Interface do Streamlit
st.title("⚽ Estatísticas da Pelada")

# 📌 Botão para atualizar ranking
if st.button("🔄 Atualizar Rankings"):
    atualizar_ranking()
    st.success("✅ Ranking atualizado!")

# 📌 Carregar dados do ranking
df = carregar_dados()

if df is not None:
    # 📌 Exibir Ranking de Artilheiros (Apenas jogadores com gols > 0)
    st.subheader("🏆 Ranking de Artilheiros")
    df_artilheiros = df[df["Gols"] > 0].sort_values(by="Gols", ascending=False)

    if df_artilheiros.empty:
        st.info("Nenhum jogador marcou gols ainda.")
    else:
        st.table(df_artilheiros[["Jogador", "Gols"]])

    # 📌 Exibir Ranking de Pontos (Ordenado por pontos, vitórias e depois gols)
    st.subheader("📊 Ranking de Pontos e V/E/D")
    df_pontos = df.sort_values(by=["Pontos", "Vitórias", "Gols"], ascending=False)
    df_pontos["V/E/D"] = (
        df_pontos["Vitórias"].astype(str)
        + "/"
        + df_pontos["Empates"].astype(str)
        + "/"
        + df_pontos["Derrotas"].astype(str)
    )

    st.table(df_pontos[["Jogador", "Pontos", "V/E/D"]])
