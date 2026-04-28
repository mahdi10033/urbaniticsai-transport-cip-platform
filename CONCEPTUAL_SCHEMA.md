# Conceptual Data Architecture

## Main entities

### Agency
Represents the city, county, MPO/TPO, or special district using the platform.

### Asset
A physical transportation asset such as sidewalk, curb ramp, roadway, bridge, crosswalk, bike lane, or transit stop.

### Project
A candidate capital improvement project linked to one or more assets.

### Needs Assessment
Records condition, safety, ADA/accessibility, LOS, demand, and deficiency information.

### Strategic Alignment
Connects projects to adopted planning goals such as MTP, LRTP, Comprehensive Plan, Complete Streets, Vision Zero, ADA Transition Plan, and resilience strategies.

### Financial Plan
Stores capital cost, funding source, funding gap, lifecycle cost, and annual operating/maintenance impact.

### Implementation Schedule
Tracks project phases, milestones, target dates, responsible units, and project status.

### Prioritization Score
Stores criterion-level scores, agency weights, total priority score, and priority classification.

## Suggested future database tables

- agencies
- users
- assets
- projects
- project_assets
- needs_assessments
- los_metrics
- demand_forecasts
- strategic_alignment
- funding_sources
- project_funding
- lifecycle_costs
- implementation_milestones
- community_input_summary
- prioritization_runs
- prioritization_scores
- reports
