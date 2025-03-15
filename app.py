import sqlite3

import pandas as pd
import streamlit as st

# 📌 Definir caminho do banco de dados
db_path = "data/dados.db"


def carregar_ranking():
    """
    📌 Carrega os rankings dos jogadores do banco de dados e corrige os nomes das colunas, se necessário.
    """
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

    # 📌 Carregar dados dos rankings
    df = pd.read_sql_query("SELECT * FROM rankings", conn)
    conn.close()

    # 📌 Exibir os nomes reais das colunas para depuração
    st.write("Colunas do DataFrame:", df.columns.tolist())

    # 📌 Ajuste de nomes de colunas caso necessário
    colunas_esperadas = ["Jogador", "Gols", "Pontos", "Vitórias", "Empates", "Derrotas"]
    mapeamento = {
        "jogador": "Jogador",
        "gols": "Gols",
        "pontos": "Pontos",
        "vitorias": "Vitórias",
        "empates": "Empates",
        "derrotas": "Derrotas",
    }

    # 📌 Renomear colunas se forem diferentes
    df.rename(columns=mapeamento, inplace=True)

    # 📌 Verificar novamente se as colunas esperadas estão presentes
    for col in colunas_esperadas:
        if col not in df.columns:
            st.error(f"🚨 Erro: Coluna '{col}' não encontrada no banco de dados.")
            return None

    return df if not df.empty else None


def exibir_ranking(df):
    """
    📌 Exibe o ranking de artilheiros e o ranking de pontos no Streamlit.
    """
    if "Gols" in df.columns and "Pontos" in df.columns:
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
    else:
        st.error("🚨 Erro: Colunas esperadas não encontradas no DataFrame.")


# 📌 Interface do Streamlit
st.title("⚽ Estatísticas da Pelada")

# 📌 Carregar ranking do banco de dados
df = carregar_ranking()

# 📌 Exibir os rankings apenas se houver dados
if df is not None:
    exibir_ranking(df)
else:
    st.warning(
        "📌 Nenhuma estatística disponível. Execute o processamento de jogos primeiro."
    )
