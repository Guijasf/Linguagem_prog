import streamlit as st
import pandas as pd
from pathlib import Path


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard de Vendas")


# ==========================================================
# CARREGAMENTO DOS DADOS
# ==========================================================

@st.cache_data
def carregar_dados():

    # Localiza a pasta onde o meu_dashboard.py está
    pasta_atual = Path(__file__).parent

    # Procura o vendas.csv nessa mesma pasta
    caminho_csv = pasta_atual / "vendas.csv"

    # Lê o arquivo
    df = pd.read_csv(caminho_csv)

    # Converte a coluna Data para data
    df["Data"] = pd.to_datetime(
        df["Data"],
        errors="coerce"
    )

    # Converte Receita para número
    df["Receita"] = pd.to_numeric(
        df["Receita"],
        errors="coerce"
    )

    return df


# Carrega os dados
df = carregar_dados()


# ==========================================================
# FILTROS LATERAIS
# ==========================================================

st.sidebar.title("Filtros")

lista_de_categorias = sorted(
    df["Categoria"]
    .dropna()
    .unique()
    .tolist()
)

categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=lista_de_categorias,
    default=lista_de_categorias
)


# ==========================================================
# FILTRAGEM DOS DADOS
# ==========================================================

if categorias_selecionadas:

    df_filtrado = df[
        df["Categoria"].isin(categorias_selecionadas)
    ].copy()

else:

    df_filtrado = df.copy()


# ==========================================================
# MÉTRICAS
# ==========================================================

receita_calculada = df_filtrado["Receita"].sum()

total_pedidos = len(df_filtrado)


col1, col2 = st.columns([1, 1])


with col1:

    st.metric(
        label="💰 Receita Total",
        value=f"R$ {receita_calculada:,.2f}"
    )


with col2:

    st.metric(
        label="📦 Total de Pedidos",
        value=total_pedidos
    )


# ==========================================================
# ABAS
# ==========================================================

aba1, aba2 = st.tabs(
    [
        "📈 Evolução Mensal",
        "📋 Tabela de Dados"
    ]
)


# ==========================================================
# ABA 1 - EVOLUÇÃO MENSAL
# ==========================================================

with aba1:

    st.subheader("Evolução Mensal da Receita")

    if not df_filtrado.empty:

        dados_mensais = (
            df_filtrado
            .dropna(subset=["Data"])
            .set_index("Data")
            .resample("ME")["Receita"]
            .sum()
        )

        st.area_chart(dados_mensais)

    else:

        st.warning(
            "Não existem dados para os filtros selecionados."
        )


# ==========================================================
# ABA 2 - TABELA
# ==========================================================

with aba2:

    st.subheader("Dados das Vendas")

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )


    # ======================================================
    # DOWNLOAD CSV
    # ======================================================

    csv = df_filtrado.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="⬇️ Baixar dados filtrados em CSV",
        data=csv,
        file_name="vendas_filtradas.csv",
        mime="text/csv"
    )