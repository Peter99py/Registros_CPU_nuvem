import streamlit as st
from src.charts.charts import grafico_linhas, grafico_colunas  # type: ignore
from src.queries.queries import time_vs_temp, temp_vs_speed, time_vs_power, temp_vs_power, faixas_temp

st.set_page_config(page_title="Meu Processador", layout="wide")

st.markdown("<h1 style='text-align: center; color: black;'>Meu Processador</h1>", unsafe_allow_html=True)
st.link_button("🔗 Acesse aqui o repositório do projeto no GitHub", "https://github.com/Peter99py/Registros_CPU")

df_faixas_temp = faixas_temp()
df_temp_vs_speed = temp_vs_speed()
df_time_vs_temp = time_vs_temp()
df_time_vs_power = time_vs_power()
df_temp_vs_power = temp_vs_power()

aba_resumo, aba_series, aba_relacoes = st.tabs(["Resumo", "Séries por Hora", "Relações"])

with aba_resumo: 
    st.subheader("Visão geral de temperaturas")
    grafico = grafico_colunas(df_faixas_temp,
        coluna_x="categoria",
        coluna_y="media diaria",
        titulo="Média Diária de Minutos por Faixa de Temperatura",
        mostrar_rotulos=True,
        posicao_rotulo="fora",
        cor_rotulo="black"
    )
    st.altair_chart(grafico, use_container_width=True)

    st.caption("Quanto tempo, em média por dia, o processador ficou em cada faixa de temperatura.")

with aba_series:
    st.subheader("Padrões ao longo do dia")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        grafico = grafico_linhas(
            df_time_vs_temp,
            coluna_x="time of day",
            coluna_y="core temp",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo ao Longo do Dia"
        )
        st.altair_chart(grafico, use_container_width=True)

    with col2:
        grafico = grafico_linhas(
            df_time_vs_power,
            coluna_x="time of day",
            coluna_y="cpu power",
            coluna_categoria="type",
            titulo="Energia do CPU ao Longo do Dia"
        )
        st.altair_chart(grafico, use_container_width=True)

    st.caption("Compare lado a lado: picos de temperatura tendem a coincidir com picos de energia?")

with aba_relacoes:
    st.subheader("Relações entre variáveis")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        grafico = grafico_linhas(
            df_temp_vs_speed,
            coluna_x="core temp",
            coluna_y="core speed",
            coluna_categoria="type",
            titulo="Temperatura do Núcleo vs Velocidade do Núcleo"
        )
        st.altair_chart(grafico, use_container_width=True)

    with col2:
        grafico = grafico_linhas(
            df_temp_vs_power,
            coluna_x="core temp",
            coluna_y="cpu power",
            coluna_categoria="type",
            titulo="Energia do CPU vs Temperatura do Núcleo"
        )
        st.altair_chart(grafico, use_container_width=True)

    st.caption("Veja como a velocidade e o consumo de energia variam conforme a temperatura do núcleo.")
