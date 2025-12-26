# Thesis Draft Generator

An LLM-powered toolkit for rapidly prototyping social science bachelor thesis drafts. Designed to work with agentic coding tools like Claude Code, Cursor, or similar AI assistants.

## What This Does

Given a research theme and measurement instruments, this toolkit guides an AI assistant through a **6-phase workflow with feasibility checkpoints**:

1. **Research** - Gathering literature, construct definitions, and instrument specifications
2. **Feasibility: Direction** - Discovering the most scientifically relevant research angle
3. **Data Simulation** - Generating realistic questionnaire responses with proper correlations
4. **Feasibility: Data** - Validating data quality, reliability, and statistical power
5. **Analysis** - Running descriptive statistics, hypothesis tests, and creating visualizations
6. **Writing** - Composing all thesis chapters in academic format

**Output**: A complete thesis draft (~35-55 pages) with theoretical framework, methodology, results, conclusions, and bibliography - optimized for scientific relevance.

## Quick Start

### Prerequisites

- Python 3.8+
- An agentic AI coding tool (Claude Code, Cursor, Windsurf, etc.)
- Internet access for literature search

### Installation

```bash
# Clone or copy the repository
cd thesis-generator

# No dependencies required for the orchestration layer
# The AI assistant will install needed packages (pandas, scipy, etc.) as needed
```

### Basic Usage

**Option 1: Interactive with AI Assistant**

Open the repository in your AI coding tool and say:

> "I want to create a thesis on [YOUR THEME] using [INSTRUMENT1] and [INSTRUMENT2] with a sample of 50 participants. Read CLAUDE.md and execute the workflow."

**Option 2: Command Line Initialization**

```bash
# Initialize your thesis project
python run.py --theme "Emotional Intelligence and Burnout" --instruments "EQ-i,MBI" --sample 50

# View workflow overview
python run.py --full

# Execute phase by phase (6 phases with 2 checkpoints)
python run.py --phase research
python run.py --phase feasibility-research  # checkpoint: review direction
python run.py --phase simulate
python run.py --phase feasibility-data      # checkpoint: validate data
python run.py --phase analyze
python run.py --phase write
```

## Example Themes

The toolkit works with any social science research theme involving measurable constructs:

| Theme | Instruments | Field |
|-------|-------------|-------|
| Emotional Intelligence and Burnout | EQ-i, MBI | Workplace psychology |
| Attachment and Relationship Satisfaction | ECR-R, RAS | Close relationships |
| Big Five and Academic Performance | NEO-FFI, GPA | Educational psychology |
| Anxiety, Depression, and Coping | STAI, BDI-II, COPE | Clinical psychology |
| Mindfulness and Stress | MAAS, PSS | Health psychology |
| Leadership Style and Team Performance | MLQ, Team surveys | Organizational behavior |

## Workflow Details

### Phase 1: Research

Gather the raw material:
- Search for recent literature (2020+) on each construct
- Find seminal/foundational works
- Gather instrument specifications (items, subscales, scoring, validity)
- Build a bibliography with 25-40 APA-formatted sources

**Outputs:** `outputs/research/`

### Phase 2: Feasibility - Research Direction (Checkpoint)

**Discover the most scientifically relevant angle:**
- Map what's already well-established (avoid pure replication)
- Identify gaps in the literature (opportunities for contribution)
- Evaluate hypothesis options for novelty, feasibility, and interest
- Recommend optimal framing and prioritized hypotheses

**Outputs:** `outputs/feasibility/direction_recommendation.md`

Review this before proceeding to ensure you're pursuing something meaningful.

### Phase 3: Data Simulation

Generate realistic synthetic data. Two modes available:

**Mode A: Statistical (default)** - Anonymous respondents with valid distributions

**Mode B: Profiled Respondents (recommended)** - Known historical/literary figures (Nietzsche, Woolf, Borges, etc.) as respondents, with psychologically coherent responses based on their documented personalities.

To use profiled mode, copy and customize:
```bash
cp inputs/respondent_profiles_template.json inputs/respondent_profiles.json
```

**Profiled Mode Considerations:**
- Correlations may **exceed** literature targets (this is good - stronger effects)
- Reliability may appear high (α > 0.90) due to profile consistency
- Results require appropriate caveats in discussion section

**Outputs:** `outputs/data/`

### Phase 4: Feasibility - Data Validation (Checkpoint)

**Validate that analysis will be meaningful:**
- Check if target correlations were achieved
- Verify scale reliability (Cronbach's alpha ≥ 0.70)
- Assess statistical power for planned tests (≥0.80)
- Flag distribution problems

**Decision:**
- ✅ PROCEED - All checks pass
- ⚠️ CAUTION - Minor issues, note limitations
- ❌ REGENERATE - Critical issues, return to Phase 3

**Outputs:** `outputs/feasibility/data_feasibility_report.md`

### Phase 5: Analysis

Full statistical analysis:
- Compute descriptive statistics (M, SD, skewness, kurtosis)
- Test hypotheses (Pearson correlations, t-tests, ANOVA)
- Calculate reliability (Cronbach's alpha)
- Generate visualizations (histograms, scatterplots, correlation matrices)

**Outputs:** `outputs/analysis/`

### Phase 6: Writing

Compose the thesis:
- Introduction, Theoretical Framework, Methods, Results, Conclusions
- Generate Abstract with keywords
- Format all citations in APA style
- Assemble final document

**Outputs:** `outputs/thesis/`

## Customization

### Custom Instruments

If your instrument isn't well-known, create a definition file:

```json
// inputs/instruments.json
{
  "instruments": [
    {
      "name": "XYZ-20",
      "full_name": "XYZ Assessment Scale",
      "author": "Smith, 2020",
      "items": 20,
      "subscales": [
        {"name": "factor_a", "items": [1,2,3,4,5,6,7,8,9,10]},
        {"name": "factor_b", "items": [11,12,13,14,15,16,17,18,19,20]}
      ],
      "scale_type": "likert",
      "scale_range": [1, 5],
      "scoring": "mean_per_subscale"
    }
  ]
}
```

### Custom Demographics

Create `inputs/demographics.json` to customize your sample profile:

```json
{
  "n": 100,
  "variables": {
    "age": {"mean": 22, "std": 3, "min": 18, "max": 35},
    "gender": {"categories": {"female": 0.65, "male": 0.35}},
    "education": {"categories": {"high_school": 0.25, "bachelor": 0.75}}
  }
}
```

See `skills/data-simulator/references/demographics_template.md` for more options.

### Language

The toolkit generates English output by default. For other languages, specify in your prompt:

> "Write all thesis chapters in Romanian"

## Key Output Files

| Phase | File | Description |
|-------|------|-------------|
| 1 | `outputs/research/instruments_detailed.json` | Full instrument specifications |
| 1 | `outputs/research/bibliography.json` | APA-formatted sources |
| 2 | `outputs/feasibility/direction_recommendation.md` | Recommended research angle |
| 3 | `outputs/data/responses_raw.csv` | Item-level responses |
| 3 | `outputs/data/computed_scores.csv` | Schema/domain scores |
| 4 | `outputs/feasibility/data_feasibility_report.md` | Data validation results |
| 5 | `outputs/analysis/hypothesis_tests.json` | All hypothesis test results |
| 5 | `outputs/analysis/figures/*.png` | Publication-quality visualizations |
| 6 | `outputs/thesis/thesis_draft.docx` | Final formatted document |

## Repository Structure

```
thesis-generator/
├── CLAUDE.md              # AI instruction file (read this first)
├── README.md              # This file (human documentation)
├── run.py                 # CLI entry point
├── inputs/                # Your configuration files
│   └── instruments_template.json
├── outputs/               # Generated during execution
│   ├── research/          # Literature & instrument data
│   ├── feasibility/       # Direction & data validation reports
│   ├── data/              # Simulated dataset
│   ├── analysis/          # Statistical results & figures
│   └── thesis/            # Final document
└── skills/                # Modular AI skill definitions
    ├── research/          # Literature gathering
    ├── feasibility-research/  # Scientific direction discovery
    ├── data-simulator/    # Data generation
    ├── feasibility-data/  # Data quality validation
    ├── data-analysis/     # Statistical analysis
    └── thesis-writer/     # Academic writing
```

## Important Notes

### This is a Drafting Tool

The generated thesis is a **first draft** for rapid prototyping. You should:

- Use it to understand thesis structure
- Use it as a starting point for writing
- Learn about statistical analysis approaches
- Practice the research-to-writing workflow

You should NOT:

- Submit it as your own work without substantial revision
- Assume all citations are accurate (verify them)
- Use simulated data for actual research publications

### Data is Simulated

The data generation phase creates **synthetic responses** that:
- Have realistic statistical properties
- Show expected theoretical relationships
- Are suitable for demonstrating analysis techniques

This is NOT real data and should be clearly labeled as simulated in any academic context.

### Citation Verification

While the research phase gathers real sources, always:
- Verify that cited papers exist
- Check that quotes and findings are accurate
- Access original sources when possible

## Troubleshooting

### "Instrument not found"

If the AI can't find instrument details:
1. Check spelling of instrument name
2. Provide the full name, not just abbreviation
3. Create a manual definition in `inputs/instruments.json`

### "Insufficient literature"

If fewer sources than expected:
1. Broaden the construct terms
2. Include related concepts
3. Extend date range to 2015+

### Analysis errors

If statistical analysis fails:
1. Check that data simulation completed successfully
2. Verify `outputs/data/responses_coded.xlsx` exists
3. Ensure sample size is adequate (N >= 30)

## Contributing

To extend the toolkit:

1. **New instruments**: Add specifications to `inputs/instruments.json`
2. **New analyses**: Add functions to `skills/data-analysis/SKILL.md`
3. **New demographics**: Add profiles to `skills/data-simulator/references/demographics_template.md`

## License

This toolkit is provided for educational and research prototyping purposes.
