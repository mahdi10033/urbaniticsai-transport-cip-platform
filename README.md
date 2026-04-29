# UrbaniticsAI Transportation CIP Platform MVP v4

This version adds investor-ready and government-ready features to the earlier MVP.

## Added in v3

- Map-centered project view
- Top priority project panel
- "Why prioritized?" explanations
- Executive risk indicators
- Scenario planning engine
- Safety-first, ADA-first, financial-first, and strategic-alignment-first scenarios
- Single-year budget scenario
- 5-year CIP funding simulation
- Deferred maintenance analysis
- Executive summary export

## Core platform modules

1. Executive overview
2. Map center
3. Top priorities
4. Risk indicators
5. Scenario planning
6. Asset inventory and needs assessment
7. LOS and demand forecasting
8. Strategic alignment
9. Financial and funding plan
10. Implementation schedule
11. CIP prioritization
12. Deferred maintenance analysis
13. Executive export
14. Data schema

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub setup

```bash
git init
git add .
git commit -m "UrbaniticsAI Transportation CIP Platform MVP v4"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/urbaniticsai-transport-cip-platform.git
git push -u origin main
```

## Deployment

Deploy through Streamlit Community Cloud using `app.py` as the main file.


## Added in v4

- Excel upload button in the Streamlit sidebar
- Downloadable Excel data intake template
- Support for agency-provided `Projects_Assets`, `Demand_Forecasts`, `Implementation_Schedule`, and `Funding_Sources` sheets
- Fallback defaults for optional sheets and missing optional columns

## Excel upload workflow

1. Download `urbaniticsai_cip_data_intake_template.xlsx`.
2. Fill the `Projects_Assets` sheet.
3. Optionally fill `Demand_Forecasts`, `Implementation_Schedule`, and `Funding_Sources`.
4. Upload the completed workbook in the app sidebar.


## Configurable Strategic Alignment Framework

The platform now supports configurable strategic alignment scoring rather than hard-coded policy initiatives.

Agencies can customize strategic priorities such as:
- Vision Zero
- Complete Streets
- ADA Transition Plans
- Metropolitan Transportation Plans (MTPs)
- Long Range Transportation Plans (LRTPs)
- Resilience strategies
- Equity strategies
- Transit-supportive development goals

This allows the platform to adapt to different agency priorities and policy environments.


## v6 AI-Assisted Narrative Features

This version adds:
- Executive summary generator
- Funding risk summary generator
- Project justification generator

These are lightweight explainable AI-assisted planning support features that do not require external APIs.


## v8 update: Decision Explainability

This version adds a dedicated Decision Explainability module that helps agencies understand and communicate why a project ranked where it did.

The module produces:
- score drivers
- readiness tradeoffs
- LOS and mobility context
- policy alignment notes
- funding readiness notes
- exportable board-ready explanation text
