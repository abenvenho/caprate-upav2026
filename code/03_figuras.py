# SPDX-License-Identifier: Apache-2.0
"""
Gera as figuras de resultados a partir dos arquivos de results/ (rode 01 antes).

  figures/previsto_observado.png       previsto × observado (OOF) por modelo
  figures/importancia_permutacao.png   importância média por permutação (top 10)
  figures/ridge_coeficientes.png       coeficientes padronizados da Ridge
  figures/residuos.png                 resíduo × previsto por modelo

Uso:  python code/03_figuras.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

import caprate as C  # noqa: E402

RES, FIG = C.ROOT / "results", C.ROOT / "figures"
FIG.mkdir(exist_ok=True)
COR = {"Ridge": "#2a78d6", "Árvore": "#eb6834", "MLP": "#1baf7a", "Ensemble": "#4a3aa7"}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

oof = pd.read_csv(RES / "previsoes_oof.csv")
t4 = pd.read_csv(RES / "tabela4_desempenho.csv").set_index("Modelo")
t4.index = [i.replace("Ensemble stacking", "Ensemble") for i in t4.index]
y = oof["cap_rate_obs"]

fig, ax = plt.subplots(1, 4, figsize=(15, 4), sharex=True, sharey=True)
for a, m in zip(ax, COR):
    a.scatter(oof[m], y, s=14, alpha=0.6, color=COR[m], edgecolor="white", linewidth=0.4)
    a.plot([3, 19], [3, 19], ls="--", lw=1, color="#8a8984")
    a.set_title(f"{m}\nRMSE {t4.loc[m, 'RMSE (p.p.)']:.4f} · R² {t4.loc[m, 'R²']:.4f}".replace(".", ","))
    a.set_xlabel("Previsto (% a.a.)")
ax[0].set_ylabel("Observado (% a.a.)")
fig.tight_layout()
fig.savefig(FIG / "previsto_observado.png", dpi=150)

fig, ax = plt.subplots(1, 4, figsize=(15, 3.6), sharey=True)
for a, m in zip(ax, COR):
    a.scatter(oof[m], y - oof[m], s=14, alpha=0.6, color=COR[m], edgecolor="white", linewidth=0.4)
    a.axhline(0, ls="--", lw=1, color="#8a8984")
    a.set_title(m)
    a.set_xlabel("Previsto (% a.a.)")
ax[0].set_ylabel("Resíduo (p.p.)")
fig.tight_layout()
fig.savefig(FIG / "residuos.png", dpi=150)

imp = pd.read_csv(RES / "importancia_permutacao.csv").head(10).iloc[::-1]
fig, a = plt.subplots(figsize=(7, 4.5))
a.barh(imp["variavel"], imp["Média"], color=COR["Ridge"])
a.set_xlabel("Aumento médio do RMSE ao embaralhar a variável (p.p.)")
a.set_title("Importância por permutação — média dos três especialistas")
fig.tight_layout()
fig.savefig(FIG / "importancia_permutacao.png", dpi=150)

co = pd.read_csv(RES / "ridge_coeficientes.csv").iloc[::-1]
fig, a = plt.subplots(figsize=(7, 5.5))
a.barh(co["variavel"], co["coef_padronizado"],
       color=["#e34948" if v < 0 else COR["Ridge"] for v in co["coef_padronizado"]])
a.axvline(0, color="#8a8984", lw=1)
a.set_xlabel("Coeficiente padronizado (p.p. por desvio-padrão)")
a.set_title("Regressão Ridge — azul eleva o cap rate, vermelho reduz")
fig.tight_layout()
fig.savefig(FIG / "ridge_coeficientes.png", dpi=150)
print("Figuras gravadas em", FIG)
