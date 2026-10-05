# SPDX-License-Identifier: Apache-2.0
"""
Funções comuns do estudo "Análise de taxas de rentabilidade no mercado imobiliário
empregando aprendizagem de máquina e combinação de especialistas" (UPAV 2026).

Especificação (artigo, Seções 3 a 5):
  * y  = cap rate anual em pontos percentuais (Taxa a.a. × 100), sem transformação;
  * X  = 16 variáveis: Área, Padrão, Estado (contínuas) + 10 dummies de região
         (referência: Barra Funda) + 3 dummies de ano (referência: 2022);
  * região = Regiao_final da reclassificação geoespacial, com "Pinheiros" (2 obs.)
         incorporada a "Jardins" -> 11 regiões (Tabela 3 do artigo);
  * especialistas: Ridge (RidgeCV, α ∈ logspace(-3, 4, 50), cv = 5),
         árvore (profundidade 5, folha mínima 10), MLP (64, 32);
         todas as variáveis padronizadas pelo escore z dentro de cada fold;
  * validação: KFold(5, shuffle, seed 42), previsões out-of-fold (OOF);
  * integrador: RidgeCV (mesma grade, cv = 5) ajustado sobre a matriz OOF (n × 3).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "base_caprate_escritorios_sp_n247.csv"

SEED = 42
ALPHAS = np.logspace(-3, 4, 50)
CONTINUAS = ["Área (m²)", "Padrão", "Estado"]
REGIAO_REF = "Barra Funda"
ANO_REF = 2022
ESPECIALISTAS = ["Ridge", "Árvore", "MLP"]


def carregar_base() -> pd.DataFrame:
    d = pd.read_csv(BASE)
    d["Regiao"] = d["Regiao_final"].replace({"Pinheiros": "Jardins"})
    d["cap_rate"] = d["Taxa a.a (%)"] * 100.0
    return d


def regioes(d: pd.DataFrame) -> list[str]:
    return sorted(r for r in d["Regiao"].unique() if r != REGIAO_REF)


def anos(d: pd.DataFrame) -> list[int]:
    return sorted(a for a in d["DATA"].unique() if a != ANO_REF)


def matriz_X(d: pd.DataFrame, lista_regioes: list[str], lista_anos: list[int]) -> pd.DataFrame:
    """Monta as 16 variáveis explicativas (funciona também para um único imóvel)."""
    X = d[CONTINUAS].astype(float).copy()
    for r in lista_regioes:
        X[f"Região: {r}"] = (d["Regiao"] == r).astype(float)
    for a in lista_anos:
        X[f"Ano: {a}"] = (d["DATA"] == a).astype(float)
    return X


def especialistas() -> dict:
    return {
        "Ridge": make_pipeline(StandardScaler(), RidgeCV(alphas=ALPHAS, cv=5)),
        "Árvore": make_pipeline(StandardScaler(),
                                DecisionTreeRegressor(max_depth=5, min_samples_leaf=10, random_state=SEED)),
        "MLP": make_pipeline(StandardScaler(),
                             MLPRegressor(hidden_layer_sizes=(64, 32), activation="relu", solver="adam",
                                          alpha=1e-4, early_stopping=True, n_iter_no_change=30,
                                          validation_fraction=0.1, max_iter=2000, random_state=SEED)),
    }


def integrador() -> RidgeCV:
    return RidgeCV(alphas=ALPHAS, cv=5)


def oof(X: np.ndarray, y: np.ndarray, cv) -> np.ndarray:
    """Previsões out-of-fold dos três especialistas (matriz n × 3)."""
    return np.column_stack([cross_val_predict(m, X, y, cv=cv) for m in especialistas().values()])


def kfold(seed: int = SEED) -> KFold:
    return KFold(n_splits=5, shuffle=True, random_state=seed)


def metricas(y: np.ndarray, p: np.ndarray) -> dict:
    import dcor
    r = p - y
    return {
        "RMSE (p.p.)": float(np.sqrt(np.mean(r**2))),
        "MAE (p.p.)": float(np.mean(np.abs(r))),
        "R²": float(1 - np.sum(r**2) / np.sum((y - y.mean()) ** 2)),
        "dCor": float(dcor.distance_correlation(y, p)),
    }
