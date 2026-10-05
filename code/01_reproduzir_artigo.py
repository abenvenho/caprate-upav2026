# SPDX-License-Identifier: Apache-2.0
"""
Reproduz os resultados numéricos do artigo a partir da base publicada:

  Tabela 1  estatísticas descritivas            -> results/tabela1_descritivas.csv
  Tabela 2  dCor marginal de cada variável       -> results/tabela2_dcor_marginal.csv
  Tabela 3  cap rate por região                  -> results/tabela3_regioes.csv
  Seção 6.1 ANOVA e Kruskal-Wallis entre regiões -> results/testes_regioes.json
  Tabela 4  desempenho OOF dos especialistas e do ensemble -> results/tabela4_desempenho.csv
  Seção 5.1 pesos do integrador                  -> results/integrador_pesos.json
  Seção 5.2 coeficientes padronizados da Ridge   -> results/ridge_coeficientes.csv
  Seção 5.3 regras da árvore                     -> results/arvore_regras.txt
  Seção 6.3 importância por permutação           -> results/importancia_permutacao.csv
  previsões out-of-fold (para gráficos/auditoria)-> results/previsoes_oof.csv

Uso:  python code/01_reproduzir_artigo.py
"""
import json
import warnings

import dcor
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.inspection import permutation_importance
from sklearn.tree import DecisionTreeRegressor, export_text

import caprate as C

warnings.filterwarnings("ignore")
OUT = C.ROOT / "results"
OUT.mkdir(exist_ok=True)

d = C.carregar_base()
y = d["cap_rate"].to_numpy()
REG, ANOS = C.regioes(d), C.anos(d)
Xdf = C.matriz_X(d, REG, ANOS)
X, cols = Xdf.to_numpy(), list(Xdf.columns)
print(f"n = {len(d)} · {len(cols)} variáveis · {d['Regiao'].nunique()} regiões")

# ---------------------------------------------------------------- Tabela 1
t1 = pd.DataFrame({
    "Cap Rate (% a.a.)": d["cap_rate"], "Área (m²)": d["Área (m²)"],
    "Padrão construtivo": d["Padrão"], "Estado de conservação": d["Estado"],
}).agg(["min", "max", "mean", "median", "std"]).T
t1.columns = ["Mín.", "Máx.", "Média", "Mediana", "D.P."]
t1.round(4).to_csv(OUT / "tabela1_descritivas.csv")

# ---------------------------------------------------------------- Tabela 2
onehot = pd.get_dummies(d["Regiao"]).astype(float).to_numpy()
t2 = pd.Series({
    "Área (m²)": dcor.distance_correlation(d["Área (m²)"].to_numpy(float), y),
    "Padrão": dcor.distance_correlation(d["Padrão"].to_numpy(float), y),
    "Estado": dcor.distance_correlation(d["Estado"].to_numpy(float), y),
    "Região (one-hot)": dcor.distance_correlation(onehot, y),
}, name="dCor")
t2.round(4).to_csv(OUT / "tabela2_dcor_marginal.csv")

# ---------------------------------------------------------------- Tabela 3 e testes
t3 = d.groupby("Regiao")["cap_rate"].agg(n="size", Media="mean", Mediana="median", DP="std")
t3 = t3.sort_values("Media", ascending=False)
t3.round(2).to_csv(OUT / "tabela3_regioes.csv")
grupos = [g["cap_rate"].to_numpy() for _, g in d.groupby("Regiao")]
F, pF = stats.f_oneway(*grupos)
H, pH = stats.kruskal(*grupos)
k, n = len(grupos), len(y)
ss_tot = np.sum((y - y.mean()) ** 2)
ss_ent = sum(len(g) * (g.mean() - y.mean()) ** 2 for g in grupos)
testes = {"ANOVA_F": F, "ANOVA_p": pF, "eta2": ss_ent / ss_tot,
          "KruskalWallis_H": H, "KruskalWallis_p": pH, "epsilon2": (H - k + 1) / (n - k)}
(OUT / "testes_regioes.json").write_text(json.dumps({a: round(float(b), 6) for a, b in testes.items()}, indent=2))

# ---------------------------------------------------------------- Tabela 4
cv = C.kfold()
M = C.oof(X, y, cv)
meta = C.integrador().fit(M, y)
p_ens = meta.predict(M)
linhas = [{"Modelo": nome, **C.metricas(y, M[:, i])} for i, nome in enumerate(C.ESPECIALISTAS)]
linhas.append({"Modelo": "Ensemble stacking", **C.metricas(y, p_ens)})
t4 = pd.DataFrame(linhas)
t4.to_csv(OUT / "tabela4_desempenho.csv", index=False, float_format="%.4f")
(OUT / "integrador_pesos.json").write_text(json.dumps({
    "pesos": dict(zip(C.ESPECIALISTAS, np.round(meta.coef_, 4).tolist())),
    "intercepto": round(float(meta.intercept_), 4), "alpha": float(meta.alpha_),
    "nota": "Ajuste RidgeCV sobre as previsões OOF; reproduz exatamente a Tabela 4. "
            "O texto do artigo (Seções 5.1 e 7.1) informa 0,0035 / 0,5144 / 0,4217, "
            "valores que não reproduzem a Tabela 4 (ver README).",
}, ensure_ascii=False, indent=2))
pd.DataFrame({"id": d["id"], "cap_rate_obs": y, "Ridge": M[:, 0], "Árvore": M[:, 1], "MLP": M[:, 2],
              "Ensemble": p_ens}).to_csv(OUT / "previsoes_oof.csv", index=False, float_format="%.6f")

# ---------------------------------------------------------------- modelos na base completa
modelos = C.especialistas()
for m in modelos.values():
    m.fit(X, y)
ridge = modelos["Ridge"][-1]
pd.DataFrame({"variavel": cols, "coef_padronizado": ridge.coef_}) \
    .sort_values("coef_padronizado", key=abs, ascending=False) \
    .to_csv(OUT / "ridge_coeficientes.csv", index=False, float_format="%.4f")
arv = DecisionTreeRegressor(max_depth=5, min_samples_leaf=10, random_state=C.SEED).fit(X, y)  # limiares na escala original
(OUT / "arvore_regras.txt").write_text(
    f"Árvore de regressão — {arv.get_n_leaves()} folhas (limiares em unidades originais; valores em % a.a.)\n\n"
    + export_text(arv, feature_names=cols, decimals=2), encoding="utf-8")

imp = {}
for nome, m in modelos.items():
    r = permutation_importance(m, X, y, scoring="neg_root_mean_squared_error", n_repeats=20, random_state=C.SEED)
    imp[nome] = r.importances_mean
I = pd.DataFrame(imp, index=cols)
I["Média"] = I.mean(axis=1)
I.sort_values("Média", ascending=False).to_csv(OUT / "importancia_permutacao.csv", float_format="%.4f",
                                               index_label="variavel")

# ---------------------------------------------------------------- resumo
pd.set_option("display.width", 120)
print("\nTabela 4 (OOF k-fold, n = 247)\n", t4.round(4).to_string(index=False))
print("\nPesos do integrador:", dict(zip(C.ESPECIALISTAS, np.round(meta.coef_, 4))), f"intercepto {meta.intercept_:.4f}")
print(f"α Ridge = {ridge.alpha_:.1f} · árvore: {arv.get_n_leaves()} folhas")
print(f"ANOVA F = {F:.2f} · Kruskal-Wallis H = {H:.2f}")
print("dCor marginal:", t2.round(3).to_dict())
print("Importância (média):", I["Média"].sort_values(ascending=False).head(4).round(3).to_dict())
print(f"\nArquivos gravados em {OUT}")
