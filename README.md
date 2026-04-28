# UrbaniticsAI Transportation CIP Platform MVP v2

This MVP expands the earlier prioritization dashboard into a broader transportation capital planning and infrastructure decision-support prototype.

## Platform concept

UrbaniticsAI helps cities and counties connect asset inventory, needs assessment, LOS analysis, demand forecasting, strategic alignment, financial planning, implementation scheduling, and CIP prioritization in one decision-support workflow.

## Included modules

1. Executive overview
2. Needs assessment and asset inventory
3. LOS and demand forecasting
4. Strategic alignment with adopted plans
5. Financial and funding plan
6. Implementation schedule and milestones
7. CIP prioritization and budget scenario
8. Decision justification report
9. Database-style schema and input requirements

## Typical reporting items included

### Financial and funding plan
- Capital cost estimates
- Funding sources
- Funding gaps
- Annual operating and maintenance impact

### LOS
- Current LOS
- Projected no-build LOS
- Expected LOS after project implementation

### Implementation schedule
- Project phases
- Milestones
- Target dates
- Responsible units
- Status

### Needs assessment and asset inventory
- Asset type
- Issue type
- Condition assessment
- Demand forecasting
- Growth context

### Strategic alignment
- Metropolitan Transportation Plan consistency
- Long Range Transportation Plan consistency
- Comprehensive Plan alignment
- Complete Streets alignment
- Vision Zero alignment
- ADA Transition Plan alignment
- Resilience alignment

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub setup

```bash
git init
git add .
git commit -m "Initial UrbaniticsAI Transportation CIP Platform MVP v2"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/urbaniticsai-transport-cip-platform.git
git push -u origin main
```
