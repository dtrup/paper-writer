---
name: feasibility-data
description: "Validate simulated data quality and assess whether planned analyses are viable. Use after data simulation to: (1) Check if target correlations were achieved, (2) Verify scale reliability is adequate, (3) Assess statistical power for planned tests, (4) Identify potential problems before full analysis, (5) Recommend adjustments if needed."
---

# Feasibility Data Skill

Validate that simulated data can support meaningful analysis before investing in full thesis writing.

## Purpose

After generating simulated data in Phase 2, this skill performs quality checks to answer:
- **Did the simulation work?** (Correlations achieved, distributions realistic)
- **Is reliability adequate?** (Cronbach's alpha acceptable for each scale)
- **Do we have statistical power?** (Can we detect the expected effects?)
- **Are there problems to address?** (Before wasting effort on bad data)

## Core Workflow

### Step 1: Load Simulation Outputs

Read from `outputs/data/`:
- `responses_coded.xlsx` - Computed subscale scores
- `simulation_parameters.json` - Target correlations and parameters
- `demographics.csv` - Sample characteristics

Also read from `outputs/feasibility/`:
- `direction_recommendation.md` - Planned hypotheses

### Step 2: Correlation Achievement Check

Compare target vs. achieved correlations.

**IMPORTANT: Interpretation Rules for Profiled Respondents**

| Achieved vs Target | Interpretation | Action |
|-------------------|----------------|--------|
| \|r\| >= \|target\| (same direction) | ✅ EXCEEDED (favorable) | Proceed - stronger effect |
| r within ±0.10 of target | ✅ MET | Proceed |
| \|r\| < \|target\| - 0.10 | ⚠️ BELOW | May need regeneration |

**Why correlations often EXCEED targets with profiled respondents:**
- Psychologically coherent profiles produce cleaner data
- No random measurement error from careless responding
- Profiles based on documented personality patterns

**This is GOOD for hypothesis testing** - stronger correlations mean:
- Higher statistical power
- Cleaner demonstration of relationships
- More interpretable findings

**Do NOT flag as problems:**
- Correlations stronger than target (same direction)
- Alpha > 0.90 (reflects profile consistency, not an error)

```python
def check_correlation_achievement(data, targets, tolerance=0.15):
    """
    Verify simulated correlations match or exceed targets.

    Key insight: For profiled respondents, correlations often EXCEED
    targets - this is favorable, not a problem!
    """
    results = {
        "checks": [],
        "concerns": [],  # Only for BELOW target
        "exceeded": [],  # Favorable - stronger than expected
        "overall_success": True
    }

    for (var1, var2), target_r in targets.items():
        actual_r = data[var1].corr(data[var2])

        # Check if same direction and at least as strong
        same_direction = (target_r >= 0 and actual_r >= 0) or (target_r < 0 and actual_r < 0)
        exceeded = same_direction and abs(actual_r) >= abs(target_r)
        met = abs(actual_r - target_r) <= tolerance
        below = abs(actual_r) < abs(target_r) - tolerance

        if exceeded:
            status = "EXCEEDED"
        elif met:
            status = "MET"
        elif below:
            status = "BELOW"
        else:
            status = "MET"  # Within tolerance

        check = {
            "variables": [var1, var2],
            "target_r": target_r,
            "achieved_r": actual_r,
            "difference": actual_r - target_r,
            "status": status
        }
        results["checks"].append(check)

        if status == "EXCEEDED":
            results["exceeded"].append(check)
        elif status == "BELOW":
            results["concerns"].append(check)
            results["overall_success"] = False

    return results
```

### Step 3: Reliability Analysis

Calculate Cronbach's alpha for each scale/subscale:

```python
def assess_reliability(data, instrument_specs):
    """
    Calculate reliability for all scales.

    Interpretation:
    - α ≥ 0.90: Excellent
    - α ≥ 0.80: Good
    - α ≥ 0.70: Acceptable
    - α ≥ 0.60: Questionable
    - α < 0.60: Poor (PROBLEM)
    """
    results = []

    for instrument in instrument_specs:
        for subscale in instrument["subscales"]:
            items = get_items_for_subscale(data, subscale)
            alpha = calculate_cronbach_alpha(items)

            results.append({
                "instrument": instrument["name"],
                "subscale": subscale["name"],
                "n_items": len(subscale["items"]),
                "alpha": alpha,
                "interpretation": interpret_alpha(alpha),
                "acceptable": alpha >= 0.70,
                "concern": alpha < 0.60
            })

    return results
```

### Step 4: Statistical Power Analysis

Assess power for planned hypothesis tests:

```python
def assess_power(n, hypotheses, alpha=0.05):
    """
    Calculate statistical power for each planned test.

    For correlations: power to detect r at given n
    For t-tests: power to detect d at given n per group
    """
    from scipy import stats
    import numpy as np

    results = []

    for h in hypotheses:
        if h["test_type"] == "correlation":
            # Power for correlation
            expected_r = h["expected_effect"]

            # Using approximation: z = arctanh(r) * sqrt(n-3)
            z_crit = stats.norm.ppf(1 - alpha/2)
            z_r = np.arctanh(expected_r)
            se = 1 / np.sqrt(n - 3)
            power = 1 - stats.norm.cdf(z_crit - z_r/se) + stats.norm.cdf(-z_crit - z_r/se)

            # Minimum n for 80% power
            min_n = required_n_for_correlation(expected_r, power=0.80)

            results.append({
                "hypothesis": h["id"],
                "test": "Pearson correlation",
                "expected_effect": expected_r,
                "effect_size_label": effect_size_label_r(expected_r),
                "current_n": n,
                "power": power,
                "adequate_power": power >= 0.80,
                "min_n_for_80_power": min_n,
                "recommendation": "OK" if power >= 0.80 else f"Need n≥{min_n}"
            })

        elif h["test_type"] == "t_test":
            expected_d = h["expected_effect"]
            n_per_group = n // 2  # Assuming equal groups

            # Power calculation for independent t-test
            power = calculate_t_test_power(n_per_group, expected_d, alpha)
            min_n = required_n_for_t_test(expected_d, power=0.80)

            results.append({
                "hypothesis": h["id"],
                "test": "Independent t-test",
                "expected_effect": expected_d,
                "effect_size_label": effect_size_label_d(expected_d),
                "current_n": n,
                "n_per_group": n_per_group,
                "power": power,
                "adequate_power": power >= 0.80,
                "min_n_for_80_power": min_n * 2,
                "recommendation": "OK" if power >= 0.80 else f"Need n≥{min_n*2}"
            })

    return results
```

### Step 5: Distribution Quality Check

Verify distributions are realistic:

```python
def check_distributions(data, expected_distributions):
    """
    Check if variable distributions match expectations.

    Flags:
    - Extreme skewness (|skew| > 2)
    - Extreme kurtosis (|kurt| > 7)
    - Floor/ceiling effects (>15% at min/max)
    - Insufficient variance
    """
    results = []

    for var in data.columns:
        series = data[var].dropna()

        checks = {
            "variable": var,
            "n": len(series),
            "mean": series.mean(),
            "std": series.std(),
            "skewness": series.skew(),
            "kurtosis": series.kurtosis(),
            "min": series.min(),
            "max": series.max(),
            "floor_effect": (series == series.min()).mean(),
            "ceiling_effect": (series == series.max()).mean(),
            "flags": []
        }

        # Flag problems
        if abs(checks["skewness"]) > 2:
            checks["flags"].append("EXTREME_SKEW")
        if abs(checks["kurtosis"]) > 7:
            checks["flags"].append("EXTREME_KURTOSIS")
        if checks["floor_effect"] > 0.15:
            checks["flags"].append("FLOOR_EFFECT")
        if checks["ceiling_effect"] > 0.15:
            checks["flags"].append("CEILING_EFFECT")
        if checks["std"] < 0.5:
            checks["flags"].append("LOW_VARIANCE")

        checks["status"] = "OK" if not checks["flags"] else "CONCERN"
        results.append(checks)

    return results
```

### Step 6: Generate Feasibility Report

Synthesize all checks into actionable recommendations:

```markdown
# Data Feasibility Report

## Executive Summary
- Overall Status: ✅ PROCEED / ⚠️ PROCEED WITH CAUTION / ❌ REGENERATE DATA
- Correlation Achievement: X/Y targets met
- Reliability: X/Y scales acceptable (α ≥ 0.70)
- Statistical Power: X/Y hypotheses adequately powered

## Detailed Findings

### Correlation Check
| Variables | Target | Achieved | Diff | Status |
|-----------|--------|----------|------|--------|
| wisdom_total × defense_immature | -0.50 | -0.47 | 0.03 | ✅ OK |

### Reliability Check
| Scale | Subscale | α | Interpretation | Status |
|-------|----------|---|----------------|--------|
| 3D-WS | Cognitive | 0.78 | Acceptable | ✅ OK |
| DSQ-40 | Neurotic | 0.62 | Questionable | ⚠️ |

### Power Analysis
| Hypothesis | Test | Expected r/d | Power | Status |
|------------|------|--------------|-------|--------|
| H1 | Correlation | r = -0.50 | 0.94 | ✅ OK |
| H2 | Correlation | r = 0.25 | 0.52 | ⚠️ Underpowered |

### Distribution Flags
[Any variables with concerning distributions]

## Recommendations

### If All Green (✅ PROCEED)
Continue to full analysis phase.

### If Warnings (⚠️ PROCEED WITH CAUTION)
- Acknowledge [specific limitation] in thesis limitations section
- Consider [adjustment] to hypothesis
- Note that [finding] should be interpreted cautiously

### If Critical Issues (❌ REGENERATE)
1. [Specific issue to fix]
2. Re-run data simulation with adjusted parameters
3. Re-run this feasibility check
```

## Output Structure

Save to `outputs/feasibility/`:

### data_quality.json
```json
{
  "analysis_date": "2025-01-15",
  "sample_size": 50,
  "correlation_checks": [...],
  "reliability_checks": [...],
  "power_analysis": [...],
  "distribution_checks": [...],
  "overall_status": "proceed|caution|regenerate",
  "critical_issues": [],
  "warnings": []
}
```

### data_feasibility_report.md
Human-readable report with tables and recommendations.

## Decision Thresholds

### Proceed (Green Light)
- All target correlations within ±0.15
- All scales α ≥ 0.70
- Primary hypotheses power ≥ 0.80
- No extreme distribution problems

### Proceed with Caution (Yellow Light)
- Most correlations achieved (1-2 minor discrepancies)
- Most scales α ≥ 0.60
- Primary hypotheses power ≥ 0.60
- Minor distribution concerns

### Regenerate Data (Red Light)
- Multiple correlation failures (>0.20 off target)
- Key scales α < 0.60
- Primary hypotheses power < 0.50
- Severe distribution problems (floor/ceiling effects)

## Common Issues and Solutions

### Correlations Not Achieved
- **Cause**: Sample too small for reliable estimation
- **Solution**: Increase n or accept wider tolerance

### Low Reliability
- **Cause**: Too few items, inconsistent simulation
- **Solution**: Check item generation parameters, may need to increase inter-item correlations

### Underpowered Tests
- **Cause**: Sample too small for expected effect size
- **Solution**:
  - Increase sample size
  - Focus on larger effects only
  - Frame as exploratory rather than confirmatory

### Distribution Problems
- **Cause**: Skew parameters too extreme, scale boundaries too narrow
- **Solution**: Adjust distribution parameters in simulation

## Integration with Workflow

This phase is a **quality gate**. After completing:

1. **If PROCEED** → Continue to Statistical Analysis (Phase 5)
2. **If CAUTION** → Note limitations, proceed carefully
3. **If REGENERATE** → Return to Data Simulation (Phase 3) with adjusted parameters

Do not proceed to full analysis with critically flawed data - it wastes effort and produces meaningless results.
