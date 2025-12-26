---
name: data-analysis
description: "Perform statistical analysis on research data including descriptive statistics, hypothesis testing, reliability analysis, and visualization. Use when: (1) Computing descriptive statistics for scale variables, (2) Testing correlational or group-difference hypotheses, (3) Calculating Cronbach's alpha reliability, (4) Creating publication-quality figures and tables."
---

# Data Analysis Skill

Statistical analysis and visualization for social science thesis research.

## Core Workflow

### Step 1: Load Data and Hypotheses
```python
# Load simulated data
data = pd.read_csv('outputs/data/responses_raw.csv')
scores = pd.read_excel('outputs/data/responses_coded.xlsx', sheet_name='Scores')
demographics = pd.read_csv('outputs/data/demographics.csv')

# Load hypotheses from research phase
with open('outputs/research/constructs.json') as f:
    constructs = json.load(f)
```

### Step 2: Descriptive Statistics

Compute for each numeric variable:

```python
def compute_descriptives(series):
    """Compute full descriptive statistics."""
    return {
        'n': series.count(),
        'n_missing': series.isna().sum(),
        'mean': series.mean(),
        'std': series.std(),
        'variance': series.var(),
        'min': series.min(),
        'max': series.max(),
        'range': series.max() - series.min(),
        'skewness': series.skew(),
        'skewness_se': np.sqrt(6/len(series)),  # SE of skewness
        'kurtosis': series.kurtosis(),
        'kurtosis_se': np.sqrt(24/len(series)),  # SE of kurtosis
        'median': series.median(),
        'q1': series.quantile(0.25),
        'q3': series.quantile(0.75),
        'iqr': series.quantile(0.75) - series.quantile(0.25)
    }
```

**Output format (thesis-ready table):**
```
| Variable              | N  | M     | SD    | Min  | Max  | Skew  | Kurt  |
|-----------------------|----|-------|-------|------|------|-------|-------|
| Wisdom Total          | 50 | 3.54  | 0.50  | 2.30 | 4.56 | -0.01 | 0.26  |
| Wisdom Cognitive      | 50 | 3.48  | 0.58  | 2.14 | 4.86 | 0.12  | -0.15 |
| Defense Immature      | 50 | 4.09  | 1.12  | 2.10 | 6.78 | 0.32  | -0.60 |
```

### Step 3: Demographic Analysis

```python
def analyze_demographics(df):
    """Generate demographic summary statistics."""
    results = {}
    
    # Age
    results['age'] = {
        'mean': df['age'].mean(),
        'std': df['age'].std(),
        'range': f"{df['age'].min()}-{df['age'].max()}"
    }
    
    # Categorical variables
    for var in ['gender', 'education', 'religion', 'generation']:
        results[var] = df[var].value_counts(normalize=True).to_dict()
    
    return results
```

### Step 4: Hypothesis Testing

#### Correlation Analysis (Pearson)
```python
from scipy import stats

def test_correlation(x, y, alpha=0.05):
    """Test Pearson correlation with full reporting."""
    # Remove missing
    mask = ~(x.isna() | y.isna())
    x_clean, y_clean = x[mask], y[mask]
    
    r, p = stats.pearsonr(x_clean, y_clean)
    n = len(x_clean)
    
    # Effect size interpretation
    if abs(r) < 0.10:
        effect = 'negligible'
    elif abs(r) < 0.30:
        effect = 'small'
    elif abs(r) < 0.50:
        effect = 'medium'
    else:
        effect = 'large'
    
    # Confidence interval (Fisher z transformation)
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    ci_z = (z - 1.96*se, z + 1.96*se)
    ci_r = (np.tanh(ci_z[0]), np.tanh(ci_z[1]))
    
    return {
        'r': r,
        'p': p,
        'n': n,
        'significant': p < alpha,
        'effect_size': effect,
        'ci_95': ci_r,
        'r_squared': r**2,
        'interpretation': f"r({n-2}) = {r:.3f}, p = {p:.3f}"
    }
```

#### T-Test (Independent Samples)
```python
def test_independent_t(group1, group2, alpha=0.05):
    """Independent samples t-test with effect size."""
    t_stat, p = stats.ttest_ind(group1, group2)
    
    # Cohen's d
    pooled_std = np.sqrt(((len(group1)-1)*group1.std()**2 + 
                          (len(group2)-1)*group2.std()**2) / 
                         (len(group1) + len(group2) - 2))
    cohens_d = (group1.mean() - group2.mean()) / pooled_std
    
    # Effect size interpretation
    if abs(cohens_d) < 0.20:
        effect = 'small'
    elif abs(cohens_d) < 0.50:
        effect = 'medium'
    else:
        effect = 'large'
    
    return {
        't': t_stat,
        'p': p,
        'df': len(group1) + len(group2) - 2,
        'cohens_d': cohens_d,
        'effect_size': effect,
        'significant': p < alpha,
        'interpretation': f"t({len(group1)+len(group2)-2}) = {t_stat:.2f}, p = {p:.3f}, d = {cohens_d:.2f}"
    }
```

#### ANOVA (One-Way)
```python
def test_anova(groups, alpha=0.05):
    """One-way ANOVA with effect size."""
    f_stat, p = stats.f_oneway(*groups)
    
    # Eta squared
    grand_mean = np.concatenate(groups).mean()
    ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
    ss_total = sum((np.concatenate(groups) - grand_mean)**2)
    eta_squared = ss_between / ss_total
    
    return {
        'F': f_stat,
        'p': p,
        'df_between': len(groups) - 1,
        'df_within': sum(len(g) for g in groups) - len(groups),
        'eta_squared': eta_squared,
        'significant': p < alpha
    }
```

### Step 5: Reliability Analysis

```python
def cronbach_alpha(items_df):
    """Calculate Cronbach's alpha for a set of items."""
    items = items_df.dropna()
    n_items = items.shape[1]
    
    # Variance of total scores
    total_var = items.sum(axis=1).var()
    
    # Sum of item variances
    item_vars = items.var(axis=0).sum()
    
    alpha = (n_items / (n_items - 1)) * (1 - item_vars / total_var)
    
    # Interpretation
    if alpha >= 0.90:
        interpretation = 'excellent'
    elif alpha >= 0.80:
        interpretation = 'good'
    elif alpha >= 0.70:
        interpretation = 'acceptable'
    elif alpha >= 0.60:
        interpretation = 'questionable'
    else:
        interpretation = 'poor'
    
    return {
        'alpha': alpha,
        'n_items': n_items,
        'n_valid': len(items),
        'interpretation': interpretation
    }
```

### Step 6: Visualizations

#### Histogram with Normal Curve
```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_histogram(data, var_name, output_path):
    """Create histogram with overlaid normal curve."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Histogram
    sns.histplot(data, kde=True, ax=ax, color='steelblue', edgecolor='white')
    
    # Normal curve overlay
    x = np.linspace(data.min(), data.max(), 100)
    y = stats.norm.pdf(x, data.mean(), data.std()) * len(data) * (data.max() - data.min()) / 20
    ax.plot(x, y, 'k-', linewidth=2, label='Normal')
    
    ax.set_xlabel(var_name)
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of {var_name}')
    
    # Add statistics annotation
    stats_text = f'M = {data.mean():.2f}\nSD = {data.std():.2f}\nN = {len(data)}'
    ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

#### Scatterplot with Regression Line
```python
def plot_scatterplot(x, y, x_label, y_label, output_path):
    """Create scatterplot with regression line and correlation."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Scatter points
    ax.scatter(x, y, alpha=0.6, edgecolors='white', s=60)
    
    # Regression line
    slope, intercept, r, p, se = stats.linregress(x, y)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, 'r-', linewidth=2, label=f'r = {r:.3f}')
    
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(f'{x_label} vs {y_label}')
    ax.legend(loc='best')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

#### Correlation Matrix Heatmap
```python
def plot_correlation_matrix(df, output_path):
    """Create correlation matrix heatmap."""
    corr = df.corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', 
                cmap='RdBu_r', center=0, vmin=-1, vmax=1,
                square=True, linewidths=0.5, ax=ax)
    
    ax.set_title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

#### Pair Plot
```python
def plot_pairplot(df, output_path):
    """Create pair plot for multiple variables."""
    g = sns.pairplot(df, diag_kind='kde', plot_kws={'alpha': 0.6})
    g.fig.suptitle('Relationships Between Variables', y=1.02)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

#### Pie Chart (Demographics)
```python
def plot_pie_chart(series, title, output_path):
    """Create pie chart for categorical variable."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    counts = series.value_counts()
    colors = plt.cm.Set3(np.linspace(0, 1, len(counts)))
    
    wedges, texts, autotexts = ax.pie(
        counts.values, labels=counts.index,
        autopct='%1.1f%%', colors=colors,
        startangle=90, explode=[0.02]*len(counts)
    )
    
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
```

## Output Structure

Save to `outputs/analysis/`:

### descriptive_stats.json
```json
{
  "wisdom_total": {
    "n": 50, "mean": 3.54, "std": 0.50, "skewness": -0.01, ...
  },
  "defense_immature": {...},
  ...
}
```

### hypothesis_tests.json
```json
{
  "H1": {
    "description": "Wisdom negatively correlates with immature defenses",
    "test": "pearson_correlation",
    "variables": ["wisdom_total", "defense_immature"],
    "result": {
      "r": -0.745,
      "p": 0.000,
      "significant": true,
      "effect_size": "large"
    },
    "interpretation": "r(48) = -0.745, p < .001",
    "conclusion": "supported"
  },
  "H2": {...},
  ...
}
```

### reliability.json
```json
{
  "3D-WS": {
    "total": {"alpha": 0.84, "interpretation": "good"},
    "subscales": {
      "cognitive": {"alpha": 0.79, "interpretation": "acceptable"},
      "reflective": {"alpha": 0.81, "interpretation": "good"},
      "affective": {"alpha": 0.76, "interpretation": "acceptable"}
    }
  },
  "DSQ40": {...}
}
```

### figures/
```
histogram_wisdom_total.png
histogram_defense_immature.png
histogram_defense_neurotic.png
histogram_defense_mature.png
scatter_wisdom_vs_immature.png
scatter_wisdom_vs_neurotic.png
scatter_wisdom_vs_mature.png
correlation_matrix.png
pairplot_all_scales.png
pie_gender.png
pie_education.png
pie_generation.png
age_distribution.png
```

### tables/
Markdown tables ready for thesis insertion:
```
table_descriptive_wisdom.md
table_descriptive_defense.md
table_correlation_h1.md
table_correlation_h2.md
table_correlation_h3.md
table_demographics.md
```

## Statistical Decision Tree

```
Hypothesis Type → Test Selection

RELATIONSHIP between two continuous variables:
  → Pearson r (if assumptions met)
  → Spearman rho (if non-normal or ordinal)

DIFFERENCE between two groups:
  → Independent t-test (if assumptions met)
  → Mann-Whitney U (if non-normal)

DIFFERENCE between 3+ groups:
  → One-way ANOVA (if assumptions met)
  → Kruskal-Wallis (if non-normal)

PREDICTION of outcome from predictor(s):
  → Simple regression (one predictor)
  → Multiple regression (2+ predictors)

INTERNAL CONSISTENCY:
  → Cronbach's alpha (most common)
  → McDonald's omega (if multidimensional)
```

## Assumption Checking

```python
def check_normality(data):
    """Check normality assumption."""
    stat, p = stats.shapiro(data)
    return {
        'test': 'Shapiro-Wilk',
        'statistic': stat,
        'p': p,
        'normal': p > 0.05,
        'recommendation': 'Use parametric' if p > 0.05 else 'Consider non-parametric'
    }

def check_homogeneity(group1, group2):
    """Check homogeneity of variance."""
    stat, p = stats.levene(group1, group2)
    return {
        'test': 'Levene',
        'statistic': stat,
        'p': p,
        'homogeneous': p > 0.05
    }
```

## Script: analyze_data.py

```python
#!/usr/bin/env python3
"""
Perform statistical analysis on research data.

Usage:
    python analyze_data.py --data outputs/data/responses_coded.xlsx --hypotheses outputs/research/constructs.json
"""

import argparse
import json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Data file (xlsx)')
    parser.add_argument('--hypotheses', required=True, help='Hypotheses JSON')
    parser.add_argument('--output', default='outputs/analysis/', help='Output directory')
    args = parser.parse_args()
    
    # Setup output directories
    output_dir = Path(args.output)
    (output_dir / 'figures').mkdir(parents=True, exist_ok=True)
    (output_dir / 'tables').mkdir(parents=True, exist_ok=True)
    
    # Load data
    scores = pd.read_excel(args.data, sheet_name='Scores')
    demographics = pd.read_excel(args.data, sheet_name='Demographics')
    
    # Run analyses
    descriptives = compute_all_descriptives(scores)
    hypothesis_results = test_all_hypotheses(scores, args.hypotheses)
    reliability = compute_all_reliability(args.data)
    
    # Generate visualizations
    generate_all_figures(scores, demographics, output_dir / 'figures')
    
    # Generate tables
    generate_all_tables(descriptives, hypothesis_results, output_dir / 'tables')
    
    # Save JSON outputs
    save_json(descriptives, output_dir / 'descriptive_stats.json')
    save_json(hypothesis_results, output_dir / 'hypothesis_tests.json')
    save_json(reliability, output_dir / 'reliability.json')
    
    print(f"Analysis complete. Results saved to {output_dir}")

if __name__ == '__main__':
    main()
```
