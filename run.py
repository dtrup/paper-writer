#!/usr/bin/env python3
"""
Thesis Draft Generator

Entry point for the thesis generation workflow.
See CLAUDE.md for full documentation.

Usage:
    # Full pipeline with arguments
    python run.py --theme "Construct A and Construct B" --instruments "SCALE1,SCALE2" --sample 50

    # Individual phases (6-phase workflow with feasibility checkpoints)
    python run.py --phase research
    python run.py --phase feasibility-research
    python run.py --phase simulate
    python run.py --phase feasibility-data
    python run.py --phase analyze
    python run.py --phase write

Examples:
    python run.py --theme "Emotional Intelligence and Job Performance" --instruments "EQ-i,JPI" --sample 100
    python run.py --full  # Uses existing inputs/config.json
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Configuration
REPO_ROOT = Path(__file__).parent
SKILLS_DIR = REPO_ROOT / "skills"
INPUTS_DIR = REPO_ROOT / "inputs"
OUTPUTS_DIR = REPO_ROOT / "outputs"

PHASES = ["research", "feasibility-research", "simulate", "feasibility-data", "analyze", "write"]

def setup_directories():
    """Create output directories if they don't exist."""
    for subdir in ["research", "feasibility", "data", "analysis", "thesis/chapters"]:
        (OUTPUTS_DIR / subdir).mkdir(parents=True, exist_ok=True)
    INPUTS_DIR.mkdir(exist_ok=True)

def parse_instruments(instruments_str: str) -> list:
    """Parse comma-separated instrument names."""
    return [i.strip() for i in instruments_str.split(",")]

def create_config(theme: str, instruments: list, sample_size: int) -> dict:
    """Create configuration for the pipeline."""
    return {
        "theme": theme,
        "instruments": instruments,
        "sample_size": sample_size,
        "created": datetime.now().isoformat(),
        "phases": {phase: {"status": "pending"} for phase in PHASES}
    }

def save_config(config: dict):
    """Save configuration to inputs directory."""
    config_path = INPUTS_DIR / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Configuration saved to {config_path}")

def load_config() -> dict:
    """Load existing configuration."""
    config_path = INPUTS_DIR / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"No configuration found at {config_path}. Run with --theme and --instruments first.")
    with open(config_path) as f:
        return json.load(f)

def print_phase_instructions(phase: str):
    """Print instructions for executing a phase."""
    instructions = {
        "research": """
+----------------------------------------------------------------------+
|  PHASE 1: RESEARCH                                                   |
+----------------------------------------------------------------------+
|  Skill: skills/research/SKILL.md                                     |
|                                                                      |
|  Tasks:                                                              |
|  1. Search literature for each construct in the theme                |
|  2. Gather instrument specifications                                 |
|  3. Build bibliography (25-40 recent sources)                        |
|  4. Document expected relationships between constructs               |
|                                                                      |
|  Outputs:                                                            |
|  - outputs/research/literature_review.md                             |
|  - outputs/research/constructs.json                                  |
|  - outputs/research/instruments_detailed.json                        |
|  - outputs/research/bibliography.json                                |
+----------------------------------------------------------------------+
""",
        "feasibility-research": """
+----------------------------------------------------------------------+
|  PHASE 2: FEASIBILITY - RESEARCH DIRECTION                           |
+----------------------------------------------------------------------+
|  Skill: skills/feasibility-research/SKILL.md                         |
|                                                                      |
|  CHECKPOINT: Discover the most scientifically relevant direction.    |
|                                                                      |
|  Tasks:                                                              |
|  1. Map established vs. novel findings                               |
|  2. Identify gaps and opportunities                                  |
|  3. Evaluate hypothesis options (novelty, feasibility, interest)     |
|  4. Recommend optimal research direction                             |
|                                                                      |
|  Outputs:                                                            |
|  - outputs/feasibility/research_landscape.json                       |
|  - outputs/feasibility/direction_recommendation.md                   |
|  - outputs/feasibility/feasibility_matrix.md                         |
|                                                                      |
|  >> Review direction_recommendation.md before proceeding! <<         |
+----------------------------------------------------------------------+
""",
        "simulate": """
+----------------------------------------------------------------------+
|  PHASE 3: DATA SIMULATION                                            |
+----------------------------------------------------------------------+
|  Skill: skills/data-simulator/SKILL.md                               |
|                                                                      |
|  Tasks:                                                              |
|  1. Load instrument specs and refined hypotheses                     |
|  2. Generate demographics (Romanian sample by default)               |
|  3. Simulate responses with embedded correlations                    |
|  4. Compute subscale scores                                          |
|                                                                      |
|  Outputs:                                                            |
|  - outputs/data/demographics.csv                                     |
|  - outputs/data/responses_raw.csv                                    |
|  - outputs/data/responses_coded.xlsx                                 |
|  - outputs/data/simulation_parameters.json                           |
+----------------------------------------------------------------------+
""",
        "feasibility-data": """
+----------------------------------------------------------------------+
|  PHASE 4: FEASIBILITY - DATA VALIDATION                              |
+----------------------------------------------------------------------+
|  Skill: skills/feasibility-data/SKILL.md                             |
|                                                                      |
|  CHECKPOINT: Validate data quality before full analysis.             |
|                                                                      |
|  Tasks:                                                              |
|  1. Check if target correlations were achieved                       |
|  2. Verify scale reliability (alpha >= 0.70)                         |
|  3. Assess statistical power for planned tests                       |
|  4. Flag distribution problems                                       |
|                                                                      |
|  Outputs:                                                            |
|  - outputs/feasibility/data_quality.json                             |
|  - outputs/feasibility/data_feasibility_report.md                    |
|                                                                      |
|  Decision:                                                           |
|  - PROCEED: All checks pass                                          |
|  - CAUTION: Minor issues, note limitations                           |
|  - REGENERATE: Critical issues, return to Phase 3                    |
+----------------------------------------------------------------------+
""",
        "analyze": """
+----------------------------------------------------------------------+
|  PHASE 5: DATA ANALYSIS                                              |
+----------------------------------------------------------------------+
|  Skill: skills/data-analysis/SKILL.md                                |
|                                                                      |
|  Tasks:                                                              |
|  1. Compute descriptive statistics                                   |
|  2. Test hypotheses (correlations, t-tests, ANOVA)                   |
|  3. Calculate reliability (Cronbach's alpha)                         |
|  4. Generate visualizations                                          |
|                                                                      |
|  Outputs:                                                            |
|  - outputs/analysis/descriptive_stats.json                           |
|  - outputs/analysis/hypothesis_tests.json                            |
|  - outputs/analysis/reliability.json                                 |
|  - outputs/analysis/figures/*.png                                    |
|  - outputs/analysis/tables/*.md                                      |
+----------------------------------------------------------------------+
""",
        "write": """
+----------------------------------------------------------------------+
|  PHASE 6: THESIS WRITING                                             |
+----------------------------------------------------------------------+
|  Skill: skills/thesis-writer/SKILL.md                                |
|                                                                      |
|  Tasks:                                                              |
|  1. Compose Introduction                                             |
|  2. Write Chapter 1 (Theory) from literature_review.md               |
|  3. Write Chapter 2 (Methods) from instruments_detailed.json         |
|  4. Write Chapter 3 (Results) from analysis outputs                  |
|  5. Write Chapter 4 (Conclusions)                                    |
|  6. Generate Abstract                                                |
|  7. Assemble final document                                          |
|                                                                      |
|  Outputs:                                                            |
|  - outputs/thesis/chapters/*.md                                      |
|  - outputs/thesis/thesis_draft.docx                                  |
+----------------------------------------------------------------------+
"""
    }
    print(instructions.get(phase, f"Unknown phase: {phase}"))

def print_full_workflow(config: dict):
    """Print the full workflow overview."""
    print(f"""
+======================================================================+
|  THESIS DRAFT GENERATOR                                              |
+======================================================================+
|  Theme: {config['theme'][:56]:<56} |
|  Instruments: {', '.join(config['instruments']):<52} |
|  Sample Size: {config['sample_size']:<53} |
+----------------------------------------------------------------------+
|  WORKFLOW (6 phases with 2 feasibility checkpoints):                 |
|                                                                      |
|  Phase 1: RESEARCH              -> Gather literature & instruments   |
|  Phase 2: FEASIBILITY-RESEARCH  -> Discover best direction [CHECK]   |
|  Phase 3: SIMULATE              -> Generate realistic data           |
|  Phase 4: FEASIBILITY-DATA      -> Validate data quality [CHECK]     |
|  Phase 5: ANALYZE               -> Statistical analysis              |
|  Phase 6: WRITE                 -> Compose thesis chapters           |
|                                                                      |
|  Execute phases sequentially. Review checkpoints before proceeding.  |
+======================================================================+
""")

def main():
    parser = argparse.ArgumentParser(
        description="Thesis Draft Generator for Social Sciences",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Configuration arguments
    parser.add_argument("--theme", help="Research theme (e.g., 'Emotional Intelligence and Burnout')")
    parser.add_argument("--instruments", help="Comma-separated instrument names (e.g., 'EQ-i,MBI')")
    parser.add_argument("--sample", type=int, default=50, help="Sample size (default: 50)")

    # Phase selection
    parser.add_argument("--phase", choices=PHASES, help="Run specific phase")
    parser.add_argument("--full", action="store_true", help="Show full workflow")

    # Utility options
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--config", help="Path to custom config file")

    args = parser.parse_args()

    # Setup directories
    setup_directories()

    # Handle configuration
    if args.theme and args.instruments:
        instruments = parse_instruments(args.instruments)
        config = create_config(args.theme, instruments, args.sample)
        save_config(config)
    elif args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        try:
            config = load_config()
        except FileNotFoundError as e:
            if not args.status:
                print(f"Error: {e}")
                print("\nRun with --theme and --instruments to initialize:")
                print('  python run.py --theme "Your Theme" --instruments "SCALE1,SCALE2"')
                sys.exit(1)
            config = None

    # Execute requested action
    if args.status:
        if config:
            print(f"\nCurrent configuration:")
            print(f"  Theme: {config['theme']}")
            print(f"  Instruments: {', '.join(config['instruments'])}")
            print(f"  Sample: {config['sample_size']}")
            print(f"\nPhase status:")
            for phase in PHASES:
                status = config.get('phases', {}).get(phase, {}).get('status', 'unknown')
                marker = "  " if status == "pending" else "* "
                print(f"  {marker}{phase}: {status}")
        else:
            print("No configuration found. Initialize with --theme and --instruments.")
    elif args.phase:
        print_phase_instructions(args.phase)
    elif args.full or config:
        print_full_workflow(config)
        print("\nTo execute a phase, run:")
        for phase in PHASES:
            print(f"  python run.py --phase {phase}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
