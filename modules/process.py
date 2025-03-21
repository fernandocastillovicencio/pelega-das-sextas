import random
import re
import unicodedata

import pandas as pd  # 🔹 Correção: importação do pandas


def normalize_name(name):
    """Remove acentos, caracteres especiais e espaços extras, além de padronizar o nome para comparação."""
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    name = re.sub(r"[^a-zA-Z0-9]", "", name)  # Remove caracteres especiais e espaços
    name = name.lower().strip()  # Converte para minúsculas
    return name


def parse_players(text):
    """
    Processa o texto de entrada para separar os jogadores mensalistas e avulsos.

    Retorna:
    - Lista única de jogadores normalizados (mensalistas + avulsos)
    """
    lines = text.split("\n")
    mensalistas = []
    avulsos = []
    section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if "MENSALISTA" in line.upper():
            section = "mensalistas"
            continue
        elif "AVULSO" in line.upper():
            section = "avulsos"
            continue

        if section in ["mensalistas", "avulsos"]:
            match = re.match(r"\d+\-\s*(.+)", line)
            if match:
                name = match.group(1)
                normalized_name = normalize_name(name)

                if section == "mensalistas":
                    mensalistas.append(normalized_name)
                elif section == "avulsos":
                    avulsos.append(normalized_name)

    # 🔹 Criar a lista única de jogadores
    jogadores = mensalistas + avulsos

    # 🔹 Printar a lista completa de jogadores antes da busca
    print("Lista completa de jogadores:", jogadores)

    return jogadores


def process_players_in_database(jogadores, df_base):
    """
    Processa os jogadores identificando se estão ou não na base de dados.

    Retorna:
    - Lista de jogadores reconhecidos na base de dados
    - Lista de jogadores não reconhecidos
    """
    matched_players = []
    unrecognized_players = []

    # 🔹 Certificar-se de que os nomes das colunas estão em minúsculas
    df_base.columns = df_base.columns.str.lower()

    for player in jogadores:
        normalized_player = normalize_name(player)

        # 🔹 Buscar jogador pelo nome correto no banco (garantindo que estamos acessando a coluna certa)
        found = df_base[df_base["nome"] == normalized_player]

        # 🔹 Printar a busca de cada jogador
        print(f"Buscando jogador: {player}... ", end="")

        if not found.empty:
            print("ENCONTRADO na base de dados.")
            matched_players.append(found.iloc[0].to_dict())
        else:
            print("NAO ENCONTRADO. Adicionando com valores padrão.")
            unrecognized_players.append(player)
            matched_players.append(
                {
                    "nome": player,
                    "fisico": 3,
                    "defesa": 3,
                    "tatica": 3,
                    "tecnica": 3,
                    "ataque": 3,
                    "velocidade": 3,
                    "posicao_primaria": "CM",
                    "posicao_secundaria": "CM",
                }
            )

    return matched_players, unrecognized_players
