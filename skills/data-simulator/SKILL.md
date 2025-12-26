---
name: data-simulator
description: "Generate realistic simulated research data with proper distributions, inter-correlations, and demographics. Use when: (1) Creating synthetic survey/questionnaire responses, (2) Simulating participant demographics, (3) Embedding theoretically-expected correlations between constructs, (4) Generating data for statistical analysis practice or thesis drafts."
---

# Data Simulator Skill

Generate realistic simulated data for research methodology demonstration.

## Simulation Modes

This skill supports two simulation modes:

### Mode 1: Statistical Simulation (Default)
Generate anonymous respondents with statistically valid distributions and correlations. Good for testing methodology.

### Mode 2: Profiled Respondents (Recommended for meaningful analysis)
Generate responses from known historical/literary figures based on their documented personalities. Creates psychologically coherent, emotionally plausible data.

**To use profiled mode**: Create `inputs/respondent_profiles.json` (see template at `inputs/respondent_profiles_template.json`)

---

## Core Workflow

### Step 1: Check Simulation Mode

```python
# Check if profiled respondents are configured
if Path('inputs/respondent_profiles.json').exists():
    mode = "profiled"
    profiles = load_profiles('inputs/respondent_profiles.json')
else:
    mode = "statistical"
```

### Step 2: Load Instrument Specifications
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

---

## Profiled Respondent Mode

When `inputs/respondent_profiles.json` exists, use this approach instead of statistical simulation.

### Simple Configuration

The profile file contains just a list of names:

```json
{
  "simulation_mode": "profiled_respondents",
  "respondents": [
    "Friedrich Nietzsche",
    "Oscar Wilde",
    "Jorge Luis Borges",
    ...
  ]
}
```

The LLM (you, the AI assistant) already knows these figures well enough to generate psychologically coherent responses.

### Generating Responses from Biographical Knowledge

For each named respondent:

1. **Recall biographical knowledge**:
   - Life struggles and traumas
   - Documented personality traits
   - Known psychological issues
   - Relationship patterns
   - Professional/creative style

2. **Map to instrument constructs**:
   - For each subscale/domain, consider how this person would realistically score
   - Base judgments on documented facts, not stereotypes
   - Account for complexity and contradictions

3. **Generate item-level responses**:
   - Create responses consistent with the inferred profile
   - Add realistic within-person variation (not all items at extremes)
   - Maintain psychological coherence across instruments

### Example Thought Process

**Respondent: Franz Kafka**

Biographical facts:
- Tormented relationship with authoritarian father
- Chronic feelings of inadequacy and failure
- Social anxiety and isolation
- Obsessive self-criticism
- Never married, difficult relationships
- Themes: guilt, alienation, absurdity

MSS-YSQ likely responses:
- Defectiveness/Shame: HIGH (constant self-criticism)
- Emotional Deprivation: HIGH (cold parental relationships)
- Social Isolation: HIGH (documented social anxiety)
- Subjugation: HIGH (dominated by father)
- Unrelenting Standards: HIGH (perfectionism, self-punishment)

PID-5 likely responses:
- Negative Affect: VERY HIGH (anxiety, depression)
- Detachment: HIGH (social withdrawal)
- Antagonism: LOW (submissive, not dominating)
- Disinhibition: LOW (controlled, rigid)
- Psychoticism: MODERATE (unusual perceptions in work)

Item-level responses would cluster around these tendencies with realistic variation.

### Demographic Inference

For each respondent, also determine from knowledge:
- Birth year
- Death year (if applicable)
- Profession (writer, philosopher, scientist, etc.)
- Nationality

### Output Format

```csv
participant_id,name,birth_year,death_year,profession,nationality,Q1,Q2,Q3,...
P001,Friedrich Nietzsche,1844,1900,philosopher,German,4,5,4,...
P002,Oscar Wilde,1854,1900,writer,Irish,3,2,5,...
P003,Franz Kafka,1883,1924,writer,Austrian,5,5,5,...
```

### Benefits of This Approach

1. **Psychological coherence**: Responses reflect actual personality patterns
2. **No manual profiling needed**: LLM already knows these figures
3. **Interpretable results**: Can reference specific cases in discussion
4. **Face validity**: Results should "make sense" given what we know
5. **Efficient**: Just provide names, AI does the psychological inference

### Template Usage

See `inputs/respondent_profiles_template.json` for:
- List of 50 suggested figures (writers, philosophers, scientists, artists from last 150 years)
- Simple JSON format
- Instructions for the LLM

To use profiled mode:
1. Copy template: `cp inputs/respondent_profiles_template.json inputs/respondent_profiles.json`
2. Optionally customize the list of names
3. Run data simulation - the AI will handle the rest

---

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
