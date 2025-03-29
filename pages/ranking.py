import os
import sqlite3

import pandas as pd
import streamlit as st

# 📌 Caminhos dos arquivos
DB_PATH = "data/dados.db"
CSS_PATH = "styles.css"


def carregar_estilo():
    """
    📌 Carrega o arquivo CSS para estilizar a página no Streamlit.
    """
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r") as f:
            css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Arquivo de estilo '{CSS_PATH}' não encontrado.")


def carregar_ranking():
    """
    📌 Lê o ranking dos jogadores do banco de dados e retorna um DataFrame.
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM rankings", conn)
    conn.close()

    if df.empty:
        return None

    # 📌 Renomear colunas para exibição
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
    return df


def exibir_tabela_estilizada(df, colunas, titulo):
    """
    📌 Exibe um DataFrame como tabela estilizada no Streamlit.
    """
    df_html = df[colunas].to_html(index=False, escape=False)

    st.subheader(titulo)
    st.markdown(
        f"""
        <div style="overflow-x: auto; width: 100%;">
            {df_html}
        </div>
    """,
        unsafe_allow_html=True,
    )


def exibir_ranking():
    """
    📌 Exibe o ranking de artilheiros e pontos.
    """
    df = carregar_ranking()

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
        exibir_tabela_estilizada(df_artilheiros, ["Jogador", "Gols"], "⚽ Artilharia")

    # 📌 Ranking de Pontos
    df_pontos = df.sort_values(by=["Pontos", "Vitórias", "Gols"], ascending=False)
    df_pontos["V/E/D"] = (
        df_pontos["Vitórias"].astype(str)
        + "/"
        + df_pontos["Empates"].astype(str)
        + "/"
        + df_pontos["Derrotas"].astype(str)
    )
    exibir_tabela_estilizada(df_pontos, ["Jogador", "Pontos", "V/E/D"], "📊 Pontuação")

    # 📌 Nota sobre a pontuação
    st.markdown(
        """
    <div style="font-size: 14px;">
        <b>NOTA - Pontuação de V/E/D:</b><br>
        <div style="margin-left: 20px;">
            Jogos com 2 times: <b>3/1/0</b> pontos.<br>
            Jogos com 3 times: <b>1/0/0</b> pontos.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# 📌 Interface Streamlit
st.title("🏆 Ranking da Pelega das Sextas")

# 📌 Carregar CSS para estilização
carregar_estilo()

# 📌 Exibir rankings
exibir_ranking()
