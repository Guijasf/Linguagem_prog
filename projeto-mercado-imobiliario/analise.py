"""Preparação e métricas compartilhadas pelo notebook e dashboard."""
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parent
CSV = ROOT / 'dados/simulacao_mercado_imobiliario_brasil.csv'
NUMERICAS = ['ano', 'mes', 'area_m2', 'quartos', 'vagas_garagem', 'preco_imovel', 'preco_m2', 'renda_media', 'taxa_juros']
CATEGORICAS = ['regiao', 'uf', 'cidade', 'bairro', 'tipo_imovel', 'nivel_preco']

def carregar():
    bruto = pd.read_csv(CSV)
    df = bruto.copy()
    for c in CATEGORICAS:
        df[c] = df[c].astype('string').str.strip().replace('', pd.NA)
    for c in NUMERICAS:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    duplicadas = int(df.duplicated().sum())
    df = df.drop_duplicates()
    validos = (df['data'].notna() & df['area_m2'].gt(0) & df['preco_imovel'].gt(0)
               & df['renda_media'].gt(0) & df[CATEGORICAS].notna().all(axis=1))
    invalidos = int((~validos).sum())
    df = df.loc[validos].copy()
    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    # A coluna fornecida é preservada: a versão calculada garante preço/área.
    df['preco_m2_calculado'] = df['preco_imovel'] / df['area_m2']
    df['divergencia_m2'] = (df['preco_m2'] - df['preco_m2_calculado']).abs().gt(0.01)
    df['preco_renda'] = df['preco_imovel'] / df['renda_media']
    q1, q3 = df['preco_imovel'].quantile([.25, .75])
    df['outlier_preco'] = df['preco_imovel'].gt(q3 + 1.5 * (q3-q1))
    auditoria = {'registros_originais':len(bruto), 'duplicadas_removidas':duplicadas,
                 'invalidos_removidos':invalidos, 'registros_validos':len(df),
                 'divergencias_preco_m2':int(df['divergencia_m2'].sum()),
                 'outliers_preservados':int(df['outlier_preco'].sum())}
    return df.sort_values('data'), auditoria

def persistir(df):
    caminho = ROOT / 'database/mercado.db'
    caminho.parent.mkdir(exist_ok=True)
    engine = create_engine(f'sqlite:///{caminho}')
    with engine.begin() as conn:
        df.to_sql('imoveis', conn, if_exists='replace', index=False)
    engine.dispose()
    return caminho

def anual(df):
    return df.groupby('ano')['preco_imovel'].mean().sort_index()

def crescimento(df):
    serie = anual(df)
    if len(serie) < 2:
        return None
    # Só comparar anos consecutivos que contenham os mesmos meses.
    meses = df.groupby('ano')['mes'].apply(lambda x: set(x))
    taxas = [(serie.loc[a]/serie.loc[a-1]-1)*100 for a in serie.index
             if a-1 in serie.index and meses.loc[a] == meses.loc[a-1]]
    return sum(taxas)/len(taxas) if taxas else None

def ranking(df, coluna):
    return df.groupby(coluna)['preco_imovel'].agg(['mean','median','count']).sort_values('mean', ascending=False)

def brl(n):
    return 'R$ ' + f'{n:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def conclusao(df):
    if df.empty:
        return 'Não há registros no recorte selecionado.'
    cidade = ranking(df, 'cidade').index[0]
    regiao = ranking(df, 'regiao').index[0]
    tipo = ranking(df, 'tipo_imovel').index[0]
    corr = df['renda_media'].corr(df['preco_imovel'])
    taxa = crescimento(df)
    return (f'No recorte de {len(df):,} observações, {cidade} apresenta o maior preço médio, '
            f'{regiao} lidera entre as regiões e {tipo} tem o maior preço médio entre os tipos. '
            f'A correlação de Pearson entre renda e preço é {corr:.3f}. '
            + (f'A média das variações anuais comparáveis é {taxa:.2f}%. ' if taxa is not None else 'Não há pares de anos comparáveis para calcular crescimento anual. ')
            + 'As médias refletem a composição da amostra; não acompanham os mesmos imóveis. '
            'Os dados são simulados e não permitem conclusões sobre o mercado brasileiro real, causalidade ou recomendações de investimento.')
