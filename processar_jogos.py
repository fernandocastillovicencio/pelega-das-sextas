import os
import sqlite3

# 📌 Definir caminho do arquivo de jogos
data_path = "data"
jogos_path = os.path.join(data_path, "jogos.txt")
db_path = os.path.join(data_path, "dados.db")


def ler_arquivo(arquivo=jogos_path):
    """
    📌 Leitura do arquivo de jogos.
    """
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo '{arquivo}' não encontrado.")
        return []

    with open(arquivo, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file]


def processar_dados(arquivo=jogos_path):
    """
    📌 Processamento dos dados dos jogos.
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
        if line.startswith("data:"):
            data_atual = line.replace("data:", "").strip()
            dados[data_atual] = {"times": {}, "jogos": [], "num_times": 0}
            print(f"\n📅 Data: {data_atual}")

        elif line.startswith("times:") and data_atual:
            dados[data_atual]["num_times"] = int(line.replace("times:", "").strip())
            print(f"📊 Número de times: {dados[data_atual]['num_times']}")

        elif line.startswith("# time"):
            partes = line.split("-")
            if len(partes) > 1:
                time_atual = partes[1].strip()
                dados[data_atual]["times"][time_atual] = {"jogadores": []}
                lendo_jogadores = True
                print(f"  🏆 Time: {time_atual}")

        elif line == "---":
            lendo_jogadores = False

        elif lendo_jogadores and time_atual:
            jogador_info = line.split("(")
            nome = jogador_info[0].strip()
            gols = (
                int(jogador_info[1].replace(")", "").strip())
                if len(jogador_info) > 1
                else 0
            )
            dados[data_atual]["times"][time_atual]["jogadores"].append((nome, gols))
            print(f"    - {nome}: {gols} gol(s)")

        elif line.startswith("jogos:") and data_atual:
            lendo_jogos = True
            print("🏆 Resultados das Partidas:")

        elif lendo_jogos and " - " in line:
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
            print(f"  ⚽ {time1} {gols1} - {gols2} {time2}")

    return dados


def calcular_pontuacao_e_resultado(data, info):
    """
    📌 Etapa 2: Calcula os pontos e estatísticas individuais da data.
    """
    estatisticas = {time: {"P": 0, "V": 0, "E": 0, "D": 0} for time in info["times"]}
    num_times = info["num_times"]
    pontos_vitoria = 3 if num_times == 2 else 1
    pontos_empate = 1 if num_times == 2 else 0

    print(f"\n📌 Etapa 2: Calculando pontuação e resultados da data {data}...")

    for time1, gols1, time2, gols2 in info["jogos"]:
        if gols1 > gols2:
            estatisticas[time1]["P"] += pontos_vitoria
            estatisticas[time1]["V"] += 1
            estatisticas[time2]["D"] += 1
            resultado = f"(🏆 vitória {time1})"
        elif gols2 > gols1:
            estatisticas[time2]["P"] += pontos_vitoria
            estatisticas[time2]["V"] += 1
            estatisticas[time1]["D"] += 1
            resultado = f"(🏆 vitória {time2})"
        else:
            estatisticas[time1]["P"] += pontos_empate
            estatisticas[time2]["P"] += pontos_empate
            estatisticas[time1]["E"] += 1
            estatisticas[time2]["E"] += 1
            resultado = "(🤝 empate)"

        print(f"    {time1} {gols1} - {gols2} {time2} {resultado}")

    return estatisticas


def exibir_estatisticas(data, info, estatisticas):
    """
    📌 Etapa 3: Exibe as estatísticas dos jogadores da data.
    """
    print(f"\n📌 Etapa 3: Exibindo estatísticas da data {data}...")

    for time, stats in estatisticas.items():
        print(f"  🏆 Time: {time}")
        for jogador, gols in info["times"][time]["jogadores"]:
            print(
                f"    - {jogador}: {stats['P']} ponto(s), V/E/D: {stats['V']}/{stats['E']}/{stats['D']}"
            )


def exibir_resumo(resumo_jogadores):
    """
    📌 Etapa 4: Exibição do resumo final consolidado.
    """
    print("\n📌 Etapa 4: Exibindo resumo final consolidado...")
    print("\n📊 **Resumo Final**")
    print("Lista de todos os jogadores que participaram:")

    for jogador, stats in resumo_jogadores.items():
        print(
            f"  - {jogador}: {stats['gols']} gol(s), {stats['pontos']} ponto(s), V/E/D: {stats['V']}/{stats['E']}/{stats['D']}"
        )


def salvar_estatisticas_no_banco(resumo_jogadores):
    """
    📌 Salva as estatísticas finais dos jogadores no banco de dados.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 📌 Criar a tabela rankings caso não exista
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS rankings (
            jogador TEXT PRIMARY KEY,
            gols INTEGER DEFAULT 0,
            pontos INTEGER DEFAULT 0,
            vitorias INTEGER DEFAULT 0,
            empates INTEGER DEFAULT 0,
            derrotas INTEGER DEFAULT 0
        )
    """
    )

    # 📌 Inserir ou atualizar os dados de cada jogador
    for jogador, stats in resumo_jogadores.items():
        cursor.execute(
            """
            INSERT INTO rankings (jogador, gols, pontos, vitorias, empates, derrotas)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(jogador) DO UPDATE
            SET gols = excluded.gols,
                pontos = excluded.pontos,
                vitorias = excluded.vitorias,
                empates = excluded.empates,
                derrotas = excluded.derrotas
        """,
            (
                jogador,
                stats["gols"],
                stats["pontos"],
                stats["V"],
                stats["E"],
                stats["D"],
            ),
        )

    conn.commit()
    conn.close()
    print("📌 Estatísticas salvas no banco de dados!")


if __name__ == "__main__":
    dados_processados = processar_dados()
    resumo_jogadores = {}

    for data, info in dados_processados.items():
        print(f"\n📌 Etapa 1: Processando dados da data {data}...")

        estatisticas = calcular_pontuacao_e_resultado(data, info)
        exibir_estatisticas(data, info, estatisticas)

        # Atualiza o resumo dos jogadores
        for time, stats in estatisticas.items():
            for jogador, gols in info["times"][time]["jogadores"]:
                if jogador not in resumo_jogadores:
                    resumo_jogadores[jogador] = {
                        "gols": 0,
                        "pontos": 0,
                        "V": 0,
                        "E": 0,
                        "D": 0,
                    }

                resumo_jogadores[jogador]["gols"] += gols
                resumo_jogadores[jogador]["pontos"] += stats["P"]
                resumo_jogadores[jogador]["V"] += stats["V"]
                resumo_jogadores[jogador]["E"] += stats["E"]
                resumo_jogadores[jogador]["D"] += stats["D"]

    exibir_resumo(resumo_jogadores)
    salvar_estatisticas_no_banco(resumo_jogadores)
    print("✅ Processamento concluído!")
