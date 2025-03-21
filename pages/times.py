import sqlite3

import numpy as np
import pandas as pd
import streamlit as st

from modules.balance import balance_teams
from modules.combine_images import create_combined_image
from modules.process import normalize_name, parse_players, process_players_in_database
from modules.radar_chart import create_radar_chart
from modules.team_selection import calcular_diferenca_mg

# 📌 Configuração da Página
st.title("🏆 Seleção de Times")
st.write("Monte times equilibrados com base nas estatísticas dos jogadores.")

# 📌 Entrada da lista de jogadores via texto
st.subheader("📋 Lista de Jogadores")
player_input = st.text_area("Cole a lista de jogadores aqui", height=300)

# 📌 Seleção do número de times
num_teams = st.radio("⚽ Número de Times:", [2, 3])

# 📌 Número de combinações a avaliar
num_combinacoes = st.number_input(
    "🔄 Número de Times Avaliados (N)", min_value=1, max_value=3000, value=100, step=100
)

# 📌 Conectar ao banco de dados e carregar a base de jogadores
DB_PATH = "data/dados.db"


def carregar_base_jogadores():
    """Lê os jogadores do banco de dados e retorna um DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM jogadores"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


df_base = carregar_base_jogadores()
df_base["nome"] = df_base["nome"].apply(normalize_name)  # Padronizar nomes

# 📌 Botão para gerar os times
if st.button("FAZER TIMES"):
    if not player_input.strip():
        st.warning("⚠️ Insira a lista de jogadores antes de continuar.")
    else:
        # 🔹 Processa o texto para obter a lista única de jogadores
        jogadores = parse_players(player_input)

        # 🔹 Processa a busca na base de dados
        matched_players, unrecognized_players = process_players_in_database(
            jogadores, df_base
        )

        # 🔹 Criar DataFrame para armazenar os resultados das combinações
        resultados = []

        # 🔹 Criar barra de progresso
        progress_bar = st.progress(0)

        # 🔹 Gerar combinações e avaliar a melhor
        melhor_diff = float("inf")
        melhor_times = None
        melhor_medias = None

        for i in range(num_combinacoes):
            teams = balance_teams(pd.DataFrame(matched_players), num_teams=num_teams)
            medias, diff = calcular_diferenca_mg(teams, pd.DataFrame(matched_players))

            # Salvar os resultados
            resultados.append(
                {
                    "Iteração": i + 1,
                    "Times": teams,
                    "Médias": medias,
                    "Diferença MG": diff,
                }
            )

            # Atualizar se for a melhor combinação
            if diff < melhor_diff:
                melhor_diff = diff
                melhor_times = teams
                melhor_medias = medias

            # Atualizar barra de progresso
            progress_bar.progress((i + 1) / num_combinacoes)

        # 🔹 Exibir título final antes dos gráficos
        st.subheader("🏅 Melhor Configuração")

        # 🔹 Exibir as médias da melhor configuração
        cores_times = {1: "Vermelho", 2: "Azul", 3: "Preto"}
        for i, media in enumerate(melhor_medias):
            st.write(f"**Time {i+1} ({cores_times[i+1]}):** {media:.3f}")

        # 🔹 Exibir diferença de MG final
        st.write(f"**Diferença Total:** {melhor_diff:.3f}")

        # 🔹 Gerar gráficos radar para os melhores times
        # 🔹 Gerar gráficos radar para os melhores times
        colors = ["red", "blue", "black"]
        image_paths = []
        team_lists = []

        for i, team in melhor_times.items():
            team_number = i + 1

            # 🔹 Calcular média dos atributos para o time
            team_data = {
                attr: pd.DataFrame(matched_players)[
                    pd.DataFrame(matched_players)["nome"].isin(team)
                ][attr].mean()
                for attr in [
                    "fisico",
                    "defesa",
                    "tatica",
                    "tecnica",
                    "ataque",
                    "velocidade",
                ]
            }

            # 🔹 Gerar e salvar gráfico de radar do time
            image_path = f"generated/team_{team_number}.png"
            create_radar_chart(team_number, team_data, image_path, color=colors[i])

            image_paths.append(image_path)
            team_lists.append(team)

        # 🔹 Criar imagem combinada com listas + radares
        fig_size = 520
        combined_image_path = "generated/combined_teams.png"
        create_combined_image(image_paths, team_lists, combined_image_path, fig_size)

        # 🔹 Exibir a imagem combinada no Streamlit
        st.image(combined_image_path, caption="Melhor Configuração de Times", width=700)

        # 🔹 Botão para baixar a imagem final
        with open(combined_image_path, "rb") as file:
            st.download_button(
                label="Baixar Imagem dos Times",
                data=file,
                file_name="times_combinados.png",
                mime="image/png",
            )
