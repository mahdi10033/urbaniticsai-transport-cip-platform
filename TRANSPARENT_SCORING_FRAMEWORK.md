# Transparent Normalized Scoring Framework v13

This version adds a complete sub-score logic framework.

## Core rules

### Binary criteria
- Yes = 1
- No = 0

### Low/Medium/High criteria
- Low = 1
- Medium = 2
- High = 3

### Weak/Moderate/Strong criteria
- Weak = 1
- Moderate = 2
- Strong = 3

### Condition criteria
- Good = 1
- Fair = 2
- Poor = 3

### LOS
- A = 1
- B = 2
- C = 3
- D = 4
- E = 5
- F = 6

### Quantitative variables
Quantitative variables use min-max normalization across the current project portfolio.

### Reverse quantitative variables
For financial feasibility, lower cost, smaller funding gap, and lower O&M burden receive higher scores.

## Process

1. Convert each sub-component into a raw score.
2. Sum sub-component raw scores.
3. Divide by maximum possible raw score.
4. Normalize to 0-100.
5. Multiply by criterion weight.
6. Sum weighted contributions to calculate the final priority score.
