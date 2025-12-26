---
name: research
description: "Gather academic literature and instrument/measurement specifications for thesis research. Use when: (1) Researching academic constructs or variables, (2) Finding instrument details (items, subscales, scoring, validity), (3) Building literature reviews with recent sources, (4) Identifying theoretical frameworks and key authors."
---

# Research Skill

Systematic literature gathering and measurement specification for academic thesis work.

## Core Workflow

### Step 1: Parse Research Theme
Extract constructs/variables from the theme string:
- "X and Y" → ["X", "Y"]
- "The Effect of A on B" → ["A", "B"]
- "Relationship between P, Q, and R" → ["P", "Q", "R"]

### Step 2: Gather Literature Per Construct

For each construct, execute searches in this order:

**Search 1 - Recent empirical work (2020-2025):**
```
"{construct}" empirical study 2023 OR 2024
```

**Search 2 - Recent reviews/meta-analyses:**
```
"{construct}" systematic review OR meta-analysis 2020-2024
```

**Search 3 - Foundational/seminal works:**
```
"{construct}" seminal theory definition
```

**Search 4 - Measurement/instruments:**
```
"{construct}" scale questionnaire measurement validation
```

### Step 3: Extract and Synthesize

From each quality source, extract:
- **Definition**: How the construct is defined
- **Dimensions**: Subdimensions or components
- **Theoretical framework**: Which theory situates it
- **Key findings**: Empirical relationships with other variables
- **Measurement**: How it's typically measured

### Step 4: Instrument Specification

For each named instrument, gather:

```json
{
  "name": "INSTRUMENT_CODE",
  "full_name": "Full Instrument Name",
  "authors": "Author(s)",
  "year": 2000,
  "purpose": "What the instrument measures",
  "items": 40,
  "subscales": [
    {
      "name": "subscale_1",
      "items": [1, 2, 3, 4, 5],
      "description": "What this subscale measures"
    }
  ],
  "scale_type": "likert",
  "scale_range": [1, 5],
  "scale_anchors": {"1": "strongly disagree", "5": "strongly agree"},
  "scoring": "mean_per_subscale",
  "reverse_scored": [],
  "validity": {
    "cronbach_alpha": 0.85,
    "test_retest": "adequate",
    "convergent": "correlates with related measures"
  },
  "norms": {
    "population": "general adult",
    "means": {"subscale_1": 3.5}
  }
}
```

### Step 5: Build Bibliography

Format all sources in APA 7th edition:

**Journal article:**
```
Author, A. A., & Author, B. B. (Year). Title of article. Journal Name, Volume(Issue), pages. https://doi.org/xxx
```

**Book chapter:**
```
Author, A. A. (Year). Title of chapter. In E. E. Editor (Ed.), Title of book (pp. xx-xx). Publisher.
```

**Book:**
```
Author, A. A. (Year). Title of work: Capital letter also for subtitle. Publisher.
```

## Output Structure

Save all outputs to `outputs/research/`:

### literature_review.md
```markdown
# Literature Review: [Theme]

## 1. [Construct 1 Name]

### 1.1 Definition and Conceptualization
[Synthesized definition with citations]

### 1.2 Theoretical Frameworks
[Major theories and models]

### 1.3 Dimensions and Components
[Subdimensions with descriptions]

### 1.4 Empirical Findings
[Key relationships with other variables]

### 1.5 Measurement Approaches
[How the construct is typically measured]

## 2. [Construct 2 Name]
[Same structure]

## 3. Relationship Between Constructs
[What existing research says about their relationship]

## References
[APA formatted list]
```

### constructs.json
```json
{
  "constructs": [
    {
      "name": "construct_name",
      "definition": "...",
      "dimensions": ["dim1", "dim2", "dim3"],
      "key_theorists": ["Author1", "Author2"],
      "related_constructs": ["related1", "related2"],
      "typical_correlates": {
        "positive": ["var1", "var2"],
        "negative": ["var3", "var4"]
      }
    }
  ],
  "expected_relationships": {
    "construct1_construct2": {
      "direction": "negative",
      "strength": "moderate_to_strong",
      "theoretical_basis": "..."
    }
  }
}
```

### instruments_detailed.json
Full instrument specifications as shown in Step 4.

### bibliography.json
```json
{
  "sources": [
    {
      "id": "author2023",
      "type": "journal",
      "authors": ["Author, A. A."],
      "year": 2023,
      "title": "Title of article",
      "journal": "Journal Name",
      "volume": 25,
      "issue": 3,
      "pages": "275-324",
      "doi": "10.1177/xxx",
      "apa": "Author, A. A. (2023). Title of article. Journal Name, 25(3), 275-324."
    }
  ]
}
```

## Search Quality Criteria

### Prioritize These Sources
- Peer-reviewed journals
- Academic handbooks (Cambridge, Oxford, Springer)
- Meta-analyses and systematic reviews
- Instrument validation studies
- Works by construct originators

### Avoid These Sources
- Wikipedia (use only for initial orientation, never cite)
- Non-peer-reviewed blogs
- Predatory journals
- Sources older than 2010 unless seminal

### Minimum Source Requirements
- **Theoretical chapter**: 25-40 sources
- **Per construct**: 10-15 sources minimum
- **Recent sources (2020+)**: At least 40% of total
- **Seminal works**: 3-5 foundational sources per construct

## Error Handling

### Instrument Not Found
If instrument details cannot be found:
1. Log warning to `outputs/research/warnings.log`
2. Create placeholder in `inputs/missing_instruments.json`
3. Prompt user: "Could not find full specification for [INSTRUMENT]. Please provide item texts and scoring."

### Insufficient Literature
If fewer than 10 sources found for a construct:
1. Broaden search terms (use synonyms, related concepts)
2. Extend date range to 2015+
3. Include dissertation abstracts as secondary sources
4. Log issue and proceed with available sources
