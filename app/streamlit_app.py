# SPDX-License-Identifier: Apache-2.0
"""
Aplicativo interativo do estudo "Análise de taxas de rentabilidade no mercado imobiliário
empregando aprendizagem de máquina e combinação de especialistas"
(Benvenho e Gatto, Congresso UPAV 2026, Madri).

Executar na raiz do repositório:
    pip install -r requirements.txt
    streamlit run app/streamlit_app.py
"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import caprate as C  # noqa: E402
from i18n import IDIOMAS, T  # noqa: E402

warnings.filterwarnings("ignore")
REPO = "https://github.com/abenvenho/caprate-upav2026"
COR = {"Ridge": "#2a78d6", "Árvore": "#eb6834", "MLP": "#1baf7a", "Ensemble": "#4a3aa7"}
NEUTRA = "#8a8984"
MODELOS = C.ESPECIALISTAS + ["Ensemble"]

st.set_page_config(page_title="Cap rate · UPAV 2026", page_icon="🏢", layout="wide")


# --------------------------------------------------------------------------- cálculo (em cache)
@st.cache_data(show_spinner=False)
def calcular():
    d = C.carregar_base()
    y = d["cap_rate"].to_numpy()
    reg, anos = C.regioes(d), C.anos(d)
    Xdf = C.matriz_X(d, reg, anos)
    X = Xdf.to_numpy()
    M = C.oof(X, y, C.kfold())
    meta = C.integrador().fit(M, y)
    oof = pd.DataFrame(M, columns=C.ESPECIALISTAS)
    oof["Ensemble"] = meta.predict(M)
    tab = pd.DataFrame([{"Modelo": m, **C.metricas(y, oof[m].to_numpy())} for m in MODELOS])
    return d, reg, anos, list(Xdf.columns), oof, tab, meta.coef_, float(meta.intercept_)


@st.cache_resource(show_spinner=False)
def modelos_finais():
    d = C.carregar_base()
    y = d["cap_rate"].to_numpy()
    X = C.matriz_X(d, C.regioes(d), C.anos(d)).to_numpy()
    esp = C.especialistas()
    for m in esp.values():
        m.fit(X, y)
    return esp


def ler(nome: str) -> pd.DataFrame:
    return pd.read_csv(RAIZ / "results" / nome)


# --------------------------------------------------------------------------- utilidades
with st.sidebar:
    lang = IDIOMAS[st.radio("Idioma / Language", list(IDIOMAS))]
    st.caption(T["rodape"][lang])
    st.markdown(f"[GitHub]({REPO})")


def t(k: str) -> str:
    return T[k][lang]


def num(x: float, casas: int = 2) -> str:
    s = f"{x:,.{casas}f}"
    return s if lang == "en" else s.replace(",", "§").replace(".", ",").replace("§", ".")


def md(s: str) -> str:
    return s.replace("$", "\\$")


def fmt(casas: int):
    return lambda v: num(v, casas)


def estilo(fig: go.Figure, altura: int = 380) -> go.Figure:
    fig.update_layout(height=altura, margin=dict(l=10, r=10, t=50, b=10),
                      separators=".," if lang == "en" else ",.",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridwidth=0.5, zeroline=False)
    return fig


st.title(t("titulo"))
st.caption(t("autores") + " · " + t("subtitulo"))

with st.spinner("…"):
    d, REG, ANOS, COLS, OOF, TAB, PESOS, INTERC = calcular()
y = d["cap_rate"].to_numpy()
abas = st.tabs(T["abas"][lang])

# =========================================================================== 1. Sobre
with abas[0]:
    c1, c2 = st.columns([3, 2], gap="large")
    c1.markdown(t("sobre_md"))
    tab = TAB.sort_values("RMSE (p.p.)", ascending=False)
    fig = go.Figure(go.Bar(x=tab["RMSE (p.p.)"], y=tab["Modelo"], orientation="h",
                           marker_color=[COR[m] for m in tab["Modelo"]],
                           text=[num(v, 4) for v in tab["RMSE (p.p.)"]], textposition="outside", cliponaxis=False,
                           hovertemplate="%{y}: %{x:.4f}<extra></extra>"))
    fig.update_layout(title=t("rmse_titulo"), xaxis_range=[2.0, 2.7], bargap=0.35)
    c2.plotly_chart(estilo(fig, 300), width="stretch")
    c2.subheader(t("materiais"))
    c2.markdown(t("materiais_md").format(repo=REPO))

# =========================================================================== 2. Base
with abas[1]:
    f1, f2 = st.columns(2)
    todas = sorted(d["Regiao"].unique())
    sel_r = f1.multiselect(t("regiao"), todas, default=todas)
    sel_a = f2.multiselect(t("ano"), sorted(d["DATA"].unique()), default=sorted(d["DATA"].unique()))
    sub = d[d["Regiao"].isin(sel_r) & d["DATA"].isin(sel_a)]
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(t("n_obs"), num(len(sub), 0))
    if len(sub):
        k2.metric(t("mediana"), num(sub["cap_rate"].median(), 2) + " %")
        k3.metric(t("area_med"), num(sub["Área (m²)"].median(), 0))
        k4.metric(t("edificios"), num(sub["Endereço"].str.strip().str.lower().nunique(), 0))
        fig = px.scatter_map(sub, lat="Latitude", lon="Longitude", color="cap_rate",
                             color_continuous_scale=px.colors.sequential.Blues[3:], range_color=(3, 15), zoom=11, height=480,
                             center={"lat": float(sub["Latitude"].median()), "lon": float(sub["Longitude"].median())},
                             hover_name="Endereço",
                             hover_data={"Regiao": True, "DATA": True, "cap_rate": ":.2f", "Área (m²)": True,
                                         "Latitude": False, "Longitude": False},
                             map_style="white-bg")
        fig.update_traces(marker=dict(size=10, opacity=0.85))
        # estilo embutido + camada raster de ruas: os pontos aparecem mesmo se o servidor de mapas falhar
        fig.update_layout(title=t("mapa"), margin=dict(l=0, r=0, t=40, b=0),
                          coloraxis_colorbar=dict(title="% a.a."),
                          map_layers=[{"below": "traces", "sourcetype": "raster",
                                       "sourceattribution": "© OpenStreetMap contributors © CARTO",
                                       "source": ["https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"]}])
        st.plotly_chart(fig, width="stretch")
        ordem = sub.groupby("Regiao")["cap_rate"].median().sort_values(ascending=False).index.tolist()
        fig = go.Figure()
        for r in ordem:
            fig.add_trace(go.Box(y=sub.loc[sub["Regiao"] == r, "cap_rate"], name=f"{r} ({(sub['Regiao'] == r).sum()})",
                                 marker_color=COR["Ridge"], boxpoints="all", jitter=0.3, pointpos=0,
                                 marker=dict(size=4, opacity=0.5), showlegend=False))
        fig.update_layout(title=t("box"), yaxis_title="% a.a.")
        st.plotly_chart(estilo(fig, 420), width="stretch")
        with st.expander(t("tabela")):
            st.dataframe(sub.drop(columns=["cap_rate"]), width="stretch", hide_index=True)
        st.download_button(t("baixar"), sub.drop(columns=["cap_rate"]).to_csv(index=False).encode("utf-8"),
                           "base_caprate_recorte.csv", "text/csv")
    with st.expander(t("dicionario")):
        st.dataframe(pd.read_csv(RAIZ / "data" / "data_dictionary.csv"), width="stretch", hide_index=True)

# =========================================================================== 3. Desempenho
with abas[2]:
    st.markdown(f"**{t('t4')}**")
    tab = TAB.copy()
    tab.columns = [t("modelo")] + list(tab.columns[1:])
    st.dataframe(tab.style.format({c: fmt(4) for c in tab.columns[1:]}), width="stretch", hide_index=True)
    st.markdown(f"**{t('pesos')}:** " + " · ".join(f"{m} {num(w, 4)}" for m, w in zip(C.ESPECIALISTAS, PESOS))
                + f" · intercepto {num(INTERC, 4)}")
    st.caption(t("pesos_nota"))

    fig = make_subplots(rows=1, cols=4, subplot_titles=MODELOS, shared_yaxes=True, horizontal_spacing=0.03)
    for i, m in enumerate(MODELOS, start=1):
        fig.add_trace(go.Scatter(x=OOF[m], y=y, mode="markers", showlegend=False,
                                 marker=dict(size=6, color=COR[m], opacity=0.6, line=dict(color="white", width=0.5)),
                                 customdata=d[["Endereço", "Regiao"]],
                                 hovertemplate="%{customdata[0]} · %{customdata[1]}<br>"
                                               f"{t('previsto')}: %{{x:.2f}}<br>{t('observado')}: %{{y:.2f}}<extra>{m}</extra>"),
                      row=1, col=i)
        fig.add_trace(go.Scatter(x=[3, 19], y=[3, 19], mode="lines", hoverinfo="skip", showlegend=False,
                                 line=dict(color=NEUTRA, width=1, dash="dot")), row=1, col=i)
        fig.update_xaxes(title_text=t("previsto"), range=[2, 19], row=1, col=i)
    fig.update_yaxes(title_text=t("observado"), range=[2, 19], row=1, col=1)
    fig.update_layout(title=t("obs_prev"))
    estilo(fig, 420).update_layout(margin=dict(t=90))
    st.plotly_chart(fig, width="stretch")

    st.subheader(t("robustez"))
    st.markdown(t("robustez_md"))
    rob = ler("robustez.csv")
    media = rob[rob["esquema"].str.startswith("KFold")].groupby("modelo", sort=False)[["RMSE (p.p.)", "R²"]].mean()
    grp = rob[rob["esquema"].str.startswith("Group")].set_index("modelo")[["RMSE (p.p.)", "R²"]]
    pub = TAB.set_index("Modelo")[["RMSE (p.p.)"]]
    fig = go.Figure()
    for nome, serie, cor in [("Tabela 4", pub["RMSE (p.p.)"], NEUTRA),
                             (t("media_seeds"), media["RMSE (p.p.)"], COR["Ridge"]),
                             ("GroupKFold", grp["RMSE (p.p.)"], COR["Árvore"])]:
        fig.add_trace(go.Bar(x=MODELOS, y=[serie[m] for m in MODELOS], name=nome, marker_color=cor,
                             text=[num(serie[m], 3) for m in MODELOS], textposition="outside",
                             hovertemplate=f"{nome}<br>%{{x}}: %{{y:.4f}}<extra></extra>"))
    fig.update_layout(barmode="group", yaxis=dict(title="RMSE (p.p.)", range=[2.0, 2.8]))
    st.plotly_chart(estilo(fig, 380), width="stretch")
    rob_ex = rob.rename(columns={"esquema": t("esquema"), "modelo": t("modelo")})
    st.dataframe(rob_ex.style.format({c: fmt(4) for c in rob_ex.columns[2:]}), width="stretch", hide_index=True)

# =========================================================================== 4. Determinantes
with abas[3]:
    c1, c2 = st.columns(2, gap="large")
    imp = ler("importancia_permutacao.csv").head(10).iloc[::-1]
    fig = go.Figure()
    for m in C.ESPECIALISTAS:
        fig.add_trace(go.Bar(y=imp["variavel"], x=imp[m], name=m, orientation="h", marker_color=COR[m]))
    fig.add_trace(go.Scatter(y=imp["variavel"], x=imp["Média"], name=t("media3"), mode="markers",
                             marker=dict(symbol="diamond", size=11, color=COR["Ensemble"])))
    fig.update_layout(title=t("imp"), barmode="group", bargap=0.25)
    estilo(fig, 600).update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, x=0))
    c1.plotly_chart(fig, width="stretch")
    co = ler("ridge_coeficientes.csv").iloc[::-1]
    fig = go.Figure(go.Bar(y=co["variavel"], x=co["coef_padronizado"], orientation="h",
                           marker_color=["#e34948" if v < 0 else COR["Ridge"] for v in co["coef_padronizado"]],
                           hovertemplate="%{y}: %{x:.3f}<extra></extra>"))
    fig.update_layout(title=t("coef"))
    c2.plotly_chart(estilo(fig, 560), width="stretch")
    st.markdown(f"**{t('arvore')}**")
    st.code((RAIZ / "results" / "arvore_regras.txt").read_text(encoding="utf-8"), language=None)

# =========================================================================== 5. Simulador
with abas[4]:
    st.markdown(t("sim_intro"))
    esp = modelos_finais()
    med = d[C.CONTINUAS].median()
    g1, g2, g3 = st.columns(3, gap="large")
    area = g1.number_input(t("area"), 10, 5000, int(med["Área (m²)"]), step=10)
    padrao = g1.slider(t("padrao"), 1.0, 9.0, float(round(med["Padrão"], 2)), 0.01)
    estado = g1.slider(t("estado"), 0.0, 1.0, float(round(med["Estado"], 2)), 0.01)
    lista_reg = sorted(d["Regiao"].unique())
    regiao = g2.selectbox(t("regiao"), lista_reg, index=lista_reg.index("Paulista"))
    ano = g2.selectbox(t("ano"), sorted(d["DATA"].unique()), index=len(d["DATA"].unique()) - 1)
    obs = g3.number_input(t("obs_opc"), 0.0, 30.0, 0.0, 0.1)
    rol = g3.number_input(t("rol"), 0, 100_000_000, 0, step=10_000)

    x = pd.DataFrame([{"Área (m²)": area, "Padrão": padrao, "Estado": estado, "Regiao": regiao, "DATA": ano}])
    Xn = C.matriz_X(x, REG, ANOS).to_numpy()
    p = {m: float(esp[m].predict(Xn)[0]) for m in C.ESPECIALISTAS}
    p["Ensemble"] = float(INTERC + np.dot(PESOS, [p[m] for m in C.ESPECIALISTAS]))

    st.divider()
    cols = st.columns(4)
    for col, m in zip(cols, MODELOS):
        col.markdown(f"<span style='color:{COR[m]};font-size:1.4em'>■</span> **{m}**", unsafe_allow_html=True)
        col.metric("cap rate", num(p[m], 2) + " % a.a.")
    if rol > 0:
        st.metric(t("valor_cap"), "R$ " + num(rol / (p["Ensemble"] / 100), 0))
    if obs > 0:
        lim = 2 * TAB.set_index("Modelo").loc["Ensemble", "RMSE (p.p.)"]
        desvio = obs - p["Ensemble"]
        (st.warning if abs(desvio) > lim else st.success)(
            md(t("triagem_alerta" if abs(desvio) > lim else "triagem_ok").format(
                d=("+" if desvio >= 0 else "−") + num(abs(desvio), 2), lim=num(lim, 2))))
    fora = []
    for c, v in [("Área (m²)", area), ("Padrão", padrao), ("Estado", estado)]:
        if not d[c].min() <= v <= d[c].max():
            fora.append(f"{c} ({num(d[c].min(), 2)}–{num(d[c].max(), 2)})")
    if fora:
        st.warning(t("fora").format(v="; ".join(fora)))
    n_reg = int((d["Regiao"] == regiao).sum())
    if n_reg < 10:
        st.info(t("poucos").format(r=regiao, n=n_reg))

st.divider()
st.caption(t("autores") + " · " + t("rodape"))
