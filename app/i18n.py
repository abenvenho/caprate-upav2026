# SPDX-License-Identifier: Apache-2.0
"""Textos da interface em português, espanhol e inglês."""

IDIOMAS = {"Português": "pt", "Español": "es", "English": "en"}

T = {
    "titulo": {
        "pt": "Cap rates de escritórios por combinação de especialistas",
        "es": "Cap rates de oficinas por combinación de expertos",
        "en": "Office cap rates by combination of experts",
    },
    "subtitulo": {
        "pt": "247 escritórios corporativos · 11 regiões de São Paulo · 2022–2026 · Congresso UPAV 2026, Madri",
        "es": "247 oficinas corporativas · 11 regiones de São Paulo · 2022–2026 · Congreso UPAV 2026, Madrid",
        "en": "247 corporate offices · 11 São Paulo submarkets · 2022–2026 · UPAV 2026 Congress, Madrid",
    },
    "autores": {
        "pt": "Agnaldo Calvi Benvenho · Osório Accioly Gatto",
        "es": "Agnaldo Calvi Benvenho · Osório Accioly Gatto",
        "en": "Agnaldo Calvi Benvenho · Osório Accioly Gatto",
    },
    "abas": {
        "pt": ["Sobre o estudo", "Base de dados", "Desempenho", "Determinantes", "Simulador"],
        "es": ["Sobre el estudio", "Base de datos", "Desempeño", "Determinantes", "Simulador"],
        "en": ["About the study", "Dataset", "Performance", "Drivers", "Simulator"],
    },
    "rodape": {
        "pt": "Código: Apache 2.0 · Dados, artigo e apresentação: CC BY 4.0",
        "es": "Código: Apache 2.0 · Datos, artículo y presentación: CC BY 4.0",
        "en": "Code: Apache 2.0 · Data, paper and slides: CC BY 4.0",
    },
    "sobre_md": {
        "pt": """
**Pergunta.** O cap rate — renda operacional líquida anual ÷ valor do imóvel — converte renda em valor
no método da capitalização. Pequenas diferenças de taxa movem muito o valor: a mesma renda capitalizada
a 6% ou a 10% a.a. resulta em valores 40% diferentes. Combinar modelos de aprendizado de máquina melhora
a estimativa do cap rate de escritórios?

**Método.** Três especialistas com funções complementares — **regressão Ridge** (tendência média,
coeficientes interpretáveis), **árvore de regressão rasa** (regras condicionais) e **rede neural MLP**
pequena (relações não lineares) — combinados por **stacking**: um integrador Ridge aprende quanto pesar
cada um a partir das previsões fora do treino. Variáveis: área útil, padrão construtivo (IUP/IBAPE-SP),
estado de conservação (Ross-Heidecke), região (11 submercados) e ano. Validação cruzada 5-fold.

**Resultado.** O ensemble obteve RMSE = 2,39 p.p. e R² = 0,263, melhor que cada especialista isolado.
Os principais determinantes são a localização em Vila Olímpia, o padrão construtivo, a área e o estado
de conservação. O R² moderado é em boa parte estrutural: vacância, prazo e qualidade do locatário não
estão nos dados. Por isso o modelo serve sobretudo como **triagem** — desvios acima de cerca de duas
vezes o RMSE sinalizam um ativo cuja taxa é explicada por fatores que o avaliador deve investigar.

**Este aplicativo** recalcula todos os modelos a partir da base publicada e reproduz a Tabela 4 do
artigo. A aba *Desempenho* mostra também as verificações de robustez recomendadas no artigo.
""",
        "es": """
**Pregunta.** El cap rate —renta operativa neta anual ÷ valor del inmueble— convierte renta en valor en
el método de capitalización. Pequeñas diferencias de tasa mueven mucho el valor: la misma renta
capitalizada al 6% o al 10% anual da valores un 40% distintos. ¿Combinar modelos de aprendizaje
automático mejora la estimación del cap rate de oficinas?

**Método.** Tres expertos con funciones complementarias —**regresión Ridge** (tendencia media,
coeficientes interpretables), **árbol de regresión superficial** (reglas condicionales) y una **red
neuronal MLP** pequeña (relaciones no lineales)— combinados por **stacking**: un integrador Ridge aprende
cuánto ponderar cada uno a partir de las predicciones fuera del entrenamiento. Variables: área útil,
estándar constructivo (IUP/IBAPE-SP), estado de conservación (Ross-Heidecke), región (11 submercados) y
año. Validación cruzada de 5 pliegues.

**Resultado.** El ensemble obtuvo RMSE = 2,39 p.p. y R² = 0,263, mejor que cada experto aislado. Los
principales determinantes son la ubicación en Vila Olímpia, el estándar constructivo, el área y el
estado de conservación. El R² moderado es en buena parte estructural: vacancia, plazo y calidad del
inquilino no están en los datos. Por eso el modelo sirve sobre todo como **filtro**: desvíos superiores
a unas dos veces el RMSE señalan un activo cuya tasa responde a factores que el valuador debe investigar.

**Esta aplicación** recalcula todos los modelos a partir de la base publicada y reproduce la Tabla 4 del
artículo. La pestaña *Desempeño* muestra también las verificaciones de robustez recomendadas en el artículo.
""",
        "en": """
**Question.** The cap rate — annual net operating income ÷ property value — turns income into value in
the income capitalisation approach. Small rate differences move value a lot: the same income
capitalised at 6% or 10% a year gives values 40% apart. Does combining machine-learning models improve
the estimation of office cap rates?

**Method.** Three experts with complementary roles — **Ridge regression** (average trend, interpretable
coefficients), a **shallow regression tree** (conditional rules) and a small **MLP neural network**
(non-linear relationships) — combined by **stacking**: a Ridge integrator learns how much weight to give
each one from their out-of-fold predictions. Features: floor area, construction standard (IUP/IBAPE-SP),
condition (Ross-Heidecke), submarket (11 regions) and year. 5-fold cross-validation.

**Result.** The ensemble reached RMSE = 2.39 p.p. and R² = 0.263, better than any single expert. The main
drivers are a Vila Olímpia location, construction standard, floor area and condition. The moderate R²
is largely structural: vacancy, lease term and tenant quality are not in the data. The model is
therefore best used as a **screening tool**: deviations above roughly twice the RMSE flag an asset whose
rate is driven by factors the appraiser should investigate.

**This app** refits every model from the published dataset and reproduces Table 4 of the paper. The
*Performance* tab also shows the robustness checks recommended in the paper.
""",
    },
    "materiais": {"pt": "Materiais", "es": "Materiales", "en": "Materials"},
    "materiais_md": {
        "pt": "- [Artigo completo (PDF, em português, resumo trilíngue)]({repo}/blob/main/paper/Artigo_CapRate_UPAV_2026.pdf)\n- [Apresentação — Madri, 2026 (PDF)]({repo}/blob/main/presentation/Apresentacao_CapRate_UPAV_Madrid_2026.pdf)\n- [Repositório com dados e scripts]({repo})",
        "es": "- [Artículo completo (PDF, en portugués, resumen trilingüe)]({repo}/blob/main/paper/Artigo_CapRate_UPAV_2026.pdf)\n- [Presentación — Madrid, 2026 (PDF)]({repo}/blob/main/presentation/Apresentacao_CapRate_UPAV_Madrid_2026.pdf)\n- [Repositorio con datos y scripts]({repo})",
        "en": "- [Full paper (PDF, in Portuguese, trilingual abstract)]({repo}/blob/main/paper/Artigo_CapRate_UPAV_2026.pdf)\n- [Slides — Madrid, 2026 (PDF)]({repo}/blob/main/presentation/Apresentacao_CapRate_UPAV_Madrid_2026.pdf)\n- [Repository with data and scripts]({repo})",
    },
    "rmse_titulo": {"pt": "RMSE out-of-fold (p.p., menor é melhor)", "es": "RMSE fuera de pliegue (p.p., menor es mejor)", "en": "Out-of-fold RMSE (p.p., lower is better)"},
    # base
    "regiao": {"pt": "Região", "es": "Región", "en": "Submarket"},
    "ano": {"pt": "Ano", "es": "Año", "en": "Year"},
    "n_obs": {"pt": "Observações", "es": "Observaciones", "en": "Observations"},
    "mediana": {"pt": "Cap rate mediano", "es": "Cap rate mediano", "en": "Median cap rate"},
    "area_med": {"pt": "Área mediana (m²)", "es": "Área mediana (m²)", "en": "Median area (m²)"},
    "edificios": {"pt": "Endereços distintos", "es": "Direcciones distintas", "en": "Distinct addresses"},
    "mapa": {"pt": "Localização e cap rate (% a.a.)", "es": "Ubicación y cap rate (% anual)", "en": "Location and cap rate (% p.a.)"},
    "box": {"pt": "Cap rate por região (ordenado pela mediana)", "es": "Cap rate por región (ordenado por la mediana)", "en": "Cap rate by submarket (ordered by median)"},
    "baixar": {"pt": "Baixar recorte (CSV)", "es": "Descargar selección (CSV)", "en": "Download selection (CSV)"},
    "dicionario": {"pt": "Dicionário de dados", "es": "Diccionario de datos", "en": "Data dictionary"},
    "tabela": {"pt": "Tabela de observações", "es": "Tabla de observaciones", "en": "Observation table"},
    # desempenho
    "t4": {
        "pt": "Tabela 4 recalculada agora (validação cruzada 5-fold, seed 42, previsões out-of-fold)",
        "es": "Tabla 4 recalculada ahora (validación cruzada de 5 pliegues, semilla 42, predicciones fuera de pliegue)",
        "en": "Table 4 recomputed now (5-fold cross-validation, seed 42, out-of-fold predictions)",
    },
    "pesos": {"pt": "Pesos do integrador", "es": "Pesos del integrador", "en": "Integrator weights"},
    "pesos_nota": {
        "pt": "Pesos obtidos ao reproduzir a Tabela 4. O texto do artigo (Seções 5.1 e 7.1) informa 0,0035 · 0,5144 · 0,4217, valores que não reproduzem a Tabela 4.",
        "es": "Pesos obtenidos al reproducir la Tabla 4. El texto del artículo (Secciones 5.1 y 7.1) informa 0,0035 · 0,5144 · 0,4217, valores que no reproducen la Tabla 4.",
        "en": "Weights obtained when reproducing Table 4. The paper's text (Sections 5.1 and 7.1) reports 0.0035 · 0.5144 · 0.4217, which do not reproduce Table 4.",
    },
    "obs_prev": {"pt": "Observado × previsto (out-of-fold)", "es": "Observado × previsto (fuera de pliegue)", "en": "Observed × predicted (out-of-fold)"},
    "observado": {"pt": "Observado (% a.a.)", "es": "Observado (% anual)", "en": "Observed (% p.a.)"},
    "previsto": {"pt": "Previsto (% a.a.)", "es": "Previsto (% anual)", "en": "Predicted (% p.a.)"},
    "robustez": {"pt": "Verificações de robustez (artigo, Seção 7.3)", "es": "Verificaciones de robustez (artículo, Sección 7.3)", "en": "Robustness checks (paper, Section 7.3)"},
    "robustez_md": {
        "pt": "Na Tabela 4 o integrador é ajustado e avaliado sobre as mesmas previsões. Aqui ele também é validado fora da amostra (**aninhado**), com quatro sementes, e com **GroupKFold por edifício**, identificado pelas coordenadas, que impede que unidades do mesmo prédio fiquem em treino e teste. O ensemble é o melhor modelo na média das sementes e no GroupKFold, mas com erro maior que o da Tabela 4; com a seed 42 a árvore isolada fica à frente.",
        "es": "En la Tabla 4 el integrador se ajusta y evalúa sobre las mismas predicciones. Aquí también se valida fuera de la muestra (**anidado**), con cuatro semillas, y con **GroupKFold por edificio**, identificado por las coordenadas, que impide que unidades del mismo edificio queden en entrenamiento y prueba. El ensemble es el mejor modelo en el promedio de las semillas y en el GroupKFold, pero con un error mayor que el de la Tabla 4; con la semilla 42 el árbol aislado queda adelante.",
        "en": "In Table 4 the integrator is fitted and evaluated on the same predictions. Here it is also validated out of sample (**nested**), with four seeds, and with **GroupKFold by building**, identified by its coordinates, which keeps units of the same building out of both train and test. The ensemble is the best model on the seed average and under GroupKFold, but with a larger error than in Table 4; with seed 42 the single tree comes out ahead.",
    },
    "media_seeds": {"pt": "Média das 4 sementes (KFold aninhado)", "es": "Promedio de las 4 semillas (KFold anidado)", "en": "Average of 4 seeds (nested KFold)"},
    "esquema": {"pt": "Esquema", "es": "Esquema", "en": "Scheme"},
    "modelo": {"pt": "Modelo", "es": "Modelo", "en": "Model"},
    # determinantes
    "imp": {"pt": "Importância por permutação (aumento do RMSE, p.p.)", "es": "Importancia por permutación (aumento del RMSE, p.p.)", "en": "Permutation importance (RMSE increase, p.p.)"},
    "coef": {"pt": "Coeficientes padronizados da Ridge (p.p. por desvio-padrão)", "es": "Coeficientes estandarizados de la Ridge (p.p. por desviación estándar)", "en": "Standardised Ridge coefficients (p.p. per standard deviation)"},
    "arvore": {"pt": "Regras da árvore de regressão (limiares em unidades originais)", "es": "Reglas del árbol de regresión (umbrales en unidades originales)", "en": "Regression-tree rules (thresholds in original units)"},
    "media3": {"pt": "Média dos 3 especialistas", "es": "Promedio de los 3 expertos", "en": "Average of the 3 experts"},
    # simulador
    "sim_intro": {
        "pt": "Informe as características de um escritório. O aplicativo estima o cap rate pelos três especialistas e pelo ensemble (treinados na base completa). Uso didático: não substitui um laudo.",
        "es": "Ingrese las características de una oficina. La aplicación estima el cap rate con los tres expertos y el ensemble (entrenados con la base completa). Uso didáctico: no sustituye un informe de valuación.",
        "en": "Enter the features of an office. The app estimates the cap rate with the three experts and the ensemble (trained on the full dataset). For teaching only: it does not replace an appraisal report.",
    },
    "area": {"pt": "Área útil (m²)", "es": "Área útil (m²)", "en": "Floor area (m²)"},
    "padrao": {"pt": "Padrão construtivo (IUP)", "es": "Estándar constructivo (IUP)", "en": "Construction standard (IUP)"},
    "estado": {"pt": "Estado de conservação (Ross-Heidecke, 0–1)", "es": "Estado de conservación (Ross-Heidecke, 0–1)", "en": "Condition (Ross-Heidecke, 0–1)"},
    "obs_opc": {"pt": "Cap rate observado (% a.a., opcional)", "es": "Cap rate observado (% anual, opcional)", "en": "Observed cap rate (% p.a., optional)"},
    "rol": {"pt": "Renda operacional líquida anual (R$, opcional)", "es": "Renta operativa neta anual (R$, opcional)", "en": "Annual net operating income (R$, optional)"},
    "valor_cap": {"pt": "Valor capitalizado (renda ÷ cap rate do ensemble)", "es": "Valor capitalizado (renta ÷ cap rate del ensemble)", "en": "Capitalised value (income ÷ ensemble cap rate)"},
    "triagem_ok": {
        "pt": "Desvio de {d} p.p. em relação ao ensemble — dentro de 2 × RMSE ({lim} p.p.).",
        "es": "Desvío de {d} p.p. respecto del ensemble — dentro de 2 × RMSE ({lim} p.p.).",
        "en": "Deviation of {d} p.p. from the ensemble — within 2 × RMSE ({lim} p.p.).",
    },
    "triagem_alerta": {
        "pt": "Desvio de {d} p.p. em relação ao ensemble — acima de 2 × RMSE ({lim} p.p.). Pela proposta do artigo, a taxa deste ativo provavelmente é explicada por fatores não observados (vacância, contrato, locatário) que merecem investigação.",
        "es": "Desvío de {d} p.p. respecto del ensemble — superior a 2 × RMSE ({lim} p.p.). Según la propuesta del artículo, la tasa de este activo probablemente responde a factores no observados (vacancia, contrato, inquilino) que merecen investigación.",
        "en": "Deviation of {d} p.p. from the ensemble — above 2 × RMSE ({lim} p.p.). As proposed in the paper, this asset's rate is probably driven by unobserved factors (vacancy, lease, tenant) that deserve investigation.",
    },
    "fora": {
        "pt": "Fora da faixa da amostra: {v}. Os modelos não foram ajustados nessa região.",
        "es": "Fuera del rango de la muestra: {v}. Los modelos no fueron ajustados en esa región.",
        "en": "Outside the sample range: {v}. The models were not fitted in that region.",
    },
    "poucos": {
        "pt": "Atenção: a região {r} tem apenas {n} observações na amostra.",
        "es": "Atención: la región {r} tiene solo {n} observaciones en la muestra.",
        "en": "Note: the {r} submarket has only {n} observations in the sample.",
    },
}
