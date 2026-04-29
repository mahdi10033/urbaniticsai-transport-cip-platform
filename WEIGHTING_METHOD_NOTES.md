# Weighting Method Update v10

This version changes the scoring weights to explicit percentages.

## Rule

All scoring weights must total exactly 100%.

## Why

This makes the prioritization framework more transparent and defensible for public-sector users.

Instead of arbitrary weighting units, agencies can say:

- Safety Risk = 20% of the final score
- ADA Accessibility = 15% of the final score
- Strategic Alignment = 15% of the final score

## Default Balanced Scenario

| Criterion | Weight |
|---|---:|
| Safety Risk | 20% |
| ADA Accessibility | 15% |
| Asset Condition | 12% |
| LOS Performance | 12% |
| Demand Need | 8% |
| Strategic Alignment | 15% |
| Financial Feasibility | 8% |
| Equity Impact | 5% |
| Community Concern | 5% |
| Total | 100% |

## User Experience

The sidebar now displays:

- Scoring Weights (%)
- Total Weight
- Success message if total = 100%
- Error message and stop if total is not 100%

This prevents misleading rankings based on invalid weighting totals.
