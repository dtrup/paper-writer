---
name: data-simulator
description: "Generate realistic simulated research data with proper distributions, inter-correlations, and demographics. Use when: (1) Creating synthetic survey/questionnaire responses, (2) Simulating participant demographics, (3) Embedding theoretically-expected correlations between constructs, (4) Generating data for statistical analysis practice or thesis drafts."
---

# Data Simulator Skill

Generate realistic simulated data for research methodology demonstration.

## Core Workflow

### Step 1: Load Instrument Specifications
Read from `outputs/research/instruments_detailed.json`:
- Item count per instrument
- Subscale structure
- Response scale (Likert range)
- Expected distributions

### Step 2: Load Theoretical Expectations
Read from `outputs/research/constructs.json`:
- Expected correlations between constructs
- Direction of relationships (positive/negative)
- Effect sizes from literature (if available)

### Step 3: Load Demographics Configuration

Read from `inputs/demographics.json` (or use defaults):

```json
{
  "n": 50,
  "variables": {
    "age": {
      "distribution": "normal_truncated",
      "mean": 35,
      "std": 12,
      "min": 18,
      "max": 70
    },
    "gender": {
      "distribution": "categorical",
      "categories": {"female": 0.60, "male": 0.40}
    },
    "education": {
      "distribution": "categorical",
      "categories": {
        "high_school": 0.20,
        "bachelor": 0.45,
        "master": 0.30,
        "doctorate": 0.05
      }
    }
  }
}
```

See `skills/data-simulator/references/demographics_template.md` for customization options.

### Step 4: Generate Correlated Response Data

Use copula-based simulation or Cholesky decomposition to embed correlations.

**Target Correlation Structure (example):**
```python
target_correlations = {
    ("construct1_total", "construct2_subscale1"): -0.50,  # negative
    ("construct1_total", "construct2_subscale2"): 0.05,   # near zero
    ("construct1_total", "construct2_subscale3"): 0.30,   # positive
    # Within-scale correlations
    ("construct1_dim1", "construct1_dim2"): 0.60,
    ("construct1_dim1", "construct1_dim3"): 0.55,
}
```

**Algorithm:**
```python
import numpy as np
from scipy import stats

def generate_correlated_data(n, correlation_matrix, marginals):
    """
    Generate data with specified correlations and marginal distributions.

    1. Generate multivariate normal with target correlations
    2. Transform to uniform via normal CDF
    3. Transform to target marginals via inverse CDF
    """
    # Generate MVN
    mvn = np.random.multivariate_normal(
        mean=np.zeros(len(marginals)),
        cov=correlation_matrix,
        size=n
    )

    # Transform to uniform [0,1]
    uniform = stats.norm.cdf(mvn)

    # Transform to target distributions
    data = {}
    for i, (var_name, marginal) in enumerate(marginals.items()):
        if marginal['type'] == 'likert':
            data[var_name] = discretize_likert(
                uniform[:, i],
                marginal['min'],
                marginal['max'],
                marginal.get('skew', 0)
            )

    return data

def discretize_likert(uniform_vals, min_val, max_val, skew=0):
    """Convert uniform [0,1] to Likert scale with optional skew."""
    if skew != 0:
        uniform_vals = stats.beta.ppf(
            uniform_vals,
            a=2-skew,
            b=2+skew
        )
    continuous = uniform_vals * (max_val - min_val) + min_val
    return np.round(continuous).astype(int).clip(min_val, max_val)
```

### Step 5: Generate Item-Level Responses

From subscale scores, generate individual item responses:

```python
def generate_items_from_subscale(subscale_score, n_items, scale_range, noise=0.3):
    """
    Generate item responses that average to subscale score.

    - Add realistic noise (some items higher, some lower)
    - Maintain within-subscale correlations (r ~ 0.3-0.5)
    - Respect scale boundaries
    """
    base = subscale_score
    items = []
    for i in range(n_items):
        item_score = base + np.random.normal(0, noise * (scale_range[1] - scale_range[0]))
        item_score = np.clip(item_score, scale_range[0], scale_range[1])
        items.append(round(item_score))
    return items
```

### Step 6: Add Realistic Noise Patterns

**Careless responding (2-5% of sample):**
```python
def add_careless_responses(data, rate=0.03):
    """Add some straight-lining or random responding."""
    n_careless = int(len(data) * rate)
    careless_ids = np.random.choice(len(data), n_careless, replace=False)
    for idx in careless_ids:
        pattern = np.random.choice(['straightline', 'random'])
        if pattern == 'straightline':
            val = np.random.randint(scale_min, scale_max)
            data.iloc[idx] = val
        else:
            data.iloc[idx] = np.random.randint(scale_min, scale_max+1, len(data.columns))
    return data
```

**Missing data (1-3% of responses):**
```python
def add_missing_data(data, rate=0.02):
    """Randomly introduce missing values."""
    mask = np.random.random(data.shape) < rate
    data[mask] = np.nan
    return data
```

## Output Structure

Save to `outputs/data/`:

### responses_raw.csv
```csv
participant_id,age,gender,education,Q1,Q2,Q3,...
P001,35,female,bachelor,4,3,5,...
P002,29,male,master,3,4,4,...
```

### responses_coded.xlsx
Includes computed subscale scores:
```
Sheet 1: Raw Responses
Sheet 2: Demographics
Sheet 3: Computed Scores
  - construct1_dim1, construct1_dim2, construct1_total
  - construct2_subscale1, construct2_subscale2, etc.
Sheet 4: Correlation Check (verify embedded correlations achieved)
```

### demographics.csv
```csv
participant_id,age,gender,education
P001,35,female,bachelor
...
```

### simulation_parameters.json
```json
{
  "n": 50,
  "seed": 42,
  "target_correlations": {},
  "achieved_correlations": {},
  "demographics_distribution": {},
  "noise_parameters": {
    "careless_rate": 0.03,
    "missing_rate": 0.02
  }
}
```

## Realistic Distribution Guidelines

### Likert Scale Tendencies
- **Most self-report scales**: Slight positive skew, mean slightly above midpoint
- **Negative constructs** (anxiety, depression): Strong positive skew in non-clinical samples
- **Positive constructs** (wellbeing, satisfaction): Slight negative skew

### Inter-Item Correlations
- Items within same subscale: r = 0.30-0.60
- Items across subscales (same instrument): r = 0.10-0.30
- Items across instruments: r = 0.00-0.20 (unless theoretically related)

### Sample Size Considerations
- N=50: Adequate for correlation detection (r > 0.35)
- N=100: Better power for moderate effects
- N=200+: Required for regression/SEM

## Validation Checks

Before outputting data, verify:

1. **Correlation achievement**: |target - achieved| < 0.10
2. **Distribution shapes**: Skewness within expected ranges
3. **Scale boundaries**: No values outside valid range
4. **Missing pattern**: MCAR (missing completely at random)
5. **Internal consistency**: Cronbach alpha > 0.70 for subscales

```python
def validate_simulated_data(data, targets):
    checks = {
        "correlations_ok": check_correlations(data, targets),
        "distributions_ok": check_distributions(data),
        "boundaries_ok": check_boundaries(data),
        "reliability_ok": check_reliability(data)
    }
    return all(checks.values()), checks
```

## Script: generate_responses.py

Main entry point for data generation:

```python
#!/usr/bin/env python3
"""
Generate simulated research data.

Usage:
    python generate_responses.py --config outputs/research/instruments_detailed.json --n 50 --seed 42
"""

import argparse
import json
import numpy as np
import pandas as pd
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True, help='Instrument config JSON')
    parser.add_argument('--n', type=int, default=50, help='Sample size')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--output', default='outputs/data/', help='Output directory')
    args = parser.parse_args()

    np.random.seed(args.seed)

    # Load configurations
    with open(args.config) as f:
        instruments = json.load(f)

    correlations = load_target_correlations('outputs/research/constructs.json')
    demographics_config = load_demographics('inputs/demographics.json')

    # Generate data
    demographics = generate_demographics(args.n, demographics_config)
    responses = generate_correlated_responses(args.n, instruments, correlations)

    # Add noise
    responses = add_careless_responses(responses)
    responses = add_missing_data(responses)

    # Compute subscale scores
    scores = compute_subscale_scores(responses, instruments)

    # Validate
    valid, checks = validate_simulated_data(scores, correlations)
    if not valid:
        print(f"Warning: Validation failed: {checks}")

    # Save outputs
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    demographics.to_csv(output_dir / 'demographics.csv', index=False)
    responses.to_csv(output_dir / 'responses_raw.csv', index=False)

    with pd.ExcelWriter(output_dir / 'responses_coded.xlsx') as writer:
        responses.to_excel(writer, sheet_name='Raw', index=False)
        demographics.to_excel(writer, sheet_name='Demographics', index=False)
        scores.to_excel(writer, sheet_name='Scores', index=False)

    print(f"Generated {args.n} responses to {output_dir}")

if __name__ == '__main__':
    main()
```
