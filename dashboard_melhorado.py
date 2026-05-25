import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Observatório Mulher Segura – Teresina",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PALETTE = ["#ff2d9a", "#a78bfa", "#38d9a9", "#ff9f43", "#4dabf7", "#f783ac"]
ZONE_COLORS = {
    "Zona Centro": "#ff2d9a",
    "Zona Norte": "#4dabf7",
    "Zona Sul": "#38d9a9",
    "Zona Sudeste": "#ff9f43",
    "Zona Leste": "#a78bfa",
}
ORDEM_FAIXA = ["Menor de 18", "18-24 anos", "25-34 anos", "35-44 anos", "45-59 anos", "60+ anos"]

# ─────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,500&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@300;400;500&display=swap');

:root{
  --bg:#070711; --panel:#0f1020; --panel2:#15162a; --line:#ffffff14;
  --pink:#ff2d9a; --pink-soft:#ff2d9a22; --text:#f8fafc; --muted:#8b98ad;
  --purple:#a78bfa; --green:#38d9a9; --blue:#4dabf7; --orange:#ff9f43;
}
html { scroll-behavior:smooth; }
html, body, [class*="css"] { font-family:'DM Sans', sans-serif; }
.main, .stApp { background:var(--bg); }
.block-container { padding:0 !important; max-width:100% !important; }
section[data-testid="stSidebar"] { display:none; }
[data-testid="stToolbar"] { right: 1rem; }

::-webkit-scrollbar{width:6px} ::-webkit-scrollbar-track{background:#070711}
::-webkit-scrollbar-thumb{background:#ff2d9a55;border-radius:10px}

.hero-section{
  min-height:96vh; position:relative; display:grid; place-items:center; text-align:center;
  padding:88px 28px 42px; overflow:hidden;
  background:
    radial-gradient(circle at 50% 25%, #ff2d9a22 0%, transparent 33%),
    radial-gradient(circle at 20% 75%, #4dabf711 0%, transparent 28%),
    linear-gradient(180deg, #05050c 0%, #090912 100%);
}
.hero-grid{position:absolute; inset:0; opacity:.22; background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px); background-size:44px 44px; mask-image:radial-gradient(circle at center, black, transparent 75%)}
.hero-content{position:relative; z-index:2; max-width:980px; margin:auto;}
.hero-eyebrow{font-family:'DM Mono',monospace; color:var(--pink); letter-spacing:.26em; text-transform:uppercase; font-size:.78rem; margin-bottom:24px;}
.hero-title{font-family:'Cormorant Garamond',serif; font-size:clamp(3.6rem,8vw,7.4rem); line-height:.94; color:var(--text); margin:0 0 26px; font-weight:600; letter-spacing:-.04em;}
.hero-title em{color:var(--pink); font-style:italic; font-weight:500;}
.hero-sub{max-width:760px; margin:0 auto 34px; color:#a5b0c4; font-size:1.08rem; line-height:1.8; font-weight:300;}
.hero-actions{display:flex; justify-content:center; align-items:center; gap:14px; flex-wrap:wrap;}
.btn-primary,.btn-secondary{display:inline-flex; align-items:center; justify-content:center; gap:10px; min-height:48px; padding:0 28px; border-radius:999px; text-decoration:none; text-transform:uppercase; letter-spacing:.12em; font:600 .76rem 'DM Mono',monospace; transition:.25s ease;}
.btn-primary{background:linear-gradient(135deg,var(--pink),#b83280); color:white; box-shadow:0 18px 50px #ff2d9a2c; border:1px solid #ffffff18;}
.btn-primary:hover{transform:translateY(-2px); box-shadow:0 22px 58px #ff2d9a40;}
.btn-secondary{border:1px solid #ffffff22; color:#dbeafe; background:#ffffff06;}
.btn-secondary:hover{border-color:#ff2d9a99; color:white; background:#ff2d9a12;}
.scroll-cue{position:absolute; bottom:28px; left:50%; transform:translateX(-50%); color:#8b98ad; font-family:'DM Mono'; font-size:.68rem; letter-spacing:.18em; text-transform:uppercase; animation:float 1.7s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translate(-50%,0)}50%{transform:translate(-50%,8px)}}

.stats-bar{display:grid; grid-template-columns:repeat(4,1fr); border-top:1px solid var(--line); border-bottom:1px solid var(--line); background:#0b0c18;}
.stat-item{padding:34px 22px; text-align:center; border-right:1px solid var(--line);}
.stat-item:last-child{border-right:0}.stat-number{font-family:'Cormorant Garamond'; font-size:2.8rem; line-height:1; color:#fff; margin-bottom:8px}.stat-label{font-family:'DM Mono'; color:#76839a; text-transform:uppercase; letter-spacing:.14em; font-size:.66rem;}

.section{padding:78px 5.5vw; border-bottom:1px solid var(--line);} .section.compact{padding-top:54px;padding-bottom:48px}
.section-kicker{font-family:'DM Mono'; color:var(--pink); letter-spacing:.22em; text-transform:uppercase; font-size:.7rem; margin-bottom:14px;}
.section-title{font-family:'Cormorant Garamond'; color:#fff; font-size:clamp(2.2rem,4vw,4rem); line-height:1.05; margin:0 0 14px; font-weight:500;}.section-title em{color:var(--purple);font-style:italic}.section-sub{color:#91a0b6; max-width:760px; line-height:1.8; font-size:1rem;}
.about-grid{display:grid; grid-template-columns:1fr 1.15fr; gap:54px; align-items:start}.fact-grid{display:grid; grid-template-columns:repeat(2,1fr); gap:16px}.fact-card{background:linear-gradient(180deg,#121326,#0d0e1c); border:1px solid var(--line); border-radius:18px; padding:22px; min-height:154px; box-shadow:0 20px 80px #00000020}.fact-card b{display:block; font-family:'DM Mono'; color:#fff; font-size:.78rem; letter-spacing:.1em; text-transform:uppercase; margin-bottom:10px}.fact-card p{color:#8b98ad; line-height:1.65; margin:0; font-size:.92rem}

.map-layout{display:grid; grid-template-columns:.9fr 1.1fr; gap:24px; align-items:stretch}.map-card,.insight-card{background:linear-gradient(180deg,#111224,#0b0c18); border:1px solid var(--line); border-radius:24px; padding:26px; position:relative; overflow:hidden; box-shadow:0 28px 90px #00000030}.map-card:before{content:''; position:absolute; inset:auto -80px -80px auto; width:240px; height:240px; background:radial-gradient(circle,#ff2d9a2f,transparent 65%)}.piaui-map{width:100%; max-width:420px; margin:0 auto; display:block}.map-note{font-family:'DM Mono'; color:#77849a; font-size:.7rem; letter-spacing:.1em; text-transform:uppercase; text-align:center; margin-top:12px}.zone-list{display:grid; gap:12px}.zone-row{display:grid; grid-template-columns:12px 1fr auto; gap:12px; align-items:center; padding:13px 14px; border-radius:14px; background:#ffffff07; border:1px solid #ffffff0d}.zone-dot{width:12px; height:12px; border-radius:50%;}.zone-row span{color:#dfe7f5; font-weight:600}.zone-row small{color:#8b98ad}.product-strip{display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:20px}.product-card{border:1px solid #ffffff12; border-radius:18px; background:#ffffff06; padding:18px}.product-card b{color:#fff}.product-card p{color:#8b98ad; font-size:.86rem; line-height:1.55; margin:.5rem 0 0}

#dashboard{background:#090a14}.dash-header{text-align:center; margin-bottom:34px}.dash-sub{color:#7f8da4}.filter-shell{background:#101122; border:1px solid var(--line); border-radius:22px; padding:22px; margin-bottom:28px}.filter-title{font-family:'DM Mono'; color:var(--pink); font-size:.7rem; letter-spacing:.22em; text-transform:uppercase; margin-bottom:16px}.stMultiSelect label,.stSelectbox label{color:#8996ad!important; font-family:'DM Mono'!important; letter-spacing:.1em!important; text-transform:uppercase!important; font-size:.68rem!important}.stMultiSelect [data-baseweb="select"], .stSelectbox [data-baseweb="select"]{background:#17182b!important; border-radius:14px!important; border:1px solid #ffffff16!important; min-height:44px!important}.stMultiSelect span[data-baseweb="tag"]{background:#ff2d9a!important; border-radius:999px!important; font-size:.82rem!important;}

[data-testid="metric-container"]{background:linear-gradient(150deg,#15172e,#0e0f1e); border:1px solid #ffffff12; border-radius:20px; padding:20px 18px; box-shadow:0 18px 60px #00000022; min-height:118px}[data-testid="metric-container"] label{color:#8794aa!important; font-family:'DM Mono'!important; font-size:.64rem!important; letter-spacing:.12em!important; text-transform:uppercase!important}[data-testid="stMetricValue"]{font-family:'Cormorant Garamond'!important; color:#fff!important; font-size:2.2rem!important;}
.chart-card{background:linear-gradient(180deg,#111224,#0b0c18); border:1px solid var(--line); border-radius:22px; padding:18px; margin-bottom:22px; box-shadow:0 18px 70px #00000025}.chart-title{font-family:'DM Mono'; color:#7f8da4; letter-spacing:.14em; text-transform:uppercase; font-size:.66rem; padding:4px 4px 14px; border-bottom:1px solid #ffffff0b; margin-bottom:12px}.site-footer{background:#05050b; border-top:1px solid var(--line); padding:42px 5.5vw; display:flex; justify-content:space-between; gap:16px; align-items:center}.footer-brand{font-family:'Cormorant Garamond'; color:#ffffff55; font-size:1.5rem}.footer-copy{font-family:'DM Mono'; color:#516078; font-size:.66rem; letter-spacing:.1em; text-transform:uppercase}

@media(max-width:980px){.stats-bar,.about-grid,.map-layout,.product-strip{grid-template-columns:1fr}.fact-grid{grid-template-columns:1fr}.section{padding:56px 22px}.hero-section{min-height:92vh}.stat-item{border-right:0;border-bottom:1px solid var(--line)}.site-footer{flex-direction:column; text-align:center}}
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_excel("dados_violencia_mulheres_teresina.xlsx")

df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────────────────────────────────────────
def fmt_num(v):
    try:
        return f"{int(v):,}".replace(",", ".")
    except Exception:
        return str(v)


def plot_layout(fig, h=360, legend=True):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#dbe4f0"),
        height=h,
        margin=dict(t=18, l=12, r=12, b=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,.08)", borderwidth=1),
        showlegend=legend,
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,.07)", zerolinecolor="rgba(255,255,255,.08)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,.07)", zerolinecolor="rgba(255,255,255,.08)")
    return fig


def chart_title(text):
    st.markdown(f'<div class="chart-card"><div class="chart-title">{text}</div>', unsafe_allow_html=True)


def chart_end():
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# LANDING
# ─────────────────────────────────────────────────────────────────────────────
total_geral = df["Casos"].sum()
anos_range = f"{df['Ano'].min()}–{df['Ano'].max()}"
n_bairros = df["Bairro"].nunique() if "Bairro" in df.columns else "—"
n_tipos = df["Tipo_Violencia"].nunique()

st.markdown(
    f"""
<section class="hero-section" id="inicio">
  <div class="hero-grid"></div>
  <div class="hero-content">
    <div class="hero-eyebrow">Observatório Mulher Segura · Teresina – PI</div>
    <h1 class="hero-title">Violência<br><em>contra a Mulher</em></h1>
    <p class="hero-sub">
      Plataforma executiva para leitura territorial dos registros de violência contra a mulher em Teresina,
      com filtros por zona, bairro, tipo de ocorrência, faixa etária e perfil do agressor.
    </p>
    <div class="hero-actions">
      <a class="btn-primary" href="#dashboard">Ver painel completo ↓</a>
      <a class="btn-secondary" href="#mapa-piaui">Navegar pelo mapa do Piauí</a>
    </div>
  </div>
  <div class="scroll-cue">Role para explorar</div>
</section>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="stats-bar">
  <div class="stat-item"><div class="stat-number">{fmt_num(total_geral)}</div><div class="stat-label">Casos registrados</div></div>
  <div class="stat-item"><div class="stat-number">{anos_range}</div><div class="stat-label">Período analisado</div></div>
  <div class="stat-item"><div class="stat-number">{n_bairros}</div><div class="stat-label">Bairros mapeados</div></div>
  <div class="stat-item"><div class="stat-number">{n_tipos}</div><div class="stat-label">Tipos monitorados</div></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<section class="section compact">
  <div class="about-grid">
    <div>
      <div class="section-kicker">Proposta do produto</div>
      <h2 class="section-title">De painel acadêmico a <em>produto vendável</em></h2>
      <p class="section-sub">
        A landing page foi reorganizada como uma solução de inteligência pública: abertura institucional,
        navegação territorial, indicadores executivos, filtros analíticos e módulos que podem ser evoluídos
        para prefeituras, secretarias, ONGs, imprensa e equipes de pesquisa.
      </p>
    </div>
    <div class="fact-grid">
      <div class="fact-card"><b>Leitura rápida</b><p>KPIs no topo facilitam a apresentação para gestores e bancas avaliadoras.</p></div>
      <div class="fact-card"><b>Foco territorial</b><p>O mapa do Piauí conduz o usuário para Teresina e para as zonas da capital.</p></div>
      <div class="fact-card"><b>Exploração guiada</b><p>Filtros menores e organizados deixam os gráficos com mais destaque.</p></div>
      <div class="fact-card"><b>Escalabilidade</b><p>A estrutura aceita novos municípios, novas fontes de dados e relatórios automáticos.</p></div>
    </div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# MAPA PIAUÍ + NAVEGAÇÃO
# ─────────────────────────────────────────────────────────────────────────────
zone_totals = df.groupby("Zona")["Casos"].sum().sort_values(ascending=False)
zone_rows = "".join(
    f"<div class='zone-row'><i class='zone-dot' style='background:{ZONE_COLORS.get(z, '#ff2d9a')}'></i><span>{z}</span><small>{fmt_num(v)} casos</small></div>"
    for z, v in zone_totals.items()
)

st.markdown(
    f"""
<section class="section" id="mapa-piaui">
  <div class="section-kicker">Navegação territorial</div>
  <h2 class="section-title">Mapa do Piauí como porta de entrada</h2>
  <p class="section-sub">
    A ideia do mapa transforma o painel em uma experiência mais comercial: o usuário entende rapidamente
    que o produto pode sair de Teresina e evoluir para uma plataforma estadual, com recortes por município,
    zona e bairro.
  </p>
  <div style="height:24px"></div>
  <div class="map-layout">
    <div class="map-card">
      <svg class="piaui-map" viewBox="0 0 360 520" role="img" aria-label="Mapa estilizado do Piauí com Teresina destacada">
        <defs>
          <linearGradient id="piauigrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#ff2d9a" stop-opacity=".52"/>
            <stop offset="55%" stop-color="#a78bfa" stop-opacity=".28"/>
            <stop offset="100%" stop-color="#4dabf7" stop-opacity=".18"/>
          </linearGradient>
          <filter id="glow"><feGaussianBlur stdDeviation="5" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <path d="M190 18 C160 54 169 98 138 130 C102 168 123 214 96 253 C68 294 57 339 78 386 C91 415 91 448 72 494 C110 485 135 460 160 423 C188 383 223 360 236 318 C247 283 241 244 263 206 C287 164 262 122 281 84 C244 76 220 48 190 18 Z" fill="url(#piauigrad)" stroke="#ff2d9a" stroke-opacity=".65" stroke-width="2"/>
        <path d="M190 18 C160 54 169 98 138 130 C102 168 123 214 96 253 C68 294 57 339 78 386 C91 415 91 448 72 494 C110 485 135 460 160 423 C188 383 223 360 236 318 C247 283 241 244 263 206 C287 164 262 122 281 84 C244 76 220 48 190 18 Z" fill="none" stroke="#ffffff" stroke-opacity=".12" stroke-width="8"/>
        <circle cx="205" cy="83" r="15" fill="#ff2d9a" filter="url(#glow)"/>
        <circle cx="205" cy="83" r="6" fill="#fff"/>
        <text x="226" y="78" fill="#ffffff" font-family="DM Mono, monospace" font-size="14" font-weight="600">Teresina</text>
        <text x="226" y="98" fill="#9aa7bd" font-family="DM Sans, sans-serif" font-size="12">capital analisada</text>
      </svg>
      <div class="map-note">Protótipo visual: expansão futura para municípios do Piauí</div>
    </div>
    <div class="insight-card">
      <div class="section-kicker">Zonas de Teresina</div>
      <h2 class="section-title" style="font-size:2.4rem">Ranking territorial</h2>
      <div class="zone-list">{zone_rows}</div>
      <div class="product-strip">
        <div class="product-card"><b>Plano Gestor</b><p>Visão executiva para tomada de decisão pública.</p></div>
        <div class="product-card"><b>Plano Pesquisa</b><p>Exportação de dados e recortes para estudos acadêmicos.</p></div>
        <div class="product-card"><b>Plano Estado</b><p>Expansão para outras cidades e regiões do Piauí.</p></div>
      </div>
    </div>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

# Controle navegável real no Streamlit
with st.container():
    st.markdown('<section class="section" id="dashboard">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="dash-header">
          <div class="section-kicker">Análise de dados</div>
          <h2 class="section-title">Painel Analítico</h2>
          <p class="dash-sub">Escolha uma área no controle territorial e refine os filtros para investigar padrões.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_opcoes = ["Todo o município"] + sorted(df["Zona"].unique())
    foco = st.selectbox("Navegação territorial", nav_opcoes, index=0, help="Use este campo como navegação do mapa: ele já pré-seleciona a zona no painel.")

    st.markdown('<div class="filter-shell"><div class="filter-title">Filtros de análise</div>', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        anos = sorted(df["Ano"].unique())
        ano_sel = st.multiselect("Ano", anos, default=anos, key="ano")
    with fc2:
        zonas = sorted(df["Zona"].unique())
        zona_default = zonas if foco == "Todo o município" else [foco]
        zona_sel = st.multiselect("Zona", zonas, default=zona_default, key=f"zona_{foco}")
    with fc3:
        tipos = sorted(df["Tipo_Violencia"].unique())
        tipo_sel = st.multiselect("Tipo de violência", tipos, default=tipos, key="tipo")
    with fc4:
        faixas = sorted(df["Faixa_Etaria"].unique(), key=lambda x: ORDEM_FAIXA.index(x) if x in ORDEM_FAIXA else 999)
        faixa_sel = st.multiselect("Faixa etária", faixas, default=faixas, key="faixa")
    st.markdown('</div>', unsafe_allow_html=True)

mask = (
    df["Ano"].isin(ano_sel) &
    df["Zona"].isin(zona_sel) &
    df["Tipo_Violencia"].isin(tipo_sel) &
    df["Faixa_Etaria"].isin(faixa_sel)
)
dff = df[mask].copy()

# KPIs
total = dff["Casos"].sum()
feminicidio = dff.loc[dff["Tipo_Violencia"] == "Feminicídio", "Casos"].sum()
t_fem = dff.loc[dff["Tipo_Violencia"] == "Tentativa de Feminicídio", "Casos"].sum()
menores = dff.loc[dff["Faixa_Etaria"] == "Menor de 18", "Casos"].sum()
zona_critica = dff.groupby("Zona")["Casos"].sum().idxmax() if not dff.empty else "—"

def top_value(col):
    return dff.groupby(col)["Casos"].sum().idxmax() if not dff.empty else "—"

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total de casos", fmt_num(total))
k2.metric("Feminicídios", fmt_num(feminicidio))
k3.metric("Tentativas", fmt_num(t_fem))
k4.metric("Menores de 18", fmt_num(menores))
k5.metric("Zona crítica", zona_critica.replace("Zona ", "") if zona_critica != "—" else "—")

st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)

# Gráficos
col_a, col_b = st.columns([2, 1])
with col_a:
    chart_title("Evolução anual por tipo de violência")
    ev = dff.groupby(["Ano", "Tipo_Violencia"], as_index=False)["Casos"].sum()
    fig = px.line(ev, x="Ano", y="Casos", color="Tipo_Violencia", markers=True, color_discrete_sequence=PALETTE)
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(xaxis=dict(tickmode="linear", dtick=1), legend_title_text="Tipo")
    st.plotly_chart(plot_layout(fig, 370), use_container_width=True)
    chart_end()
with col_b:
    chart_title("Composição por tipo")
    tipo_total = dff.groupby("Tipo_Violencia", as_index=False)["Casos"].sum()
    fig = px.pie(tipo_total, names="Tipo_Violencia", values="Casos", hole=.58, color_discrete_sequence=PALETTE)
    fig.update_traces(textinfo="percent", textfont_size=12, marker=dict(line=dict(color="#090a14", width=2)))
    st.plotly_chart(plot_layout(fig, 370, legend=False), use_container_width=True)
    chart_end()

col_c, col_d = st.columns(2)
with col_c:
    chart_title("Mapa territorial simplificado — zonas")
    zona_df = dff.groupby("Zona", as_index=False)["Casos"].sum().sort_values("Casos", ascending=False)
    fig = px.bar(zona_df, x="Zona", y="Casos", color="Zona", color_discrete_map=ZONE_COLORS, text="Casos")
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Casos")
    st.plotly_chart(plot_layout(fig, 350, legend=False), use_container_width=True)
    chart_end()
with col_d:
    chart_title("Perfil do agressor")
    agr_df = dff.groupby("Perfil_Agressor", as_index=False)["Casos"].sum().sort_values("Casos")
    fig = px.bar(agr_df, x="Casos", y="Perfil_Agressor", orientation="h", color="Casos", color_continuous_scale=["#231025", "#ff2d9a"])
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Casos")
    st.plotly_chart(plot_layout(fig, 350, legend=False), use_container_width=True)
    chart_end()

col_e, col_f = st.columns([1, 2])
with col_e:
    chart_title("Faixa etária das vítimas")
    faixa_df = dff.groupby("Faixa_Etaria")["Casos"].sum().reindex(ORDEM_FAIXA).fillna(0).reset_index()
    fig = px.bar(faixa_df, x="Casos", y="Faixa_Etaria", orientation="h", color="Casos", color_continuous_scale=["#16112f", "#a78bfa"])
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Casos")
    st.plotly_chart(plot_layout(fig, 350, legend=False), use_container_width=True)
    chart_end()
with col_f:
    chart_title("Mapa de calor — zona × ano")
    heat_df = dff.groupby(["Zona", "Ano"], as_index=False)["Casos"].sum().pivot(index="Zona", columns="Ano", values="Casos").fillna(0)
    fig = px.imshow(heat_df, text_auto=True, aspect="auto", color_continuous_scale=["#08080f", "#ff2d9a"])
    fig.update_layout(coloraxis_showscale=False, xaxis_title="Ano", yaxis_title="")
    st.plotly_chart(plot_layout(fig, 350, legend=False), use_container_width=True)
    chart_end()

col_g, col_h = st.columns(2)
with col_g:
    chart_title("Top 10 bairros com mais registros")
    top_bairros = dff.groupby("Bairro", as_index=False)["Casos"].sum().nlargest(10, "Casos").sort_values("Casos")
    fig = px.bar(top_bairros, x="Casos", y="Bairro", orientation="h", color="Casos", color_continuous_scale=["#071527", "#4dabf7"])
    fig.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Casos")
    st.plotly_chart(plot_layout(fig, 380, legend=False), use_container_width=True)
    chart_end()
with col_h:
    chart_title("Agressor × tipo de violência")
    agr_tipo = dff.groupby(["Perfil_Agressor", "Tipo_Violencia"], as_index=False)["Casos"].sum()
    fig = px.bar(agr_tipo, x="Perfil_Agressor", y="Casos", color="Tipo_Violencia", barmode="group", color_discrete_sequence=PALETTE)
    fig.update_layout(xaxis_title="", yaxis_title="Casos", xaxis_tickangle=-18, legend_title_text="Tipo")
    st.plotly_chart(plot_layout(fig, 380), use_container_width=True)
    chart_end()

chart_title("Dados filtrados para conferência")
resumo = dff.groupby(["Ano", "Zona", "Bairro", "Tipo_Violencia", "Faixa_Etaria", "Perfil_Agressor"], as_index=False)["Casos"].sum().sort_values(["Ano", "Casos"], ascending=[True, False])
st.dataframe(resumo, use_container_width=True, height=300)
chart_end()

st.markdown('</section>', unsafe_allow_html=True)

st.markdown(
    """
<footer class="site-footer">
  <div class="footer-brand">Observatório <em>Mulher Segura</em></div>
  <div class="footer-copy">Teresina – PI · 2020–2024 · Protótipo comercializável</div>
</footer>
""",
    unsafe_allow_html=True,
)
