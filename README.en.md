# Office cap rates by combination of experts

[Português](README.md) · [Español](README.es.md) · **English**

[![Code: Apache 2.0](https://img.shields.io/badge/code-Apache%202.0-blue.svg)](LICENSE)
[![Data and texts: CC BY 4.0](https://img.shields.io/badge/data%20and%20texts-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

Data, code, results, paper, slides and interactive app for the paper

> **Análise de taxas de rentabilidade no mercado imobiliário empregando aprendizagem de máquina e combinação de especialistas**
> (Analysis of real-estate yield rates using machine learning and a combination of experts)
> Agnaldo Calvi Benvenho · Osório Accioly Gatto — 40th Pan-American Valuation Congress, UPAV 2026, Madrid.
> Track: artificial intelligence and new technologies applied to valuation.

---

## What was done

The cap rate — annual net operating income divided by property value — turns income into value in the
income capitalisation approach, sets the terminal value in income-based appraisals and serves as a check
on discount rates. Small rate differences produce large value differences: the same income capitalised at
6% or 10% a year gives values 40% apart.

The study asks whether **combining machine-learning models improves cap rate estimation** for corporate
offices. Three experts with complementary roles are combined by *stacking*:

| Expert | Role | Configuration |
|---|---|---|
| Ridge regression | average trend, interpretable coefficients | α chosen by internal validation (α = 51.8) |
| Shallow regression tree | conditional rules | depth 5, at least 10 observations per leaf |
| MLP neural network | moderate non-linear relationships | two hidden layers (64 → 32), ReLU, early stopping |
| **Integrator** | learns each expert's weight | Ridge over the out-of-fold predictions |

**Data:** 247 observations of corporate offices in São Paulo, Brazil, from 2022 to 2026, in 11 market
submarkets defined by a geospatial reclassification. Features: floor area, construction standard (IUP,
IBAPE/SP), condition (Ross-Heidecke), submarket and year. 5-fold cross-validation (seed 42).

## Main results (Table 4 of the paper)

| Model | RMSE (p.p.) | MAE (p.p.) | R² | dCor |
|---|---:|---:|---:|---:|
| Ridge | 2.5266 | 1.8745 | 0.1786 | 0.4615 |
| Regression tree | 2.4241 | 1.7878 | 0.2439 | 0.5131 |
| MLP | 2.5907 | 1.9572 | 0.1364 | 0.4322 |
| **Stacking ensemble** | **2.3933** | **1.7836** | **0.2630** | **0.5214** |

The main drivers, consistent across the three experts, are a **Vila Olímpia** location (permutation
importance 0.369), **construction standard** (0.271), **floor area** (0.163) and **condition** (0.127).

## Conclusions

- The combination of experts outperformed every single model. To the authors' knowledge, it is the first
  application in Brazil of machine learning to cap rate estimation for commercial real estate.
- **Distance correlation** revealed non-linear associations that linear measures understate — for
  example, construction standard with dCor = 0.375 against |ρ| = 0.28 (Spearman) — which supports the use
  of non-linear experts.
- The moderate R² (about 74% of the variance unexplained) is largely **structural**: vacancy, remaining
  lease term, indexation and tenant quality are not in the data and can, on their own, move the cap rate of
  physically identical assets by 2 to 4 p.p.
- The model is therefore best used as a **screening tool**: a gap between observed and predicted cap rate
  above roughly 2 × RMSE (≈ 4.8 p.p.) flags an asset whose rate is driven by uncaptured factors that the
  appraiser should investigate. The model supports professional judgement rather than replacing it.

## Reproducibility and robustness

The whole paper was recomputed from the published dataset (`code/01_reproduzir_artigo.py`):

| Paper item | Published | Recomputed |
|---|---|---|
| Table 4: 3 experts and ensemble, 4 metrics | see above | **identical** (4 decimal places) |
| Ridge α and standardised coefficients | 51.8; +0.558 / −0.418 / +0.373 / −0.351 | **identical** |
| Tree: leaves, first split, highest leaf | 12; Standard ≤ 4.03; 11.48% | **identical** |
| Permutation importance (top 4) | 0.369 / 0.271 / 0.163 / 0.127 | **identical** |
| Tables 1 and 3; ANOVA F | — ; 5.81 | identical; 5.81 |
| Kruskal-Wallis H; region dCor; Jardins s.d. | 51.51; 0.354; 1.27 | 51.49; 0.355; 1.33 |
| **Integrator weights** (Sections 5.1 and 7.1) | 0.0035 / 0.5144 / 0.4217 | **0.1788 / 0.6411 / 0.1417** |

**Integrator weights.** The fit that reproduces Table 4 exactly gives Ridge, tree and MLP weights of
0.18, 0.64 and 0.14 (intercept 0.32). Applied to the same predictions, the weights printed in the paper
cannot reach the 2.3933 RMSE (the best they can do is 2.41). The reading that the prediction rests mostly
on the tree still holds; the reading that Ridge has near-zero weight and the MLP ≈ 0.42 does not.

**Robustness** (`code/02_robustez.py`, checks recommended in Section 7.3 of the paper). In Table 4 the
integrator is fitted and evaluated on the same 247 predictions, which is slightly optimistic. With the
integrator also validated out of sample (**nested** validation), across four seeds, and with **GroupKFold
by building** (182 buildings identified by their coordinates, so that units of the same building are never
in both train and test):

| Scheme | Ridge | Tree | MLP | Ensemble |
|---|---:|---:|---:|---:|
| Table 4 (seed 42) | 2.527 | 2.424 | 2.591 | **2.393** |
| Nested, average of 4 seeds | 2.495 | 2.503 | 2.531 | **2.445** |
| Nested, seed 42 | 2.527 | **2.424** | 2.591 | 2.490 |
| GroupKFold by building | 2.514 | 2.615 | 2.582 | **2.497** |

RMSE in p.p. The ensemble is the best model on the seed average and under GroupKFold — the paper's central
conclusion holds — but with an error of 2.45 to 2.50 p.p. instead of 2.39 p.p. (R² of 0.20 to 0.23). With
the seed-42 split, the single tree comes out ahead of the ensemble when the latter is validated in nested
fashion.

## Repository contents

```
paper/          Full paper (PDF, in Portuguese, with abstracts in Portuguese, Spanish and English)
presentation/   UPAV 2026 Congress slides, Madrid (PDF and PPTX)
data/
  base_caprate_escritorios_sp_n247.csv   247 × 22 — full dataset (UTF-8, comma-separated)
  data_dictionary.csv                    description, use in the paper, type and range (in Portuguese)
code/
  caprate.py                 shared specification (features, experts, validation, metrics)
  01_reproduzir_artigo.py    Tables 1 to 4, tests, weights, coefficients, tree, importance
  02_robustez.py             nested validation, several seeds and GroupKFold by building
  03_figuras.py              result figures
results/        Script outputs (CSV, JSON and TXT), including the out-of-fold predictions
figures/        Predicted × observed, residuals, permutation importance, Ridge coefficients
app/            Streamlit app
```

## Interactive app

The app refits every model from the published dataset, in Portuguese, Spanish and English:

- **About the study**: summary and performance comparison;
- **Dataset**: map of the 247 observations, cap rate by submarket, filters and download;
- **Performance**: recomputed Table 4, integrator weights, observed × predicted and robustness;
- **Drivers**: permutation importance, Ridge coefficients and tree rules;
- **Simulator**: estimates an office's cap rate with the three experts and the ensemble, computes the
  capitalised value from an income you enter and applies the **screening rule** proposed in the paper
  (observed cap rate deviating by more than 2 × RMSE), with an extrapolation warning.

**Run locally** (Python 3.10 or later):

```bash
git clone https://github.com/abenvenho/caprate-upav2026.git
cd caprate-upav2026
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

**Publish for free** on [Streamlit Community Cloud](https://share.streamlit.io): *Create app* →
repository `abenvenho/caprate-upav2026`, branch `main`, file `app/streamlit_app.py`.

## Reproducing the study

```bash
pip install -r requirements.txt
python code/01_reproduzir_artigo.py     # about 15 s
python code/02_robustez.py              # about 3 min
python code/03_figuras.py
```

The MLP is sensitive to the scikit-learn version. Table 4 was reproduced exactly with the versions in
`code/requirements-verificacao.txt` (scikit-learn 1.9.1); with other versions the MLP and ensemble
results may differ in the second decimal place. Script comments and messages are in Portuguese.

## Data: provenance and limitations

- **Provenance.** Market observations of corporate offices in São Paulo compiled by the authors, 2022 to
  2026, with geocoded addresses (latitude and longitude), municipal land value index and distances to
  reference axes.
- **Submarkets.** `Regiao_final` comes from a geospatial reclassification with polygons drawn by the
  appraiser (GeoPandas, EPSG:4326); properties outside the polygons are assigned to the nearest one. The
  scripts merge "Pinheiros" (2 observations) into "Jardins", giving the paper's 11 submarkets.
- **Target.** `Taxa a.a (%)` is in decimal form (0.07 = 7% p.a.); the scripts multiply it by 100.
- **Time concentration.** 166 of the 247 observations are from 2026; there are none from 2023.
- **Clustering.** 182 buildings (distinct coordinates), 40 of them with two or more units; the paper
  reports ICC ≈ 0.41 across addresses.
- **Missing variables.** Vacancy, lease terms and tenant quality are not available — the main limit on
  explanatory power.
- Latitude, longitude, land value index and distances were tested in the paper and dropped because they
  worsened performance; they remain in the dataset for other studies.

## Licences

| Content | Licence |
|---|---|
| Code (`code/`, `app/`) | [Apache License 2.0](LICENSE) |
| Data, results and figures (`data/`, `results/`, `figures/`) | [CC BY 4.0](LICENSE-CC-BY-4.0) |
| Paper and slides (`paper/`, `presentation/`) | [CC BY 4.0](LICENSE-CC-BY-4.0) |

Both allow free use, including commercial use, with attribution. See also [`NOTICE`](NOTICE).

## How to cite

> BENVENHO, A. C.; GATTO, O. A. Análise de taxas de rentabilidade no mercado imobiliário empregando
> aprendizagem de máquina e combinação de especialistas. In: XL Congreso Panamericano de Valuación —
> UPAV 2026, Madrid, 2026.

Citation metadata in [`CITATION.cff`](CITATION.cff) (GitHub shows "Cite this repository" in the sidebar).

## Authors

**Agnaldo Calvi Benvenho**: mechanical engineer (POLI-USP), MSc in Appraisal Engineering (Universidad
Politécnica de Valencia), BP Avaliações e Perícias, IBAPE.
**Osório Accioly Gatto**: IBAPE.

See also the study presented at the same congress:
[KAN + Symbolic Regression for real-estate appraisal](https://github.com/abenvenho/kan-sr-upav2026).
