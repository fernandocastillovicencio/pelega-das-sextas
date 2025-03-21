import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def create_text_image(players, team_number, fig_size, color):
    """
    Cria uma imagem separada com a lista de jogadores do time.

    Parâmetros:
    - players: Lista de jogadores.
    - team_number: Número do time.
    - fig_size: Tamanho da figura.
    - color: Cor do time.

    Retorna:
    - Caminho da imagem gerada.
    """
    width = fig_size
    height = fig_size
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(
            "arial.ttf", int(fig_size * 0.07)
        )  # Fonte proporcional
    except:
        font = ImageFont.load_default()

    title_y = int(fig_size * 0.06)
    draw.text((width // 4, title_y), f"Time {team_number}", fill=color, font=font)

    text_y = title_y + int(fig_size * 0.1)
    line_spacing = int(fig_size * 0.08)

    for player in players:
        draw.text((width // 6, text_y), f"- {player}", fill=color, font=font)
        text_y += line_spacing

    os.makedirs("generated", exist_ok=True)
    img_path = f"generated/team_{team_number}_list.png"
    img.save(img_path)
    return img_path


def create_combined_image(team_images, team_players, save_path, fig_size):
    """
    Cria uma imagem combinada organizando os radares e listas em um layout 2xN.

    Parâmetros:
    - team_images: Lista de caminhos dos gráficos de radar.
    - team_players: Lista com listas de jogadores de cada time.
    - save_path: Caminho para salvar a imagem final.
    - fig_size: Tamanho das imagens.

    Retorna:
    - Caminho da imagem final combinada.
    """
    num_teams = len(team_images)
    list_images = []

    colors = ["red", "blue", "black"]
    for i, (players, color) in enumerate(zip(team_players, colors[:num_teams])):
        list_img = create_text_image(players, i + 1, fig_size, color)
        list_images.append(list_img)

    combined_width = 2 * fig_size
    combined_height = num_teams * fig_size
    combined_img = Image.new("RGB", (combined_width, combined_height), "white")

    for i in range(num_teams):
        list_img = Image.open(list_images[i])
        radar_img = Image.open(team_images[i])

        list_img = list_img.resize((fig_size, fig_size))
        radar_img = radar_img.resize((fig_size, fig_size))

        combined_img.paste(list_img, (0, i * fig_size))
        combined_img.paste(radar_img, (fig_size, i * fig_size))

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    combined_img.save(save_path)

    return save_path
