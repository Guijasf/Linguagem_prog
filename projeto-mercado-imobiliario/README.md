# Observatório do Mercado Imobiliário Brasileiro
**Guilherme Familiar do Amaral · Tema 12 · Avaliação G1**

Análise de 4.440 observações simuladas, de 2015 a 2024, com 37 cidades e 20 UFs. Perguntas: quais cidades, regiões e tipos têm maior preço médio? Como as médias evoluem? Qual a associação entre área, renda e preço?

## Executar no Windows / VS Code
1. Extraia o ZIP. Abra a pasta `projeto-mercado-imobiliario` no VS Code.
2. Instale Python 3.11 ou 3.12, se necessário.
3. No terminal dessa pasta, execute:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

Abra o endereço local mostrado no terminal. Para encerrar, pressione Ctrl+C.
No Linux/macOS, use `python3 -m venv .venv` e `.venv/bin/python` nos dois comandos seguintes.

## Notebook
Abra `notebooks/analise_mercado_imobiliario.ipynb` no VS Code com as extensões Python e Jupyter. Selecione o Python de `.venv` e clique em Executar Tudo. O notebook entregue já contém resultados. `analise.py` compartilha o tratamento com o dashboard.

## Estrutura
- `app.py`: dashboard, sete filtros, KPIs e quatro seções.
- `analise.py`: limpeza, métricas, conclusões e persistência.
- `dados/`: CSV original do professor.
- `database/`: banco SQLite, reconstruído automaticamente.
- `notebooks/`: análise executada e comentada.
- `imagens/`: gráficos exportados pelo notebook.
- `index.html`: apresentação para GitHub Pages.
- `ROTEIRO_APRESENTACAO.md`: guia para explicar o projeto.

## Metodologia
Médias simples por observação; rankings incluem mediana e contagem. Preço/m² é a média de `preco_imovel / area_m2`. A coluna original diverge desse cálculo e é preservada para auditoria. Dados ausentes essenciais, valores não positivos essenciais e duplicatas são tratados; outliers de preço são sinalizados por 1,5 IQR e preservados. O nível de preço é o rótulo original, sem limites conhecidos.

Crescimento médio anual: média aritmética das taxas do preço médio entre anos consecutivos que contenham os mesmos meses selecionados. Com apenas um ano ou sem pares comparáveis, aparece N/D. Não equivale à valorização de um mesmo imóvel. Não há correção inflacionária. Comparações por cidade entre anos extremos também refletem composição da amostra.

A base é simulada e não representa o mercado real. Cobertura parcial, falta de pesos amostrais e ausência de identificador de imóvel limitam inferências. Correlação de Pearson não indica causalidade. A razão exploratória preço/renda não tem unidade temporal definida na documentação da fonte.

## Requisitos atendidos
| Requisito | Implementação |
|---|---|
| Python, Pandas | Tratamento e análise |
| Matplotlib, Seaborn | Linha, barras, dispersão e heatmaps |
| Streamlit | Dashboard com filtros e tabelas |
| Intermediárias | Filtros múltiplos, KPIs dinâmicos, série temporal, seções, comparação |
| Avançada 1 | SQLAlchemy + SQLite: gravação e consulta SQL no notebook |
| Avançada 2 | Correlação estatística com Pandas e interpretação |
| Notebook | Problema, base, limpeza, atributos, EDA, KPIs, gráficos, interpretação e conclusão |
| HTML | Apresentação com resultados e links locais |
| Publicação | Pendente: executar as etapas abaixo na sua conta |

## Publicar e entregar
Os arquivos estão preparados; nenhum serviço foi publicado automaticamente.

1. Crie um repositório público chamado `projeto-mercado-imobiliario` na sua conta GitHub. Envie o conteúdo da pasta, com `app.py` e `index.html` na raiz. O CSV deve estar em `dados/`. Não envie `.venv`.
2. No GitHub, abra Settings → Pages, escolha publicação pela branch `main`, pasta `/ (root)`, e salve. O GitHub mostrará o endereço após a publicação.
3. No Streamlit Community Cloud, conecte sua conta GitHub, crie um aplicativo usando esse repositório, branch `main`, arquivo `app.py`. Escolha Python 3.11 ou 3.12 nas opções disponíveis e publique.
4. Em `index.html`, encontre o comentário `LINKS DE PUBLICAÇÃO`. Substitua o parágrafo de publicação pendente por links reais do repositório e do dashboard. Atualize também a seção abaixo deste README.
5. Verifique os três links em janela anônima e teste um filtro. Entregue os links do GitHub, Pages e Streamlit, além do notebook, código e base conforme a atividade.

### Links de entrega — preencher após publicar
- GitHub: https://github.com/Guijasf/Linguagem_prog
- GitHub Pages: https://guijasf.github.io/Linguagem_prog/projeto-mercado-imobiliario/
- Streamlit: https://linguagemprog-krw6j7ucjan67pkfntmvg5.streamlit.app/

O SQLite é recriado quando necessário. No Streamlit Cloud, o armazenamento local pode ser temporário. A fonte definitiva do projeto é o CSV versionado.

## Fonte
https://github.com/AlexandreLouzada/Dados-Simulados-G1
Arquivo: `datasets_g1_30_temas/simulacao_mercado_imobiliario_brasil.csv`.
Commit da fonte: `b0e6390d001a221653ce42c8374b5da8cfc1b1b7`.
O enunciado específico diz G2 no título, mas está na atividade G1. A identificação adotada acompanha o aviso e a avaliação geral: G1.
