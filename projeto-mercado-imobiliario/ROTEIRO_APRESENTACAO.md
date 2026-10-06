# Roteiro de apresentação — aproximadamente 5 minutos

## 1. Problema (30 segundos)
“Meu projeto analisa o mercado imobiliário em uma base simulada de 2015 a 2024. A proposta é comparar preços por localização e tipo, observar a evolução temporal e analisar relações com área e renda.”

## 2. Dados e tratamento (1 minuto)
Mostre a seção Relações e qualidade.
“São 4.440 registros. Verifiquei campos ausentes, duplicatas e tipos. Um problema foi o preço por metro quadrado original: ele não correspondia ao preço dividido pela área. Preservei a coluna e criei outra calculada. Valores extremos foram sinalizados, sem exclusão automática.”

## 3. Indicadores e filtros (1 minuto)
Mostre a Visão geral. Explique preço médio, preço/m² e cidade mais cara. Selecione uma região e dois anos para mostrar que os indicadores e gráficos mudam. Filtro vazio significa todos. Limpe os filtros ao terminar.
“O crescimento é a média das variações anuais comparáveis. Não acompanhamos o mesmo imóvel, então não posso afirmar valorização individual.”

## 4. Comparações e relações (1 minuto)
Mostre rankings, heatmap e dispersão. Leia os líderes efetivamente exibidos.
“A comparação inclui média, mediana e quantidade de observações. Pearson mede associação linear entre variáveis; não demonstra causa e efeito.”

## 5. Integração e conclusão (1 minuto)
Mostre o notebook, sua consulta SQL e a página HTML.
“Pandas prepara a base, Matplotlib e Seaborn geram os gráficos, Streamlit apresenta os filtros. SQLAlchemy persiste os dados no SQLite. O tratamento compartilhado evita divergências entre notebook e dashboard.”
Leia a conclusão do recorte completo e destaque: os dados são simulados, a amostra não cobre todo o país e falta ajuste por inflação.

## Perguntas que você precisa saber responder
- **Por que recalcular preço/m²?** Para garantir consistência matemática entre preço e área.
- **Por que não apagar outliers?** Imóveis caros podem ser válidos; exclusão sem critério substantivo distorceria o resultado.
- **Quais são as duas funcionalidades avançadas?** Persistência em SQLite com SQLAlchemy e correlação estatística.
- **Por que média e mediana?** A média é mais sensível aos valores extremos; a mediana ajuda a comparar.
- **Por que usar cache?** Para evitar repetir a leitura e o tratamento a cada interação.
- **É um retrato do mercado real?** Não. É uma análise da base simulada fornecida para a atividade.
- **O que fica no GitHub Pages?** A apresentação HTML. O código Python é executado no Streamlit Cloud.

Antes de apresentar: execute o projeto no seu computador, confira os três links públicos e pratique explicar `carregar`, `crescimento` e os filtros. Apresentação presencial indicada para 8 de outubro.
