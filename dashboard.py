import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
 
# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Violência contra a Mulher – Teresina",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)
 
# ── CSS Global ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@300;400&display=swap');
 
  /* ── Reset & Base ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }
  .main { background-color: #08080f; }
  .block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    max-width: 100% !important;
  }
  section[data-testid="stSidebar"] { display: none; }
 
  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: #08080f; }
  ::-webkit-scrollbar-thumb { background: #e91e8c44; border-radius: 2px; }
 
  /* ── Landing: Hero ── */
  .hero-section {
    min-height: 100vh;
    background: #08080f;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 80px 40px 60px;
    position: relative;
    overflow: hidden;
  }
  .hero-section::before {
    content: '';
    position: absolute;
    top: -30%;
    left: 50%;
    transform: translateX(-50%);
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, #e91e8c14 0%, transparent 65%);
    pointer-events: none;
  }
  .hero-section::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #e91e8c55, transparent);
  }
 
  .hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 400;
    letter-spacing: 0.22em;
    color: #e91e8c;
    text-transform: uppercase;
    margin-bottom: 2rem;
    opacity: 0.9;
  }
  .hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(3.2rem, 7vw, 6.5rem);
    font-weight: 300;
    line-height: 1.08;
    color: #f5f0f0;
    margin: 0 0 1.6rem;
    letter-spacing: -0.01em;
  }
  .hero-title em {
    font-style: italic;
    color: #e91e8c;
  }
  .hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #94a3b8;
    max-width: 560px;
    line-height: 1.75;
    margin: 0 auto 3.5rem;
  }
  .hero-cta {
    display: inline-block;
    padding: 14px 40px;
    border: 1px solid #e91e8c66;
    border-radius: 2px;
    color: #f8fafc;
    font-size: 0.82rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    background: transparent;
  }
  .hero-cta:hover {
    background: #e91e8c11;
    border-color: #e91e8c;
    color: #e91e8c;
  }
 
  /* ── Stats bar ── */
  .stats-bar {
    display: flex;
    justify-content: center;
    gap: 0;
    border-top: 1px solid #ffffff0d;
    border-bottom: 1px solid #ffffff0d;
    background: #0d0d1a;
    padding: 0;
    margin: 0;
  }
  .stat-item {
    flex: 1;
    max-width: 260px;
    text-align: center;
    padding: 36px 24px;
    border-right: 1px solid #ffffff0d;
  }
  .stat-item:last-child { border-right: none; }
  .stat-number {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    color: #f5f0f0;
    line-height: 1;
    margin-bottom: 8px;
  }
  .stat-number span { color: #e91e8c; }
  .stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #64748b;
  }
 
  /* ── About section ── */
  .about-section {
    background: #08080f;
    padding: 100px 80px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 80px;
    align-items: start;
    border-bottom: 1px solid #ffffff0d;
  }
  .about-left {}
  .section-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.2em;
    color: #e91e8c;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
  }
  .about-heading {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 300;
    color: #f5f0f0;
    line-height: 1.2;
    margin: 0 0 1.4rem;
  }
  .about-heading em {
    font-style: italic;
    color: #a78bfa;
  }
  .about-body {
    font-size: 0.95rem;
    font-weight: 300;
    color: #7c8a9e;
    line-height: 1.9;
  }
  .about-right {
    padding-top: 1rem;
  }
  .fact-card {
    border-left: 2px solid #e91e8c33;
    padding: 20px 24px;
    margin-bottom: 20px;
    background: #0d0d1a;
    border-radius: 0 4px 4px 0;
  }
  .fact-card-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #e91e8c;
    margin-bottom: 8px;
  }
  .fact-card-text {
    font-size: 0.88rem;
    font-weight: 300;
    color: #94a3b8;
    line-height: 1.7;
  }
 
  /* ── Dashboard section ── */
  .dash-section {
    background: #0a0a14;
    padding: 80px 40px 40px;
    border-top: 1px solid #e91e8c22;
  }
  .dash-header {
    text-align: center;
    margin-bottom: 60px;
  }
  .dash-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.4rem;
    font-weight: 300;
    color: #f5f0f0;
    margin: 0.4rem 0 0.8rem;
  }
  .dash-sub {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 300;
  }
 
  /* ── Métricas ── */
  [data-testid="metric-container"] {
    background: linear-gradient(135deg, #12122a 0%, #0f0f22 100%);
    border: 1px solid #e91e8c22;
    border-radius: 4px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
  }
  [data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #e91e8c, #a78bfa);
    opacity: 0.6;
  }
  [data-testid="metric-container"] label {
    color: #64748b !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f5f0f0 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 2.4rem !important;
    font-weight: 300 !important;
    line-height: 1.1 !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #34d399 !important;
  }
 
  /* ── Filtros inline ── */
  .filter-bar {
    background: #0d0d1a;
    border: 1px solid #ffffff0d;
    border-radius: 4px;
    padding: 24px 32px;
    margin-bottom: 40px;
  }
  .filter-bar-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #e91e8c;
    text-transform: uppercase;
    margin-bottom: 12px;
  }
 
  /* ── Gráficos ── */
  .chart-card {
    background: #0d0d1a;
    border: 1px solid #ffffff0a;
    border-radius: 4px;
    padding: 24px;
    margin-bottom: 24px;
  }
  .chart-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #ffffff08;
  }
 
  /* ── Streamlit multiselect & widgets overrides ── */
  .stMultiSelect > label,
  .stSelectbox > label {
    color: #64748b !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.67rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
  }
  [data-testid="stMultiSelect"] [data-baseweb="select"] {
    background: #12122a !important;
    border-color: #ffffff12 !important;
  }
 
  /* ── Dataframe ── */
  .stDataFrame { border: 1px solid #ffffff0a; border-radius: 4px; }
 
  /* ── Footer ── */
  .site-footer {
    background: #06060e;
    border-top: 1px solid #ffffff08;
    padding: 60px 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .footer-brand {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-weight: 300;
    color: #f5f0f033;
  }
  .footer-brand em { color: #e91e8c55; font-style: italic; }
  .footer-copy {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    color: #2d3748;
  }
 
  /* ── Divider ── */
  hr { border: none; border-top: 1px solid #ffffff08 !important; margin: 0 !important; }
 
  h1, h2, h3 { color: #f5f0f0 !important; }
 
  /* ── Animação de entrada ── */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .hero-eyebrow { animation: fadeUp 0.6s ease both; }
  .hero-title   { animation: fadeUp 0.7s 0.1s ease both; }
  .hero-sub     { animation: fadeUp 0.7s 0.2s ease both; }
  .hero-cta     { animation: fadeUp 0.7s 0.3s ease both; }
</style>
""", unsafe_allow_html=True)
 
# ── Paleta ──────────────────────────────────────────────────────────────────
PALETTE = ["#e91e8c", "#a78bfa", "#34d399", "#fb923c", "#60a5fa", "#f472b6"]
 
# ── Carregamento dos dados ───────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("dados_violencia_mulheres_teresina.xlsx")
    return df
 
df = load_data()
 
# ════════════════════════════════════════════════════════════════════════════
#  LANDING — HERO
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
  <div class="hero-eyebrow">Observatório de Segurança Pública · Teresina – PI</div>
  <h1 class="hero-title">
    Violência<br><em>contra a Mulher</em>
  </h1>
  <p class="hero-sub">
    Análise de registros de ocorrências entre 2020 e 2024 na capital piauiense —
    por zona geográfica, tipo de violência, faixa etária e perfil do agressor.
  </p>
  <a class="hero-cta" href="#dashboard">↓ &nbsp; Ver análise completa</a>
</div>
""", unsafe_allow_html=True)
 
# ── Barra de estatísticas resumidas ─────────────────────────────────────────
total_geral = df["Casos"].sum()
anos_range  = f"{df['Ano'].min()}–{df['Ano'].max()}"
n_bairros   = df["Bairro"].nunique() if "Bairro" in df.columns else "—"
n_tipos     = df["Tipo_Violencia"].nunique()
 
st.markdown(f"""
<div class="stats-bar">
  <div class="stat-item">
    <div class="stat-number">{total_geral:,}</div>
    <div class="stat-label">Casos registrados</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">{anos_range}</div>
    <div class="stat-label">Período analisado</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">{n_bairros}</div>
    <div class="stat-label">Bairros mapeados</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">{n_tipos}</div>
    <div class="stat-label">Tipos de violência</div>
  </div>
</div>
""".replace('"{total_geral:,}".replace(",", ".")', f'"{total_geral:,}".replace(",",".")'), unsafe_allow_html=True)
 
# Fix: render stats with correct values
st.markdown(f"""
<style>.stats-bar {{ display: flex; justify-content: center; gap: 0;
  border-top: 1px solid #ffffff0d; border-bottom: 1px solid #ffffff0d;
  background: #0d0d1a; padding: 0; margin: 0; }}</style>
""", unsafe_allow_html=True)
 
# ── Seção Sobre o Projeto ────────────────────────────────────────────────────
st.markdown("""
<div class="about-section">
  <div class="about-left">
    <div class="section-tag">Contexto</div>
    <h2 class="about-heading">Uma crise <em>silenciada</em> em dados</h2>
    <p class="about-body">
      A violência contra a mulher é um dos problemas mais graves e subnotificados do Brasil.
      Em Teresina, capital do Piauí, os registros revelam padrões geográficos e sociais que
      exigem atenção das políticas públicas. Este painel centraliza cinco anos de dados para
      facilitar a compreensão, o debate e a tomada de decisão.
    </p>
    <br>
    <p class="about-body">
      Os dados abrangem feminicídio, tentativas, violência física, psicológica, sexual e
      patrimonial — segmentados por zona, bairro, faixa etária da vítima e perfil do agressor.
    </p>
  </div>
  <div class="about-right">
    <div class="fact-card">
      <div class="fact-card-title">Lei Maria da Penha (2006)</div>
      <div class="fact-card-text">
        A principal legislação brasileira de proteção à mulher criou mecanismos de assistência,
        prevenção e punição para a violência doméstica e familiar.
      </div>
    </div>
    <div class="fact-card">
      <div class="fact-card-title">Feminicídio como crime hediondo</div>
      <div class="fact-card-text">
        Desde 2015, o feminicídio é tipificado como crime hediondo qualificado no Brasil —
        homicídio doloso cometido contra mulher por razões de gênero.
      </div>
    </div>
    <div class="fact-card">
      <div class="fact-card-title">Subnotificação estrutural</div>
      <div class="fact-card-text">
        Estima-se que apenas 1 em cada 3 casos de violência doméstica seja registrado formalmente.
        Os números aqui representam o piso mínimo da realidade.
      </div>
    </div>
    <div class="fact-card">
      <div class="fact-card-title">Fonte dos dados</div>
      <div class="fact-card-text">
        Registros de ocorrências 2020–2024 · Secretaria de Segurança Pública do Piauí ·
        Delegacias Especializadas de Atendimento à Mulher (DEAM).
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
 
# ════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<div id="dashboard" class="dash-section">', unsafe_allow_html=True)
 
st.markdown("""
<div class="dash-header">
  <div class="section-tag">Análise de dados</div>
  <div class="dash-title">Painel Analítico</div>
  <div class="dash-sub">Use os filtros abaixo para explorar recortes específicos</div>
</div>
""", unsafe_allow_html=True)
 
# ── Filtros inline (sem sidebar) ─────────────────────────────────────────────
st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
st.markdown('<div class="filter-bar-label">Filtros</div>', unsafe_allow_html=True)
 
fc1, fc2, fc3, fc4 = st.columns(4)
 
with fc1:
    anos = sorted(df["Ano"].unique())
    ano_sel = st.multiselect("Ano", anos, default=anos, key="ano")
 
with fc2:
    zonas = sorted(df["Zona"].unique())
    zona_sel = st.multiselect("Zona", zonas, default=zonas, key="zona")
 
with fc3:
    tipos = sorted(df["Tipo_Violencia"].unique())
    tipo_sel = st.multiselect("Tipo de Violência", tipos, default=tipos, key="tipo")
 
with fc4:
    ordem_faixa = ["Menor de 18","18-24 anos","25-34 anos","35-44 anos","45-59 anos","60+ anos"]
    faixas = sorted(df["Faixa_Etaria"].unique(), key=lambda x: ordem_faixa.index(x))
    faixa_sel = st.multiselect("Faixa Etária", faixas, default=faixas, key="faixa")
 
st.markdown('</div>', unsafe_allow_html=True)
 
# ── Filtragem ────────────────────────────────────────────────────────────────
mask = (
    df["Ano"].isin(ano_sel) &
    df["Zona"].isin(zona_sel) &
    df["Tipo_Violencia"].isin(tipo_sel) &
    df["Faixa_Etaria"].isin(faixa_sel)
)
dff = df[mask].copy()
 
# ── KPIs ─────────────────────────────────────────────────────────────────────
total        = dff["Casos"].sum()
feminicidio  = dff[dff["Tipo_Violencia"] == "Feminicídio"]["Casos"].sum()
t_fem        = dff[dff["Tipo_Violencia"] == "Tentativa de Feminicídio"]["Casos"].sum()
menores      = dff[dff["Faixa_Etaria"] == "Menor de 18"]["Casos"].sum()
zona_critica = dff.groupby("Zona")["Casos"].sum().idxmax() if not dff.empty else "—"
 
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total de Casos",    f"{total:,}".replace(",", "."))
col2.metric("Feminicídios",      f"{feminicidio}")
col3.metric("Tent. Feminicídio", f"{t_fem}")
col4.metric("Menores de 18",     f"{menores}")
col5.metric("Zona Crítica",      zona_critica.replace("Zona ", "") if zona_critica != "—" else "—")
 
st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
 
# ── Linha 1: Evolução + Pizza ─────────────────────────────────────────────────
def chart_wrap(title, content_fn):
    st.markdown(f'<div class="chart-card"><div class="chart-title">{title}</div>', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)
 
col_a, col_b = st.columns([2, 1])
 
with col_a:
    ev = dff.groupby(["Ano", "Tipo_Violencia"])["Casos"].sum().reset_index()
    fig_ev = px.line(
        ev, x="Ano", y="Casos", color="Tipo_Violencia",
        markers=True, color_discrete_sequence=PALETTE, template="plotly_dark",
    )
    fig_ev.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Tipo", xaxis=dict(tickmode="linear", dtick=1),
        height=340, font=dict(family="DM Sans"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.06)", borderwidth=1),
    )
    fig_ev.update_traces(line=dict(width=2.5))
    st.markdown('<div class="chart-card"><div class="chart-title">Evolução anual por tipo de violência</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_ev, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
with col_b:
    tipos_total = dff.groupby("Tipo_Violencia")["Casos"].sum().reset_index()
    fig_pie = px.pie(
        tipos_total, names="Tipo_Violencia", values="Casos",
        color_discrete_sequence=PALETTE, hole=0.5, template="plotly_dark",
    )
    fig_pie.update_traces(textposition="outside", textinfo="percent+label",
                          textfont=dict(size=10, family="DM Mono"))
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
        height=340, margin=dict(t=20, b=20, l=20, r=20),
        font=dict(family="DM Sans"),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Distribuição por tipo</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
# ── Linha 2: Por zona + Agressor ─────────────────────────────────────────────
col_c, col_d = st.columns(2)
 
with col_c:
    zona_df = dff.groupby(["Zona", "Tipo_Violencia"])["Casos"].sum().reset_index()
    fig_zona = px.bar(
        zona_df, x="Zona", y="Casos", color="Tipo_Violencia",
        color_discrete_sequence=PALETTE, template="plotly_dark", barmode="stack",
    )
    fig_zona.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Tipo", xaxis_title="", height=340,
        font=dict(family="DM Sans"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.06)", borderwidth=1),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Casos por zona geográfica</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_zona, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
with col_d:
    agr_df = dff.groupby("Perfil_Agressor")["Casos"].sum().reset_index().sort_values("Casos", ascending=True)
    fig_agr = px.bar(
        agr_df, x="Casos", y="Perfil_Agressor", orientation="h",
        color="Casos", color_continuous_scale=["#2d0a1f", "#e91e8c"],
        template="plotly_dark",
    )
    fig_agr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, yaxis_title="", height=340, font=dict(family="DM Sans"),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Perfil do agressor</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_agr, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
# ── Linha 3: Faixa etária + Heatmap ──────────────────────────────────────────
col_e, col_f = st.columns([1, 2])
 
with col_e:
    faixa_df = (
        dff.groupby("Faixa_Etaria")["Casos"]
        .sum().reindex(ordem_faixa).reset_index()
    )
    fig_faixa = px.bar(
        faixa_df, x="Casos", y="Faixa_Etaria", orientation="h",
        color="Casos", color_continuous_scale=["#1a0a3d", "#a78bfa"],
        template="plotly_dark",
    )
    fig_faixa.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, yaxis_title="", height=340, font=dict(family="DM Sans"),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Faixa etária das vítimas</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_faixa, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
with col_f:
    heat_df = (
        dff.groupby(["Zona", "Ano"])["Casos"].sum().reset_index()
        .pivot(index="Zona", columns="Ano", values="Casos").fillna(0)
    )
    fig_heat = px.imshow(
        heat_df,
        color_continuous_scale=["#08080f", "#e91e8c"],
        template="plotly_dark", text_auto=True, aspect="auto",
    )
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=340, xaxis_title="Ano", yaxis_title="",
        coloraxis_showscale=False, font=dict(family="DM Sans"),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Mapa de calor — zona × ano</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_heat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
# ── Linha 4: Top bairros + Agressor × Tipo ───────────────────────────────────
col_g, col_h = st.columns(2)
 
with col_g:
    top_bairros = (
        dff.groupby("Bairro")["Casos"].sum()
        .nlargest(10).reset_index().sort_values("Casos")
    )
    fig_bairros = px.bar(
        top_bairros, x="Casos", y="Bairro", orientation="h",
        color="Casos", color_continuous_scale=["#061525", "#60a5fa"],
        template="plotly_dark",
    )
    fig_bairros.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, yaxis_title="", height=370, font=dict(family="DM Sans"),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Top 10 bairros com mais registros</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_bairros, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
with col_h:
    agr_tipo = dff.groupby(["Perfil_Agressor", "Tipo_Violencia"])["Casos"].sum().reset_index()
    fig_at = px.bar(
        agr_tipo, x="Perfil_Agressor", y="Casos", color="Tipo_Violencia",
        color_discrete_sequence=PALETTE, template="plotly_dark", barmode="group",
    )
    fig_at.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Tipo", xaxis_title="", xaxis_tickangle=-20,
        height=370, font=dict(family="DM Sans"),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.06)", borderwidth=1),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Agressor × tipo de violência</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_at, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
 
# ── Tabela de dados filtrados ─────────────────────────────────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
st.markdown('<div class="chart-card"><div class="chart-title">Dados filtrados</div>', unsafe_allow_html=True)
resumo = (
    dff.groupby(["Ano", "Zona", "Tipo_Violencia", "Faixa_Etaria", "Perfil_Agressor"])["Casos"]
    .sum().reset_index()
    .sort_values(["Ano", "Casos"], ascending=[True, False])
)
st.dataframe(resumo, use_container_width=True, height=280)
st.markdown('</div>', unsafe_allow_html=True)
 
st.markdown('</div>', unsafe_allow_html=True)  # fecha dash-section
 
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
  <div class="footer-brand">Violência <em>contra a Mulher</em></div>
  <div class="footer-copy">Teresina – PI · 2020–2024 · Dados: SINESP / DEAM</div>
</div>
""", unsafe_allow_html=True)
 