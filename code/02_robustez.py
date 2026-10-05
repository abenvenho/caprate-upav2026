# SPDX-License-Identifier: Apache-2.0
"""
Verificações de robustez recomendadas no artigo (Seção 7.3) e não executadas nele.

1. Validação aninhada: o integrador é ajustado, em cada fold externo, sobre previsões
   OOF internas da amostra de treino e avaliado no fold externo. Na Tabela 4 o
   integrador é ajustado e avaliado sobre as mesmas 247 previsões OOF, o que é
   ligeiramente otimista.
2. Sementes: repete a validação aninhada com as sementes 42, 0, 7 e 123.
3. GroupKFold por edifício: impede que unidades do mesmo edifício (ICC ≈ 0,41)
   fiquem ao mesmo tempo em treino e teste. O edifício é identificado pelas coordenadas
   geocodificadas, que unem grafias diferentes do mesmo endereço ("Av."/"Avenida").

Saída: results/robustez.csv
Uso:   python code/02_robustez.py      (cerca de 2 a 4 minutos)
"""
import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, cross_val_predict

import caprate as C

warnings.filterwarnings("ignore")

d = C.carregar_base()
y = d["cap_rate"].to_numpy()
X = C.matriz_X(d, C.regioes(d), C.anos(d)).to_numpy()
edificio = d[["Latitude", "Longitude"]].round(5).astype(str).agg(",".join, axis=1).factorize()[0]


def aninhado(divisoes) -> np.ndarray:
    """Retorna matriz n × 4 (Ridge, Árvore, MLP, Ensemble) de previsões fora da amostra."""
    P = np.zeros((len(y), 4))
    for tr, te in divisoes:
        M_in = np.column_stack([cross_val_predict(m, X[tr], y[tr], cv=C.kfold())
                                for m in C.especialistas().values()])
        meta = C.integrador().fit(M_in, y[tr])
        M_te = np.column_stack([m.fit(X[tr], y[tr]).predict(X[te]) for m in C.especialistas().values()])
        P[te, :3] = M_te
        P[te, 3] = meta.predict(M_te)
    return P


linhas = []
for seed in (42, 0, 7, 123):
    P = aninhado(C.kfold(seed).split(X))
    for i, nome in enumerate(C.ESPECIALISTAS + ["Ensemble"]):
        linhas.append({"esquema": f"KFold aninhado, seed {seed}", "modelo": nome, **C.metricas(y, P[:, i])})
    print(f"seed {seed} concluída")
P = aninhado(GroupKFold(n_splits=5).split(X, y, edificio))
for i, nome in enumerate(C.ESPECIALISTAS + ["Ensemble"]):
    linhas.append({"esquema": f"GroupKFold por edifício ({edificio.max() + 1} edifícios)", "modelo": nome,
                   **C.metricas(y, P[:, i])})

R = pd.DataFrame(linhas)
R.to_csv(C.ROOT / "results" / "robustez.csv", index=False, float_format="%.4f")
pd.set_option("display.width", 140)
print(R.round(4).to_string(index=False))
media = R[R["esquema"].str.startswith("KFold")].groupby("modelo")[["RMSE (p.p.)", "R²"]].mean()
print("\nMédia das 4 sementes (KFold aninhado):\n", media.round(4))
