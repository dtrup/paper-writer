# Thesis Draft Generator

An LLM-mediated workflow for rapidly generating first drafts of social science bachelor theses (psychology, sociology, education, etc.).

## Quick Start

```bash
python run.py --theme "Emotional Intelligence and Burnout" --instruments "EQ-i,MBI" --sample 50
```

Then work through phases sequentially with Claude Code.

## Repository Structure

```
thesis-generator/
├── CLAUDE.md              # This file - main orchestration guide
├── run.py                 # Entry point script
├── inputs/                # User-provided configurations
│   ├── config.json        # Generated from run.py arguments
│   ├── demographics.json  # Optional: custom sample demographics
│   └── instruments.json   # Optional: custom instrument definitions
├── outputs/               # All generated artifacts
│   ├── research/          # Literature & construct summaries
│   ├── feasibility/       # Direction & data validation reports
│   ├── data/              # Simulated dataset + demographics
│   ├── analysis/          # Statistical outputs & visualizations
│   └── thesis/            # Final document chapters
└── skills/                # Modular skill definitions
    ├── research/          # Literature gathering & synthesis
    ├── feasibility-research/  # Scientific direction discovery
    ├── data-simulator/    # Realistic response generation
    ├── feasibility-data/  # Data quality validation
    ├── data-analysis/     # Statistical analysis & visualization
    └── thesis-writer/     # Academic writing composition
```

## Workflow Overview

Execute these phases sequentially. The workflow includes two **feasibility checkpoints** to ensure scientific relevance and data quality before investing in full analysis and writing.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 1: RESEARCH          →  Gather literature & instruments          │
│                                                                         │
│  Phase 2: FEASIBILITY-RESEARCH  →  Discover best scientific direction  │
│           ↓                      (checkpoint: review before proceeding) │
│                                                                         │
│  Phase 3: DATA SIMULATION   →  Generate realistic responses             │
│                                                                         │
│  Phase 4: FEASIBILITY-DATA  →  Validate data quality & power            │
│           ↓                    (checkpoint: review before proceeding)   │
│                                                                         │
│  Phase 5: ANALYSIS          →  Statistical tests & visualizations       │
│                                                                         │
│  Phase 6: WRITING           →  Compose thesis chapters                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 1: Research & Instrument Definition
**Skill**: `skills/research/SKILL.md`

Gather the raw material for the thesis.

1. Search for recent literature (2020+) on the theme constructs
2. Gather instrument metadata (items, subscales, scoring, validity)
3. Identify theoretical frameworks and key authors
4. Document expected relationships between constructs
5. Store bibliography in APA format

**Outputs**: `outputs/research/`
- `literature_review.md` - Synthesized literature
- `constructs.json` - Construct definitions + expected correlations
- `instruments_detailed.json` - Full instrument specs
- `bibliography.json` - APA citations

---

### Phase 2: Feasibility - Research Direction ⚡
**Skill**: `skills/feasibility-research/SKILL.md`

**CHECKPOINT**: Discover the most scientifically relevant direction.

1. Map what's already well-established (avoid pure replication)
2. Identify gaps and contested findings (opportunities)
3. Evaluate hypothesis options for novelty, feasibility, and interest
4. Recommend optimal research direction and framing
5. Generate prioritized hypothesis list

**Outputs**: `outputs/feasibility/`
- `research_landscape.json` - Analysis of established vs. novel findings
- `direction_recommendation.md` - Recommended focus and hypotheses
- `feasibility_matrix.md` - Comparison of hypothesis options

**Decision Point**: Review `direction_recommendation.md` before proceeding. Adjust hypotheses or theme if needed.

---

### Phase 3: Data Simulation
**Skill**: `skills/data-simulator/SKILL.md`

Generate realistic synthetic data based on refined hypotheses.

1. Load instrument definitions and recommended hypotheses
2. Generate demographic profiles (Romanian sample by default)
3. Simulate instrument responses with realistic distributions
4. Embed expected correlations from feasibility analysis
5. Export to CSV/Excel with proper variable coding

**Outputs**: `outputs/data/`
- `responses_raw.csv` - Raw response data
- `responses_coded.xlsx` - Coded with subscale scores
- `demographics.csv` - Participant demographics
- `simulation_parameters.json` - Embedded correlations

---

### Phase 4: Feasibility - Data Validation ⚡
**Skill**: `skills/feasibility-data/SKILL.md`

**CHECKPOINT**: Validate that the data can support meaningful analysis.

1. Check if target correlations were achieved (within tolerance)
2. Verify scale reliability (Cronbach's alpha ≥ 0.70)
3. Assess statistical power for planned hypothesis tests
4. Flag distribution problems (skew, floor/ceiling effects)
5. Recommend proceed, caution, or regenerate

**Outputs**: `outputs/feasibility/`
- `data_quality.json` - All validation metrics
- `data_feasibility_report.md` - Human-readable report with recommendations

**Decision Point**:
- ✅ **PROCEED** - All checks pass, continue to analysis
- ⚠️ **CAUTION** - Minor issues, note limitations and proceed
- ❌ **REGENERATE** - Critical issues, return to Phase 3 with adjustments

---

### Phase 5: Statistical Analysis
**Skill**: `skills/data-analysis/SKILL.md`

Full analysis on validated data.

1. Compute descriptive statistics per variable
2. Test hypotheses (correlations, t-tests, ANOVA as needed)
3. Calculate reliability (Cronbach alpha) for scales
4. Generate visualizations (histograms, scatterplots, heatmaps)
5. Export tables in thesis-ready format

**Outputs**: `outputs/analysis/`
- `descriptive_stats.json` - Per-variable statistics
- `hypothesis_tests.json` - Test results with effect sizes
- `reliability.json` - Cronbach alpha values
- `figures/` - All visualizations (PNG)
- `tables/` - Formatted tables (Markdown)

---

### Phase 6: Thesis Composition
**Skill**: `skills/thesis-writer/SKILL.md`

Write the complete thesis draft.

1. Write Introduction (context, relevance, structure)
2. Write Chapter 1: Theoretical Framework (from research outputs)
3. Write Chapter 2: Methods (instruments, procedures)
4. Write Chapter 3: Results (from analysis outputs)
5. Write Chapter 4: Conclusions (discussion, limitations, implications)
6. Generate Abstract with keywords
7. Compile Bibliography
8. Assemble final document

**Outputs**: `outputs/thesis/`
- `chapters/` - Individual chapter markdown files
- `thesis_draft.docx` - Assembled document
- `abstract.md` - Standalone abstract

---

## Input Specification

### Theme Format
A research theme connecting 2+ constructs:
- "Wisdom and Defense Mechanisms"
- "Emotional Intelligence and Academic Performance"
- "Attachment Styles and Relationship Satisfaction"
- "Burnout and Coping Strategies"

### Instrument Names
Provide instruments as comma-separated names. The research phase will:
1. First search for the instrument's standard items and scoring
2. If not found, prompt user to provide instrument definition

### Custom Instruments
If using non-standard instruments, create `inputs/instruments.json`:
```json
{
  "instruments": [
    {
      "name": "CUSTOM-SCALE",
      "full_name": "Custom Scale Name",
      "author": "Author, Year",
      "items": 20,
      "subscales": [
        {"name": "subscale1", "items": [1,2,3,4,5], "description": "..."},
        {"name": "subscale2", "items": [6,7,8,9,10], "description": "..."}
      ],
      "scale_type": "likert",
      "scale_range": [1, 5],
      "scoring": "mean_per_subscale"
    }
  ]
}
```

### Demographics Configuration
Create `inputs/demographics.json` for custom sample characteristics (Romanian defaults used otherwise):
```json
{
  "n": 50,
  "variables": {
    "age": {"mean": 44, "std": 12, "min": 18, "max": 70},
    "gender": {"categories": {"female": 0.80, "male": 0.20}},
    "education": {"categories": {"highschool": 0.16, "bachelor": 0.46, "master": 0.34, "phd": 0.04}}
  }
}
```

See `skills/data-simulator/references/demographics_template.md` for Romanian presets and options.

## Execution Commands

```bash
# Initialize new project
python run.py --theme "Your Theme" --instruments "SCALE1,SCALE2" --sample 50

# Check status
python run.py --status

# View phase instructions
python run.py --phase research
python run.py --phase feasibility-research
python run.py --phase simulate
python run.py --phase feasibility-data
python run.py --phase analyze
python run.py --phase write
```

## Quality Guidelines

### Research Standards
- Prioritize sources from 2020-2025
- Include seminal/foundational works regardless of date
- Minimum 25-40 references for theoretical chapter
- Use peer-reviewed sources (journals, handbooks)

### Feasibility Standards
- Don't just replicate well-established findings
- Focus on novel angles: specific dimensions, moderators, new populations
- Ensure adequate power (≥0.80) for primary hypotheses
- Accept only reliable scales (α ≥ 0.70)

### Data Realism
- Responses follow realistic distributions (slight positive skew typical)
- Inter-item correlations within subscales: r = 0.3-0.6
- Cross-construct correlations match theoretical expectations
- Include realistic noise (some inconsistent responses, missing data)

### Statistical Rigor
- Report effect sizes alongside p-values
- Use appropriate tests based on distribution assumptions
- Include confidence intervals where applicable
- Flag any assumption violations

### Writing Standards
- Academic tone, third person
- Clear paragraph structure (topic sentence → evidence → interpretation)
- Proper APA citations (Author, Year)
- Tables and figures numbered sequentially per chapter

## Skill Dependencies

Read skills in this order for full context:
1. `skills/research/SKILL.md` - Research methodology
2. `skills/feasibility-research/SKILL.md` - Direction discovery
3. `skills/data-simulator/SKILL.md` - Data generation approach
4. `skills/feasibility-data/SKILL.md` - Data validation
5. `skills/data-analysis/SKILL.md` - Analysis procedures
6. `skills/thesis-writer/SKILL.md` - Writing conventions

Each skill is self-contained but references outputs from prior phases.

## Error Handling

If a phase fails:
1. Check `outputs/{phase}/` for partial outputs
2. Common issues:
   - Instrument not found → Provide manual definition in `inputs/instruments.json`
   - Insufficient literature → Broaden search terms or check spelling
   - Correlations not achieved → Adjust simulation parameters
   - Low reliability → Check inter-item correlation settings
   - Underpowered tests → Increase sample size or focus on larger effects

## Customization

### Adding New Instruments
Create `inputs/instruments.json` with full specification including:
- All item texts (optional but helpful)
- Subscale assignments
- Scoring instructions
- Known reliability values

### Adjusting Demographics
Create `inputs/demographics.json` to match your target population.
See `skills/data-simulator/references/demographics_template.md` for Romanian presets.

### Modifying Thesis Structure
Edit `skills/thesis-writer/references/thesis-structure.md` for different chapter organization or formatting requirements.
