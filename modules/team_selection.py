import itertools
import random

import numpy as np
import pandas as pd


# Função para calcular a MG (média geral ponderada) de um jogador
def calcular_mg_jogador(row):
    return (
        row["fisico"] * 0.4
        + row["velocidade"] * 0.2
        + row["defesa"] * 0.1
        + row["tatica"] * 0.05
        + row["tecnica"] * 0.05
        + row["ataque"] * 0.1
    )


# Função para calcular a MG média de um time
def calcular_media_mg_time(df_players, team):
    """Calcula a média MG do time com base nos jogadores atribuídos."""
    df_team = df_players[
        df_players["nome"].isin(team)
    ]  # Corrigido de "Nome" para "nome"
    return df_team.apply(calcular_mg_jogador, axis=1).mean()


# Função para calcular a diferença entre as médias dos times
def calcular_diferenca_mg(teams, df_players):
    """Calcula a diferença entre os times baseada na média MG."""
    medias = [calcular_media_mg_time(df_players, team) for team in teams.values()]

    if len(medias) == 2:
        diff = abs(medias[0] - medias[1])
    elif len(medias) == 3:
        diff = np.sqrt(
            (abs(medias[0] - medias[1]) ** 2)
            + (abs(medias[0] - medias[2]) ** 2)
            + (abs(medias[1] - medias[2]) ** 2)
        )
    else:
        raise ValueError("Apenas suportado para 2 ou 3 times.")

    return medias, diff
