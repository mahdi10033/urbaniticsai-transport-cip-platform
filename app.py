
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="UrbaniticsAI Transportation CIP Platform",
    layout="wide"
)

# =====================================================
# UI STYLE
# =====================================================

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

/* Sidebar labels and headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: white !important;
}

/* Keep inputs readable */
section[data-testid="stSidebar"] input {
    color: #111827 !important;
    background-color: white !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #111827 !important;
}

div[data-baseweb="popover"] span,
div[data-baseweb="menu"] span,
ul[role="listbox"] li {
    color: #111827 !important;
}

section[data-testid="stSidebar"] div[data-baseweb="tag"] span {
    color: #111827 !important;
}

section[data-testid="stSidebar"] button {
    color: #111827 !important;
}

section[data-testid="stSidebar"] small {
    color: #DDEAF6 !important;
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

</style>
""", unsafe_allow_html=True)

priority_colors = {
    "Critical": "#B00020",
    "High": "#E65100",
    "Medium": "#F9A825",
    "Low": "#2E7D32"
}

# =====================================================
# SCENARIO WEIGHT PROFILES
# =====================================================

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

# =====================================================
# BASIC SCORING MAPS
# =====================================================

LOW_MED_HIGH_MAP = {"Low": 1, "Medium": 2, "High": 3}
WEAK_MOD_STRONG_MAP = {"Weak": 1, "Moderate": 2, "Strong": 3}
CONDITION_MAP = {"Good": 1, "Fair": 2, "Poor": 3}
LOS_MAP = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}

# =====================================================
# DATA LOADING
# =====================================================

@st.cache_data
def load_default_tables():
    projects = pd.read_csv("projects_assets.csv")
    funding = pd.read_csv("funding_sources.csv")
    schedule = pd.read_csv("implementation_schedule.csv")
    demand = pd.read_csv("demand_forecasts.csv")
    dictionary = pd.read_csv("data_dictionary.csv")
    return projects, funding, schedule, demand, dictionary

def load_uploaded_workbook(uploaded_file):
    try:
        projects = pd.read_excel(uploaded_file, sheet_name="projects_assets")
        uploaded_file.seek(0)
        demand = pd.read_excel(uploaded_file, sheet_name="demand_forecasts")
        uploaded_file.seek(0)

        try:
            schedule = pd.read_excel(uploaded_file, sheet_name="implementation_schedule")
        except Exception:
            schedule = pd.read_csv("implementation_schedule.csv")

        uploaded_file.seek(0)

        try:
            funding = pd.read_excel(uploaded_file, sheet_name="funding_sources")
        except Exception:
            funding = pd.read_csv("funding_sources.csv")

        dictionary = pd.read_csv("data_dictionary.csv")
        return projects, funding, schedule, demand, dictionary, None

    except Exception as e:
        return None, None, None, None, None, str(e)

# =====================================================
# UTILITY SCORING HELPERS
# =====================================================

def binary_score(value, positive_value="Yes"):
    if pd.isna(value):
        return 0
    return 1 if str(value).strip().lower() == str(positive_value).strip().lower() else 0

def ordinal_score(value, mapping):
    if pd.isna(value):
        return 0
    return mapping.get(value, mapping.get(str(value).strip(), 0))

def normalize_raw_score(raw_score, max_score):
    if max_score <= 0:
        return 0
    return round((raw_score / max_score) * 100, 1)

def minmax_normalize(value, min_value, max_value):
    if pd.isna(value) or max_value == min_value:
        return 0
    return round(((value - min_value) / (max_value - min_value)) * 100, 1)

def reverse_minmax_normalize(value, min_value, max_value):
    if pd.isna(value) or max_value == min_value:
        return 100
    return round((1 - ((value - min_value) / (max_value - min_value))) * 100, 1)

def component_table(items):
    df = pd.DataFrame(items)
    raw_total = df["Raw Score"].sum()
    max_total = df["Max Score"].sum()
    normalized = normalize_raw_score(raw_total, max_total)
    return df, raw_total, max_total, normalized

# =====================================================
# TRANSPARENT SUB-SCORE BREAKDOWNS
# =====================================================

def safety_component_breakdown(row):
    items = [
        {"Component": "Safety risk level", "Input Value": row.get("safety_risk"), "Raw Score": ordinal_score(row.get("safety_risk"), LOW_MED_HIGH_MAP), "Max Score": 3, "Logic": "Low=1, Medium=2, High=3"},
        {"Component": "Crash history nearby", "Input Value": row.get("crash_history_nearby"), "Raw Score": binary_score(row.get("crash_history_nearby")), "Max Score": 1, "Logic": "Yes=1, No=0"},
        {"Component": "Near school", "Input Value": row.get("near_school"), "Raw Score": binary_score(row.get("near_school")), "Max Score": 1, "Logic": "Yes=1, No=0"},
        {"Component": "Near transit", "Input Value": row.get("near_transit"), "Raw Score": binary_score(row.get("near_transit")), "Max Score": 1, "Logic": "Yes=1, No=0"},
    ]
    return component_table(items)

def ada_component_breakdown(row):
    items = [{"Component": "ADA/accessibility concern", "Input Value": row.get("ada_accessibility_concern"), "Raw Score": binary_score(row.get("ada_accessibility_concern")), "Max Score": 1, "Logic": "Yes=1, No=0"}]
    return component_table(items)

def condition_component_breakdown(row):
    items = [{"Component": "Asset condition", "Input Value": row.get("condition"), "Raw Score": ordinal_score(row.get("condition"), CONDITION_MAP), "Max Score": 3, "Logic": "Good=1, Fair=2, Poor=3"}]
    return component_table(items)

def los_component_breakdown(row):
    current = LOS_MAP.get(str(row.get("current_los")).strip(), 0)
    nobuild = LOS_MAP.get(str(row.get("projected_los_no_build")).strip(), 0)
    after = LOS_MAP.get(str(row.get("expected_los_after_project")).strip(), 0)
    improvement = max(nobuild - after, 0)

    items = [
        {"Component": "Current LOS severity", "Input Value": row.get("current_los"), "Raw Score": current, "Max Score": 6, "Logic": "A=1, B=2, C=3, D=4, E=5, F=6"},
        {"Component": "Projected no-build LOS severity", "Input Value": row.get("projected_los_no_build"), "Raw Score": nobuild, "Max Score": 6, "Logic": "A=1, B=2, C=3, D=4, E=5, F=6"},
        {"Component": "LOS improvement benefit", "Input Value": f"{row.get('projected_los_no_build')} to {row.get('expected_los_after_project')}", "Raw Score": improvement, "Max Score": 5, "Logic": "No-build LOS score minus after-project LOS score"}
    ]
    return component_table(items)

def demand_component_breakdown(row, scored):
    forecast = row.get("forecast_year_volume_or_demand", 0)
    min_forecast = scored["forecast_year_volume_or_demand"].min() if "forecast_year_volume_or_demand" in scored else forecast
    max_forecast = scored["forecast_year_volume_or_demand"].max() if "forecast_year_volume_or_demand" in scored else forecast
    forecast_norm_0_3 = round(minmax_normalize(forecast, min_forecast, max_forecast) / 100 * 3, 2)

    items = [
        {"Component": "Demand growth level", "Input Value": row.get("demand_growth_level"), "Raw Score": ordinal_score(row.get("demand_growth_level"), LOW_MED_HIGH_MAP), "Max Score": 3, "Logic": "Low=1, Medium=2, High=3"},
        {"Component": "Forecast demand volume", "Input Value": forecast, "Raw Score": forecast_norm_0_3, "Max Score": 3, "Logic": "Min-max normalized across portfolio, then converted to 0-3 scale"}
    ]
    return component_table(items)

def strategic_alignment_component_breakdown(row):
    components = [
        ("MTP alignment", "mtp_alignment"),
        ("LRTP alignment", "lrtp_alignment"),
        ("Complete Streets alignment", "complete_streets_alignment"),
        ("Vision Zero alignment", "vision_zero_alignment"),
        ("ADA Transition Plan alignment", "ada_transition_plan_alignment"),
        ("Resilience strategy alignment", "resilience_alignment"),
        ("Comprehensive plan alignment", "comp_plan_alignment"),
    ]

    items = []
    for label, col in components:
        items.append({
            "Component": label,
            "Input Value": row.get(col),
            "Raw Score": ordinal_score(row.get(col), WEAK_MOD_STRONG_MAP),
            "Max Score": 3,
            "Logic": "Weak=1, Moderate=2, Strong=3"
        })
    return component_table(items)

def financial_component_breakdown(row, scored):
    cap_cost = row.get("estimated_capital_cost", 0)
    gap = row.get("funding_gap", 0)
    om = row.get("estimated_annual_om_cost", 0)

    min_cost, max_cost = scored["estimated_capital_cost"].min(), scored["estimated_capital_cost"].max()
    min_gap, max_gap = scored["funding_gap"].min(), scored["funding_gap"].max()
    min_om, max_om = scored["estimated_annual_om_cost"].min(), scored["estimated_annual_om_cost"].max()

    cost_score = round(reverse_minmax_normalize(cap_cost, min_cost, max_cost) / 100 * 3, 2)
    gap_score = round(reverse_minmax_normalize(gap, min_gap, max_gap) / 100 * 3, 2)
    om_score = round(reverse_minmax_normalize(om, min_om, max_om) / 100 * 3, 2)

    items = [
        {"Component": "Capital cost burden", "Input Value": f"${cap_cost:,.0f}", "Raw Score": cost_score, "Max Score": 3, "Logic": "Reverse min-max. Lower cost receives higher score."},
        {"Component": "Funding gap burden", "Input Value": f"${gap:,.0f}", "Raw Score": gap_score, "Max Score": 3, "Logic": "Reverse min-max. Smaller funding gap receives higher score."},
        {"Component": "Annual O&M burden", "Input Value": f"${om:,.0f}", "Raw Score": om_score, "Max Score": 3, "Logic": "Reverse min-max. Lower annual O&M receives higher score."},
    ]
    return component_table(items)

def equity_component_breakdown(row):
    items = [{"Component": "Equity priority area", "Input Value": row.get("equity_priority_area"), "Raw Score": binary_score(row.get("equity_priority_area")), "Max Score": 1, "Logic": "Yes=1, No=0"}]
    return component_table(items)

def community_component_breakdown(row, scored):
    complaints = row.get("citizen_complaints_count", 0)
    min_complaints = scored["citizen_complaints_count"].min()
    max_complaints = scored["citizen_complaints_count"].max()
    complaint_score = round(minmax_normalize(complaints, min_complaints, max_complaints) / 100 * 3, 2)

    items = [
        {"Component": "Community concern level", "Input Value": row.get("community_concern_level"), "Raw Score": ordinal_score(row.get("community_concern_level"), LOW_MED_HIGH_MAP), "Max Score": 3, "Logic": "Low=1, Medium=2, High=3"},
        {"Component": "Citizen complaint count", "Input Value": complaints, "Raw Score": complaint_score, "Max Score": 3, "Logic": "Min-max normalized across portfolio, then converted to 0-3 scale"}
    ]
    return component_table(items)

def transparent_score_breakdowns(row, scored):
    return {
        "Safety Risk": safety_component_breakdown(row),
        "ADA & Accessibility": ada_component_breakdown(row),
        "Asset Condition": condition_component_breakdown(row),
        "LOS Performance": los_component_breakdown(row),
        "Demand Need": demand_component_breakdown(row, scored),
        "Strategic Alignment": strategic_alignment_component_breakdown(row),
        "Financial Feasibility": financial_component_breakdown(row, scored),
        "Equity Impact": equity_component_breakdown(row),
        "Community Concern": community_component_breakdown(row, scored),
    }

def build_transparent_score_breakdown(row, scored, weights):
    breakdowns = transparent_score_breakdowns(row, scored)

    rows = []
    key_map = {
        "Safety Risk": "safety_risk",
        "ADA & Accessibility": "ada_accessibility",
        "Asset Condition": "asset_condition",
        "LOS Performance": "los_performance",
        "Demand Need": "demand_need",
        "Strategic Alignment": "strategic_alignment",
        "Financial Feasibility": "financial_feasibility",
        "Equity Impact": "equity_impact",
        "Community Concern": "community_concern",
    }

    for criterion, (sub_df, raw_total, max_total, normalized_score) in breakdowns.items():
        weight = weights.get(key_map[criterion], 0)
        contribution = round(normalized_score * weight / 100, 2)

        rows.append({
            "Criterion": criterion,
            "Raw Score": round(raw_total, 2),
            "Maximum Raw Score": round(max_total, 2),
            "Component Score (0-100)": normalized_score,
            "Weight (%)": weight,
            "Weighted Contribution": contribution,
        })

    return pd.DataFrame(rows), breakdowns

# =====================================================
# PRIMARY SCORING ENGINE
# =====================================================

def calculate_scores(projects, demand, weights):
    data = projects.merge(demand, on="project_id", how="left")

    # Ensure quantitative fields exist
    for col in ["forecast_year_volume_or_demand", "estimated_capital_cost", "funding_gap", "estimated_annual_om_cost", "citizen_complaints_count"]:
        if col not in data.columns:
            data[col] = 0

    score_rows = []
    for _, row in data.iterrows():
        summary_df, _ = build_transparent_score_breakdown(row, data, weights)

        record = row.to_dict()

        mapping = {
            "Safety Risk": "safety_risk_score",
            "ADA & Accessibility": "ada_accessibility_score",
            "Asset Condition": "asset_condition_score",
            "LOS Performance": "los_performance_score",
            "Demand Need": "demand_need_score",
            "Strategic Alignment": "strategic_alignment_score",
            "Financial Feasibility": "financial_feasibility_score",
            "Equity Impact": "equity_impact_score",
            "Community Concern": "community_concern_score",
        }

        for _, s in summary_df.iterrows():
            record[mapping[s["Criterion"]]] = s["Component Score (0-100)"]

        record["priority_score"] = round(summary_df["Weighted Contribution"].sum(), 1)

        if record["priority_score"] >= 85:
            record["priority_level"] = "Critical"
        elif record["priority_score"] >= 70:
            record["priority_level"] = "High"
        elif record["priority_score"] >= 50:
            record["priority_level"] = "Medium"
        else:
            record["priority_level"] = "Low"

        record["deferred_5yr_cost"] = round(record.get("estimated_capital_cost", 0) * 1.25, 0)
        record["deferred_cost_increase"] = record["deferred_5yr_cost"] - record.get("estimated_capital_cost", 0)

        score_rows.append(record)

    scored = pd.DataFrame(score_rows)
    scored = scored.sort_values("priority_score", ascending=False).reset_index(drop=True)
    scored["rank"] = scored.index + 1

    return scored

# =====================================================
# EXPLAINABILITY AND NARRATIVE HELPERS
# =====================================================

def risk_indicators(scored):
    return {
        "ADA Exposure": int((scored["ada_accessibility_concern"] == "Yes").sum()),
        "LOS Failure Risk": int(scored["projected_los_no_build"].isin(["E", "F"]).sum()),
        "High Safety Concern": int((scored["safety_risk"] == "High").sum()),
        "Poor Condition Assets": int((scored["condition"] == "Poor").sum()),
        "High Community Concern": int((scored["community_concern_level"] == "High").sum())
    }

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

def generate_project_justification(row):
    return (
        f"{row['project_name']} is recommended as a {row['priority_level']} priority. "
        f"The project scored {row['priority_score']} and ranked #{int(row['rank'])}. "
        f"Primary drivers include {project_why(row)}. "
        f"This explanation is intended as decision-support text for agency review."
    )

def generate_executive_narrative(scored, scenario_name):
    if len(scored) == 0:
        return "No projects are available under the current filters."

    total_need = scored["estimated_capital_cost"].sum()
    gap = scored["funding_gap"].sum()
    critical_high = int(scored["priority_level"].isin(["Critical", "High"]).sum())
    ada = int((scored["ada_accessibility_concern"] == "Yes").sum())
    los_risk = int(scored["projected_los_no_build"].isin(["E", "F"]).sum())
    high_safety = int((scored["safety_risk"] == "High").sum())

    return (
        f"The {scenario_name} analysis identified {len(scored)} candidate transportation infrastructure projects, "
        f"including {critical_high} Critical or High priority projects. The total estimated capital need is ${total_need:,.0f}, "
        f"with a current funding gap of ${gap:,.0f}. The analysis identified {ada} ADA/accessibility-related concerns, "
        f"{los_risk} projected LOS risk projects, and {high_safety} projects with high safety concern."
    )

def generate_funding_risk_summary(scored):
    high_priority = scored[scored["priority_level"].isin(["Critical", "High"])]
    unfunded_high = high_priority[high_priority["funding_gap"] > 0]

    return (
        f"The current project list includes {len(high_priority)} Critical or High priority projects. "
        f"Of these, {len(unfunded_high)} have an identified funding gap. "
        f"The total funding gap across filtered projects is ${scored['funding_gap'].sum():,.0f}."
    )

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
    if row.get("projected_los_no_build") in ["E", "F"]:
        drivers.append(f"Projected no-build LOS of {row.get('projected_los_no_build')} increased the mobility need.")

    if not drivers:
        drivers.append("The project is supported by a balanced mix of planning, asset, funding, and policy factors.")

    if row.get("estimated_capital_cost", 0) >= scored["estimated_capital_cost"].quantile(0.75):
        tradeoffs.append("High capital cost may reduce near-term implementability under constrained budgets.")
    if row.get("funding_gap", 0) >= scored["funding_gap"].quantile(0.75):
        tradeoffs.append("Large funding gap may reduce financial readiness.")
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
        policy.append("No strong strategic alignment category is currently flagged.")

    mobility.append(f"Current LOS: {row.get('current_los')}.")
    mobility.append(f"Projected no-build LOS: {row.get('projected_los_no_build')}.")
    mobility.append(f"Expected LOS after project: {row.get('expected_los_after_project')}.")

    funding.append(f"Primary funding source: {row.get('primary_funding_source')}.")
    funding.append(f"Estimated funding gap: ${row.get('funding_gap', 0):,.0f}.")
    funding.append(f"Estimated annual O&M impact: ${row.get('estimated_annual_om_cost', 0):,.0f}.")

    return drivers, tradeoffs, policy, mobility, funding

def generate_decision_explainability_report(row, drivers, tradeoffs, policy, mobility, funding):
    drivers_text = "\n".join([f"- {x}" for x in drivers])
    tradeoffs_text = "\n".join([f"- {x}" for x in tradeoffs])
    policy_text = "\n".join([f"- {x}" for x in policy])
    mobility_text = "\n".join([f"- {x}" for x in mobility])
    funding_text = "\n".join([f"- {x}" for x in funding])

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

This project ranking reflects the selected criteria weights and available project evidence. The result should be interpreted as decision support for agency review, not as an automatic final funding decision.
"""

def generate_transparent_formula_text(row, summary_df):
    lines = []
    for _, r in summary_df.iterrows():
        lines.append(
            f"{r['Criterion']}: ({r['Raw Score']} / {r['Maximum Raw Score']}) × 100 = {r['Component Score (0-100)']} ; "
            f"{r['Component Score (0-100)']} × {r['Weight (%)']}% = {r['Weighted Contribution']}"
        )

    return (
        "Transparent Priority Score Calculation\n\n"
        + "\n".join(lines)
        + f"\n\nFinal Priority Score = {summary_df['Weighted Contribution'].sum():.2f}"
        + f"\nDisplayed Priority Score = {row.get('priority_score')}"
    )

# =====================================================
# SESSION STATE FOR SCENARIO WEIGHTS
# =====================================================

def load_scenario_weights(scenario_name):
    for key, value in SCENARIOS[scenario_name].items():
        st.session_state[f"weight_{key}"] = int(value)

def initialize_scenario_state(default_scenario="Balanced"):
    if "selected_scenario" not in st.session_state:
        st.session_state["selected_scenario"] = default_scenario
        load_scenario_weights(default_scenario)

def on_scenario_change():
    scenario = st.session_state["scenario_select"]
    st.session_state["selected_scenario"] = scenario
    load_scenario_weights(scenario)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class='urban-hero'>
    <h1>UrbaniticsAI</h1>
    <h3>Transportation Infrastructure Decision Intelligence Platform</h3>
    <p style='margin-bottom:0;'>
    Transportation capital planning, CIP prioritization, strategic alignment, funding analysis, and explainable scoring in one workflow.
    </p>
</div>
""", unsafe_allow_html=True)

st.success("Demo Context: Orange County, Florida public-source-informed transportation planning dataset")
st.warning("This platform provides decision-support analysis for transportation planning and CIP evaluation. Final decisions should remain subject to agency review and policy processes.")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("## UrbaniticsAI")
st.sidebar.caption("CIP Intelligence Platform")
st.sidebar.markdown("---")

uploaded_excel = st.sidebar.file_uploader("Upload agency Excel workbook", type=["xlsx"])

if uploaded_excel:
    projects, funding, schedule, demand, dictionary, error = load_uploaded_workbook(uploaded_excel)
    if error:
        st.sidebar.error("Could not load workbook. Using default sample data.")
        st.sidebar.caption(error)
        projects, funding, schedule, demand, dictionary = load_default_tables()
    else:
        st.sidebar.success("Uploaded workbook loaded successfully.")
else:
    projects, funding, schedule, demand, dictionary = load_default_tables()

st.sidebar.header("Analysis Level")
analysis_level = st.sidebar.radio(
    "Select analysis level",
    ["Portfolio Intelligence", "Project Intelligence"]
)

st.sidebar.header("Scenario")

initialize_scenario_state("Balanced")

scenario_name = st.sidebar.selectbox(
    "Prioritization scenario",
    list(SCENARIOS.keys()),
    index=list(SCENARIOS.keys()).index(st.session_state.get("selected_scenario", "Balanced")),
    key="scenario_select",
    on_change=on_scenario_change,
    help="Selecting a scenario automatically loads its predefined 100% scoring weight profile."
)

base_weights = SCENARIOS[scenario_name].copy()

st.sidebar.header("Scoring Weights (%)")
st.sidebar.caption("Weights must total 100%. Selecting a scenario automatically loads its recommended profile.")

weights = {}

for key, default in base_weights.items():
    state_key = f"weight_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = int(default)

    weights[key] = st.sidebar.slider(
        key.replace("_", " ").title(),
        min_value=0,
        max_value=100,
        step=1,
        key=state_key,
        help="Weight as percentage of the final priority score"
    )

total_weight = sum(weights.values())

if total_weight == 100:
    st.sidebar.success(f"Total Weight: {total_weight}%")
else:
    st.sidebar.error(f"Total Weight: {total_weight}%. Please adjust weights to equal 100%.")

st.sidebar.header("Filters")

district_filter = st.sidebar.multiselect("District", sorted(projects["district"].dropna().unique()))
asset_filter = st.sidebar.multiselect("Asset Type", sorted(projects["asset_type"].dropna().unique()))
priority_filter = st.sidebar.multiselect("Priority Level", ["Critical", "High", "Medium", "Low"])

st.sidebar.header("Budget Scenario")
budget = st.sidebar.number_input("Single-year CIP budget", min_value=0, value=5000000, step=100000)
annual_budget = st.sidebar.number_input("Annual budget for 5-year CIP", min_value=0, value=5000000, step=100000)

if total_weight != 100:
    st.error("Scoring cannot run until the total weight equals 100%. Please adjust the sidebar weights.")
    st.stop()

filtered_projects = projects.copy()

if district_filter:
    filtered_projects = filtered_projects[filtered_projects["district"].isin(district_filter)]

if asset_filter:
    filtered_projects = filtered_projects[filtered_projects["asset_type"].isin(asset_filter)]

scored = calculate_scores(filtered_projects, demand, weights)

if priority_filter:
    scored = scored[scored["priority_level"].isin(priority_filter)]

# =====================================================
# PORTFOLIO INTELLIGENCE
# =====================================================

if analysis_level == "Portfolio Intelligence":

    tabs = st.tabs([
        "Executive Overview",
        "Priority Map",
        "Top Priorities",
        "Portfolio Risk Indicators",
        "Scenario Planning",
        "Asset Inventory & Needs",
        "Mobility Performance",
        "Strategic Alignment",
        "Capital & Funding Strategy",
        "Implementation Schedule",
        "Investment Prioritization",
        "Deferred Maintenance",
        "Data Governance"
    ])

    with tabs[0]:
        st.subheader("Executive Overview")
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
            fig = px.histogram(scored, x="district", y="estimated_capital_cost", color="priority_level", histfunc="sum", title="Capital Need by District", color_discrete_map=priority_colors)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.subheader("Priority Map")
        st.caption("Color represents priority level. Circle size represents priority score.")

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
        fig.update_layout(mapbox_style="carto-positron", margin={"r": 0, "t": 0, "l": 0, "b": 0}, legend_title_text="Priority Level")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Mapped Project List")
        st.dataframe(
            scored[["rank", "project_id", "project_name", "asset_type", "district", "priority_score", "priority_level", "estimated_capital_cost"]],
            use_container_width=True,
            hide_index=True
        )

    with tabs[2]:
        st.subheader("Top Priority Projects")
        top = scored.head(15).copy()
        top["Why prioritized?"] = top.apply(project_why, axis=1)

        st.dataframe(
            top[["rank", "project_id", "project_name", "asset_type", "district", "priority_score", "priority_level", "estimated_capital_cost", "estimated_annual_om_cost", "Why prioritized?"]],
            use_container_width=True,
            hide_index=True
        )

    with tabs[3]:
        st.subheader("Portfolio Risk Indicators")
        st.caption("This page summarizes infrastructure and planning risks across the full transportation project portfolio currently being evaluated.")

        risk = risk_indicators(scored)
        risk_df = pd.DataFrame({"Risk Indicator": list(risk.keys()), "Count": list(risk.values())})
        st.dataframe(risk_df, use_container_width=True, hide_index=True)

        fig = px.bar(risk_df, x="Risk Indicator", y="Count", title="Portfolio-Level Infrastructure Risk Indicators")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[4]:
        st.subheader("Scenario Planning")
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

        st.dataframe(pd.DataFrame(scenario_results), use_container_width=True, hide_index=True)

    with tabs[5]:
        st.subheader("Asset Inventory & Needs")
        summary = scored.groupby(["asset_type", "condition"]).agg(
            assets=("asset_id", "count"),
            capital_need=("estimated_capital_cost", "sum"),
            avg_priority=("priority_score", "mean")
        ).reset_index()
        summary["avg_priority"] = summary["avg_priority"].round(1)
        st.dataframe(summary, use_container_width=True, hide_index=True)

        fig = px.bar(summary, x="asset_type", y="assets", color="condition", title="Condition Assessment by Asset Type")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[6]:
        st.subheader("Mobility Performance")
        cols = ["project_id", "project_name", "asset_type", "district", "current_los", "projected_los_no_build", "expected_los_after_project", "demand_growth_level", "forecast_year", "base_year_volume_or_demand", "forecast_year_volume_or_demand", "los_performance_score", "demand_need_score"]
        existing_cols = [c for c in cols if c in scored.columns]
        st.dataframe(scored[existing_cols], use_container_width=True, hide_index=True)

    with tabs[7]:
        st.subheader("Strategic Alignment")
        alignment_cols = ["mtp_alignment", "lrtp_alignment", "complete_streets_alignment", "vision_zero_alignment", "ada_transition_plan_alignment", "resilience_alignment", "comp_plan_alignment"]
        display_cols = ["project_id", "project_name", "priority_score", "strategic_alignment_score"] + alignment_cols
        st.dataframe(scored[display_cols], use_container_width=True, hide_index=True)

        alignment_long = scored[alignment_cols].melt(var_name="Plan/Policy", value_name="Alignment")
        fig = px.histogram(alignment_long, x="Plan/Policy", color="Alignment", title="Alignment with Adopted Plans and Policies")
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

    with tabs[8]:
        st.subheader("Capital & Funding Strategy")
        financial_cols = ["project_id", "project_name", "estimated_capital_cost", "estimated_annual_om_cost", "primary_funding_source", "funding_gap", "financial_feasibility_score", "priority_score"]
        st.dataframe(scored[financial_cols], use_container_width=True, hide_index=True)

        fig = px.scatter(scored, x="estimated_capital_cost", y="estimated_annual_om_cost", color="priority_level", hover_name="project_name", title="Capital Cost vs Annual O&M Impact", color_discrete_map=priority_colors)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Funding Source Reference")
        st.dataframe(funding, use_container_width=True, hide_index=True)

    with tabs[9]:
        st.subheader("Implementation Schedule")
        joined_schedule = schedule.merge(scored[["project_id", "project_name", "priority_score", "priority_level", "cip_phase"]], on="project_id", how="inner")
        st.dataframe(joined_schedule.sort_values(["project_id", "target_date"]), use_container_width=True, hide_index=True)

    with tabs[10]:
        st.subheader("Investment Prioritization")
        scenario_df = budget_scenario(scored, budget)
        funded = scenario_df[scenario_df["funding_status"] == "Funded"]
        deferred = scenario_df[scenario_df["funding_status"] == "Deferred"]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Available Budget", f"${budget:,.0f}")
        c2.metric("Funded Projects", f"{len(funded):,}")
        c3.metric("Budget Used", f"${funded['estimated_capital_cost'].sum():,.0f}")
        c4.metric("Deferred Need", f"${deferred['estimated_capital_cost'].sum():,.0f}")

        rank_cols = ["rank", "project_id", "project_name", "asset_type", "district", "priority_score", "priority_level", "estimated_capital_cost", "estimated_annual_om_cost", "funding_gap", "cip_phase", "funding_status"]
        st.dataframe(scenario_df[rank_cols], use_container_width=True, hide_index=True)

        st.subheader("5-Year CIP Simulation")
        five_year = multiyear_cip(scored, annual_budget, years=5)
        if len(five_year) > 0:
            st.dataframe(five_year, use_container_width=True, hide_index=True)
        else:
            st.warning("No projects fit within the annual budget.")

    with tabs[11]:
        st.subheader("Deferred Maintenance")
        cols = ["rank", "project_id", "project_name", "priority_score", "priority_level", "estimated_capital_cost", "deferred_5yr_cost", "deferred_cost_increase"]
        st.dataframe(scored[cols], use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        c1.metric("Current Capital Need", f"${scored['estimated_capital_cost'].sum()/1000000:.1f}M")
        c2.metric("Estimated 5-Year Deferred Cost", f"${scored['deferred_5yr_cost'].sum()/1000000:.1f}M")

    with tabs[12]:
        st.subheader("Data Governance")
        st.dataframe(dictionary, use_container_width=True, hide_index=True)

# =====================================================
# PROJECT INTELLIGENCE
# =====================================================

else:
    selected_project = st.sidebar.selectbox(
        "Project for Analysis",
        scored["project_name"].tolist()
    )

    project_row = scored[scored["project_name"] == selected_project].iloc[0]

    tabs = st.tabs([
        "Project Profile",
        "Decision Explainability",
        "Score Breakdown",
        "Sub-Score Logic",
        "AI Planning Narratives",
        "Download Project Report"
    ])

    with tabs[0]:
        st.subheader("Project Profile")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Priority Score", f"{project_row['priority_score']}")
        c2.metric("Priority Level", f"{project_row['priority_level']}")
        c3.metric("Rank", f"#{int(project_row['rank'])}")
        c4.metric("Capital Cost", f"${project_row['estimated_capital_cost']:,.0f}")

        st.dataframe(pd.DataFrame(project_row).reset_index().rename(columns={"index": "Field", project_row.name: "Value"}), use_container_width=True, hide_index=True)

    with tabs[1]:
        st.subheader("Decision Explainability")

        drivers, tradeoffs, policy, mobility, funding_notes = explain_project_drivers(project_row, scored)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Priority Score", f"{project_row['priority_score']}")
        c2.metric("Priority Level", f"{project_row['priority_level']}")
        c3.metric("Current Rank", f"#{int(project_row['rank'])}")
        c4.metric("Funding Gap", f"${project_row['funding_gap']:,.0f}")

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
            for item in funding_notes:
                st.info(item)

        with right:
            st.markdown("### Strategic Alignment")
            for item in policy:
                st.info(item)

        st.markdown("### Board-Ready Explanation")
        explain_report = generate_decision_explainability_report(project_row, drivers, tradeoffs, policy, mobility, funding_notes)
        st.text_area("Editable explanation report", explain_report, height=420)

        st.download_button(
            "Download Decision Explainability Report",
            explain_report,
            f"{project_row['project_id']}_decision_explainability_report.txt",
            "text/plain"
        )

    with tabs[2]:
        st.subheader("Score Breakdown")

        summary_df, detailed_breakdowns = build_transparent_score_breakdown(project_row, scored, weights)
        formula_text = generate_transparent_formula_text(project_row, summary_df)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Final Priority Score", f"{project_row['priority_score']}")
        c2.metric("Calculated Score", f"{summary_df['Weighted Contribution'].sum():.2f}")
        c3.metric("Priority Level", f"{project_row['priority_level']}")
        c4.metric("Rank", f"#{int(project_row['rank'])}")

        st.markdown("### Weighted Contribution Table")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        fig = px.bar(summary_df, x="Criterion", y="Weighted Contribution", text="Weighted Contribution", title="Weighted Contribution to Final Priority Score")
        fig.update_layout(xaxis_tickangle=-35)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Formula")
        st.code(formula_text)

    with tabs[3]:
        st.subheader("Sub-Score Logic")
        st.caption("This tab explains how qualitative and quantitative project inputs are converted into numeric criterion scores.")

        summary_df, detailed_breakdowns = build_transparent_score_breakdown(project_row, scored, weights)

        st.markdown("### Criterion-Level Summary")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        st.markdown("### Detailed Sub-Component Scoring")
        for criterion, (detail_df, raw_total, max_total, normalized_score) in detailed_breakdowns.items():
            with st.expander(f"{criterion}: raw {round(raw_total,2)} / {round(max_total,2)} → {normalized_score}/100"):
                st.dataframe(detail_df, use_container_width=True, hide_index=True)
                st.write(f"Normalized {criterion} score = ({round(raw_total,2)} / {round(max_total,2)}) × 100 = {normalized_score}")

    with tabs[4]:
        st.subheader("AI-Assisted Planning Narratives")
        st.caption("Rule-based narrative generation for explainable planning support.")

        narrative_type = st.selectbox(
            "Narrative Type",
            ["Project Justification", "Executive Summary", "Funding Risk Summary"]
        )

        if narrative_type == "Executive Summary":
            output = generate_executive_narrative(scored, scenario_name)
        elif narrative_type == "Funding Risk Summary":
            output = generate_funding_risk_summary(scored)
        else:
            output = generate_project_justification(project_row)

        st.markdown(f"""
        <div class='ai-narrative-box'>
            <h3>Generated Narrative</h3>
            <p>{output}</p>
        </div>
        """, unsafe_allow_html=True)

        st.text_area("Editable narrative text", output, height=220)

        st.download_button(
            "Download Narrative",
            output,
            f"{project_row['project_id']}_narrative.txt",
            "text/plain"
        )

    with tabs[5]:
        st.subheader("Download Project Report")

        summary_df, detailed_breakdowns = build_transparent_score_breakdown(project_row, scored, weights)
        drivers, tradeoffs, policy, mobility, funding_notes = explain_project_drivers(project_row, scored)

        full_report = f"""UrbaniticsAI Project Intelligence Report

Project: {project_row['project_name']}
Project ID: {project_row['project_id']}
Priority Score: {project_row['priority_score']}
Priority Level: {project_row['priority_level']}
Rank: #{int(project_row['rank'])}
Capital Cost: ${project_row['estimated_capital_cost']:,.0f}
Funding Gap: ${project_row['funding_gap']:,.0f}

Decision Explanation
{generate_decision_explainability_report(project_row, drivers, tradeoffs, policy, mobility, funding_notes)}

Score Breakdown
{generate_transparent_formula_text(project_row, summary_df)}

Criterion Summary
{summary_df.to_string(index=False)}
"""

        st.text_area("Project report preview", full_report, height=520)

        st.download_button(
            "Download Full Project Report",
            full_report,
            f"{project_row['project_id']}_full_project_report.txt",
            "text/plain"
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")
st.markdown(
    "<div class='footer'>UrbaniticsAI | Transportation Infrastructure Decision Intelligence Platform</div>",
    unsafe_allow_html=True
)
