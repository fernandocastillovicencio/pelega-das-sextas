import os
import sqlite3

import pandas as pd
import streamlit as st

# ----------------------------------------------------
# 📌 Caminhos dos arquivos (ajuste se necessário)
DB_PATH = "data/dados.db"
CSS_PATH = "styles.css"
JOGOS_PATH = "data/jogos.txt"

# ----------------------------------------------------
# 📌 1. Carrega o estilo CSS
def carregar_estilo():
    """
    Carrega o arquivo CSS para estilizar as tabelas no Streamlit.
    """
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH, "r") as f:
            css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Arquivo de estilo '{CSS_PATH}' não encontrado.")


# ----------------------------------------------------
# 📌 2. Carrega o ranking do banco de dados
def carregar_ranking():
    """
    Lê o ranking (estatísticas dos jogadores) do banco de dados.
    Retorna um DataFrame com colunas renomeadas para exibição.
    """
    if not os.path.exists(DB_PATH):
        st.warning("⚠️ Banco de dados não encontrado.")
        return None

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM rankings", conn)
    conn.close()

    if df.empty:
        return None

    # Renomear colunas para exibição
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


# ----------------------------------------------------
# 📌 3. Exibe o ranking (artilharia e pontos)


def exibir_tabela_estilizada(df, colunas, titulo):
    """
    📌 Converte DataFrame para HTML estilizado e exibe no Streamlit.
    """
    df_html = df[colunas].to_html(index=False, escape=False)

    # 📌 Ajuste para responsividade
    st.subheader(titulo)
    st.markdown(
        f"""
        <div style="overflow-x: auto; width: 100%;">
            {df_html}
        </div>
    """,
        unsafe_allow_html=True,
    )


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

    exibir_tabela_estilizada(df_pontos, ["Jogador", "Pontos", "V/E/D"], "📊 Pontos")

    # nota:
    st.markdown(
        """
    <div style="font-size: 14px;">
        <b>NOTA - pontos para V/E/D:</b><br>
        <div style="margin-left: 20px;">
            Jogos com 2 times: <b>3/1/0</b> pontos.<br>
            Jogos com 3 times: <b>1/0/0</b> pontos.
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------
# 📌 4. Lê o conteúdo do arquivo 'jogos.txt'
def carregar_historico_arquivo():
    """
    Lê o arquivo 'data/jogos.txt' e retorna o texto inteiro.
    """
    if not os.path.exists(JOGOS_PATH):
        return "⚠️ O arquivo de jogos não foi encontrado."

    with open(JOGOS_PATH, "r", encoding="utf-8") as file:
        return file.read()


# ----------------------------------------------------
# 📌 Início da aplicação Streamlit
def main():
    # Criar abas
    aba_ranking, aba_historico = st.tabs(["📊 Ranking", "📜 Histórico de Jogos"])

    with aba_ranking:
        st.title("🏆 Estatísticas da Pelega de Sextas")
        carregar_estilo()  # Aplica CSS, se existir

        df = carregar_ranking()
        exibir_ranking(df)

    with aba_historico:
        st.title("📜 Histórico de Jogos")

        # Ler o conteúdo do arquivo
        historico_texto = carregar_historico_arquivo()

        # Exibir o conteúdo do arquivo como texto puro
        # Usando Markdown com ``` para exibir como bloco de código
        st.markdown(f"```\n{historico_texto}\n```")


# ----------------------------------------------------
# Executar a função principal no Streamlit
if __name__ == "__main__":
    main()
