import os
import sqlite3

# 📌 Definir caminho do arquivo de jogos
jogos_path = "data/jogos.txt"
db_path = "data/dados.db"


def ler_arquivo(arquivo=jogos_path):
    """
    Lê o arquivo 'data/jogos.txt' e retorna uma lista de linhas normalizadas (sem espaços extras e em minúsculas).
    """
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo '{arquivo}' não encontrado.")
        return []

    with open(arquivo, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file]


def processar_dados(arquivo=jogos_path):
    """
    Lê e estrutura todas as informações do arquivo 'data/jogos.txt' em um único dicionário.
    Retorna um dicionário estruturado no formato:
    {
        data1: {
            "times": {time1: {"jogadores": [(nome, gols), ...]}, time2: {...}},
            "jogos": [(time1, gols1, time2, gols2), ...],
            "num_times": X
        },
        ...
    }
    """
    linhas = ler_arquivo(arquivo)
    if not linhas:
        return {}

    dados = {}
    data_atual = None
    time_atual = None
    lendo_jogadores = False
    lendo_jogos = False

    for line in linhas:
        # 📌 Identificar nova data
        if line.startswith("data:"):
            data_atual = line.replace("data:", "").strip()
            dados[data_atual] = {"times": {}, "jogos": [], "num_times": 0}

        # 📌 Identificar número de times
        elif line.startswith("times:") and data_atual:
            dados[data_atual]["num_times"] = int(line.replace("times:", "").strip())

        # 📌 Identificar início de um novo time
        elif line.startswith("# time"):
            partes = line.split("-")
            if len(partes) > 1:
                time_atual = partes[1].strip()
                dados[data_atual]["times"][time_atual] = {"jogadores": []}
                lendo_jogadores = True

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
            dados[data_atual]["times"][time_atual]["jogadores"].append((nome, gols))

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
            dados[data_atual]["jogos"].append((time1, gols1, time2, gols2))

    return dados


def exibir_dados(dados, resultados):
    """
    Exibe os dados processados, garantindo que:
    - A primeira vez mostra os times e gols apenas
    - Depois da exibição dos jogos, mostra as estatísticas de pontos (V/E/D).
    """
    for data in sorted(dados.keys()):
        print(f"\n📅 Data: {data}")
        print(f"📊 Número de times: {dados[data]['num_times']}")
        print("-------")

        # 📌 Primeira exibição dos times (apenas gols)
        for time, detalhes in dados[data]["times"].items():
            print(f"  🏆 Time: {time}")
            for jogador_info in detalhes["jogadores"]:
                nome = jogador_info[0]  # Sempre o nome está na primeira posição
                gols = jogador_info[1]  # Sempre os gols estão na segunda posição
                print(f"    - {nome}: {gols} gol(s)")

        print("-------\n🏆 Resultados das Partidas:")
        for time1, gols1, time2, gols2, resultado in resultados[data]:
            print(f"  ⚽ {time1:<10} {gols1} - {gols2} {time2:<10} {resultado}")

        print("-------")

        # 📌 Segunda exibição dos times (agora com estatísticas completas)
        print(f"\n📊 Estatísticas dos jogadores da data {data}")
        for time, detalhes in dados[data]["times"].items():
            print(f"  🏆 Time: {time}")
            for jogador_info in detalhes["jogadores"]:
                (
                    nome,
                    gols,
                    pontos,
                    v,
                    e,
                    d,
                ) = jogador_info  # Pegando todos os dados agora
                print(f"    - {nome}: {pontos} ponto(s), V/E/D: {v}/{e}/{d}")

        print("-------")


def calcular_pontuacao_e_resultado(dados):
    """
    Para cada jogo, calcula os pontos dos times e define o resultado (vitória ou empate).
    Atualiza diretamente a estrutura de dados e retorna os resultados formatados.
    """
    resultados_formatados = {}

    for data, info in dados.items():
        estatisticas = {
            time: {"P": 0, "V": 0, "E": 0, "D": 0} for time in info["times"]
        }
        num_times = info["num_times"]
        pontos_vitoria = 3 if num_times == 2 else 1
        pontos_empate = 1 if num_times == 2 else 0

        resultados_formatados[data] = []

        for time1, gols1, time2, gols2 in info["jogos"]:
            if gols1 > gols2:
                resultado = f"(🏆 vitória {time1})"
                estatisticas[time1]["P"] += pontos_vitoria
                estatisticas[time1]["V"] += 1
                estatisticas[time2]["D"] += 1
            elif gols2 > gols1:
                resultado = f"(🏆 vitória {time2})"
                estatisticas[time2]["P"] += pontos_vitoria
                estatisticas[time2]["V"] += 1
                estatisticas[time1]["D"] += 1
            else:
                resultado = "(🤝 empate)"
                estatisticas[time1]["P"] += pontos_empate
                estatisticas[time2]["P"] += pontos_empate
                estatisticas[time1]["E"] += 1
                estatisticas[time2]["E"] += 1

            resultados_formatados[data].append((time1, gols1, time2, gols2, resultado))

        # 📌 Atualizar a estrutura de jogadores corretamente
        for time, stats in estatisticas.items():
            jogadores_atualizados = []
            for jogador_info in info["times"][time]["jogadores"]:
                if len(jogador_info) == 2:  # Apenas nome e gols
                    nome, gols = jogador_info
                else:  # Já contém estatísticas, manter os valores anteriores
                    nome, gols, _, _, _, _ = jogador_info

                jogadores_atualizados.append(
                    (nome, gols, stats["P"], stats["V"], stats["E"], stats["D"])
                )

            dados[data]["times"][time]["jogadores"] = jogadores_atualizados

    return resultados_formatados


# ---------------------------------------------------------------------------- #


def adicionar_jogadores_novos(jogadores):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for jogador in jogadores:
        cursor.execute("SELECT jogador FROM rankings WHERE jogador = ?", (jogador,))
        if cursor.fetchone() is None:
            # Se o jogador não existe, adicionamos ele com 0 pontos, 0 gols e 0 V/E/D
            cursor.execute(
                """
                INSERT INTO rankings (jogador, vitorias, empates, derrotas, pontos, gols) 
                VALUES (?, 0, 0, 0, 0, 0)
            """,
                (jogador,),
            )

    conn.commit()
    conn.close()


def atualizar_gols_jogadores(dados):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for data, info in dados.items():
        for time, detalhes in info["times"].items():
            for jogador, gols in detalhes["jogadores"]:
                cursor.execute(
                    "UPDATE rankings SET gols = gols + ? WHERE jogador = ?",
                    (gols, jogador),
                )

    conn.commit()
    conn.close()


def atualizar_pontos_jogadores(dados):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for data, info in dados.items():
        estatisticas = {
            time: {"P": 0, "V": 0, "E": 0, "D": 0} for time in info["times"]
        }
        num_times = info["num_times"]
        pontos_vitoria = 3 if num_times == 2 else 1
        pontos_empate = 1 if num_times == 2 else 0

        for time1, gols1, time2, gols2 in info["jogos"]:
            if gols1 > gols2:
                estatisticas[time1]["P"] += pontos_vitoria
                estatisticas[time1]["V"] += 1
                estatisticas[time2]["D"] += 1
            elif gols2 > gols1:
                estatisticas[time2]["P"] += pontos_vitoria
                estatisticas[time2]["V"] += 1
                estatisticas[time1]["D"] += 1
            else:
                estatisticas[time1]["P"] += pontos_empate
                estatisticas[time2]["P"] += pontos_empate
                estatisticas[time1]["E"] += 1
                estatisticas[time2]["E"] += 1

        for time, stats in estatisticas.items():
            for jogador, _ in dados[data]["times"][time]["jogadores"]:
                cursor.execute(
                    """
                    UPDATE rankings 
                    SET pontos = pontos + ?, 
                        vitorias = vitorias + ?, 
                        empates = empates + ?, 
                        derrotas = derrotas + ? 
                    WHERE jogador = ?
                """,
                    (stats["P"], stats["V"], stats["E"], stats["D"], jogador),
                )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    dados_processados = processar_dados()  # 1. Ler os jogos do arquivo
    jogadores_unicos = set()

    # 2. Identificar todos os jogadores
    for data, info in dados_processados.items():
        for time, detalhes in info["times"].items():
            for jogador, _ in detalhes["jogadores"]:
                jogadores_unicos.add(jogador)

    adicionar_jogadores_novos(
        jogadores_unicos
    )  # 3. Adicionar jogadores novos à base de dados
    atualizar_gols_jogadores(dados_processados)  # 4. Atualizar os gols
    atualizar_pontos_jogadores(dados_processados)  # 5. Atualizar pontos e V/E/D

    print("✅ Processamento concluído!")


# ---------------------------------------------------------------------------- #
# 🔹 Executar extração e exibição dos dados de forma modular
if __name__ == "__main__":
    dados_processados = processar_dados()
    resultados_partidas = calcular_pontuacao_e_resultado(dados_processados)
    exibir_dados(dados_processados, resultados_partidas)
