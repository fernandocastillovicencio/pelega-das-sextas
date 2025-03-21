import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 📌 Configuração da Página
st.title("📊 Avaliação Individual dos Jogadores")

# 📌 Caminho do banco de dados
DB_PATH = "data/dados.db"


def carregar_jogadores():
    """Lê os jogadores do banco de dados e retorna um DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM jogadores"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# 📌 Carregar dados dos jogadores
df_jogadores = carregar_jogadores()

# 📌 Criar dropdown para seleção do jogador
jogador_selecionado = st.selectbox("Selecione um jogador:", df_jogadores["nome"])

# 📌 Filtrar os dados do jogador selecionado
dados_jogador = df_jogadores[df_jogadores["nome"] == jogador_selecionado].iloc[0]

# 📌 Ajustar os atributos e suas posições angulares
categorias = [
    "ataque",
    "tecnica",
    "tatica",
    "defesa",
    "tatica",
    "tecnica",
]  # Ajuste da ordem e repetição para fechamento do gráfico
angulos = [0, 60, 120, 180, 240, 300, 0]  # Ângulos personalizados para cada atributo

# 📌 Obter os valores do jogador
valores = [dados_jogador[cat] for cat in categorias]
valores.append(valores[0])  # Fechar o gráfico

# 📌 Criar o gráfico Radar com cores ajustadas
fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=valores,
        theta=angulos,
        fill="toself",
        name=jogador_selecionado,
        marker=dict(color="red"),  # Define a cor do traçado
        fillcolor="rgba(255, 0, 0, 0.3)",  # Define a cor de preenchimento transparente
    )
)

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5],
            showticklabels=True,
            tickmode="linear",
            tick0=0,
            dtick=1,
        ),
        angularaxis=dict(
            tickmode="array",
            tickvals=angulos[:-1],  # Sem repetir o último valor
            ticktext=categorias[:-1],  # Ajuste para exibir os textos corretos
        ),
    ),
    showlegend=False,
)

# 📌 Exibir o gráfico no Streamlit
st.plotly_chart(fig)
