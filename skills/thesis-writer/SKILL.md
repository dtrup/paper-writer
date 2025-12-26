---
name: thesis-writer
description: "Compose academic thesis chapters with proper structure, APA formatting, and integration of research and analysis outputs. Use when: (1) Writing theoretical/literature review chapters, (2) Composing methods and results sections, (3) Generating abstract, introduction, and conclusions, (4) Formatting citations and bibliography in APA style, (5) Assembling final thesis document."
---

# Thesis Writer Skill

Academic writing and document composition for social science bachelor theses.

## Thesis Structure Template

```
TITLE PAGE
TABLE OF CONTENTS
LIST OF TABLES
LIST OF FIGURES
ABSTRACT (150-300 words)

INTRODUCTION (2-4 pages)
- Research context and relevance
- Problem statement
- Research objectives
- Thesis structure overview

CHAPTER 1: THEORETICAL FRAMEWORK (15-25 pages)
1.1 [Construct 1]
    1.1.1 Definition and conceptualization
    1.1.2 Theoretical models
    1.1.3 Dimensions/components
1.2 [Construct 2]
    1.2.1 Definition and conceptualization
    1.2.2 Classification/types
    1.2.3 Detailed descriptions
1.3 Relationship between constructs

CHAPTER 2: METHODOLOGY (3-5 pages)
2.1 Research methods for [Construct 1]
2.2 Research methods for [Construct 2]
2.3 Instruments used in this study

CHAPTER 3: RESEARCH RESULTS (10-15 pages)
3.1 Purpose, objectives, and hypotheses
3.2 Sample description
3.3 Instruments and data collection procedures
3.4 Data analysis
    3.4.1 Descriptive statistics
    3.4.2 Hypothesis testing

CHAPTER 4: CONCLUSIONS (3-5 pages)
4.1 Summary of findings
4.2 Theoretical implications
4.3 Practical implications
4.4 Limitations
4.5 Future research directions

REFERENCES (APA format)

APPENDICES
- Appendix A: [Instrument 1] items
- Appendix B: [Instrument 2] items
```

## Writing Guidelines

### Academic Tone
- Third person ("The present research investigated..." not "I investigated...")
- Formal vocabulary (avoid colloquialisms)
- Precise terminology (use construct names consistently)
- Hedged claims where appropriate ("suggests," "indicates," "appears to")

### Paragraph Structure
```
1. Topic sentence (main claim)
2. Evidence/citation (supporting research)
3. Elaboration (explain significance)
4. Transition (connect to next point)
```

**Example:**
```
Wisdom has been conceptualized as a multidimensional construct integrating
cognitive, reflective, and affective components (Ardelt, 2003). The cognitive
dimension encompasses a deep understanding of life and the ability to perceive
truth beyond surface-level appearances. This understanding extends to recognizing
the complexity and ambiguity inherent in human existence. Such cognitive depth
distinguishes wisdom from mere intelligence or factual knowledge.
```

### Citation Integration

**Narrative citation:**
```
According to Ardelt (2003), wisdom represents the integration of three dimensions...
Vaillant (1993) demonstrated that defense mechanisms evolve across the lifespan...
```

**Parenthetical citation:**
```
Wisdom has been defined as a personality characteristic (Ardelt, 2003).
Defense mechanisms can be classified hierarchically (Vaillant, 1993; Perry & Bond, 2012).
```

**Multiple sources:**
```
Several researchers have emphasized the reflective component of wisdom 
(Ardelt, 2003; Staudinger & Glück, 2011; Webster, 2019).
```

### Numbers and Statistics
- Spell out numbers below 10 (unless statistical)
- Use numerals for statistics: "r = -.745, p < .001"
- Report effect sizes: "Cohen's d = 0.85"
- Include confidence intervals where appropriate

## Chapter-Specific Instructions

### Introduction

**Structure:**
1. Opening hook (broad context, why topic matters)
2. Narrow to specific research area
3. Gap in literature or need for study
4. Research purpose and objectives
5. Brief overview of methodology
6. Thesis structure preview

**Length:** 2-4 pages (500-1000 words)

**Template:**
```markdown
# Introduction

In recent decades, [broad context]. [Statistics or trend]. This raises the
question of [research area].

[Construct 1] has received increasing attention in psychological research
due to [reasons]. At the same time, [Construct 2] represents [brief definition].
Understanding the relationship between these constructs holds significance
for [practical implications].

Despite growing interest, [gap in literature]. Few studies have examined
[specific relationship]. The present research addresses this gap by
investigating [specific research question].

The primary objectives of this study are:
- O1: [First objective]
- O2: [Second objective]
- O3: [Third objective]

To address these objectives, [brief methodology]. A sample of [N] participants
completed [instruments].

This thesis is organized as follows: Chapter 1 presents the theoretical
framework, reviewing literature on [constructs]. Chapter 2 discusses
research methods and instruments. Chapter 3 reports the results of [analyses].
Finally, Chapter 4 offers conclusions, discusses implications, and
identifies directions for future research.
```

### Chapter 1: Theoretical Framework

**Source:** Pull from `outputs/research/literature_review.md`

**Structure per construct:**
1. Definition (how researchers define it)
2. Theoretical models (major frameworks)
3. Dimensions/components (subtypes or factors)
4. Measurement approaches (brief)
5. Key empirical findings

**Integration section:**
- What existing research says about relationship between constructs
- Theoretical rationale for expected relationships
- Research gap this study addresses

**Citation density:** Approximately 2-3 citations per paragraph

### Chapter 2: Methodology

**Structure:**
1. Overview of research methods in the field
2. Specific instruments used
   - Development history
   - Structure (items, subscales)
   - Psychometric properties
   - Scoring procedures
3. Why these instruments were chosen

**For each instrument, include:**
```markdown
## 2.X [Instrument Name]

The [Full Instrument Name] ([Abbreviation]; Author, Year) was developed
to measure [construct]. The instrument consists of [N] items organized
into [N] subscales: [list subscales].

Respondents rate each item on a [X]-point Likert scale ranging from
[anchor 1] to [anchor N]. Subscale scores are computed by [scoring method].

Psychometric properties have been established across multiple studies.
[Author] (Year) reported Cronbach's alpha values of [values] for [subscales].
Test-retest reliability over [period] was [value]. The scale demonstrates
[convergent/discriminant] validity through correlations with [related measures].

In the present study, the [language] version was used, validated by [process].
```

### Chapter 3: Results

**Source:** Pull from `outputs/analysis/`

**Structure:**
1. Research purpose, objectives, hypotheses (restate)
2. Sample description
   - Demographics table
   - Sample characteristics narrative
3. Instruments and procedures
4. Data analysis
   - Descriptive statistics per variable
   - Hypothesis testing (one section per hypothesis)

**Descriptive statistics format:**
```markdown
### 3.4.1 Descriptive Statistics

Table 3.1 presents descriptive statistics for [scale] scores. The mean
score was M = [value] (SD = [value]), indicating [interpretation]. The
distribution showed [skewness interpretation] (skewness = [value]) and
[kurtosis interpretation] (kurtosis = [value]).

*Table 3.1. Descriptive Statistics for [Scale]*
| Variable | N | M | SD | Min | Max | Skew | Kurt |
|----------|---|---|----|----|-----|------|------|
| [var1]   | 50| 3.54| 0.50| 2.30| 4.56| -0.01| 0.26|

*Figure 3.1. Distribution of [Variable]*
[Insert histogram]
```

**Hypothesis testing format:**
```markdown
### 3.4.2 Hypothesis Testing

**Hypothesis 1:** [State hypothesis]

A Pearson correlation analysis was conducted to examine the relationship
between [variable 1] and [variable 2]. Results indicated a [strength]
[direction] correlation, r(48) = [value], p [comparison] .05 (see Table 3.X
and Figure 3.X).

*Table 3.X. Correlation Between [Var1] and [Var2]*
| | [Var1] | [Var2] |
|----------|--------|--------|
| [Var1] | 1 | [r] |
| [Var2] | [r] | 1 |
| p-value | - | [p] |

This result [supports/does not support] Hypothesis 1. The [direction]
correlation suggests that [interpretation]. This finding aligns with
[previous research/theoretical expectations].
```

### Chapter 4: Conclusions

**Structure:**
1. Summary of main findings
2. Interpretation and theoretical implications
3. Practical implications
4. Limitations
5. Future research directions

**Template:**
```markdown
# Conclusions

## 4.1 Summary of Findings

The present research investigated [research question]. Based on a sample
of [N] participants, the following findings emerged:

Regarding Hypothesis 1, [summary of finding]. This represents a [effect size]
effect and [supports/contradicts] previous research by [Author] (Year).

[Continue for each hypothesis]

## 4.2 Theoretical Implications

These findings contribute to understanding [construct relationship] in
several ways. First, [implication 1]. Second, [implication 2].

The strong negative correlation between [construct 1] and [construct 2]
suggests that [theoretical interpretation]. This aligns with [theoretical
framework] proposed by [Author] (Year).

## 4.3 Practical Implications

From a practical perspective, these results suggest [application 1].
In [context], practitioners might consider [recommendation].

## 4.4 Limitations

Several limitations should be considered when interpreting these findings.
First, [limitation 1 - e.g., sample characteristics]. Second, [limitation 2 -
e.g., self-report measures]. Third, [limitation 3 - e.g., cross-sectional design].

## 4.5 Future Research

Future research should address these limitations by [suggestion 1].
Additionally, [suggestion 2] would extend understanding of [topic].
Longitudinal designs could examine [temporal question].
```

### Abstract

**Structure (IMRAD):**
- Introduction (1-2 sentences): Context and purpose
- Methods (1-2 sentences): Sample and instruments
- Results (2-3 sentences): Main findings
- Discussion (1-2 sentences): Implications

**Length:** 150-300 words

**Template:**
```markdown
# Abstract

The present research investigated [relationship/topic] conceptualized
according to [theoretical framework]. Specifically, the study examined
[specific relationships/hypotheses].

A sample of [N] participants ([demographics]) completed [instruments].
[Brief procedure note].

Results indicated [main finding 1]. [Main finding 2]. [Main finding 3
if applicable]. No significant relationships were found for [null findings].

These findings suggest [main implication]. [Secondary implication].
The [specific dimension/factor] appears particularly relevant for
[outcome]. Implications for [theory/practice] are discussed.

**Keywords:** [keyword1], [keyword2], [keyword3], [keyword4], [keyword5]
```

## APA Reference Formatting

### Journal Article
```
Author, A. A., Author, B. B., & Author, C. C. (Year). Title of article.
    Journal Name, Volume(Issue), pages. https://doi.org/xxxxx
```

### Book
```
Author, A. A. (Year). Title of work: Capital letter also for subtitle.
    Publisher.
```

### Edited Book Chapter
```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Title of
    book (pp. xx-xx). Publisher.
```

### Multiple Authors
- 2 authors: Author & Author (Year)
- 3+ authors: Author et al. (Year)

### In-Text Citation Examples
```
Single author: (Smith, 2020) or Smith (2020)
Two authors: (Smith & Jones, 2020) or Smith and Jones (2020)
Three+ authors: (Smith et al., 2020) or Smith et al. (2020)
Multiple works: (Smith, 2019, 2020; Jones et al., 2021)
Page numbers: (Smith, 2020, p. 45) or (Smith, 2020, pp. 45-47)
```

## Table and Figure Formatting

### Tables
```markdown
*Table [Chapter].[Number]. [Title in Italics]*

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| data | data | data |

*Note.* [Any explanatory notes]
```

### Figures
```markdown
*Figure [Chapter].[Number]. [Title in Italics]*

[Image]

*Source:* [source if applicable]
```

## Output Files

Generate to `outputs/thesis/`:

### chapters/
```
00_abstract.md
01_introduction.md
02_chapter1_theory.md
03_chapter2_methods.md
04_chapter3_results.md
05_chapter4_conclusions.md
06_references.md
07_appendix_a.md
08_appendix_b.md
```

### thesis_draft.docx
Assembled document with:
- Title page
- Table of contents (auto-generated)
- All chapters
- Proper heading styles (Heading 1, 2, 3)
- Page numbers
- APA-formatted references

## Assembly Script

Use the docx skill to assemble final document:
1. Read all chapter markdown files
2. Convert to docx with proper formatting
3. Insert tables and figures
4. Generate table of contents
5. Apply consistent styling

See `skills/docx/SKILL.md` for document creation procedures.
