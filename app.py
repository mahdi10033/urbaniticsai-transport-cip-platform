import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="UrbaniticsAI", layout="wide")

st.markdown("""
<style>
.main {
    background-color: #F5F7FA;
}
section[data-testid="stSidebar"] {
    background-color: #1F2A38;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
h1 {
    color: #17324D;
    font-weight: 800;
}
[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #D9E2EC;
}
.hero {
    background: linear-gradient(90deg, #17324D 0%, #274C77 100%);
    padding: 25px;
    border-radius: 16px;
    color: white;
    margin-bottom: 20px;
}
.hero h1 {
    color: white;
}
.narrative-box {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #D9E2EC;
}
</style>
""", unsafe_allow_html=True)

# Logo
logo = Image.open("assets/logo.png")

st.sidebar.image(logo, width=180)
st.sidebar.markdown("## UrbaniticsAI")
st.sidebar.caption("Transportation Infrastructure Decision Intelligence Platform")

# Load data
projects = pd.read_csv("projects_assets.csv")

# Header
col1, col2 = st.columns([1, 6])

with col1:
    st.image(logo, width=120)

with col2:
    st.markdown("""
    <div class='hero'>
        <h1>UrbaniticsAI</h1>
        <h3>
        Transportation Infrastructure Decision Intelligence Platform
        </h3>
        <p>
        Integrating transportation planning, LOS analysis, strategic alignment,
        funding evaluation, and AI-assisted decision support.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.success("Demo Context: Orange County, Florida public-source-informed transportation planning dataset")

tabs = st.tabs([
    "Executive Overview",
    "Priority Map",
    "Investment Prioritization",
    "Mobility Performance",
    "Capital & Funding Strategy",
    "AI Planning Narratives"
])

with tabs[0]:
    st.subheader("Executive Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Candidate Projects", f"{len(projects):,}")
    c2.metric("Capital Need", f"${projects['estimated_capital_cost'].sum()/1000000:.1f}M")
    c3.metric("Funding Gap", f"${projects['funding_gap'].sum()/1000000:.1f}M")

    fig = px.histogram(
        projects,
        x="asset_type",
        title="Projects by Asset Type"
    )
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Priority Map")

    fig = px.scatter_mapbox(
        projects,
        lat="latitude",
        lon="longitude",
        hover_name="project_name",
        color="asset_type",
        size="estimated_capital_cost",
        zoom=8,
        height=600
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("Investment Prioritization")

    st.dataframe(
        projects[[
            "project_name",
            "asset_type",
            "district",
            "estimated_capital_cost",
            "funding_gap"
        ]],
        use_container_width=True
    )

with tabs[3]:
    st.subheader("Mobility Performance")

    st.dataframe(
        projects[[
            "project_name",
            "current_los",
            "projected_los_no_build",
            "expected_los_after_project"
        ]],
        use_container_width=True
    )

with tabs[4]:
    st.subheader("Capital & Funding Strategy")

    fig = px.scatter(
        projects,
        x="estimated_capital_cost",
        y="funding_gap",
        color="asset_type",
        hover_name="project_name"
    )

    st.plotly_chart(fig, use_container_width=True)

with tabs[5]:
    st.subheader("AI-Assisted Planning Narratives")

    selected_project = st.selectbox(
        "Select Project",
        projects["project_name"].tolist()
    )

    narrative = f"""
    {selected_project} is recommended for prioritization due to its transportation planning significance,
    infrastructure condition, funding considerations, and strategic transportation relevance.
    """

    st.markdown(
        f"""
        <div class='narrative-box'>
            <h3>Generated Narrative</h3>
            <p>{narrative}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
st.caption("UrbaniticsAI | Transportation Infrastructure Decision Intelligence Platform")
