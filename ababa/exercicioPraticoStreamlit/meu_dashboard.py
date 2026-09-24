import streamlit as st
import pandas as pd


# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)

st.title("Dashboard de Vendas")


# --------------------------------------------------
# CARREGAMENTO DOS DADOS
# --------------------------------------------------

@st.cache_data
def carregar_dados():
    df = pd.read_csv("vendas.csv")

    # Converter a coluna Data para formato de data
    df["Data"] = pd.to_datetime(df["Data"])

    return df


df = carregar_dados()


# --------------------------------------------------
# FILTROS LATERAIS
# --------------------------------------------------

st.sidebar.title("Filtros")

lista_de_categorias = sorted(df["Categoria"].dropna().unique())

categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)


# --------------------------------------------------
# FILTRAGEM DOS DADOS
# --------------------------------------------------

if categorias_selecionadas:
    df_filtrado = df[
        df["Categoria"].isin(categorias_selecionadas)
    ]
else:
    df_filtrado = df.copy()


# --------------------------------------------------
# MÉTRICAS
# --------------------------------------------------

receita_calculada = df_filtrado["Receita"].sum()

# Caso cada linha represente um pedido
total_pedidos = len(df_filtrado)


col1, col2 = st.columns([1, 1])

with col1:
    st.metric(
        label="Receita Total",
        value=f"R$ {receita_calculada:,.2f}"
    )

with col2:
    st.metric(
        label="Total de Pedidos",
        value=total_pedidos
    )


# --------------------------------------------------
# ABAS
# --------------------------------------------------

aba1, aba2 = st.tabs([
    "Evolução Mensal",
    "Tabela de Dados"
])


# --------------------------------------------------
# ABA 1 - GRÁFICO
# --------------------------------------------------

with aba1:

    st.subheader("Evolução Mensal da Receita")

    dados_mensais = (
        df_filtrado
        .set_index("Data")
        .resample("ME")["Receita"]
        .sum()
    )

    st.area_chart(dados_mensais)


# --------------------------------------------------
# ABA 2 - TABELA
# --------------------------------------------------

with aba2:

    st.subheader("Dados das Vendas")

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )


    # --------------------------------------------------
    # EXPORTAÇÃO CSV
    # --------------------------------------------------

    csv = df_filtrado.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Baixar dados filtrados em CSV",
        data=csv,
        file_name="vendas_filtradas.csv",
        mime="text/csv"
    )