import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="UrbaniticsAI Transportation CIP Platform MVP v4", layout="wide")


# -----------------------------
# UrbaniticsAI UI polish
# -----------------------------
priority_colors = {
    "Critical": "#B00020",
    "High": "#E65100",
    "Medium": "#F9A825",
    "Low": "#2E7D32"
}

st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background-color: #1F2A38;
}



section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stFileUploader label {
    color: white !important;
    font-weight: 600;
}

h1 {
    color: #17324D;
    font-weight: 800;
}

h2, h3 {
    color: #274C77;
}

[data-testid="metric-container"] {
    background-color: white;
    border-radius: 14px;
    padding: 16px;
    border: 1px solid #D9E2EC;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
}

.stTabs [data-baseweb="tab"] {
    font-size: 15px;
    padding: 10px 18px;
    font-weight: 600;
}

div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
}

.urban-card {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #D9E2EC;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 16px;
}

.urban-hero {
    background: linear-gradient(90deg, #17324D 0%, #274C77 100%);
    padding: 24px;
    border-radius: 16px;
    color: white;
    margin-bottom: 18px;
}

.urban-hero h1 {
    color: white;
    margin-bottom: 0;
}

.urban-hero h3 {
    color: #DDEAF6;
    margin-top: 4px;
    font-weight: 400;
}

.urban-subtle {
    color: #5A6B7A;
}

.ai-narrative-box {
    background-color: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #D9E2EC;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    line-height: 1.55;
}

.footer {
    color: #5A6B7A;
    font-size: 13px;
    text-align: center;
    padding-top: 20px;
}



/* ===== Sidebar visibility fix ===== */
section[data-testid="stSidebar"] {
    background-color: #1F2A38;
}

/* Sidebar section titles and labels only */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: white !important;
}

/* Input text should stay dark and readable */
section[data-testid="stSidebar"] input {
    color: #111827 !important;
    background-color: white !important;
}

/* Selectbox / multiselect selected text */
section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #111827 !important;
}

/* Dropdown menu text */
div[data-baseweb="popover"] span,
div[data-baseweb="menu"] span,
ul[role="listbox"] li {
    color: #111827 !important;
}

/* Multiselect selected tags */
section[data-testid="stSidebar"] div[data-baseweb="tag"] span {
    color: #111827 !important;
}

/* Number input buttons */
section[data-testid="stSidebar"] button {
    color: #111827 !important;
}

/* Help / uploader small text */
section[data-testid="stSidebar"] small {
    color: #DDEAF6 !important;
}

</style>
""", unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class='urban-hero'>
        <h1>UrbaniticsAI</h1>
        <h3>Transportation Infrastructure Decision Intelligence Platform</h3>
        <p style='margin-bottom:0;'>
        Integrating transportation planning, LOS analysis, strategic alignment, funding evaluation, scenario planning, and AI-assisted decision support into one workflow.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("---")
    st.markdown(
        "<div class='footer'>UrbaniticsAI | Transportation Infrastructure Decision Intelligence Platform</div>",
        unsafe_allow_html=True
    )

def priority_badge_text(level):
    return {
        "Critical": "Critical Priority",
        "High": "High Priority",
        "Medium": "Medium Priority",
        "Low": "Low Priority"
    }.get(level, level)

def highlight_priority_table(df):
    """
    Safely highlight the priority_level column.

    Newer pandas versions removed Styler.applymap and replaced it with Styler.map.
    This helper tries the newer method first and falls back gracefully.
    """
    def style_priority(val):
        if val == "Critical":
            return "background-color: #FFCDD2; color: #7F0000; font-weight: bold;"
        if val == "High":
            return "background-color: #FFE0B2; color: #8A3A00; font-weight: bold;"
        if val == "Medium":
            return "background-color: #FFF9C4; color: #6D5600;"
        if val == "Low":
            return "background-color: #C8E6C9; color: #1B5E20;"
        return ""

    if "priority_level" not in df.columns:
        return df

    styler = df.style
    try:
        return styler.map(style_priority, subset=["priority_level"])
    except AttributeError:
        try:
            return styler.applymap(style_priority, subset=["priority_level"])
        except Exception:
            return df
    except Exception:
        return df


LEVEL_MAP = {"Low": 1, "Medium": 3, "High": 5}
ALIGN_MAP = {"Weak": 1, "Moderate": 3, "Strong": 5}
YES_NO_MAP = {"No": 1, "Yes": 5}
CONDITION_MAP = {"Good": 1, "Fair": 3, "Poor": 5}
LOS_MAP = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 5}

BASE_WEIGHTS = {
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

SCENARIOS = {
    "Balanced": {
        "safety_risk": 20,
        "ada_accessibility": 15,
        "asset_condition": 12,
        "los_performance": 12,
        "demand_need": 8,
        "strategic_alignment": 15,
        "financial_feasibility": 8,
        "equity_impact": 5,
        "community_concern": 5
    },
    "Safety First": {
        "safety_risk": 35,
        "ada_accessibility": 12,
        "asset_condition": 10,
        "los_performance": 12,
        "demand_need": 6,
        "strategic_alignment": 10,
        "financial_feasibility": 5,
        "equity_impact": 5,
        "community_concern": 5
    },
    "ADA & Accessibility First": {
        "safety_risk": 15,
        "ada_accessibility": 35,
        "asset_condition": 10,
        "los_performance": 8,
        "demand_need": 5,
        "strategic_alignment": 12,
        "financial_feasibility": 5,
        "equity_impact": 5,
        "community_concern": 5
    },
    "Financial Feasibility First": {
        "safety_risk": 15,
        "ada_accessibility": 10,
        "asset_condition": 10,
        "los_performance": 10,
        "demand_need": 5,
        "strategic_alignment": 15,
        "financial_feasibility": 25,
        "equity_impact": 5,
        "community_concern": 5
    },
    "Strategic Alignment First": {
        "safety_risk": 15,
        "ada_accessibility": 10,
        "asset_condition": 10,
        "los_performance": 10,
        "demand_need": 8,
        "strategic_alignment": 30,
        "financial_feasibility": 7,
        "equity_impact": 5,
        "community_concern": 5
    }
}

def load_scenario_weights(scenario_name):
    """Load the selected scenario's predefined weights into Streamlit session state."""
    for key, value in SCENARIOS[scenario_name].items():
        st.session_state[f"weight_{key}"] = int(value)

def initialize_scenario_state(default_scenario="Balanced"):
    """Initialize scenario and weight state once."""
    if "selected_scenario" not in st.session_state:
        st.session_state["selected_scenario"] = default_scenario
        load_scenario_weights(default_scenario)

def on_scenario_change():
    """Automatically update all scoring weights when the scenario changes."""
    scenario = st.session_state["scenario_select"]
    st.session_state["selected_scenario"] = scenario
    load_scenario_weights(scenario)



def norm(raw):
    return (raw - 1) / 4 * 100

REQUIRED_PROJECT_COLUMNS = [
    "project_id", "asset_id", "project_name", "asset_type", "issue_type", "district", "corridor_or_location",
    "latitude", "longitude", "condition", "safety_risk", "ada_accessibility_concern", "equity_priority_area",
    "community_concern_level", "citizen_complaints_count", "near_school", "near_transit", "crash_history_nearby",
    "current_los", "projected_los_no_build", "expected_los_after_project", "demand_growth_level",
    "estimated_capital_cost", "estimated_annual_om_cost", "funding_gap", "primary_funding_source",
    "mtp_alignment", "lrtp_alignment", "complete_streets_alignment", "vision_zero_alignment",
    "ada_transition_plan_alignment", "resilience_alignment", "comp_plan_alignment", "project_status",
    "cip_phase", "report_date", "notes"
]
PROJECT_DEFAULTS = {
    "asset_id": "", "project_name": "Unnamed Project", "asset_type": "Roadway", "issue_type": "", "district": "Unassigned",
    "corridor_or_location": "", "latitude": 29.95, "longitude": -81.32, "condition": "Fair", "safety_risk": "Medium",
    "ada_accessibility_concern": "No", "equity_priority_area": "No", "community_concern_level": "Low",
    "citizen_complaints_count": 0, "near_school": "No", "near_transit": "No", "crash_history_nearby": "No",
    "current_los": "C", "projected_los_no_build": "D", "expected_los_after_project": "C", "demand_growth_level": "Medium",
    "estimated_capital_cost": 0, "estimated_annual_om_cost": 0, "funding_gap": 0, "primary_funding_source": "Unfunded",
    "mtp_alignment": "Moderate", "lrtp_alignment": "Moderate", "complete_streets_alignment": "Moderate",
    "vision_zero_alignment": "Moderate", "ada_transition_plan_alignment": "Moderate", "resilience_alignment": "Moderate",
    "comp_plan_alignment": "Moderate", "project_status": "Candidate", "cip_phase": "Short-term 1-3 years",
    "report_date": "", "notes": ""
}
DEMAND_COLUMNS = ["project_id", "base_year_volume_or_demand", "forecast_year_volume_or_demand", "forecast_year", "growth_context", "demand_forecast_confidence"]
SCHEDULE_COLUMNS = ["project_id", "milestone", "target_date", "status", "responsible_unit"]
FUNDING_COLUMNS = ["funding_source_id", "funding_source", "eligible_assets", "typical_match_requirement", "notes"]

def ensure_columns(df, columns, defaults=None):
    defaults = defaults or {}
    df = df.copy()
    for col in columns:
        if col not in df.columns:
            df[col] = defaults.get(col, "")
    return df[columns]

def clean_uploaded_table(df):
    df = df.dropna(how="all").copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df

@st.cache_data
def load_default_tables():
    projects = pd.read_csv("projects_assets.csv")
    funding = pd.read_csv("funding_sources.csv")
    schedule = pd.read_csv("implementation_schedule.csv")
    demand = pd.read_csv("demand_forecasts.csv")
    dictionary = pd.read_csv("data_dictionary.csv")
    return projects, funding, schedule, demand, dictionary

def load_uploaded_excel(uploaded_file, default_funding, default_schedule, default_demand, dictionary):
    workbook = pd.ExcelFile(uploaded_file)
    sheets = {name.lower(): name for name in workbook.sheet_names}
    if "projects_assets" not in sheets:
        st.error("The uploaded workbook must include a sheet named Projects_Assets.")
        return None

    projects = clean_uploaded_table(pd.read_excel(workbook, sheet_name=sheets["projects_assets"]))
    projects = ensure_columns(projects, REQUIRED_PROJECT_COLUMNS, PROJECT_DEFAULTS)
    projects = projects[projects["project_id"].notna() & (projects["project_id"].astype(str).str.strip() != "")]

    if "demand_forecasts" in sheets:
        demand = ensure_columns(clean_uploaded_table(pd.read_excel(workbook, sheet_name=sheets["demand_forecasts"])), DEMAND_COLUMNS)
    else:
        demand = default_demand[default_demand["project_id"].isin(projects["project_id"])].copy()
        if demand.empty:
            demand = pd.DataFrame({
                "project_id": projects["project_id"],
                "base_year_volume_or_demand": 0,
                "forecast_year_volume_or_demand": 0,
                "forecast_year": 2035,
                "growth_context": "Unknown",
                "demand_forecast_confidence": "Medium"
            })

    if "implementation_schedule" in sheets:
        schedule = ensure_columns(clean_uploaded_table(pd.read_excel(workbook, sheet_name=sheets["implementation_schedule"])), SCHEDULE_COLUMNS)
    else:
        schedule = default_schedule[default_schedule["project_id"].isin(projects["project_id"])].copy()
        if schedule.empty:
            schedule = pd.DataFrame(columns=SCHEDULE_COLUMNS)

    if "funding_sources" in sheets:
        funding = ensure_columns(clean_uploaded_table(pd.read_excel(workbook, sheet_name=sheets["funding_sources"])), FUNDING_COLUMNS)
    else:
        funding = default_funding.copy()

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
    if total_weight != 100:
        raise ValueError("Scoring weights must total 100%.")
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

    # Deferred maintenance model for demo purposes
    data["deferred_5yr_cost"] = (data["estimated_capital_cost"] * 1.25).round(0)
    data["deferred_cost_increase"] = data["deferred_5yr_cost"] - data["estimated_capital_cost"]

    return data.sort_values("priority_score", ascending=False)

def budget_scenario(scored, budget):
    ranked = scored.sort_values("priority_score", ascending=False).copy()
    ranked["cumulative_cost"] = ranked["estimated_capital_cost"].cumsum()
    ranked["funding_status"] = ranked["cumulative_cost"].apply(lambda x: "Funded" if x <= budget else "Deferred")
    return ranked

def multiyear_cip(scored, annual_budget, years=5):
    projects = scored.sort_values("priority_score", ascending=False).copy()
    rows = []
    idx = 0
    for y in range(1, years + 1):
        remaining = annual_budget
        while idx < len(projects) and projects.iloc[idx]["estimated_capital_cost"] <= remaining:
            p = projects.iloc[idx]
            rows.append({
                "CIP Year": f"Year {y}",
                "project_id": p["project_id"],
                "project_name": p["project_name"],
                "priority_score": p["priority_score"],
                "priority_level": p["priority_level"],
                "estimated_capital_cost": p["estimated_capital_cost"]
            })
            remaining -= p["estimated_capital_cost"]
            idx += 1
    return pd.DataFrame(rows)

def risk_indicators(scored):
    return {
        "ADA Exposure": int((scored["ada_accessibility_concern"] == "Yes").sum()),
        "LOS Failure Risk": int(scored["projected_los_no_build"].isin(["E", "F"]).sum()),
        "High Safety Concern": int((scored["safety_risk"] == "High").sum()),
        "Poor Condition Assets": int((scored["condition"] == "Poor").sum()),
        "High Community Concern": int((scored["community_concern_level"] == "High").sum())
    }

def project_why(row):
    reasons = []
    if row["safety_risk"] == "High" or row["crash_history_nearby"] == "Yes":
        reasons.append("high safety or crash exposure")
    if row["ada_accessibility_concern"] == "Yes":
        reasons.append("ADA/accessibility concern")
    if row["projected_los_no_build"] in ["E", "F"]:
        reasons.append("projected LOS failure risk")
    if row["strategic_alignment_score"] >= 70:
        reasons.append("strong alignment with adopted plans")
    if row["community_concern_level"] == "High":
        reasons.append("strong agency-recorded community concern")
    if row["condition"] == "Poor":
        reasons.append("poor asset condition")
    return ", ".join(reasons[:4]) if reasons else "balanced need across scoring criteria"

default_projects, default_funding, default_schedule, default_demand, dictionary = load_default_tables()
projects, funding, schedule, demand = default_projects, default_funding, default_schedule, default_demand


def generate_project_justification(row):
    reasons = []
    if row.get("safety_risk") == "High":
        reasons.append("high safety concerns")
    if row.get("ada_accessibility_concern") == "Yes":
        reasons.append("ADA accessibility deficiencies")
    if row.get("projected_los_no_build") in ["E","F"]:
        reasons.append("projected LOS deterioration")
    if row.get("condition") == "Poor":
        reasons.append("poor infrastructure condition")
    if row.get("community_concern_level") == "High":
        reasons.append("strong community concern")
    if row.get("strategic_alignment_score",0) >= 70:
        reasons.append("strong strategic alignment")

    if not reasons:
        reasons.append("multiple transportation planning considerations")

    return (
        f"This project is prioritized due to " +
        ", ".join(reasons) +
        ". The recommendation is based on the platform's integrated transportation planning and CIP prioritization framework."
    )

def generate_executive_summary(scored):
    return (
        f"The analysis identified {len(scored)} candidate projects, including "
        f"{len(scored[scored['priority_level'].isin(['Critical','High'])])} high-priority projects. "
        f"Total estimated capital need is ${scored['estimated_capital_cost'].sum():,.0f}."
    )

def generate_funding_risk(scored):
    return (
        f"The current funding gap across filtered projects is "
        f"${scored['funding_gap'].sum():,.0f}. Deferred implementation may increase future costs."
    )



# =====================================================
# DECISION EXPLAINABILITY ENGINE
# =====================================================

def explain_project_drivers(row, scored):
    drivers = []
    tradeoffs = []
    policy = []
    funding = []
    mobility = []

    if row.get("safety_risk") == "High":
        drivers.append("High safety risk increased the project score.")
    if row.get("crash_history_nearby") == "Yes":
        drivers.append("Nearby crash history strengthened the safety justification.")
    if row.get("ada_accessibility_concern") == "Yes":
        drivers.append("ADA/accessibility concern increased the accessibility priority.")
    if row.get("condition") == "Poor":
        drivers.append("Poor asset condition increased the needs-assessment score.")
    if row.get("community_concern_level") == "High":
        drivers.append("Strong agency-recorded community concern increased the public concern component.")
    if row.get("equity_priority_area") == "Yes":
        drivers.append("Location in an equity priority area increased the equity component.")
    if row.get("projected_los_no_build") in ["E", "F"]:
        drivers.append(f"Projected no-build LOS of {row.get('projected_los_no_build')} increased the mobility/performance need.")
    if row.get("demand_growth_level") == "High":
        drivers.append("High demand-growth context increased the future need score.")
    if row.get("strategic_alignment_score", 0) >= 70:
        drivers.append("Strong strategic alignment increased the policy consistency score.")

    if not drivers:
        drivers.append("The project is supported by a balanced mix of planning, asset, funding, and policy factors.")

    try:
        if row.get("estimated_capital_cost", 0) >= scored["estimated_capital_cost"].quantile(0.75):
            tradeoffs.append("High capital cost may reduce near-term implementability under constrained budgets.")
        if row.get("funding_gap", 0) >= scored["funding_gap"].quantile(0.75):
            tradeoffs.append("Large funding gap may reduce financial readiness.")
        if row.get("estimated_annual_om_cost", 0) >= scored["estimated_annual_om_cost"].quantile(0.75):
            tradeoffs.append("Higher annual operating and maintenance impact may create future fiscal pressure.")
    except Exception:
        pass

    if row.get("financial_feasibility_score", 100) < 45:
        tradeoffs.append("Lower financial feasibility score reduced the final priority score.")
    if row.get("cip_phase") == "Long-term 8-15 years":
        tradeoffs.append("Long-term CIP phase may reduce immediate implementation readiness.")

    if not tradeoffs:
        tradeoffs.append("No major negative tradeoff was identified from the available dataset.")

    alignments = [
        ("mtp_alignment", "Metropolitan Transportation Plan"),
        ("lrtp_alignment", "Long Range Transportation Plan"),
        ("complete_streets_alignment", "Complete Streets"),
        ("vision_zero_alignment", "Vision Zero / safety policy"),
        ("ada_transition_plan_alignment", "ADA Transition Plan"),
        ("resilience_alignment", "resilience strategy"),
        ("comp_plan_alignment", "comprehensive plan"),
    ]

    for col, label in alignments:
        if row.get(col) == "Strong":
            policy.append(f"Strong alignment with {label}.")

    if not policy:
        policy.append("No strong strategic alignment category is currently flagged. Agency review may add local plan references.")

    mobility.append(f"Current LOS: {row.get('current_los')}.")
    mobility.append(f"Projected no-build LOS: {row.get('projected_los_no_build')}.")
    mobility.append(f"Expected LOS after project: {row.get('expected_los_after_project')}.")

    if row.get("primary_funding_source") and row.get("primary_funding_source") != "Unfunded":
        funding.append(f"Primary funding source identified: {row.get('primary_funding_source')}.")
    else:
        funding.append("No clear primary funding source is identified.")

    funding.append(f"Estimated funding gap: ${row.get('funding_gap', 0):,.0f}.")
    funding.append(f"Estimated annual O&M impact: ${row.get('estimated_annual_om_cost', 0):,.0f}.")

    return drivers, tradeoffs, policy, mobility, funding


def generate_decision_explainability_report(row, drivers, tradeoffs, policy, mobility, funding):
    drivers_text = "\\n".join([f"- {x}" for x in drivers])
    tradeoffs_text = "\\n".join([f"- {x}" for x in tradeoffs])
    policy_text = "\\n".join([f"- {x}" for x in policy])
    mobility_text = "\\n".join([f"- {x}" for x in mobility])
    funding_text = "\\n".join([f"- {x}" for x in funding])

    return f"""Decision Explainability Report

Project: {row['project_name']}
Project ID: {row['project_id']}
Priority Score: {row['priority_score']}
Priority Level: {row['priority_level']}
Current Rank: #{int(row['rank'])}
Estimated Capital Cost: ${row['estimated_capital_cost']:,.0f}
Funding Gap: ${row['funding_gap']:,.0f}

Why this project ranked where it did
{drivers_text}

Tradeoffs and factors reducing readiness
{tradeoffs_text}

Mobility and LOS context
{mobility_text}

Strategic alignment
{policy_text}

Funding readiness
{funding_text}

AI-assisted explanation
This project ranking reflects the selected criteria weights and available project evidence. The result should be interpreted as decision support for agency review, not as an automatic final funding decision.
"""



# =====================================================
# TRANSPARENT SCORE CONTRIBUTION ENGINE
# =====================================================

def build_score_breakdown(row, weights):
    breakdown_items = [
        {
            "Criterion": "Safety Risk",
            "Component Score (0-100)": row.get("safety_risk_score", 0),
            "Weight (%)": weights.get("safety_risk", 0),
            "Evidence / Input": f"Safety risk: {row.get('safety_risk')}; Crash history nearby: {row.get('crash_history_nearby')}; Near school: {row.get('near_school')}"
        },
        {
            "Criterion": "ADA & Accessibility",
            "Component Score (0-100)": row.get("ada_accessibility_score", 0),
            "Weight (%)": weights.get("ada_accessibility", 0),
            "Evidence / Input": f"ADA/accessibility concern: {row.get('ada_accessibility_concern')}"
        },
        {
            "Criterion": "Asset Condition",
            "Component Score (0-100)": row.get("asset_condition_score", 0),
            "Weight (%)": weights.get("asset_condition", 0),
            "Evidence / Input": f"Asset condition: {row.get('condition')}"
        },
        {
            "Criterion": "LOS Performance",
            "Component Score (0-100)": row.get("los_performance_score", 0),
            "Weight (%)": weights.get("los_performance", 0),
            "Evidence / Input": f"Current LOS: {row.get('current_los')}; No-build LOS: {row.get('projected_los_no_build')}; Expected after project: {row.get('expected_los_after_project')}"
        },
        {
            "Criterion": "Demand Need",
            "Component Score (0-100)": row.get("demand_need_score", 0),
            "Weight (%)": weights.get("demand_need", 0),
            "Evidence / Input": f"Demand growth level: {row.get('demand_growth_level')}; Forecast demand: {row.get('forecast_year_volume_or_demand')}"
        },
        {
            "Criterion": "Strategic Alignment",
            "Component Score (0-100)": row.get("strategic_alignment_score", 0),
            "Weight (%)": weights.get("strategic_alignment", 0),
            "Evidence / Input": (
                f"MTP: {row.get('mtp_alignment')}; LRTP: {row.get('lrtp_alignment')}; "
                f"Complete Streets: {row.get('complete_streets_alignment')}; Vision Zero: {row.get('vision_zero_alignment')}; "
                f"ADA Plan: {row.get('ada_transition_plan_alignment')}; Resilience: {row.get('resilience_alignment')}; "
                f"Comprehensive Plan: {row.get('comp_plan_alignment')}"
            )
        },
        {
            "Criterion": "Financial Feasibility",
            "Component Score (0-100)": row.get("financial_feasibility_score", 0),
            "Weight (%)": weights.get("financial_feasibility", 0),
            "Evidence / Input": f"Capital cost: ${row.get('estimated_capital_cost', 0):,.0f}; Funding gap: ${row.get('funding_gap', 0):,.0f}; Annual O&M: ${row.get('estimated_annual_om_cost', 0):,.0f}"
        },
        {
            "Criterion": "Equity Impact",
            "Component Score (0-100)": row.get("equity_impact_score", 0),
            "Weight (%)": weights.get("equity_impact", 0),
            "Evidence / Input": f"Equity priority area: {row.get('equity_priority_area')}"
        },
        {
            "Criterion": "Community Concern",
            "Component Score (0-100)": row.get("community_concern_score", 0),
            "Weight (%)": weights.get("community_concern", 0),
            "Evidence / Input": f"Community concern: {row.get('community_concern_level')}; Complaints: {row.get('citizen_complaints_count')}"
        },
    ]

    df = pd.DataFrame(breakdown_items)
    df["Component Score (0-100)"] = pd.to_numeric(df["Component Score (0-100)"], errors="coerce").fillna(0).round(1)
    df["Weight (%)"] = pd.to_numeric(df["Weight (%)"], errors="coerce").fillna(0).round(1)
    df["Weighted Contribution"] = (df["Component Score (0-100)"] * df["Weight (%)"] / 100).round(2)
    df["Maximum Possible Contribution"] = df["Weight (%)"]
    return df


def generate_score_formula_text(row, breakdown_df):
    lines = []
    for _, r in breakdown_df.iterrows():
        lines.append(
            f"{r['Criterion']}: {r['Component Score (0-100)']:.1f} × {r['Weight (%)']:.1f}% = {r['Weighted Contribution']:.2f}"
        )

    calculated_score = breakdown_df["Weighted Contribution"].sum()

    return (
        "Priority Score Calculation\n\n"
        + "\n".join(lines)
        + f"\n\nFinal Priority Score = {calculated_score:.2f}"
        + f"\nDisplayed Priority Score = {row.get('priority_score')}"
    )


def component_scoring_explanations():
    return {
        "Safety Risk": "Safety uses safety risk, crash history, school proximity, and transit context. Higher-risk conditions increase the component score.",
        "ADA & Accessibility": "ADA/accessibility is higher when the project addresses accessibility barriers, sidewalk gaps, curb ramps, or transit access deficiencies.",
        "Asset Condition": "Asset condition converts Good/Fair/Poor into a numeric needs score. Poorer condition increases priority.",
        "LOS Performance": "LOS performance uses current LOS, projected no-build LOS, and expected LOS after the project. Poorer no-build LOS and stronger improvement increase the score.",
        "Demand Need": "Demand need uses growth level, forecast confidence, and relative forecast demand. Higher growth and demand increase priority.",
        "Strategic Alignment": "Strategic alignment converts plan consistency indicators, such as Vision Zero, Complete Streets, MTP/LRTP, ADA, resilience, and comprehensive plan alignment into a numeric score.",
        "Financial Feasibility": "Financial feasibility is higher when the funding gap is smaller and annual O&M burden is more manageable.",
        "Equity Impact": "Equity impact is higher when the project serves an identified equity priority area.",
        "Community Concern": "Community concern uses agency-recorded concern level and complaint count."
    }


render_header()

st.success("Demo Context: Orange County, Florida public-source-informed transportation planning dataset")
st.warning("This platform provides decision-support analysis for transportation planning and CIP evaluation. Final decisions should remain subject to agency review and policy processes.")

with st.sidebar:
    st.header("Data Upload")
    uploaded_excel = st.file_uploader("Upload CIP Excel template", type=["xlsx"])
    try:
        with open("urbaniticsai_cip_data_intake_template.xlsx", "rb") as template_file:
            st.download_button(
                "Download blank Excel template",
                data=template_file,
                file_name="urbaniticsai_cip_data_intake_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except FileNotFoundError:
        st.caption("Template file is not available in this deployment.")

    if uploaded_excel is not None:
        uploaded_tables = load_uploaded_excel(uploaded_excel, default_funding, default_schedule, default_demand, dictionary)
        if uploaded_tables is not None:
            projects, funding, schedule, demand, dictionary = uploaded_tables
            st.success(f"Loaded {len(projects)} projects from uploaded workbook.")
        else:
            projects, funding, schedule, demand = default_projects, default_funding, default_schedule, default_demand
    else:
        st.info("Using sample data. Upload the Excel template to analyze agency data.")

    st.header("Scenario")

    initialize_scenario_state("Balanced")

    scenario_name = st.selectbox(
        "Prioritization scenario",
        list(SCENARIOS.keys()),
        index=list(SCENARIOS.keys()).index(st.session_state.get("selected_scenario", "Balanced")),
        key="scenario_select",
        on_change=on_scenario_change,
        help="Selecting a scenario automatically loads its predefined 100% scoring weight profile."
    )

    base_weights = SCENARIOS[scenario_name].copy()

    st.header("Scoring Weights (%)")

    st.caption("Weights must total 100%. Selecting a predefined scenario automatically loads its recommended weight profile. You may adjust weights manually, but the total must remain 100%.")

    weights = {}

    for key, default in base_weights.items():
        state_key = f"weight_{key}"
        if state_key not in st.session_state:
            st.session_state[state_key] = int(default)

        weights[key] = st.slider(
            key.replace("_", " ").title(),
            min_value=0,
            max_value=100,
            step=1,
            key=state_key,
            help="Weight as percentage of the total priority score"
        )

    total_weight = sum(weights.values())

    if total_weight == 100:
        st.success(f"Total Weight: {total_weight}%")
    else:
        st.error(f"Total Weight: {total_weight}%. Please adjust the weights so the total equals 100%.")

    with st.expander("Current Scenario Profile"):
        st.write(f"**Selected Scenario:** {scenario_name}")
        st.write("The weights shown above were loaded from the selected scenario profile. Manual edits are allowed, but the total must remain 100%.")

    st.header("Filters")
    district_filter = st.multiselect("District", sorted(projects["district"].unique()))
    asset_filter = st.multiselect("Asset Type", sorted(projects["asset_type"].unique()))
    priority_filter = st.multiselect("Priority Level", ["Critical", "High", "Medium", "Low"])

    st.header("Budget Scenario")
    budget = st.number_input("Single-year CIP budget", min_value=0, value=5000000, step=100000)
    annual_budget = st.number_input("Annual budget for 5-year CIP", min_value=0, value=5000000, step=100000)

filtered_projects = projects.copy()
if district_filter:
    filtered_projects = filtered_projects[filtered_projects["district"].isin(district_filter)]
if asset_filter:
    filtered_projects = filtered_projects[filtered_projects["asset_type"].isin(asset_filter)]

if sum(weights.values()) != 100:
    st.error("Scoring cannot run until the total weight equals 100%. Please adjust the sidebar weights.")
    st.stop()

scored_all = calculate_scores(filtered_projects, demand, weights)
scored = scored_all.copy()
if priority_filter:
    scored = scored[scored["priority_level"].isin(priority_filter)]

tabs = st.tabs([
    "Executive Overview",
    "Priority Map",
    "Top Priorities",
    "Risk Indicators",
    "Scenario Planning",
    "Decision Explainability",
    "Score Breakdown",
    "Asset Inventory & Needs",
    "Mobility Performance",
    "Strategic Alignment",
    "Capital & Funding Strategy",
    "Implementation Schedule",
    "Investment Prioritization",
    "Deferred Maintenance",
    "AI Planning Narratives",
    "Data Governance"
])

with tabs[0]:
    st.info("This executive dashboard summarizes CIP candidate projects, priority levels, capital needs, funding gaps, O&M impacts, and key transportation risk indicators.")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("CIP Candidate Projects", f"{len(scored):,}")
    c2.metric("Critical/High", f"{len(scored[scored['priority_level'].isin(['Critical','High'])]):,}")
    c3.metric("Capital Need", f"${scored['estimated_capital_cost'].sum()/1000000:.1f}M")
    c4.metric("Annual O&M Impact", f"${scored['estimated_annual_om_cost'].sum()/1000000:.2f}M")
    c5.metric("Funding Gap", f"${scored['funding_gap'].sum()/1000000:.1f}M")
    c6.metric("Average Priority Score", f"{scored['priority_score'].mean():.1f}")

    risk = risk_indicators(scored)
    st.subheader("Executive Risk Snapshot")
    rcols = st.columns(5)
    for col, (label, value) in zip(rcols, risk.items()):
        col.metric(label, value)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(scored, x="asset_type", color="priority_level", title="Projects by Asset Type and Priority", color_discrete_map=priority_colors)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.histogram(scored, x="district", y="estimated_capital_cost", color="priority_level",
                           histfunc="sum", title="Capital Need by District")
        st.plotly_chart(fig, use_container_width=True)


with tabs[1]:
    st.subheader("Priority Map")
    st.caption("Color represents priority level. Circle size represents priority score. The table below keeps the ranked project list visible for planners and managers.")

    fig = px.scatter_mapbox(
        scored,
        lat="latitude",
        lon="longitude",
        color="priority_level",
        size="priority_score",
        hover_name="project_name",
        hover_data={
            "asset_type": True,
            "district": True,
            "priority_score": True,
            "priority_level": True,
            "estimated_capital_cost": ":,.0f",
            "latitude": False,
            "longitude": False
        },
        color_discrete_map=priority_colors,
        size_max=32,
        zoom=8,
        height=650
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend_title_text="Priority Level"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Mapped Project List")

    map_table_cols = [
        "rank",
        "project_id",
        "project_name",
        "asset_type",
        "district",
        "priority_score",
        "priority_level",
        "estimated_capital_cost"
    ]

    st.dataframe(
        scored[map_table_cols],
        use_container_width=True,
        hide_index=True
    )


with tabs[2]:
    st.subheader("Top Priority Projects")
    st.caption("Projects are ranked using the selected scenario weights. The explanation column helps support board, commission, grant, and staff-level discussions.")
    top = scored.head(15).copy()
    top["Why prioritized?"] = top.apply(project_why, axis=1)
    cols = ["rank", "project_id", "project_name", "asset_type", "district", "priority_score", "priority_level",
            "estimated_capital_cost", "estimated_annual_om_cost", "Why prioritized?"]
    st.dataframe(highlight_priority_table(top[cols]), use_container_width=True, hide_index=True)

    fig = px.bar(top, x="project_name", y="priority_score", color="priority_level", title="Top Priority Scores")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("Risk Indicators")
    risk = risk_indicators(scored)
    risk_df = pd.DataFrame({"Risk Indicator": list(risk.keys()), "Count": list(risk.values())})
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    fig = px.bar(risk_df, x="Risk Indicator", y="Count", title="Infrastructure and Planning Risk Indicators")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    These indicators help managers and elected officials quickly understand the scale of risk exposure across ADA,
    LOS, safety, condition, and community concern dimensions.
    """)

with tabs[4]:
    st.subheader("Scenario Planning Engine")
    st.write(f"Current scenario: **{scenario_name}**")

    scenario_results = []
    for name, w in SCENARIOS.items():
        temp = calculate_scores(filtered_projects, demand, w)
        scenario_results.append({
            "Scenario": name,
            "Average Priority Score": round(temp["priority_score"].mean(), 1),
            "Critical/High Projects": int(temp["priority_level"].isin(["Critical", "High"]).sum()),
            "Top Project": temp.iloc[0]["project_name"],
            "Top Project Score": temp.iloc[0]["priority_score"]
        })
    scenario_df = pd.DataFrame(scenario_results)
    st.dataframe(scenario_df, use_container_width=True, hide_index=True)

    top_compare = []
    for name, w in SCENARIOS.items():
        temp = calculate_scores(filtered_projects, demand, w).head(10)
        for _, row in temp.iterrows():
            top_compare.append({"Scenario": name, "Project": row["project_name"], "Score": row["priority_score"]})
    top_compare_df = pd.DataFrame(top_compare)
    fig = px.bar(top_compare_df, x="Project", y="Score", color="Scenario", barmode="group", title="Top 10 Project Scores by Scenario")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)


with tabs[5]:
    st.subheader("Decision Explainability")
    st.caption("Explain why a project ranked where it did, including score drivers, tradeoffs, LOS context, policy alignment, and funding readiness.")

    selected_explain_project = st.selectbox(
        "Select a project to explain",
        scored["project_name"].tolist(),
        key="decision_explainability_project"
    )

    explain_row = scored[scored["project_name"] == selected_explain_project].iloc[0]
    drivers, tradeoffs, policy, mobility, funding = explain_project_drivers(explain_row, scored)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Priority Score", f"{explain_row['priority_score']}")
    c2.metric("Priority Level", f"{explain_row['priority_level']}")
    c3.metric("Current Rank", f"#{int(explain_row['rank'])}")
    c4.metric("Funding Gap", f"${explain_row['funding_gap']:,.0f}")

    st.markdown("### Main Drivers of Ranking")
    for item in drivers:
        st.success(item)

    st.markdown("### Tradeoffs / Factors Reducing Readiness")
    for item in tradeoffs:
        st.warning(item)

    left, right = st.columns(2)

    with left:
        st.markdown("### Mobility and LOS Context")
        for item in mobility:
            st.info(item)

        st.markdown("### Funding Readiness")
        for item in funding:
            st.info(item)

    with right:
        st.markdown("### Strategic Alignment")
        for item in policy:
            st.info(item)

        st.markdown("### Scenario Sensitivity")
        st.info("Current version explains the selected scenario. Next version can compare ranks across all weighting scenarios.")

    
    st.markdown("### Numeric Score Contribution Summary")
    mini_breakdown = build_score_breakdown(explain_row, weights)
    st.dataframe(
        mini_breakdown[["Criterion", "Component Score (0-100)", "Weight (%)", "Weighted Contribution"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Board-Ready Explanation")
    explain_report = generate_decision_explainability_report(explain_row, drivers, tradeoffs, policy, mobility, funding)
    st.text_area("Editable explanation report", explain_report, height=420)

    st.download_button(
        "Download Decision Explainability Report",
        explain_report,
        f"{explain_row['project_id']}_decision_explainability_report.txt",
        "text/plain",
        key="download_decision_explainability"
    )

    st.info("This module supports transparent human decision-making. It explains the score, but does not make final funding decisions.")



with tabs[6]:
    st.subheader("Transparent Score Breakdown")
    st.caption("This module shows exactly how each criterion contributes numeric points to the final priority score.")

    selected_score_project = st.selectbox(
        "Select a project for score breakdown",
        scored["project_name"].tolist(),
        key="score_breakdown_project"
    )

    score_row = scored[scored["project_name"] == selected_score_project].iloc[0]
    breakdown_df = build_score_breakdown(score_row, weights)
    formula_text = generate_score_formula_text(score_row, breakdown_df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Final Priority Score", f"{score_row['priority_score']}")
    c2.metric("Calculated Score", f"{breakdown_df['Weighted Contribution'].sum():.2f}")
    c3.metric("Priority Level", f"{score_row['priority_level']}")
    c4.metric("Current Rank", f"#{int(score_row['rank'])}")

    st.markdown("### Weighted Contribution Table")
    st.dataframe(
        breakdown_df[
            [
                "Criterion",
                "Component Score (0-100)",
                "Weight (%)",
                "Weighted Contribution",
                "Maximum Possible Contribution",
                "Evidence / Input"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Score Contribution Chart")
    fig = px.bar(
        breakdown_df,
        x="Criterion",
        y="Weighted Contribution",
        title="Point Contribution to Final Priority Score",
        text="Weighted Contribution"
    )
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Formula")
    st.code(formula_text)

    st.markdown("### How Qualitative Inputs Become Scores")
    for criterion, explanation in component_scoring_explanations().items():
        with st.expander(criterion):
            st.write(explanation)

    score_report = f"""Transparent Score Breakdown Report

Project: {score_row['project_name']}
Project ID: {score_row['project_id']}
Priority Level: {score_row['priority_level']}
Rank: #{int(score_row['rank'])}

{formula_text}

Detailed Contributions:
{breakdown_df.to_string(index=False)}
"""

    st.download_button(
        "Download Score Breakdown Report",
        score_report,
        f"{score_row['project_id']}_score_breakdown_report.txt",
        "text/plain",
        key="download_score_breakdown"
    )


with tabs[7]:
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

with tabs[8]:
    st.subheader("LOS and Demand Forecasting")
    los_cols = ["project_id", "project_name", "asset_type", "district", "current_los", "projected_los_no_build",
                "expected_los_after_project", "demand_growth_level", "forecast_year",
                "base_year_volume_or_demand", "forecast_year_volume_or_demand", "demand_forecast_confidence",
                "los_performance_score", "demand_need_score"]
    st.dataframe(highlight_priority_table(scored[los_cols]), use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(scored, x="projected_los_no_build", color="asset_type", title="Projected No-Build LOS")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.scatter(scored, x="base_year_volume_or_demand", y="forecast_year_volume_or_demand",
                         color="priority_level", hover_name="project_name", title="Demand Growth Context")
        st.plotly_chart(fig, use_container_width=True)

with tabs[9]:
    st.subheader("Strategic Alignment")
    alignment_cols = [
        "mtp_alignment", "lrtp_alignment", "complete_streets_alignment", "vision_zero_alignment",
        "ada_transition_plan_alignment", "resilience_alignment", "comp_plan_alignment"
    ]
    display_cols = ["project_id", "project_name", "priority_score", "strategic_alignment_score"] + alignment_cols
    st.dataframe(highlight_priority_table(scored[display_cols]), use_container_width=True, hide_index=True)

    alignment_long = scored[alignment_cols].melt(var_name="Plan/Policy", value_name="Alignment")
    fig = px.histogram(alignment_long, x="Plan/Policy", color="Alignment", title="Alignment with Adopted Plans and Policies")
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

with tabs[10]:
    st.subheader("Financial and Funding Plan")
    financial_cols = ["project_id", "project_name", "estimated_capital_cost", "estimated_annual_om_cost",
                      "primary_funding_source", "funding_gap", "financial_feasibility_score", "priority_score"]
    st.dataframe(highlight_priority_table(scored[financial_cols]), use_container_width=True, hide_index=True)

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

with tabs[11]:
    st.subheader("Implementation Schedule")
    joined_schedule = schedule.merge(scored[["project_id", "project_name", "priority_score", "priority_level", "cip_phase"]], on="project_id", how="inner")
    if joined_schedule.empty:
        st.info("No implementation schedule records are available for the selected projects.")
    else:
        st.dataframe(joined_schedule.sort_values(["project_id", "target_date"]), use_container_width=True, hide_index=True)
        milestone_counts = joined_schedule.groupby(["milestone", "status"]).size().reset_index(name="count")
        fig = px.bar(milestone_counts, x="milestone", y="count", color="status", title="Milestone Status")
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

with tabs[12]:
    st.subheader("CIP Prioritization and Budget Scenario")
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
    st.dataframe(highlight_priority_table(scenario[rank_cols]), use_container_width=True, hide_index=True)

    st.subheader("5-Year CIP Simulation")
    five_year = multiyear_cip(scored, annual_budget, years=5)
    if len(five_year) > 0:
        st.dataframe(five_year, use_container_width=True, hide_index=True)
        yearly = five_year.groupby("CIP Year").agg(
            projects=("project_id", "count"),
            capital_cost=("estimated_capital_cost", "sum")
        ).reset_index()
        fig = px.bar(yearly, x="CIP Year", y="capital_cost", title="5-Year Programmed Capital Cost")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No projects fit within the annual budget.")

    st.download_button("Download CIP ranked list", scenario[rank_cols].to_csv(index=False), "cip_ranked_projects.csv", "text/csv")

with tabs[13]:
    st.subheader("Deferred Maintenance Analysis")
    cols = ["rank", "project_id", "project_name", "priority_score", "priority_level", "estimated_capital_cost", "deferred_5yr_cost", "deferred_cost_increase"]
    st.dataframe(scored[cols], use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    c1.metric("Current Capital Need", f"${scored['estimated_capital_cost'].sum()/1000000:.1f}M")
    c2.metric("Estimated 5-Year Deferred Cost", f"${scored['deferred_5yr_cost'].sum()/1000000:.1f}M")
    fig = px.scatter(scored, x="estimated_capital_cost", y="deferred_cost_increase",
                     color="priority_level", hover_name="project_name", title="Estimated Cost of Deferral")
    st.plotly_chart(fig, use_container_width=True)

with tabs[12]:
    st.subheader("Executive Summary Export")
    top = scored.head(10).copy()
    top["Why prioritized?"] = top.apply(project_why, axis=1)

    report = f"""UrbaniticsAI Transportation CIP Platform - Executive Summary

Scenario: {scenario_name}

Key Metrics
- CIP Candidate Projects: {len(scored)}
- Critical/High Projects: {len(scored[scored['priority_level'].isin(['Critical','High'])])}
- Total Capital Need: ${scored['estimated_capital_cost'].sum():,.0f}
- Annual O&M Impact: ${scored['estimated_annual_om_cost'].sum():,.0f}
- Funding Gap: ${scored['funding_gap'].sum():,.0f}
- Average Priority Score: {scored['priority_score'].mean():.1f}

Risk Snapshot
- ADA Exposure: {risk_indicators(scored)['ADA Exposure']}
- LOS Failure Risk: {risk_indicators(scored)['LOS Failure Risk']}
- High Safety Concern: {risk_indicators(scored)['High Safety Concern']}
- Poor Condition Assets: {risk_indicators(scored)['Poor Condition Assets']}
- High Community Concern: {risk_indicators(scored)['High Community Concern']}

Top Priority Projects
"""
    for _, r in top.iterrows():
        report += f"- {int(r['rank'])}. {r['project_name']} | Score: {r['priority_score']} | Cost: ${r['estimated_capital_cost']:,.0f} | Why: {r['Why prioritized?']}\n"

    report += """

Planning Interpretation
The platform integrates asset condition, LOS and demand forecasting, strategic plan alignment, financial and funding considerations, implementation scheduling, equity, and structured community concern into one defensible CIP prioritization workflow.
"""

    st.text_area("Executive summary text", report, height=500)
    st.download_button("Download executive summary", report, "urbaniticsai_executive_summary.txt", "text/plain")

with tabs[15]:
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



with tabs[14]:
    st.subheader("AI-Assisted Planning Narratives")
    st.caption("Rule-based narrative generation for explainable planning support.")

    narrative_type = st.selectbox(
        "Narrative Type",
        [
            "Executive Summary",
            "Funding Risk Summary",
            "Project Justification"
        ]
    )

    if narrative_type == "Executive Summary":
        output = generate_executive_summary(scored)

    elif narrative_type == "Funding Risk Summary":
        output = generate_funding_risk(scored)

    else:
        selected_project = st.selectbox(
            "Select Project",
            scored["project_name"].tolist()
        )
        row = scored[scored["project_name"] == selected_project].iloc[0]
        output = generate_project_justification(row)

    st.markdown(f"""
    <div class='ai-narrative-box'>
        <h3>AI-Assisted Planning Narrative</h3>
        <p>{output}</p>
    </div>
    """, unsafe_allow_html=True)
    st.text_area("Editable narrative text", output, height=220)

    st.download_button(
        "Download Narrative",
        output,
        "urbaniticsai_narrative.txt",
        "text/plain"
    )

    st.info(
        "This feature provides AI-assisted planning support narratives and does not make automatic final decisions."
    )