import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="UrbaniticsAI Transportation CIP Platform MVP v2", layout="wide")

LEVEL_MAP = {"Low": 1, "Medium": 3, "High": 5}
ALIGN_MAP = {"Weak": 1, "Moderate": 3, "Strong": 5}
YES_NO_MAP = {"No": 1, "Yes": 5}
CONDITION_MAP = {"Good": 1, "Fair": 3, "Poor": 5}
LOS_MAP = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 5}

DEFAULT_WEIGHTS = {
    "safety_risk": 20,
    "ada_accessibility": 15,
    "asset_condition": 12,
    "los_performance": 12,
    "demand_need": 8,
    "strategic_alignment": 15,
    "financial_feasibility": 8,
    "equity_impact": 5,
    "community_concern": 5
}

def norm(raw):
    return (raw - 1) / 4 * 100

@st.cache_data
def load_tables():
    projects = pd.read_csv("projects_assets.csv")
    funding = pd.read_csv("funding_sources.csv")
    schedule = pd.read_csv("implementation_schedule.csv")
    demand = pd.read_csv("demand_forecasts.csv")
    dictionary = pd.read_csv("data_dictionary.csv")
    return projects, funding, schedule, demand, dictionary

def calculate_scores(df, demand, weights):
    data = df.merge(demand, on="project_id", how="left")

    data["safety_raw"] = (
        data["safety_risk"].map(LEVEL_MAP).fillna(1) * 0.45
        + data["crash_history_nearby"].map(YES_NO_MAP).fillna(1) * 0.25
        + data["near_school"].map(YES_NO_MAP).fillna(1) * 0.20
        + data["near_transit"].map(YES_NO_MAP).fillna(1) * 0.10
    )
    data["ada_raw"] = data["ada_accessibility_concern"].map(YES_NO_MAP).fillna(1)
    data["condition_raw"] = data["condition"].map(CONDITION_MAP).fillna(1)
    data["los_raw"] = (
        data["current_los"].map(LOS_MAP).fillna(1) * 0.35
        + data["projected_los_no_build"].map(LOS_MAP).fillna(1) * 0.45
        + (6 - data["expected_los_after_project"].map(LOS_MAP).fillna(5)) * 0.20
    )
    data["demand_raw"] = (
        data["demand_growth_level"].map(LEVEL_MAP).fillna(1) * 0.60
        + data["demand_forecast_confidence"].map(LEVEL_MAP).fillna(1) * 0.20
        + data["forecast_year_volume_or_demand"].rank(pct=True) * 5 * 0.20
    )

    alignment_cols = [
        "mtp_alignment", "lrtp_alignment", "complete_streets_alignment", "vision_zero_alignment",
        "ada_transition_plan_alignment", "resilience_alignment", "comp_plan_alignment"
    ]
    data["strategic_alignment_raw"] = data[alignment_cols].apply(lambda row: row.map(ALIGN_MAP).fillna(1).mean(), axis=1)

    data["funding_gap_ratio"] = (data["funding_gap"] / data["estimated_capital_cost"]).clip(0, 1)
    data["om_ratio"] = (data["estimated_annual_om_cost"] / data["estimated_capital_cost"]).clip(0, 0.1)
    data["financial_raw"] = (
        (5 - data["funding_gap_ratio"] * 4) * 0.70
        + (5 - data["om_ratio"] / 0.1 * 4) * 0.30
    )

    data["equity_raw"] = data["equity_priority_area"].map(YES_NO_MAP).fillna(1)
    data["community_raw"] = (
        data["community_concern_level"].map(LEVEL_MAP).fillna(1) * 0.70
        + data["citizen_complaints_count"].clip(0, 15) / 15 * 5 * 0.30
    )

    components = {
        "safety_risk": "safety_raw",
        "ada_accessibility": "ada_raw",
        "asset_condition": "condition_raw",
        "los_performance": "los_raw",
        "demand_need": "demand_raw",
        "strategic_alignment": "strategic_alignment_raw",
        "financial_feasibility": "financial_raw",
        "equity_impact": "equity_raw",
        "community_concern": "community_raw"
    }

    total_weight = sum(weights.values())
    data["priority_score"] = 0.0
    for key, raw_col in components.items():
        score_col = f"{key}_score"
        data[score_col] = data[raw_col].apply(norm)
        data["priority_score"] += data[score_col] * weights[key] / total_weight

    data["priority_score"] = data["priority_score"].round(1)

    def label(score):
        if score >= 85: return "Critical"
        if score >= 70: return "High"
        if score >= 50: return "Medium"
        return "Low"

    data["priority_level"] = data["priority_score"].apply(label)
    data["rank"] = data["priority_score"].rank(method="first", ascending=False).astype(int)
    return data.sort_values("priority_score", ascending=False)

def budget_scenario(scored, budget):
    ranked = scored.sort_values("priority_score", ascending=False).copy()
    ranked["cumulative_cost"] = ranked["estimated_capital_cost"].cumsum()
    ranked["funding_status"] = ranked["cumulative_cost"].apply(lambda x: "Funded" if x <= budget else "Deferred")
    return ranked

projects, funding, schedule, demand, dictionary = load_tables()

st.title("UrbaniticsAI Transportation CIP Platform MVP v2")
st.caption("Integrated reporting, asset inventory, needs assessment, LOS, strategic alignment, financial planning, implementation scheduling, and CIP prioritization.")

with st.sidebar:
    st.header("Scoring Weights")
    weights = {}
    for key, default in DEFAULT_WEIGHTS.items():
        weights[key] = st.slider(key.replace("_", " ").title(), 0, 40, default)

    st.header("Filters")
    district_filter = st.multiselect("District", sorted(projects["district"].unique()))
    asset_filter = st.multiselect("Asset Type", sorted(projects["asset_type"].unique()))

    st.header("Budget Scenario")
    budget = st.number_input("Available CIP budget", min_value=0, value=5000000, step=100000)

filtered_projects = projects.copy()
if district_filter:
    filtered_projects = filtered_projects[filtered_projects["district"].isin(district_filter)]
if asset_filter:
    filtered_projects = filtered_projects[filtered_projects["asset_type"].isin(asset_filter)]

scored = calculate_scores(filtered_projects, demand, weights)

tabs = st.tabs([
    "Executive Overview",
    "Asset Inventory & Needs",
    "LOS & Demand",
    "Strategic Alignment",
    "Financial Plan",
    "Implementation Schedule",
    "CIP Prioritization",
    "Decision Report",
    "Data Schema"
])

with tabs[0]:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Candidate Projects", f"{len(scored):,}")
    c2.metric("Critical/High", f"{len(scored[scored['priority_level'].isin(['Critical','High'])]):,}")
    c3.metric("Capital Need", f"${scored['estimated_capital_cost'].sum()/1000000:.1f}M")
    c4.metric("Annual O&M Impact", f"${scored['estimated_annual_om_cost'].sum()/1000000:.2f}M")
    c5.metric("Funding Gap", f"${scored['funding_gap'].sum()/1000000:.1f}M")
    c6.metric("Avg Score", f"{scored['priority_score'].mean():.1f}")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(scored, x="asset_type", color="priority_level", title="Projects by Asset Type and Priority")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(scored, x="district", y="estimated_capital_cost", color="priority_level",
                           histfunc="sum", title="Capital Need by District")
        st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("Needs Assessment and Asset Inventory")
    summary = scored.groupby(["asset_type", "condition"]).agg(
        assets=("asset_id", "count"),
        capital_need=("estimated_capital_cost", "sum"),
        avg_priority=("priority_score", "mean")
    ).reset_index()
    summary["avg_priority"] = summary["avg_priority"].round(1)
    st.dataframe(summary, use_container_width=True, hide_index=True)

    fig = px.bar(summary, x="asset_type", y="assets", color="condition", title="Condition Assessment by Asset Type")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Inventory Map")
    st.map(scored.rename(columns={"latitude": "lat", "longitude": "lon"})[["lat", "lon"]])

with tabs[2]:
    st.subheader("LOS and Demand Forecasting")
    los_cols = ["project_id", "project_name", "asset_type", "district", "current_los", "projected_los_no_build",
                "expected_los_after_project", "demand_growth_level", "forecast_year", 
                "base_year_volume_or_demand", "forecast_year_volume_or_demand", "demand_forecast_confidence",
                "los_performance_score", "demand_need_score"]
    st.dataframe(scored[los_cols], use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(scored, x="projected_los_no_build", color="asset_type", title="Projected No-Build LOS")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(scored, x="base_year_volume_or_demand", y="forecast_year_volume_or_demand",
                         color="priority_level", hover_name="project_name", title="Demand Growth Context")
        st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("Strategic Alignment")
    alignment_cols = [
        "mtp_alignment", "lrtp_alignment", "complete_streets_alignment", "vision_zero_alignment",
        "ada_transition_plan_alignment", "resilience_alignment", "comp_plan_alignment"
    ]
    display_cols = ["project_id", "project_name", "priority_score", "strategic_alignment_score"] + alignment_cols
    st.dataframe(scored[display_cols], use_container_width=True, hide_index=True)

    alignment_long = scored[alignment_cols].melt(var_name="Plan/Policy", value_name="Alignment")
    fig = px.histogram(alignment_long, x="Plan/Policy", color="Alignment", title="Alignment with Adopted Plans and Policies")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

with tabs[4]:
    st.subheader("Financial and Funding Plan")
    financial_cols = ["project_id", "project_name", "estimated_capital_cost", "estimated_annual_om_cost", 
                      "primary_funding_source", "funding_gap", "financial_feasibility_score", "priority_score"]
    st.dataframe(scored[financial_cols], use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(scored, x="primary_funding_source", y="estimated_capital_cost", histfunc="sum",
                           title="Capital Cost by Funding Source")
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(scored, x="estimated_capital_cost", y="estimated_annual_om_cost",
                         color="priority_level", hover_name="project_name", title="Capital Cost vs Annual O&M Impact")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Funding Source Reference")
    st.dataframe(funding, use_container_width=True, hide_index=True)

with tabs[5]:
    st.subheader("Implementation Schedule")
    joined_schedule = schedule.merge(scored[["project_id", "project_name", "priority_score", "priority_level", "cip_phase"]], on="project_id", how="inner")
    st.dataframe(joined_schedule.sort_values(["project_id", "target_date"]), use_container_width=True, hide_index=True)

    milestone_counts = joined_schedule.groupby(["milestone", "status"]).size().reset_index(name="count")
    fig = px.bar(milestone_counts, x="milestone", y="count", color="status", title="Milestone Status")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

with tabs[6]:
    st.subheader("CIP Prioritization")
    scenario = budget_scenario(scored, budget)
    funded = scenario[scenario["funding_status"] == "Funded"]
    deferred = scenario[scenario["funding_status"] == "Deferred"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Available Budget", f"${budget:,.0f}")
    c2.metric("Funded Projects", f"{len(funded):,}")
    c3.metric("Budget Used", f"${funded['estimated_capital_cost'].sum():,.0f}")
    c4.metric("Deferred Need", f"${deferred['estimated_capital_cost'].sum():,.0f}")

    rank_cols = ["rank", "project_id", "project_name", "asset_type", "district", "priority_score", "priority_level",
                 "estimated_capital_cost", "estimated_annual_om_cost", "funding_gap", "cip_phase", "funding_status"]
    st.dataframe(scenario[rank_cols], use_container_width=True, hide_index=True)

    st.download_button("Download CIP ranked list", scenario[rank_cols].to_csv(index=False), "cip_ranked_projects.csv", "text/csv")

with tabs[7]:
    st.subheader("Decision Justification Report")
    selected = st.selectbox("Select project", scored["project_name"].tolist())
    row = scored[scored["project_name"] == selected].iloc[0]

    st.markdown(f"### {row['project_name']}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Priority Score", row["priority_score"])
    c2.metric("Priority Level", row["priority_level"])
    c3.metric("Capital Cost", f"${row['estimated_capital_cost']:,.0f}")
    c4.metric("Annual O&M", f"${row['estimated_annual_om_cost']:,.0f}")

    breakdown = pd.DataFrame({
        "Criterion": [
            "Safety Risk", "ADA & Accessibility", "Asset Condition", "LOS Performance", "Demand Need",
            "Strategic Alignment", "Financial Feasibility", "Equity Impact", "Community Concern"
        ],
        "Score": [
            row["safety_risk_score"], row["ada_accessibility_score"], row["asset_condition_score"],
            row["los_performance_score"], row["demand_need_score"], row["strategic_alignment_score"],
            row["financial_feasibility_score"], row["equity_impact_score"], row["community_concern_score"]
        ],
        "Weight": [
            weights["safety_risk"], weights["ada_accessibility"], weights["asset_condition"],
            weights["los_performance"], weights["demand_need"], weights["strategic_alignment"],
            weights["financial_feasibility"], weights["equity_impact"], weights["community_concern"]
        ]
    })
    breakdown["Weighted Contribution"] = (breakdown["Score"] * breakdown["Weight"] / sum(weights.values())).round(1)
    st.dataframe(breakdown, use_container_width=True, hide_index=True)

    fig = px.bar(breakdown, x="Criterion", y="Weighted Contribution", title="Priority Score Contribution")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Planning Justification")
    st.write(
        "This project is ranked based on agency-defined priorities across infrastructure condition, safety, ADA/accessibility, "
        "LOS and demand needs, strategic alignment with adopted plans, financial feasibility, equity impact, and structured "
        "community concern. Strategic alignment includes MTP/LRTP consistency, comprehensive plan alignment, Complete Streets, "
        "Vision Zero, ADA transition planning, and resilience goals."
    )

with tabs[8]:
    st.subheader("Database-Style Schema and Input Requirements")
    st.dataframe(dictionary, use_container_width=True, hide_index=True)

    st.markdown("""
    **Core tables in this MVP**
    - `projects_assets.csv`: main asset/project inventory and planning fields
    - `funding_sources.csv`: eligible funding source reference table
    - `implementation_schedule.csv`: phases and milestones
    - `demand_forecasts.csv`: demand and growth assumptions
    - `scoring_config.json`: default scoring weights
    """)
