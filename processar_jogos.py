import sqlite3
import re
import os

# 📌 Definir caminho do banco de dados na pasta 'data'
db_path = "data/dados.db"
jogos_path = "data/jogos.txt"

def processar_jogos(arquivo=jogos_path):
    """
    Lê o arquivo 'data/jogos.txt', detecta automaticamente se o jogo foi de 2 ou 3 times,
    e sobrescreve jogos já existentes caso tenham sido modificados no arquivo.
    """
    # Verificar se o arquivo de jogos existe
    if not os.path.exists(arquivo):
        print(f"⚠️ Arquivo '{arquivo}' não encontrado.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 📌 Ler conteúdo do arquivo
    with open(arquivo, "r", encoding="utf-8") as file:
        conteudo = file.read().lower()  # Converter tudo para minúsculas

    # 📌 Separar blocos de jogos corretamente usando `# ---------------------------------------------------------------------------- #`
    blocos = re.split(r"# ---------------------------------------------------------------------------- #", conteudo)

    for bloco in blocos:
        if not bloco.strip():  # Ignorar blocos vazios
            continue

        # 📌 Encontrar a data do jogo
        data_match = re.search(r"# 📅 data do jogo\n([\d/]+)", bloco)
        if not data_match:
            print("⚠️ Data não encontrada em um dos blocos, ignorando...")
            continue
        data = data_match.group(1).strip()

        # 📌 Capturar os times envolvidos no jogo
        times_match = re.findall(r"time \d+ - (\w+)", bloco)
        num_times = len(times_match)  # Determina se o jogo é de 2 ou 3 times

        if num_times < 2:
            print(f"⚠️ Número insuficiente de times para a data {data}, ignorando...")
            continue

        # 📌 Definir regras de pontuação conforme o número de times
        if num_times == 2:
            pontos_vitoria = 3
            pontos_empate = 1
        elif num_times == 3:
            pontos_vitoria = 1
            pontos_empate = 0

        # 📌 Capturar os jogos dentro do bloco
        jogos_match = re.search(r"# 🎮 jogos e resultados\n([\s\S]+?)(?:\n#|\Z)", bloco, re.DOTALL)
        if not jogos_match:
            print(f"⚠️ Nenhum jogo encontrado para a data {data}, ignorando...")
            continue

        jogos = jogos_match.group(1).strip().split("\n")

        for linha in jogos:
            if " - " in linha:
                try:
                    # Separar times e gols corretamente
                    partes = linha.split(" - ")
                    time1_gols = partes[0].rsplit(" ", 1)
                    time2_gols = partes[1].split(" ", 1)

                    if len(time1_gols) < 2 or len(time2_gols) < 2:
                        print(f"⚠️ Erro ao processar linha: {linha}")
                        continue

                    time1, gols1 = time1_gols
                    time2, gols2 = time2_gols

                    gols1, gols2 = int(gols1), int(gols2)

                    # 📌 Apagar jogo existente para sobrescrever os dados
                    cursor.execute("""
                        DELETE FROM jogos WHERE data=? AND time1=? AND time2=?
                    """, (data, time1, time2))

                    # 📌 Obter artilheiros desse jogo
                    artilheiros_padrao = re.findall(r"([\w]+)\s*\((\d+)\)", bloco)
                    artilheiros = ", ".join([f"{nome}({gols})" for nome, gols in artilheiros_padrao])

                    # 📌 Inserir jogo atualizado no banco
                    cursor.execute("""
                        INSERT INTO jogos (data, time1, gols_time1, time2, gols_time2, artilheiros, num_times, pontos_vitoria, pontos_empate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (data, time1, gols1, time2, gols2, artilheiros, num_times, pontos_vitoria, pontos_empate))

                    print(f"✅ Jogo atualizado: {time1} {gols1} - {gols2} {time2} ({data}), Times: {num_times}")
                    
                except Exception as e:
                    print(f"⚠️ Erro ao processar linha '{linha}': {e}")

    conn.commit()
    conn.close()

# 🔹 Executar a função
if __name__ == "__main__":
    processar_jogos()
