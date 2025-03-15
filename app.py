import sqlite3

import pandas as pd
import streamlit as st

# 📌 Definir caminho do banco de dados e CSS
db_path = "data/dados.db"
css_path = "styles.css"


def carregar_estilo():
    """
    📌 Carrega o arquivo CSS para estilizar as tabelas no Streamlit.
    """
    with open(css_path, "r") as f:
        css = f"<style>{f.read()}</style>"
    st.markdown(css, unsafe_allow_html=True)


def carregar_ranking():
    """
    📌 Carrega os rankings dos jogadores do banco de dados.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM rankings", conn)
    conn.close()

    # 📌 Renomear colunas para exibição correta
    df.rename(
        columns={
            "jogador": "Jogador",
            "gols": "Gols",
            "pontos": "Pontos",
            "vitorias": "Vitórias",
            "empates": "Empates",
            "derrotas": "Derrotas",
        },
        inplace=True,
    )

    return df if not df.empty else None


def exibir_tabela_estilizada(df, colunas, titulo):
    """
    📌 Converte DataFrame para HTML estilizado e exibe no Streamlit.
    """
    df_html = df[colunas].to_html(index=False, escape=False)
    st.subheader(titulo)
    st.markdown(df_html, unsafe_allow_html=True)


def exibir_ranking(df):
    """
    📌 Exibe os rankings de artilheiros e pontos de forma estilizada.
    """
    if df is None:
        st.warning(
            "⚠️ Nenhuma estatística disponível. Execute o processamento de jogos primeiro."
        )
        return

    # 📌 Ranking de Artilheiros
    df_artilheiros = df[df["Gols"] > 0].sort_values(by="Gols", ascending=False)
    if df_artilheiros.empty:
        st.info("Nenhum jogador marcou gols ainda.")
    else:
        exibir_tabela_estilizada(
            df_artilheiros, ["Jogador", "Gols"], "🏆 Ranking de Artilheiros"
        )

    # 📌 Ranking de Pontos
    df_pontos = df.sort_values(by=["Pontos", "Vitórias", "Gols"], ascending=False)
    df_pontos["V/E/D"] = (
        df_pontos["Vitórias"].astype(str)
        + "/"
        + df_pontos["Empates"].astype(str)
        + "/"
        + df_pontos["Derrotas"].astype(str)
    )

    exibir_tabela_estilizada(
        df_pontos, ["Jogador", "Pontos", "V/E/D"], "📊 Ranking de Pontos e V/E/D"
    )


# 📌 Interface do Streamlit
st.title("⚽ Estatísticas da Pelada")

# 📌 Carregar estilo CSS
carregar_estilo()

# 📌 Carregar ranking do banco de dados
df = carregar_ranking()

# 📌 Exibir os rankings apenas se houver dados
exibir_ranking(df)
