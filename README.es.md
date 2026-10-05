# Cap rates de oficinas por combinación de expertos

[Português](README.md) · **Español** · [English](README.en.md)

[![Código: Apache 2.0](https://img.shields.io/badge/c%C3%B3digo-Apache%202.0-blue.svg)](LICENSE)
[![Datos y textos: CC BY 4.0](https://img.shields.io/badge/datos%20y%20textos-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

Datos, código, resultados, artículo, presentación y aplicación interactiva del trabajo

> **Análise de taxas de rentabilidade no mercado imobiliário empregando aprendizagem de máquina e combinação de especialistas**
> (Análisis de tasas de rentabilidad en el mercado inmobiliario mediante aprendizaje automático y combinación de expertos)
> Agnaldo Calvi Benvenho · Osório Accioly Gatto — XL Congreso Panamericano de Valuación, UPAV 2026, Madrid.
> Eje temático: inteligencia artificial y nuevas tecnologías aplicadas a la valuación.

---

## Qué se hizo

El cap rate —renta operativa neta anual dividida por el valor del inmueble— convierte renta en valor en el
método de capitalización, define la perpetuidad en las valuaciones por la renta y sirve para criticar las
tasas de descuento. Pequeñas diferencias de tasa producen grandes diferencias de valor: la misma renta
capitalizada al 6% o al 10% anual da valores un 40% distintos.

El estudio pregunta si **combinar modelos de aprendizaje automático mejora la estimación del cap rate** de
oficinas corporativas. Tres expertos con funciones complementarias se combinan por *stacking*:

| Experto | Función | Configuración |
|---|---|---|
| Regresión Ridge | tendencia media, coeficientes interpretables | α elegido por validación interna (α = 51,8) |
| Árbol de regresión superficial | reglas condicionales | profundidad 5, mínimo de 10 observaciones por hoja |
| Red neuronal MLP | relaciones no lineales moderadas | dos capas ocultas (64 → 32), ReLU, *early stopping* |
| **Integrador** | aprende el peso de cada experto | Ridge sobre las predicciones fuera del entrenamiento |

**Datos:** 247 observaciones de oficinas corporativas en São Paulo (Brasil), de 2022 a 2026, en 11 regiones
de mercado definidas por reclasificación geoespacial. Variables: área útil, estándar constructivo (IUP,
IBAPE/SP), estado de conservación (Ross-Heidecke), región y año. Validación cruzada de 5 pliegues
(semilla 42).

## Principales resultados (Tabla 4 del artículo)

| Modelo | RMSE (p.p.) | MAE (p.p.) | R² | dCor |
|---|---:|---:|---:|---:|
| Ridge | 2,5266 | 1,8745 | 0,1786 | 0,4615 |
| Árbol de regresión | 2,4241 | 1,7878 | 0,2439 | 0,5131 |
| MLP | 2,5907 | 1,9572 | 0,1364 | 0,4322 |
| **Ensemble stacking** | **2,3933** | **1,7836** | **0,2630** | **0,5214** |

Los principales determinantes, coherentes entre los tres expertos, son la ubicación en **Vila Olímpia**
(importancia por permutación 0,369), el **estándar constructivo** (0,271), el **área útil** (0,163) y el
**estado de conservación** (0,127).

## Conclusiones

- La combinación de expertos superó a cada modelo aislado. Es, hasta donde los autores pudieron
  averiguar, la primera aplicación en Brasil del aprendizaje automático a la estimación de cap rates de
  inmuebles comerciales.
- La **correlación de distancias** (dCor) reveló asociaciones no lineales que las medidas lineales
  subestiman —por ejemplo, estándar constructivo con dCor = 0,375 frente a |ρ| = 0,28 (Spearman)—, lo que
  fundamenta el uso de expertos no lineales.
- El R² moderado (cerca del 74% de la varianza sin explicar) es en buena parte **estructural**: vacancia,
  plazo remanente de arrendamiento, indexador y calidad del inquilino no están en los datos y pueden, por
  sí solos, separar en 2 a 4 p.p. el cap rate de activos físicamente idénticos.
- Por eso el modelo es útil sobre todo como **herramienta de filtro**: un desvío entre el cap rate
  observado y el previsto superior a unas 2 × RMSE (≈ 4,8 p.p.) señala un activo cuya tasa responde a
  factores no capturados, que el valuador debe investigar. El modelo apoya —y no sustituye— el juicio
  profesional.

## Reproducibilidad y robustez

Todo el artículo se recalculó a partir de la base publicada (`code/01_reproduzir_artigo.py`):

| Elemento del artículo | Publicado | Recalculado |
|---|---|---|
| Tabla 4: 3 expertos y ensemble, 4 métricas | ver arriba | **idéntico** (4 decimales) |
| α de la Ridge y coeficientes estandarizados | 51,8; +0,558 / −0,418 / +0,373 / −0,351 | **idéntico** |
| Árbol: hojas, 1.er corte, hoja de mayor valor | 12; Estándar ≤ 4,03; 11,48% | **idéntico** |
| Importancia por permutación (top 4) | 0,369 / 0,271 / 0,163 / 0,127 | **idéntico** |
| Tablas 1 y 3; ANOVA F | — ; 5,81 | idéntico; 5,81 |
| Kruskal-Wallis H; dCor de la región; D.E. de Jardins | 51,51; 0,354; 1,27 | 51,49; 0,355; 1,33 |
| **Pesos del integrador** (Secciones 5.1 y 7.1) | 0,0035 / 0,5144 / 0,4217 | **0,1788 / 0,6411 / 0,1417** |

**Pesos del integrador.** El ajuste que reproduce exactamente la Tabla 4 asigna a la Ridge, al árbol y a
la MLP los pesos 0,18, 0,64 y 0,14 (intercepto 0,32). Aplicados a las mismas predicciones, los pesos
impresos en el artículo no alcanzan el RMSE de 2,3933 (lo mejor posible con ellos es 2,41). La lectura de
que la predicción se apoya sobre todo en el árbol se mantiene; la de que la Ridge tiene peso prácticamente
nulo y la MLP ≈ 0,42, no.

**Robustez** (`code/02_robustez.py`, verificaciones recomendadas en la Sección 7.3 del artículo). En la
Tabla 4 el integrador se ajusta y evalúa sobre las mismas 247 predicciones, lo que es ligeramente
optimista. Con el integrador también validado fuera de la muestra (validación **anidada**), en cuatro
semillas, y con **GroupKFold por edificio** (182 edificios identificados por las coordenadas, para que
unidades del mismo edificio no queden en entrenamiento y prueba):

| Esquema | Ridge | Árbol | MLP | Ensemble |
|---|---:|---:|---:|---:|
| Tabla 4 (semilla 42) | 2,527 | 2,424 | 2,591 | **2,393** |
| Anidado, promedio de 4 semillas | 2,495 | 2,503 | 2,531 | **2,445** |
| Anidado, semilla 42 | 2,527 | **2,424** | 2,591 | 2,490 |
| GroupKFold por edificio | 2,514 | 2,615 | 2,582 | **2,497** |

RMSE en p.p. El ensemble es el mejor modelo en el promedio de las semillas y en el GroupKFold —la
conclusión central del artículo se mantiene—, pero con un error de 2,45 a 2,50 p.p. en lugar de 2,39 p.p.
(R² de 0,20 a 0,23). Con la partición de la semilla 42, el árbol aislado queda por delante del ensemble
cuando este se valida de forma anidada.

## Contenido del repositorio

```
paper/          Artículo completo (PDF, en portugués, con resumen en portugués, español e inglés)
presentation/   Presentación del Congreso UPAV 2026, Madrid (PDF y PPTX)
data/
  base_caprate_escritorios_sp_n247.csv   247 × 22 — base completa (UTF-8, separada por comas)
  data_dictionary.csv                    descripción, uso en el artículo, tipo y rango (en portugués)
code/
  caprate.py                 especificación común (variables, expertos, validación, métricas)
  01_reproduzir_artigo.py    Tablas 1 a 4, pruebas, pesos, coeficientes, árbol, importancia
  02_robustez.py             validación anidada, varias semillas y GroupKFold por edificio
  03_figuras.py              figuras de resultados
results/        Salidas de los scripts (CSV, JSON y TXT), incluidas las predicciones fuera de pliegue
figures/        Previsto × observado, residuos, importancia por permutación, coeficientes de la Ridge
app/            Aplicación Streamlit
```

## Aplicación interactiva

La aplicación recalcula todos los modelos a partir de la base publicada, en portugués, español e inglés:

- **Sobre el estudio**: resumen y comparación de desempeño;
- **Base de datos**: mapa de las 247 observaciones, cap rate por región, filtros y descarga;
- **Desempeño**: Tabla 4 recalculada, pesos del integrador, observado × previsto y robustez;
- **Determinantes**: importancia por permutación, coeficientes de la Ridge y reglas del árbol;
- **Simulador**: estima el cap rate de una oficina con los tres expertos y el ensemble, calcula el valor
  capitalizado a partir de una renta ingresada y aplica el **filtro** propuesto en el artículo (desvío del
  cap rate observado superior a 2 × RMSE), con aviso de extrapolación.

**Ejecutar localmente** (Python 3.10 o superior):

```bash
git clone https://github.com/abenvenho/caprate-upav2026.git
cd caprate-upav2026
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

**Publicar gratis** en [Streamlit Community Cloud](https://share.streamlit.io): *Create app* →
repositorio `abenvenho/caprate-upav2026`, rama `main`, archivo `app/streamlit_app.py`.

## Reproducir el estudio

```bash
pip install -r requirements.txt
python code/01_reproduzir_artigo.py     # unos 15 s
python code/02_robustez.py              # unos 3 min
python code/03_figuras.py
```

La MLP es sensible a la versión de scikit-learn. La reproducción exacta de la Tabla 4 se obtuvo con las
versiones de `code/requirements-verificacao.txt` (scikit-learn 1.9.1); con otras versiones, los resultados
de la MLP y del ensemble pueden variar en el segundo decimal. Los scripts y sus mensajes están en portugués.

## Datos: origen y limitaciones

- **Origen.** Observaciones de mercado de oficinas corporativas en São Paulo compiladas por los autores,
  de 2022 a 2026, con geocodificación de las direcciones (latitud y longitud), índice fiscal del terreno y
  distancias a ejes de referencia.
- **Regiones.** `Regiao_final` resulta de la reclasificación geoespacial con polígonos dibujados por el
  valuador (GeoPandas, EPSG:4326); los inmuebles fuera de los polígonos se asignan al más cercano. Los
  scripts incorporan "Pinheiros" (2 observaciones) a "Jardins", con lo que se obtienen las 11 regiones del
  artículo.
- **Variable dependiente.** `Taxa a.a (%)` está en forma decimal (0,07 = 7% anual); los scripts la
  multiplican por 100.
- **Concentración temporal.** 166 de las 247 observaciones son de 2026; no hay observaciones de 2023.
- **Agrupamiento.** 182 edificios (coordenadas distintas), 40 de ellos con dos o más unidades; el
  artículo informa ICC ≈ 0,41 entre direcciones.
- **Variables ausentes.** Vacancia, plazo y condiciones contractuales y calidad del inquilino no están
  disponibles; son el principal límite del poder explicativo.
- Latitud, longitud, índice fiscal y distancias se probaron en el artículo y se descartaron porque
  empeoraban el desempeño; permanecen en la base para otros estudios.

## Licencias

| Contenido | Licencia |
|---|---|
| Código (`code/`, `app/`) | [Apache License 2.0](LICENSE) |
| Datos, resultados y figuras (`data/`, `results/`, `figures/`) | [CC BY 4.0](LICENSE-CC-BY-4.0) |
| Artículo y presentación (`paper/`, `presentation/`) | [CC BY 4.0](LICENSE-CC-BY-4.0) |

Ambas permiten el uso libre, incluso comercial, con atribución. Véase también [`NOTICE`](NOTICE).

## Cómo citar

> BENVENHO, A. C.; GATTO, O. A. Análise de taxas de rentabilidade no mercado imobiliário empregando
> aprendizagem de máquina e combinação de especialistas. En: XL Congreso Panamericano de Valuación —
> UPAV 2026, Madrid, 2026.

Metadatos de citación en [`CITATION.cff`](CITATION.cff) (GitHub ofrece "Cite this repository" en el menú
lateral).

## Autores

**Agnaldo Calvi Benvenho**: ingeniero mecánico (POLI-USP), máster en Ingeniería de Valuaciones
(Universidad Politécnica de Valencia), BP Avaliações e Perícias, IBAPE.
**Osório Accioly Gatto**: IBAPE.

Véase también el estudio presentado en el mismo congreso:
[KAN + Regresión Simbólica en la valuación de inmuebles](https://github.com/abenvenho/kan-sr-upav2026).
