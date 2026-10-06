"""Execute: python -m streamlit run app.py."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from analise import carregar, persistir, ranking, crescimento, conclusao, brl, anual

st.set_page_config(page_title='Observatório Imobiliário | G1', page_icon='🏙️', layout='wide')
sns.set_theme(style='whitegrid', palette='crest')

@st.cache_data
def obter_dados():
    df, auditoria = carregar()
    persistir(df)
    return df, auditoria

df, auditoria = obter_dados()
st.title('Observatório do Mercado Imobiliário')
st.caption('Guilherme Familiar do Amaral · Tema 12 · Avaliação G1')
st.write('Como preços, localização, área e renda se relacionam na base simulada de 2015 a 2024?')
st.info('Base didática simulada. Os resultados descrevem somente esta amostra. Preço/m² é recalculado como preço ÷ área.')

st.sidebar.header('Explore os dados')
selecionado = df.copy()
for coluna, rotulo in [('ano','Ano'),('mes','Mês'),('regiao','Região'),('uf','Estado'),('cidade','Cidade'),('tipo_imovel','Tipo de imóvel'),('nivel_preco','Nível de preço (original)')]:
    opcoes = sorted(selecionado[coluna].dropna().unique().tolist())
    escolha = st.sidebar.multiselect(rotulo, opcoes, key=coluna, help='Vazio significa todos. Os filtros seguintes respeitam os anteriores.')
    if escolha:
        selecionado = selecionado[selecionado[coluna].isin(escolha)]
st.sidebar.caption('Nível de preço é a classificação original simulada; não foi inferido do valor.')
pagina = st.sidebar.radio('Seção', ['Visão geral', 'Comparações', 'Relações e qualidade', 'Dados e conclusão'])
d = selecionado
if d.empty:
    st.warning('Nenhum registro encontrado. Revise os filtros.')
    st.stop()
st.caption(f'{len(d):,} registros · {d.cidade.nunique()} cidades · {d.data.min():%m/%Y} a {d.data.max():%m/%Y}')

if pagina == 'Visão geral':
    a,b,c = st.columns(3)
    a.metric('Preço médio', brl(d.preco_imovel.mean()))
    b.metric('Preço médio/m² calculado', brl(d.preco_m2_calculado.mean()))
    taxa = crescimento(d)
    c.metric('Crescimento médio anual', 'N/D' if taxa is None else f'{taxa:.2f}%')
    a,b,c = st.columns(3)
    a.metric('Cidade mais cara', ranking(d,'cidade').index[0])
    b.metric('Região mais cara', ranking(d,'regiao').index[0])
    c.metric('Tipo com maior preço médio', ranking(d,'tipo_imovel').index[0])
    st.caption('Crescimento: média aritmética das variações de preço médio entre anos consecutivos com os mesmos meses selecionados. Não é valorização de um imóvel individual.')
    st.subheader('Evolução mensal dos preços')
    serie = d.groupby('data').preco_imovel.agg(['mean','median'])
    fig, ax = plt.subplots(figsize=(11,4))
    ax.plot(serie.index, serie['mean'], label='Média', color='#087e8b')
    ax.plot(serie.index, serie['median'], label='Mediana', color='#d58b32', alpha=.8)
    ax.set(xlabel='Data', ylabel='Preço (R$)'); ax.legend(); fig.tight_layout()
    st.pyplot(fig); plt.close(fig)
    st.write('Média e mediana permitem avaliar a influência de valores elevados. Mudanças podem refletir imóveis diferentes em cada período.')
    st.dataframe(anual(d).rename('Preço médio anual (R$)'), width='stretch')
    st.write(conclusao(d))

elif pagina == 'Comparações':
    for coluna, titulo in [('cidade','Cidades com maior preço médio'),('regiao','Preço por região'),('tipo_imovel','Preço por tipo de imóvel')]:
        st.subheader(titulo)
        r = ranking(d,coluna).head(15)
        fig, ax = plt.subplots(figsize=(10,max(3,len(r)*.3)))
        ax.barh(r.index[::-1], r['mean'].iloc[::-1], color='#087e8b')
        ax.set_xlabel('Preço médio (R$)'); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
        st.dataframe(r.rename(columns={'mean':'Média (R$)','median':'Mediana (R$)','count':'Observações'}), width='stretch')
    st.subheader('Heatmap regional por ano')
    pivot = d.pivot_table(index='regiao', columns='ano', values='preco_imovel', aggfunc='mean')
    fig, ax = plt.subplots(figsize=(11,4))
    sns.heatmap(pivot/1000, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax, cbar_kws={'label':'Preço médio (mil R$)'})
    ax.set(xlabel='Ano',ylabel='Região'); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    st.subheader('Variação por cidade entre os anos extremos')
    cidade_ano = d.pivot_table(index='cidade',columns='ano',values='preco_imovel',aggfunc='mean')
    if len(cidade_ano.columns) > 1:
        primeiro, ultimo = cidade_ano.columns.min(), cidade_ano.columns.max()
        variacao = cidade_ano[[primeiro,ultimo]].dropna().copy()
        variacao['Variação (%)'] = (variacao[ultimo]/variacao[primeiro]-1)*100
        st.dataframe(variacao.sort_values('Variação (%)',ascending=False).rename(columns=str),width='stretch')
        st.caption('Variação das médias amostrais. Compare os meses e tipos disponíveis antes de interpretar diferenças como tendência.')
    else:
        st.info('Selecione dois ou mais anos para comparar.')

elif pagina == 'Relações e qualidade':
    st.subheader('Área, renda e preço')
    for coluna, titulo in [('area_m2','Área (m²)'),('renda_media','Renda média (R$)')]:
        fig, ax = plt.subplots(figsize=(10,4))
        sns.scatterplot(data=d,x=coluna,y='preco_imovel',hue='regiao',alpha=.4,s=18,ax=ax)
        ax.set(xlabel=titulo,ylabel='Preço (R$)'); fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    st.subheader('Correlação de Pearson')
    cols = ['area_m2','preco_imovel','renda_media','taxa_juros']
    fig, ax = plt.subplots(figsize=(8,4))
    sns.heatmap(d[cols].corr(),annot=True,fmt='.2f',vmin=-1,vmax=1,center=0,cmap='vlag',ax=ax)
    fig.tight_layout(); st.pyplot(fig); plt.close(fig)
    st.write('Correlação resume associação linear, não demonstra causalidade. Poucos registros ou variáveis constantes produzem coeficientes indefinidos. Valores próximos de zero não excluem relações não lineares.')
    st.subheader('Auditoria da base completa')
    st.json(auditoria)
    st.warning('O preço/m² fornecido diverge do cálculo preço/área. Preservamos a coluna original e utilizamos preco_m2_calculado nos indicadores. Valores extremos são sinalizados, sem remoção automática.')
    st.dataframe(d[['preco_imovel','area_m2','preco_m2','preco_m2_calculado','divergencia_m2','outlier_preco']].head(30),width='stretch')

else:
    st.subheader('Tabela dinâmica')
    st.dataframe(d.pivot_table(index=['regiao','uf','cidade'],columns='tipo_imovel',values='preco_imovel',aggfunc='mean'), width='stretch')
    st.subheader('Dados filtrados')
    st.dataframe(d,width='stretch')
    st.download_button('Baixar CSV filtrado',d.to_csv(index=False).encode('utf-8-sig'),'imoveis_filtrados.csv','text/csv')
    st.subheader('Conclusão executiva')
    st.write(conclusao(d))
    st.write('Para aprofundar a análise, seria necessário acompanhar imóveis equivalentes, ajustar por inflação e validar dados reais de transações. A amostra cobre 37 cidades em 20 UFs, sem pesos populacionais.')
    st.caption('Persistência: tabela imoveis em database/mercado.db, gerada com SQLAlchemy + SQLite. O arquivo é reconstruível; armazenamento em hospedagem pode ser temporário.')
