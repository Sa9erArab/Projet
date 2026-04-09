import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------
# CONFIG PAGE
# ---------------------------
st.set_page_config(page_title="AI Dashboard Pro", layout="wide")

st.title("📊 Dashboard Intelligent (Streamlit + Plotly)")

# ---------------------------
# DATA (Simulation réaliste)
# ---------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    df = pd.DataFrame({
        "Region": np.random.choice(["Africa", "Europe", "Asia"], 500),
        "Product": np.random.choice(["A", "B", "C"], 500),
        "Revenue": np.random.randint(1000, 10000, 500),
        "Cost": np.random.randint(500, 8000, 500),
        "Customers": np.random.randint(50, 500, 500)
    })
    df["Profit"] = df["Revenue"] - df["Cost"]
    return df

df = load_data()

# ---------------------------
# SIDEBAR (FILTRES)
# ---------------------------
st.sidebar.header("🔎 Filtres")

region_filter = st.sidebar.multiselect(
    "Choisir région",
    df["Region"].unique(),
    default=df["Region"].unique()
)

product_filter = st.sidebar.multiselect(
    "Choisir produit",
    df["Product"].unique(),
    default=df["Product"].unique()
)

# Filtrage
filtered_df = df[
    (df["Region"].isin(region_filter)) &
    (df["Product"].isin(product_filter))
]

# ---------------------------
# KPI (INDICATEURS)
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue Total", f"{filtered_df['Revenue'].sum():,.0f}")
col2.metric("📈 Profit Total", f"{filtered_df['Profit'].sum():,.0f}")
col3.metric("👥 Clients", f"{filtered_df['Customers'].sum():,.0f}")

# ---------------------------
# TABS (STRUCTURE PRO)
# ---------------------------
tab1, tab2, tab3 = st.tabs(["📊 Analyse", "📈 Avancé", "📂 Données"])

# ===========================
# TAB 1 – VISUALISATION
# ===========================
with tab1:

    st.subheader("Analyse des revenus")

    fig1 = px.bar(
        filtered_df,
        x="Region",
        y="Revenue",
        color="Product",
        barmode="group",
        title="Revenue par région et produit"
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(
        filtered_df,
        names="Product",
        values="Revenue",
        title="Distribution des revenus"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ===========================
# TAB 2 – ANALYSE AVANCÉE
# ===========================
with tab2:

    st.subheader("Analyse corrélation")

    fig3 = px.scatter(
        filtered_df,
        x="Revenue",
        y="Profit",
        size="Customers",
        color="Region",
        hover_data=["Product"],
        title="Revenue vs Profit"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Histogramme")

    col_choice = st.selectbox("Choisir variable", ["Revenue", "Profit", "Customers"])

    fig4 = px.histogram(filtered_df, x=col_choice, nbins=30)

    st.plotly_chart(fig4, use_container_width=True)

# ===========================
# TAB 3 – DATA
# ===========================
with tab3:

    st.subheader("Dataset filtré")

    st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Télécharger CSV",
        csv,
        "data.csv",
        "text/csv"
    )

# ---------------------------
# BONUS – SIMULATION IA
# ---------------------------
st.sidebar.header("🤖 Simulation")

simulate = st.sidebar.slider("Augmenter Revenue (%)", 0, 100, 0)

if simulate > 0:
    sim_df = filtered_df.copy()
    sim_df["Revenue"] *= (1 + simulate / 100)

    st.subheader("📈 Simulation Impact")

    fig_sim = px.line(sim_df, y="Revenue", title="Simulation Revenue")

    st.plotly_chart(fig_sim, use_container_width=True)