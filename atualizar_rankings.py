import sqlite3
import re
import os

# 📌 Definir caminho do banco de dados na pasta 'data'
db_path = "data/dados.db"

def atualizar_rankings():
    """
    Calcula e atualiza o ranking de jogadores (Vitórias, Empates, Derrotas, Pontos e Gols)
    com base nos jogos já cadastrados no banco de dados.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 📌 Zerar rankings antes de recalcular
    cursor.execute("DELETE FROM rankings")

    # 📌 Buscar jogos registrados no banco
    cursor.execute("SELECT time1, gols_time1, time2, gols_time2, artilheiros FROM jogos")
    jogos = cursor.fetchall()

    estatisticas = {}

    for time1, gols1, time2, gols2, artilheiros in jogos:
        # 📌 Processar Artilheiros
        for info in artilheiros.split(", "):
            if "(" in info:
                jogador, gols = info.split("(")
                gols = int(gols.replace(")", "").strip())

                if jogador not in estatisticas:
                    estatisticas[jogador] = {"V": 0, "E": 0, "D": 0, "Pontos": 0, "Gols": 0}

                estatisticas[jogador]["Gols"] += gols

        # 📌 Determinar Vitórias, Empates e Derrotas
        if gols1 > gols2:  # Time1 venceu
            vencedores = [time1]
            perdedores = [time2]
            empatados = []
        elif gols2 > gols1:  # Time2 venceu
            vencedores = [time2]
            perdedores = [time1]
            empatados = []
        else:  # Empate
            vencedores = []
            perdedores = []
            empatados = [time1, time2]

        # 📌 Determinar Pontuação por Tipo de Jogo
        if len(jogos) == 2:  # Jogo de 2 times (Vitória = 3 pontos)
            pontos_vitoria = 3
            pontos_empate = 1
        else:  # Jogo de 3 times (Vitória = 1 ponto)
            pontos_vitoria = 1
            pontos_empate = 0

        for time in vencedores:
            for jogador in estatisticas:
                estatisticas[jogador]["V"] += 1
                estatisticas[jogador]["Pontos"] += pontos_vitoria

        for time in perdedores:
            for jogador in estatisticas:
                estatisticas[jogador]["D"] += 1

        for time in empatados:
            for jogador in estatisticas:
                estatisticas[jogador]["E"] += 1
                estatisticas[jogador]["Pontos"] += pontos_empate

    # 📌 Salvar Ranking no Banco
    for jogador, stats in estatisticas.items():
        cursor.execute("""
            INSERT INTO rankings (jogador, vitorias, empates, derrotas, pontos, gols)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (jogador, stats["V"], stats["E"], stats["D"], stats["Pontos"], stats["Gols"]))

    conn.commit()
    conn.close()

    print("✅ Rankings Atualizados com Sucesso!")

# 🔹 Executar a função
if __name__ == "__main__":
    atualizar_rankings()
