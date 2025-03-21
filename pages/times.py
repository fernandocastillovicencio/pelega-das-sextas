import streamlit as st

# 📌 Configuração da página
st.title("🏆 Seleção de Times")
st.write("Monte times equilibrados com base nas estatísticas dos jogadores.")

# 📌 Entrada da lista de jogadores
player_input = st.text_area("📋 Cole a lista de jogadores aqui", height=300)

# 📌 Seleção do número de times
num_teams = st.radio("⚽ Número de Times:", [2, 3])

# 📌 Número de combinações a avaliar
num_combinacoes = st.number_input(
    "🔄 Número de Combinações Avaliadas (N)",
    min_value=1,
    max_value=3000,
    value=1000,
    step=100,
)

# 📌 Botão para gerar os times
if st.button("FAZER TIMES"):
    if not player_input.strip():
        st.warning("⚠️ Insira a lista de jogadores antes de continuar.")
    else:
        st.info(
            "🔄 Processando... (Integração com a lógica de balanceamento virá nos próximos passos)"
        )
