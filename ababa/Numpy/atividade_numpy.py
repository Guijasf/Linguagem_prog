import numpy as np


# ============================================================
# ATIVIDADE 1 - ANÁLISE DE DADOS NO VAREJO COM NUMPY
# ============================================================

print("=" * 70)
print("ATIVIDADE 1 - ANÁLISE DE DADOS NO VAREJO COM NUMPY")
print("=" * 70)


# ============================================================
# NÍVEL 1 - BÁSICO
# Faturamento Semanal e Filtros
# ============================================================

print("\n--- NÍVEL 1: Faturamento Semanal e Filtros ---")


# ------------------------------------------------------------
# Passo 1 - Array com peças vendidas durante a semana
# ------------------------------------------------------------

pecas_vendidas = np.array(
    [150, 120, 90, 210, 300, 250, 180]
)

print("\nPeças vendidas durante a semana:")
print(pecas_vendidas)


# ------------------------------------------------------------
# Passo 2 - Faturamento diário
# Preço médio de cada peça = R$ 50,00
# ------------------------------------------------------------

preco_medio = 50

faturamento_diario = pecas_vendidas * preco_medio

print("\nFaturamento diário:")
print(faturamento_diario)


print(
    "\nFaturamento total da semana: "
    f"R$ {faturamento_diario.sum():,.2f}"
)


# ------------------------------------------------------------
# Passo 3 - Dias em que foram vendidas mais de 200 peças
# ------------------------------------------------------------

mascara_pico = pecas_vendidas > 200

dias_pico = pecas_vendidas[mascara_pico]

print("\nMáscara booleana:")
print(mascara_pico)

print("\nVendas superiores a 200 peças:")
print(dias_pico)


# ============================================================
# NÍVEL 2 - INTERMEDIÁRIO
# Múltiplas Filiais e Falhas de Sistema
# ============================================================

print("\n" + "=" * 70)
print("NÍVEL 2 - Múltiplas Filiais e Falhas de Sistema")
print("=" * 70)


# ------------------------------------------------------------
# Passo 1 - Matriz de vendas
#
# Linhas = lojas
# Colunas = dias
# ------------------------------------------------------------

vendas_lojas = np.array(
    [
        [200, 220, np.nan, 250],  # Loja A
        [150, 180, 160, 190],     # Loja B
        [300, 310, 290, 330],     # Loja C
    ]
)


print("\nMatriz de vendas:")
print(vendas_lojas)


# ------------------------------------------------------------
# Passo 2 - Total vendido por loja
# ------------------------------------------------------------

# Se utilizarmos np.sum(), a Loja A terá resultado NaN,
# pois existe um valor ausente.

total_com_sum = np.sum(
    vendas_lojas,
    axis=1
)

print("\nTotal utilizando np.sum():")
print(total_com_sum)


# Para obter o total ignorando o NaN:
total_por_loja = np.nansum(
    vendas_lojas,
    axis=1
)

print("\nTotal por loja ignorando valores NaN:")

for i, total in enumerate(total_por_loja):
    print(f"Loja {chr(65 + i)}: {total:.0f} peças")


# ------------------------------------------------------------
# Passo 3 - Média geral ignorando NaN
# ------------------------------------------------------------

media_normal = np.mean(vendas_lojas)

media_geral = np.nanmean(vendas_lojas)


print("\nMédia utilizando np.mean():")
print(media_normal)


print("\nMédia geral utilizando np.nanmean():")
print(f"{media_geral:.2f} peças")


# ------------------------------------------------------------
# Passo 4 - Classificação da meta
# Meta diária = 200 peças
# ------------------------------------------------------------

situacao_meta = np.where(
    vendas_lojas >= 200,
    "Meta Atingida",
    "Abaixo"
)


print("\nSituação das metas:")
print(situacao_meta)


# ============================================================
# NÍVEL 3 - AVANÇADO
# Categorização e Destaques de Marketing
# ============================================================

print("\n" + "=" * 70)
print("NÍVEL 3 - Categorização e Destaques de Marketing")
print("=" * 70)


# ------------------------------------------------------------
# Passo 1 - Simulação de 50 vendas
# ------------------------------------------------------------

rng = np.random.default_rng(42)


departamentos = np.array(
    [
        "Eletrônicos",
        "Roupas",
        "Casa",
    ]
)


vendas_clientes = rng.choice(
    departamentos,
    size=50
)


print("\n50 vendas simuladas:")
print(vendas_clientes)


# ------------------------------------------------------------
# Passo 2 - Contagem das vendas por departamento
# ------------------------------------------------------------

categorias, quantidades = np.unique(
    vendas_clientes,
    return_counts=True
)


print("\nQuantidade de vendas por departamento:")

for categoria, quantidade in zip(
    categorias,
    quantidades
):
    print(
        f"{categoria}: "
        f"{quantidade} vendas"
    )


# ------------------------------------------------------------
# Passo 3 - Campanha com maior faturamento
# ------------------------------------------------------------

faturamento_campanhas = np.array(
    [
        12000,
        45000,
        23000,
        89000,
        31000,
    ]
)


indice_campea = np.argmax(
    faturamento_campanhas
)


print("\nFaturamento das campanhas:")
print(faturamento_campanhas)


print(
    "\nÍndice da campanha campeã:",
    indice_campea
)


print(
    "Campanha campeã:",
    indice_campea + 1
)


print(
    "Faturamento da campanha campeã: "
    f"R$ {faturamento_campanhas[indice_campea]:,.2f}"
)



# ============================================================
# ATIVIDADE 2
# ORGANIZAÇÃO E TRANSFORMAÇÃO DE DADOS COM NUMPY
# ============================================================

print("\n\n")
print("=" * 70)
print("ATIVIDADE 2 - ORGANIZAÇÃO E TRANSFORMAÇÃO DE DADOS")
print("=" * 70)


# ============================================================
# NÍVEL 1 - BÁSICO
# Geração de Sequências e Tipagem
# ============================================================

print("\n--- NÍVEL 1: Geração de Sequências e Tipagem ---")


# ------------------------------------------------------------
# Passo 1 - Array com os 30 dias do mês
# ------------------------------------------------------------

dias_mes = np.arange(
    1,
    31
)


print("\nDias do mês:")
print(dias_mes)


# ------------------------------------------------------------
# Passo 2 - 5 metas igualmente espaçadas
# entre R$ 20.000 e R$ 30.000
# ------------------------------------------------------------

metas = np.linspace(
    20000,
    30000,
    5
)


print("\nMetas de vendas:")
print(metas)


# ------------------------------------------------------------
# Passo 3 - Conversão de float para inteiro
# ------------------------------------------------------------

estoque_decimal = np.array(
    [
        10.5,
        20.1,
        30.9,
    ]
)


estoque_inteiro = estoque_decimal.astype(int)


print("\nEstoque original:")
print(estoque_decimal)


print("\nEstoque convertido para inteiro:")
print(estoque_inteiro)


# ------------------------------------------------------------
# Passo 4 - Últimos cinco dias em ordem inversa
# ------------------------------------------------------------

ultimos_cinco = dias_mes[-5:][::-1]


print("\nÚltimos cinco dias em ordem inversa:")
print(ultimos_cinco)



# ============================================================
# NÍVEL 2 - INTERMEDIÁRIO
# Redimensionamento e Proteção de Dados
# ============================================================

print("\n" + "=" * 70)
print("NÍVEL 2 - Redimensionamento e Proteção de Dados")
print("=" * 70)


# ------------------------------------------------------------
# Passo 1 - Visitas durante 12 meses
# ------------------------------------------------------------

visitas_mensais = np.array(
    [
        1200,
        1350,
        1500,
        1450,
        1600,
        1750,
        1800,
        1950,
        2100,
        2050,
        2200,
        2400,
    ]
)


print("\nVisitas mensais:")
print(visitas_mensais)


# Transformando os 12 meses em:
#
# 4 linhas = trimestres
# 3 colunas = meses
# ------------------------------------------------------------

visitas_trimestres = visitas_mensais.reshape(
    4,
    3
)


print("\nVisitas organizadas por trimestre:")
print(visitas_trimestres)


# ------------------------------------------------------------
# Passo 2 - Combinando primeiro e segundo semestre
# ------------------------------------------------------------

primeiro_semestre = np.array(
    [
        [1200, 1350, 1500],
        [1450, 1600, 1750],
    ]
)


segundo_semestre = np.array(
    [
        [1800, 1950, 2100],
        [2050, 2200, 2400],
    ]
)


ano_completo = np.vstack(
    [
        primeiro_semestre,
        segundo_semestre,
    ]
)


print("\nPrimeiro semestre:")
print(primeiro_semestre)


print("\nSegundo semestre:")
print(segundo_semestre)


print("\nDados combinados com vstack:")
print(ano_completo)


# ------------------------------------------------------------
# Passo 3 - Criando uma cópia do primeiro trimestre
# ------------------------------------------------------------

primeiro_trimestre = visitas_trimestres[0].copy()


print("\nPrimeiro trimestre:")
print(primeiro_trimestre)


# Podemos alterar a cópia sem modificar o array original.

primeiro_trimestre[0] = 9999


print("\nCópia modificada:")
print(primeiro_trimestre)


print("\nMatriz original continua intacta:")
print(visitas_trimestres)


# ------------------------------------------------------------
# Passo 4 - Transformando matriz novamente em array 1D
# ------------------------------------------------------------

dados_achatados = visitas_trimestres.ravel()


print("\nDados achatados com ravel():")
print(dados_achatados)



# ============================================================
# NÍVEL 3 - AVANÇADO
# Ranking, Broadcasting e Sistemas Lineares
# ============================================================

print("\n" + "=" * 70)
print("NÍVEL 3 - Ranking, Broadcasting e Sistemas Lineares")
print("=" * 70)


# ------------------------------------------------------------
# Passo 1 - Ranking utilizando argsort()
# ------------------------------------------------------------

notas = np.array(
    [
        85,
        92,
        78,
        95,
        88,
    ]
)


indices_ordenados = np.argsort(notas)


print("\nNotas:")
print(notas)


print("\nÍndices em ordem crescente:")
print(indices_ordenados)


print("\nNotas em ordem crescente:")
print(notas[indices_ordenados])


# Para ranking do maior para o menor:
ranking = np.argsort(notas)[::-1]


print("\nRanking do maior para o menor:")
print(ranking)


print("\nResultado do ranking:")

for posicao, indice in enumerate(
    ranking,
    start=1
):

    print(
        f"{posicao}º lugar -> "
        f"Aluno {indice + 1} -> "
        f"Nota {notas[indice]}"
    )


# ------------------------------------------------------------
# Passo 2 - np.newaxis e Broadcasting
# ------------------------------------------------------------

precos = np.array(
    [
        100,
        200,
        300,
    ]
)


print("\nPreços em formato de linha:")
print(precos)


# Transformando em coluna

precos_coluna = precos[:, np.newaxis]


print("\nPreços em formato de coluna:")
print(precos_coluna)


# Percentuais de desconto

descontos = np.array(
    [
        0.10,
        0.20,
        0.30,
    ]
)


# Broadcasting:
# cada preço será combinado com cada desconto

precos_com_desconto = (
    precos_coluna
    * (1 - descontos)
)


print("\nDescontos:")
print(descontos)


print("\nPreços após aplicação dos descontos:")
print(precos_com_desconto)


# ============================================================
# Passo 3 - Sistema de Equações
#
# Projeto A:
# 2 placas + 1 sensor = 500
#
# Projeto B:
# 1 placa - 1 sensor = 100
#
# Sistema:
#
# 2x + y = 500
# x  - y = 100
# ============================================================


A = np.array(
    [
        [2, 1],
        [1, -1],
    ]
)


b = np.array(
    [
        500,
        100,
    ]
)


solucao = np.linalg.solve(
    A,
    b
)


valor_placa = solucao[0]
valor_sensor = solucao[1]


print("\nMatriz A:")
print(A)


print("\nVetor b:")
print(b)


print("\nSolução:")
print(solucao)


print(
    f"\nValor de uma placa robótica: "
    f"R$ {valor_placa:.2f}"
)


print(
    f"Valor de um sensor: "
    f"R$ {valor_sensor:.2f}"
)


print("\n" + "=" * 70)
print("TODAS AS ATIVIDADES FORAM EXECUTADAS")
print("=" * 70)