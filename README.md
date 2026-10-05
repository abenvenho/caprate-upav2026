# Cap rates de escritórios por combinação de especialistas

**Português** · [Español](README.es.md) · [English](README.en.md)

[![Código: Apache 2.0](https://img.shields.io/badge/c%C3%B3digo-Apache%202.0-blue.svg)](LICENSE)
[![Dados e textos: CC BY 4.0](https://img.shields.io/badge/dados%20e%20textos-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

Dados, código, resultados, artigo, apresentação e aplicativo interativo do trabalho

> **Análise de taxas de rentabilidade no mercado imobiliário empregando aprendizagem de máquina e combinação de especialistas**
> Agnaldo Calvi Benvenho · Osório Accioly Gatto — XL Congresso Panamericano de Avaliação, UPAV 2026, Madri.
> Eixo temático: inteligência artificial e novas tecnologias aplicadas à valoração.

---

## O que foi feito

O cap rate — renda operacional líquida anual dividida pelo valor do imóvel — converte renda em valor no
método da capitalização, define a perpetuidade nas avaliações pela renda e serve de crítica às taxas de
desconto. Pequenas diferenças de taxa produzem grandes diferenças de valor: a mesma renda capitalizada a
6% ou a 10% a.a. resulta em valores 40% diferentes.

O estudo pergunta se **combinar modelos de aprendizado de máquina melhora a estimativa do cap rate** de
escritórios corporativos. Três especialistas com funções complementares são combinados por *stacking*:

| Especialista | Papel | Configuração |
|---|---|---|
| Regressão Ridge | tendência média, coeficientes interpretáveis | α escolhido por validação interna (α = 51,8) |
| Árvore de regressão rasa | regras condicionais | profundidade 5, mínimo de 10 observações por folha |
| Rede neural MLP | relações não lineares moderadas | duas camadas ocultas (64 → 32), ReLU, *early stopping* |
| **Integrador** | aprende o peso de cada especialista | Ridge sobre as previsões fora do treino |

**Dados:** 247 observações de escritórios corporativos em São Paulo, de 2022 a 2026, em 11 regiões de
mercado definidas por reclassificação geoespacial. Variáveis: área útil, padrão construtivo (IUP,
IBAPE/SP), estado de conservação (Ross-Heidecke), região e ano. Validação cruzada 5-fold (seed 42).

## Principais resultados (Tabela 4 do artigo)

| Modelo | RMSE (p.p.) | MAE (p.p.) | R² | dCor |
|---|---:|---:|---:|---:|
| Ridge | 2,5266 | 1,8745 | 0,1786 | 0,4615 |
| Árvore de regressão | 2,4241 | 1,7878 | 0,2439 | 0,5131 |
| MLP | 2,5907 | 1,9572 | 0,1364 | 0,4322 |
| **Ensemble stacking** | **2,3933** | **1,7836** | **0,2630** | **0,5214** |

Os principais determinantes, consistentes entre os três especialistas, são a localização em
**Vila Olímpia** (importância por permutação 0,369), o **padrão construtivo** (0,271), a **área útil**
(0,163) e o **estado de conservação** (0,127).

## Conclusões

- A combinação de especialistas superou cada modelo isolado. Trata-se, até onde os autores puderam
  apurar, da primeira aplicação no Brasil de aprendizado de máquina à estimativa de cap rates de imóveis
  comerciais.
- A **distance correlation** revelou associações não lineares que medidas lineares subestimam — por
  exemplo, padrão construtivo com dCor = 0,375 contra |ρ| = 0,28 (Spearman) —, o que fundamenta o uso de
  especialistas não lineares.
- O R² moderado (cerca de 74% da variância não explicada) é em boa parte **estrutural**: vacância, prazo
  remanescente de locação, indexador e qualidade do locatário não estão nos dados e podem, sozinhos, separar
  em 2 a 4 p.p. o cap rate de ativos fisicamente idênticos.
- Por isso o modelo é útil sobretudo como **instrumento de triagem**: um desvio entre o cap rate observado e
  o previsto acima de cerca de 2 × RMSE (≈ 4,8 p.p.) sinaliza um ativo cuja taxa é explicada por fatores
  não capturados, que o avaliador deve investigar. O modelo apoia — e não substitui — o juízo profissional.

## Reprodutibilidade e robustez

Todo o artigo foi recalculado a partir da base publicada (`code/01_reproduzir_artigo.py`):

| Item do artigo | Publicado | Recalculado |
|---|---|---|
| Tabela 4 — 3 especialistas e ensemble, 4 métricas | ver acima | **idêntico** (4 casas decimais) |
| α da Ridge e coeficientes padronizados | 51,8; +0,558 / −0,418 / +0,373 / −0,351 | **idêntico** |
| Árvore: folhas, 1º corte, folha de maior valor | 12; Padrão ≤ 4,03; 11,48% | **idêntico** |
| Importância por permutação (top 4) | 0,369 / 0,271 / 0,163 / 0,127 | **idêntico** |
| Tabelas 1 e 3; ANOVA F | — ; 5,81 | idêntico; 5,81 |
| Kruskal-Wallis H; dCor da região; D.P. de Jardins | 51,51; 0,354; 1,27 | 51,49; 0,355; 1,33 |
| **Pesos do integrador** (Seções 5.1 e 7.1) | 0,0035 / 0,5144 / 0,4217 | **0,1788 / 0,6411 / 0,1417** |

**Pesos do integrador.** O ajuste que reproduz exatamente a Tabela 4 atribui à Ridge, à árvore e à MLP os
pesos 0,18, 0,64 e 0,14 (intercepto 0,32). Aplicados às mesmas previsões, os pesos impressos no artigo não
alcançam o RMSE de 2,3933 (o melhor possível com eles é 2,41). A leitura de que a previsão se apoia
sobretudo na árvore permanece; a de que a Ridge tem peso praticamente nulo e a MLP ≈ 0,42, não.

**Robustez** (`code/02_robustez.py`, verificações recomendadas na Seção 7.3 do artigo). Na Tabela 4 o
integrador é ajustado e avaliado sobre as mesmas 247 previsões, o que é ligeiramente otimista. Com o
integrador também validado fora da amostra (validação **aninhada**), em quatro sementes, e com **GroupKFold
por edifício** (182 edifícios identificados pelas coordenadas, para que unidades do mesmo prédio não fiquem
em treino e teste):

| Esquema | Ridge | Árvore | MLP | Ensemble |
|---|---:|---:|---:|---:|
| Tabela 4 (seed 42) | 2,527 | 2,424 | 2,591 | **2,393** |
| Aninhado, média de 4 sementes | 2,495 | 2,503 | 2,531 | **2,445** |
| Aninhado, seed 42 | 2,527 | **2,424** | 2,591 | 2,490 |
| GroupKFold por edifício | 2,514 | 2,615 | 2,582 | **2,497** |

RMSE em p.p. O ensemble é o melhor modelo na média das sementes e no GroupKFold — a conclusão central do
artigo se mantém —, mas com erro de 2,45 a 2,50 p.p. em vez de 2,39 p.p. (R² de 0,20 a 0,23). Com a
partição da seed 42, a árvore isolada fica à frente do ensemble quando este é validado de forma aninhada.

## Conteúdo do repositório

```
paper/          Artigo completo (PDF, em português, com resumo em português, espanhol e inglês)
presentation/   Apresentação do Congresso UPAV 2026, Madri (PDF e PPTX)
data/
  base_caprate_escritorios_sp_n247.csv   247 × 22 — base completa (UTF-8, separada por vírgulas)
  data_dictionary.csv                    descrição, uso no artigo, tipo e faixa de cada coluna
code/
  caprate.py                 especificação comum (variáveis, especialistas, validação, métricas)
  01_reproduzir_artigo.py    Tabelas 1 a 4, testes, pesos, coeficientes, árvore, importância
  02_robustez.py             validação aninhada, várias sementes e GroupKFold por edifício
  03_figuras.py              figuras de resultados
results/        Saídas dos scripts (CSV, JSON e TXT), incluindo as previsões out-of-fold
figures/        Previsto × observado, resíduos, importância por permutação, coeficientes da Ridge
app/            Aplicativo Streamlit
```

## Aplicativo interativo

O aplicativo recalcula todos os modelos a partir da base publicada, em português, espanhol e inglês:

- **Sobre o estudo** — resumo e comparação de desempenho;
- **Base de dados** — mapa das 247 observações, cap rate por região, filtros e download;
- **Desempenho** — Tabela 4 recalculada, pesos do integrador, observado × previsto e robustez;
- **Determinantes** — importância por permutação, coeficientes da Ridge e regras da árvore;
- **Simulador** — estima o cap rate de um escritório pelos três especialistas e pelo ensemble, calcula o
  valor capitalizado a partir de uma renda informada e aplica a **triagem** proposta no artigo
  (desvio do cap rate observado acima de 2 × RMSE), com alerta de extrapolação.

**Rodar localmente** (Python 3.10 ou superior):

```bash
git clone https://github.com/abenvenho/caprate-upav2026.git
cd caprate-upav2026
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

**Publicar gratuitamente** no [Streamlit Community Cloud](https://share.streamlit.io): *Create app* →
repositório `abenvenho/caprate-upav2026`, branch `main`, arquivo `app/streamlit_app.py`.

## Reproduzir o estudo

```bash
pip install -r requirements.txt
python code/01_reproduzir_artigo.py     # cerca de 15 s
python code/02_robustez.py              # cerca de 3 min
python code/03_figuras.py
```

A MLP é sensível à versão do scikit-learn. A reprodução exata da Tabela 4 foi obtida com as versões de
`code/requirements-verificacao.txt` (scikit-learn 1.9.1); com outras versões, os resultados da MLP e do
ensemble podem variar na segunda casa decimal.

## Dados: origem e limitações

- **Origem.** Observações de mercado de escritórios corporativos em São Paulo compiladas pelos autores,
  de 2022 a 2026, com geocodificação dos endereços (latitude e longitude), índice fiscal do terreno e
  distâncias a eixos de referência.
- **Regiões.** `Regiao_final` resulta da reclassificação geoespacial por polígonos desenhados pelo
  avaliador (GeoPandas, EPSG:4326), com os imóveis fora dos polígonos atribuídos ao mais próximo. Os
  scripts incorporam "Pinheiros" (2 observações) a "Jardins", obtendo as 11 regiões do artigo.
- **Variável dependente.** `Taxa a.a (%)` está em forma decimal (0,07 = 7% a.a.); os scripts a
  multiplicam por 100.
- **Concentração temporal.** 166 das 247 observações são de 2026; não há observações de 2023.
- **Agrupamento.** 182 edifícios (coordenadas distintas), 40 deles com duas ou mais unidades; o artigo
  reporta ICC ≈ 0,41 entre endereços.
- **Variáveis ausentes.** Vacância, prazo e condições contratuais e qualidade do locatário não estão
  disponíveis — principal limite do poder explicativo.
- Latitude, longitude, índice fiscal e distâncias foram testados no artigo e descartados por piorarem o
  desempenho; permanecem na base para outros estudos.

## Licenças

| Conteúdo | Licença |
|---|---|
| Código (`code/`, `app/`) | [Apache License 2.0](LICENSE) |
| Dados, resultados e figuras (`data/`, `results/`, `figures/`) | [CC BY 4.0](LICENSE-CC-BY-4.0) |
| Artigo e apresentação (`paper/`, `presentation/`) | [CC BY 4.0](LICENSE-CC-BY-4.0) |

Ambas permitem uso livre, inclusive comercial, com atribuição. Veja também [`NOTICE`](NOTICE).

## Como citar

> BENVENHO, A. C.; GATTO, O. A. Análise de taxas de rentabilidade no mercado imobiliário empregando
> aprendizagem de máquina e combinação de especialistas. In: XL Congresso Panamericano de Avaliação —
> UPAV 2026, Madri, 2026.

Metadados de citação em [`CITATION.cff`](CITATION.cff) (o GitHub oferece "Cite this repository" no
menu lateral).

## Autores

**Agnaldo Calvi Benvenho** — Engenheiro mecânico (POLI-USP), mestre em Engenharia de Avaliações
(Universidad Politécnica de Valencia), BP Avaliações e Perícias, IBAPE.
**Osório Accioly Gatto** — IBAPE.

Ver também o estudo apresentado no mesmo congresso:
[KAN + Regressão Simbólica na avaliação de imóveis](https://github.com/abenvenho/kan-sr-upav2026).
