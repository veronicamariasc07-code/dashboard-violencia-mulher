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
    initial_sidebar_state="expanded",
)

# ── CSS customizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .block-container { padding-top: 1.5rem; }

    /* Cards de métricas */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #e91e8c33;
        border-radius: 12px;
        padding: 16px 20px;
    }
    [data-testid="metric-container"] label {
        color: #a78bfa !important;
        font-size: 0.78rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 2rem !important;
        font-weight: 700;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #34d399 !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid #e91e8c22;
    }

    /* Títulos */
    h1 { color: #f8fafc !important; font-weight: 800; }
    h2, h3 { color: #e2e8f0 !important; }

    /* Divider */
    hr { border-color: #e91e8c33 !important; }

    /* Rodapé */
    .footer {
        text-align: center;
        color: #64748b;
        font-size: 0.75rem;
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Paleta de cores consistente
PALETTE = ["#e91e8c", "#a78bfa", "#34d399", "#fb923c", "#60a5fa", "#f472b6"]
PALETTE_DARK = ["#c2185b", "#7c3aed", "#059669", "#ea580c", "#2563eb", "#db2777"]

# ── Carregamento dos dados ──────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("dados_violencia_mulheres_teresina.xlsx")
    return df

df = load_data()

# ── Sidebar – Filtros ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🌸 Filtros")
    st.markdown("---")

    anos = sorted(df["Ano"].unique())
    ano_sel = st.multiselect(
        "Ano", anos, default=anos, key="ano"
    )

    zonas = sorted(df["Zona"].unique())
    zona_sel = st.multiselect(
        "Zona", zonas, default=zonas, key="zona"
    )

    tipos = sorted(df["Tipo_Violencia"].unique())
    tipo_sel = st.multiselect(
        "Tipo de Violência", tipos, default=tipos, key="tipo"
    )

    faixas = sorted(df["Faixa_Etaria"].unique(),
                    key=lambda x: ["Menor de 18","18-24 anos","25-34 anos",
                                   "35-44 anos","45-59 anos","60+ anos"].index(x))
    faixa_sel = st.multiselect(
        "Faixa Etária", faixas, default=faixas, key="faixa"
    )

    st.markdown("---")
    st.markdown(
        "<div style='color:#64748b;font-size:0.72rem'>Dados: 2020–2024 · Teresina–PI</div>",
        unsafe_allow_html=True
    )

# ── Filtragem ───────────────────────────────────────────────────────────────
mask = (
    df["Ano"].isin(ano_sel) &
    df["Zona"].isin(zona_sel) &
    df["Tipo_Violencia"].isin(tipo_sel) &
    df["Faixa_Etaria"].isin(faixa_sel)
)
dff = df[mask].copy()

# ── Cabeçalho ───────────────────────────────────────────────────────────────
st.markdown(
    "# 🌸 Violência contra a Mulher — Teresina (PI)",
    unsafe_allow_html=False
)
st.markdown(
    "Dashboard analítico de registros de violência contra mulheres por zona, "
    "tipo de ocorrência, faixa etária e perfil do agressor.",
    unsafe_allow_html=False
)
st.markdown("---")

# ── KPIs ────────────────────────────────────────────────────────────────────
total       = dff["Casos"].sum()
feminicidio = dff[dff["Tipo_Violencia"] == "Feminicídio"]["Casos"].sum()
t_fem       = dff[dff["Tipo_Violencia"] == "Tentativa de Feminicídio"]["Casos"].sum()
menores     = dff[dff["Faixa_Etaria"] == "Menor de 18"]["Casos"].sum()
zona_critica = (
    dff.groupby("Zona")["Casos"].sum().idxmax()
    if not dff.empty else "—"
)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📋 Total de Casos", f"{total:,}".replace(",", "."))
col2.metric("⚠️ Feminicídios", f"{feminicidio}")
col3.metric("🔴 Tent. Feminicídio", f"{t_fem}")
col4.metric("👧 Menores de 18", f"{menores}")
col5.metric("📍 Zona Crítica", zona_critica.replace("Zona ", "") if zona_critica else "—")

st.markdown("---")

# ── Linha 1: Evolução temporal + Pizza tipos ────────────────────────────────
col_a, col_b = st.columns([2, 1])

with col_a:
    st.markdown("#### 📈 Evolução Anual por Tipo de Violência")
    ev = (
        dff.groupby(["Ano", "Tipo_Violencia"])["Casos"]
        .sum()
        .reset_index()
    )
    fig_ev = px.line(
        ev, x="Ano", y="Casos", color="Tipo_Violencia",
        markers=True,
        color_discrete_sequence=PALETTE,
        template="plotly_dark",
    )
    fig_ev.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Tipo",
        xaxis=dict(tickmode="linear", dtick=1),
        height=340,
    )
    st.plotly_chart(fig_ev, use_container_width=True)

with col_b:
    st.markdown("#### 🥧 Distribuição por Tipo")
    tipos_total = dff.groupby("Tipo_Violencia")["Casos"].sum().reset_index()
    fig_pie = px.pie(
        tipos_total, names="Tipo_Violencia", values="Casos",
        color_discrete_sequence=PALETTE,
        hole=0.45,
        template="plotly_dark",
    )
    fig_pie.update_traces(textposition="outside", textinfo="percent+label")
    fig_pie.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=340,
        margin=dict(t=10, b=10, l=10, r=10),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Linha 2: Por zona + Agressor ────────────────────────────────────────────
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("#### 🗺️ Casos por Zona Geográfica")
    zona_df = (
        dff.groupby(["Zona", "Tipo_Violencia"])["Casos"]
        .sum()
        .reset_index()
    )
    fig_zona = px.bar(
        zona_df, x="Zona", y="Casos", color="Tipo_Violencia",
        color_discrete_sequence=PALETTE,
        template="plotly_dark",
        barmode="stack",
    )
    fig_zona.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Tipo",
        xaxis_title="",
        height=340,
    )
    st.plotly_chart(fig_zona, use_container_width=True)

with col_d:
    st.markdown("#### 👤 Perfil do Agressor")
    agr_df = dff.groupby("Perfil_Agressor")["Casos"].sum().reset_index()
    agr_df = agr_df.sort_values("Casos", ascending=True)
    fig_agr = px.bar(
        agr_df, x="Casos", y="Perfil_Agressor",
        orientation="h",
        color="Casos",
        color_continuous_scale=["#4a0e2f", "#e91e8c"],
        template="plotly_dark",
    )
    fig_agr.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis_title="",
        height=340,
    )
    st.plotly_chart(fig_agr, use_container_width=True)

# ── Linha 3: Faixa etária + Heatmap zona×ano ────────────────────────────────
col_e, col_f = st.columns([1, 2])

with col_e:
    st.markdown("#### 👩 Faixa Etária das Vítimas")
    ordem_faixa = ["Menor de 18","18-24 anos","25-34 anos",
                   "35-44 anos","45-59 anos","60+ anos"]
    faixa_df = (
        dff.groupby("Faixa_Etaria")["Casos"]
        .sum()
        .reindex(ordem_faixa)
        .reset_index()
    )
    fig_faixa = px.bar(
        faixa_df, x="Casos", y="Faixa_Etaria",
        orientation="h",
        color="Casos",
        color_continuous_scale=["#2d0a57", "#a78bfa"],
        template="plotly_dark",
    )
    fig_faixa.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis_title="",
        height=340,
    )
    st.plotly_chart(fig_faixa, use_container_width=True)

with col_f:
    st.markdown("#### 🔥 Mapa de Calor: Zona × Ano")
    heat_df = (
        dff.groupby(["Zona", "Ano"])["Casos"]
        .sum()
        .reset_index()
        .pivot(index="Zona", columns="Ano", values="Casos")
        .fillna(0)
    )
    fig_heat = px.imshow(
        heat_df,
        color_continuous_scale=["#0f0f1a", "#e91e8c"],
        template="plotly_dark",
        text_auto=True,
        aspect="auto",
    )
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=340,
        xaxis_title="Ano",
        yaxis_title="",
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ── Linha 4: Top 10 bairros + Agressor × Tipo ───────────────────────────────
col_g, col_h = st.columns(2)

with col_g:
    st.markdown("#### 📍 Top 10 Bairros com Mais Registros")
    top_bairros = (
        dff.groupby("Bairro")["Casos"]
        .sum()
        .nlargest(10)
        .reset_index()
        .sort_values("Casos")
    )
    fig_bairros = px.bar(
        top_bairros, x="Casos", y="Bairro",
        orientation="h",
        color="Casos",
        color_continuous_scale=["#0d2137", "#60a5fa"],
        template="plotly_dark",
    )
    fig_bairros.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False,
        yaxis_title="",
        height=370,
    )
    st.plotly_chart(fig_bairros, use_container_width=True)

with col_h:
    st.markdown("#### 🔗 Agressor × Tipo de Violência")
    agr_tipo = (
        dff.groupby(["Perfil_Agressor", "Tipo_Violencia"])["Casos"]
        .sum()
        .reset_index()
    )
    fig_at = px.bar(
        agr_tipo, x="Perfil_Agressor", y="Casos", color="Tipo_Violencia",
        color_discrete_sequence=PALETTE,
        template="plotly_dark",
        barmode="group",
    )
    fig_at.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Tipo",
        xaxis_title="",
        xaxis_tickangle=-20,
        height=370,
    )
    st.plotly_chart(fig_at, use_container_width=True)

# ── Tabela de dados filtrados ────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### 📊 Dados Filtrados")
resumo = (
    dff.groupby(["Ano", "Zona", "Tipo_Violencia", "Faixa_Etaria", "Perfil_Agressor"])["Casos"]
    .sum()
    .reset_index()
    .sort_values(["Ano", "Casos"], ascending=[True, False])
)
st.dataframe(resumo, use_container_width=True, height=300)

# ── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='footer'>Dashboard de Violência contra a Mulher · Teresina–PI · 2020–2024</div>",
    unsafe_allow_html=True
)
