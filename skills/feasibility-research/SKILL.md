---
name: feasibility-research
description: "Analyze literature to identify the most scientifically relevant research direction. Use after the research phase to: (1) Identify gaps in existing literature, (2) Evaluate which hypotheses are novel vs. well-established, (3) Assess what can realistically be contributed given the constructs and instruments, (4) Recommend the most promising research angle."
---

# Feasibility Research Skill

Discover the most scientifically meaningful direction for the thesis based on literature analysis.

## Purpose

After gathering literature in Phase 1, this skill analyzes the research landscape to answer:
- **What's already well-established?** (Don't just replicate)
- **What are the gaps?** (Opportunities for contribution)
- **What's feasible with these instruments?** (Realistic scope)
- **What would be most interesting/publishable?** (Scientific value)

## Core Workflow

### Step 1: Load Research Outputs

Read from `outputs/research/`:
- `literature_review.md` - Full literature synthesis
- `constructs.json` - Construct definitions and expected relationships
- `instruments_detailed.json` - Available measurement tools
- `bibliography.json` - Source list

### Step 2: Map the Research Landscape

Create a structured analysis:

```json
{
  "established_findings": [
    {
      "relationship": "construct1 -> construct2",
      "direction": "positive/negative",
      "strength": "strong/moderate/weak",
      "replication_count": "many/several/few",
      "confidence": "high/medium/low",
      "key_citations": ["Author, Year", "..."]
    }
  ],
  "contested_findings": [
    {
      "relationship": "...",
      "inconsistency": "Description of conflicting results",
      "possible_moderators": ["age", "culture", "..."],
      "citations_pro": ["..."],
      "citations_contra": ["..."]
    }
  ],
  "gaps_identified": [
    {
      "description": "What hasn't been studied",
      "why_gap_exists": "Methodological limitation / overlooked / recent construct",
      "feasibility": "high/medium/low",
      "potential_contribution": "Description of what this would add"
    }
  ]
}
```

### Step 3: Evaluate Hypothesis Options

For each possible research direction, assess:

```json
{
  "hypothesis_options": [
    {
      "id": "H1",
      "statement": "X is negatively correlated with Y",
      "novelty": "low/medium/high",
      "novelty_rationale": "Why this is/isn't novel",
      "theoretical_grounding": "strong/moderate/weak",
      "testability": "Which instruments/subscales test this",
      "expected_effect_size": "small/medium/large (r = X.XX)",
      "sample_size_adequate": true/false,
      "minimum_n_needed": 50,
      "scientific_interest": "low/medium/high",
      "recommendation": "pursue/consider/avoid"
    }
  ]
}
```

### Step 4: Identify the Optimal Research Direction

Synthesize findings into a recommendation:

```markdown
## Research Direction Analysis

### Recommended Primary Focus
[Description of the most promising research angle]

**Why this direction:**
1. [Scientific gap it addresses]
2. [Feasibility with available instruments]
3. [Expected contribution to field]

### Recommended Hypotheses
1. **H1 (Primary)**: [Statement] - [Rationale]
2. **H2 (Secondary)**: [Statement] - [Rationale]
3. **H3 (Exploratory)**: [Statement] - [Rationale]

### What to Avoid
- [Hypothesis that would just replicate well-established findings]
- [Direction that instruments can't adequately measure]
- [Questions requiring larger sample than available]

### Suggested Angle/Framing
[How to position this research to maximize contribution]
- Instead of: "Does X relate to Y?" (already known)
- Frame as: "Does the [specific dimension] of X uniquely predict Y beyond [other factors]?" (novel)
```

## Evaluation Criteria

### Novelty Assessment
| Level | Criteria |
|-------|----------|
| High | No studies found on this specific relationship |
| Medium | Few studies, inconsistent results, or different population |
| Low | Well-replicated finding, would be pure replication |

### Feasibility Assessment
| Level | Criteria |
|-------|----------|
| High | Instruments measure exactly what's needed, adequate sample |
| Medium | Instruments approximate the construct, borderline sample |
| Low | Instruments don't capture the key variables, sample too small |

### Scientific Interest Assessment
| Level | Criteria |
|-------|----------|
| High | Would challenge or extend theory, practical implications |
| Medium | Confirms theory in new context, moderate implications |
| Low | Confirms what's already known, limited implications |

## Output Structure

Save to `outputs/feasibility/`:

### research_landscape.json
```json
{
  "theme": "Construct A and Construct B",
  "analysis_date": "2025-01-15",
  "established_findings": [...],
  "contested_findings": [...],
  "gaps_identified": [...],
  "hypothesis_options": [...]
}
```

### direction_recommendation.md
```markdown
# Research Direction Recommendation

## Executive Summary
[2-3 sentence summary of recommended direction]

## Analysis of Options
[Detailed comparison of possible directions]

## Recommended Hypotheses
[Prioritized list with rationale]

## Positioning Strategy
[How to frame the research for maximum contribution]

## Risk Assessment
[What could go wrong, backup options]
```

### feasibility_matrix.md
```markdown
# Feasibility Matrix

| Hypothesis | Novelty | Feasibility | Interest | Power | Recommendation |
|------------|---------|-------------|----------|-------|----------------|
| H1: ... | High | High | High | OK | **PURSUE** |
| H2: ... | Medium | High | Medium | OK | Consider |
| H3: ... | Low | High | Low | OK | Avoid |
```

## Decision Framework

### When to Pivot the Research Direction

If analysis reveals:
1. **All obvious hypotheses are well-established** → Look for moderators, mediators, or specific subgroups
2. **Instruments don't match constructs well** → Consider different framing or acknowledge limitation
3. **Sample size insufficient for expected effects** → Focus on larger effects or exploratory analysis
4. **No clear gap exists** → Frame as replication with novel population/context

### Generating Novel Angles

When the basic relationship is established, consider:

1. **Subscale-level analysis**: "Which specific dimension of X drives the relationship with Y?"
2. **Moderator analysis**: "Does the X-Y relationship differ by age/gender/education?"
3. **Specificity analysis**: "Does X relate more strongly to Y1 than Y2?"
4. **Population novelty**: "Has this been tested in [Romanian/student/clinical] samples?"
5. **Incremental validity**: "Does X predict Y beyond established predictors?"

## Example Analysis

### Input
- Theme: "Wisdom and Defense Mechanisms"
- Instruments: 3D-WS (wisdom), DSQ-40 (defenses)

### Analysis Output

**Established**: Wisdom negatively correlates with immature defenses (r ≈ -0.40 to -0.60) - multiple studies confirm this.

**Gap identified**:
- Which wisdom dimension (cognitive, reflective, affective) is most strongly linked to defense maturity?
- The reflective dimension has theoretical reasons to be most important but hasn't been tested separately.

**Recommendation**:
- Instead of H1: "Wisdom negatively correlates with immature defenses" (established)
- Pursue H1: "Reflective wisdom shows the strongest negative correlation with immature defenses compared to cognitive and affective dimensions"
- This is testable with the subscales, theoretically grounded, and adds specificity to existing knowledge.

## Integration with Workflow

This phase is a **checkpoint**. After completing:

1. **If direction is clear** → Proceed to Data Simulation with refined hypotheses
2. **If direction is unclear** → Return to user with options for decision
3. **If no viable direction** → Consider different instruments or broader theme

The output `direction_recommendation.md` should be reviewed before proceeding to simulation.
