import os
import re

# 📌 Definir caminho do arquivo de jogos
jogos_path = "data/jogos.txt"


def contar_datas(arquivo=jogos_path):
    """
    Lê o arquivo 'data/jogos.txt' e retorna o número de datas distintas encontradas.
    """
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo '{arquivo}' não encontrado.")
        return 0, []

    datas_unicas = set()

    # 📌 Ler o arquivo e buscar datas
    with open(arquivo, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().lower()
            if line.startswith("data:"):  # Identifica linha de data
                data = line.replace("data:", "").strip()
                datas_unicas.add(data)

    print(f"📅 Total de datas encontradas: {len(datas_unicas)}")
    print("📆 Datas:", sorted(datas_unicas))

    # 📌 Retornar total de datas e lista ordenada
    return len(datas_unicas), sorted(datas_unicas)


def contar_times_por_data(arquivo=jogos_path):
    """
    Para cada data no arquivo 'data/jogos.txt', determina a quantidade de times no jogo.
    Retorna um dicionário no formato {data: num_times}.
    """
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo '{arquivo}' não encontrado.")
        return {}

    times_por_data = {}
    data_atual = None  # Para armazenar a data do bloco atual

    with open(arquivo, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().lower()

            # 📌 Identificar nova data
            if line.startswith("data:"):
                data_atual = line.replace("data:", "").strip()

            # 📌 Identificar número de times
            elif line.startswith("times:") and data_atual:
                num_times = int(line.replace("times:", "").strip())
                times_por_data[data_atual] = num_times

    # 📌 Exibir os resultados encontrados
    print(f"📊 Quantidade de times por data: {times_por_data}")


def extrair_times_por_data(arquivo=jogos_path):
    """
    Para cada data no arquivo 'data/jogos.txt', extrai os times e seus jogadores.
    Retorna um dicionário no formato:
    {data: {time: {"jogadores": [("nome", gols), ...]}}}
    """
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo '{arquivo}' não encontrado.")
        return {}

    times_por_data = {}
    data_atual = None
    time_atual = None
    lendo_jogadores = False  # Flag para saber se estamos lendo jogadores

    with open(arquivo, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().lower()

            # 📌 Identificar nova data
            if line.startswith("data:"):
                data_atual = line.replace("data:", "").strip()
                times_por_data[data_atual] = {}

            # 📌 Identificar início de um novo time
            elif line.startswith("# time"):
                partes = line.split("-")
                if len(partes) > 1:
                    time_atual = partes[1].strip()
                    times_por_data[data_atual][time_atual] = {"jogadores": []}
                    lendo_jogadores = True  # A partir daqui, leremos os jogadores

            # 📌 Linha separadora "---" indica que terminamos de ler um time
            elif line == "---":
                lendo_jogadores = False

            # 📌 Capturar jogadores dentro do time
            elif lendo_jogadores and time_atual:
                jogador_info = line.split("(")
                nome = jogador_info[0].strip()
                gols = (
                    int(jogador_info[1].replace(")", "").strip())
                    if len(jogador_info) > 1
                    else 0
                )
                times_por_data[data_atual][time_atual]["jogadores"].append((nome, gols))

    # 📌 Exibir os resultados encontrados
    for data, times in times_por_data.items():
        print(f"📅 Data: {data}")
        for time, info in times.items():
            print(f"  🏆 Time: {time}")
            for jogador, gols in info["jogadores"]:
                print(f"    - {jogador}: {gols} gol(s)")

    return times_por_data


def extrair_jogos_por_data(arquivo=jogos_path):
    """
    Para cada data no arquivo 'data/jogos.txt', extrai os jogos e os placares.
    Retorna um dicionário no formato:
    {data: [(time1, gols1, time2, gols2), ...]}
    """
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo '{arquivo}' não encontrado.")
        return {}

    jogos_por_data = {}
    data_atual = None
    lendo_jogos = False  # Flag para saber se estamos lendo a seção de jogos

    with open(arquivo, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().lower()

            # 📌 Identificar nova data
            if line.startswith("data:"):
                data_atual = line.replace("data:", "").strip()
                jogos_por_data[data_atual] = []

            # 📌 Identificar início do bloco de jogos
            elif line.startswith("jogos:") and data_atual:
                lendo_jogos = True

            # 📌 Capturar os jogos dentro do bloco
            elif lendo_jogos and " - " in line and not line.startswith("#"):
                partes = line.split(" - ")
                time1_gols = partes[0].rsplit(" ", 1)
                time2_gols = partes[1].split(" ", 1)

                if len(time1_gols) < 2 or len(time2_gols) < 2:
                    print(f"⚠️ Erro ao processar linha: {line}")
                    continue

                time1, gols1 = time1_gols
                time2, gols2 = time2_gols

                gols1, gols2 = int(gols1), int(gols2)
                jogos_por_data[data_atual].append((time1, gols1, time2, gols2))

    # 📌 Exibir os jogos extraídos
    for data, jogos in jogos_por_data.items():
        print(f"📅 Data: {data}")
        for time1, gols1, time2, gols2 in jogos:
            print(f"  ⚽ {time1} {gols1} - {gols2} {time2}")

    return jogos_por_data


# 🔹 Executar contagem de datas, extração de times e jogos
if __name__ == "__main__":
    contar_datas()
    contar_times_por_data()
    extrair_times_por_data()
    extrair_jogos_por_data()
