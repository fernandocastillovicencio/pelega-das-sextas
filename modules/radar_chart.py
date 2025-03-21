import os

import matplotlib.pyplot as plt
import numpy as np


def create_radar_chart(team_number, team_data, save_path, color):
    """
    Gera um gráfico radar para o time fornecido.

    Parâmetros:
    - team_number: Número do time (1, 2 ou 3)
    - team_data: Dicionário com os valores médios dos atributos do time
    - save_path: Caminho para salvar a imagem gerada
    - color: Cor principal do gráfico (ex: "red", "blue", "black")
    """

    categories = [
        "fisico",
        "defesa",
        "tatica",
        "tecnica",
        "ataque",
        "velocidade",
    ]  # Corrigido para minúsculas
    sum = np.pi / 6
    angles = np.linspace(
        0 + sum, 2 * np.pi + sum, len(categories), endpoint=False
    ).tolist()

    # Adiciona o primeiro valor ao final para fechar o gráfico
    values = [team_data[attr] for attr in categories]
    values += values[:1]  # Fechando o ciclo do gráfico
    angles += angles[:1]  # Fechando o ciclo dos ângulos

    size = 2
    fig, ax = plt.subplots(figsize=(1, 1.8), subplot_kw=dict(polar=True))
    ax.set_position([0, 0, 0, -1])

    ax.fill(angles, values, color=color, alpha=0.3)
    ax.plot(angles, values, color=color, linewidth=0.1)

    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])  # ✅ Define os níveis da grade circular

    fontsize = 6
    # plt.rcParams.update({"ytick.labelsize": fontsize})
    ax.set_yticklabels(
        ["1", "2", "3", "4", "5"], fontsize=fontsize, alpha=1
    )  # Ajusta o tamanho da fonte

    ax.set_xticks(angles[:-1])  # Definir as posições das categorias no eixo circular
    ax.set_xticklabels(categories, fontsize=fontsize, fontweight="bold")

    team_name = f"Time {team_number}"
    # ax.set_title(team_name, color=color, fontsize=14, fontweight="bold", pad=20)

    # 🔹 Criar o diretório "generated" se não existir
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.savefig(save_path, bbox_inches="tight", dpi=250)
