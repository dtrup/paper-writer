# Demographics Configuration

Configure your sample demographics in `inputs/demographics.json`. Default is Romanian adult sample.

## Default: Romanian Adult Sample

```json
{
  "sample_type": "romanian_adult",
  "n": 50,
  "variables": {
    "age": {
      "distribution": "normal_truncated",
      "mean": 44,
      "std": 12,
      "min": 18,
      "max": 70
    },
    "gender": {
      "distribution": "categorical",
      "categories": {"female": 0.80, "male": 0.20}
    },
    "education": {
      "distribution": "categorical",
      "categories": {
        "highschool": 0.16,
        "bachelor": 0.46,
        "master": 0.34,
        "phd": 0.04
      }
    },
    "religion": {
      "distribution": "categorical",
      "categories": {
        "orthodox": 0.88,
        "catholic": 0.04,
        "protestant": 0.03,
        "other": 0.03,
        "none": 0.02
      }
    },
    "residence": {
      "distribution": "categorical",
      "categories": {"urban": 0.54, "rural": 0.46}
    }
  }
}
```

Note: Psychology samples in Romania skew heavily female (70-85%) due to field demographics.

## Romanian Sample Presets

### University Student Sample
```json
{
  "sample_type": "romanian_student",
  "n": 100,
  "variables": {
    "age": {"mean": 22, "std": 3, "min": 18, "max": 35},
    "gender": {"categories": {"female": 0.75, "male": 0.25}},
    "education": {"categories": {"highschool": 0.30, "bachelor": 0.70}},
    "residence": {"categories": {"urban": 0.85, "rural": 0.15}}
  }
}
```

### Clinical/Professional Sample
```json
{
  "sample_type": "romanian_professional",
  "n": 80,
  "variables": {
    "age": {"mean": 38, "std": 10, "min": 25, "max": 65},
    "gender": {"categories": {"female": 0.70, "male": 0.30}},
    "education": {"categories": {"bachelor": 0.40, "master": 0.50, "phd": 0.10}},
    "work_experience_years": {"mean": 12, "std": 8, "min": 1, "max": 40}
  }
}
```

## Romanian Demographics Reference

### Age Distribution by Sample Type
| Sample Type | Mean | SD | Range |
|-------------|------|-----|-------|
| General adult | 42 | 15 | 18-75 |
| University student | 22 | 3 | 18-35 |
| Professional | 38-44 | 10-12 | 25-65 |

### Gender in Psychology Samples
- General population: 51% female, 49% male
- Psychology students/professionals: 75-85% female

### Education (Educated Urban Sample)
| Level | Proportion |
|-------|------------|
| High school | 16% |
| Bachelor | 46% |
| Master | 34% |
| PhD | 4% |

### Religion
| Denomination | Proportion |
|--------------|------------|
| Orthodox | 86-88% |
| Roman Catholic | 4% |
| Protestant/Reformed | 3% |
| Other | 3% |
| None | 2% |

### Residence
- Urban: 54%
- Rural: 46%

### Marital Status
```json
"marital_status": {
  "categories": {
    "single": 0.30,
    "married": 0.50,
    "divorced": 0.12,
    "widowed": 0.05,
    "cohabiting": 0.03
  }
}
```

### Employment
```json
"employment": {
  "categories": {
    "employed_fulltime": 0.45,
    "employed_parttime": 0.08,
    "self_employed": 0.07,
    "unemployed": 0.05,
    "student": 0.10,
    "retired": 0.20,
    "homemaker": 0.05
  }
}
```

## Generational Cohorts

Derived automatically from age:

| Generation | Birth Years | Age in 2025 |
|------------|-------------|-------------|
| Gen Z | 1997-2012 | 13-28 |
| Millennial | 1981-1996 | 29-44 |
| Gen X | 1965-1980 | 45-60 |
| Boomer | 1946-1964 | 61-79 |

```python
def assign_generation(age, reference_year=2025):
    birth_year = reference_year - age
    if birth_year >= 1997:
        return "gen_z"
    elif birth_year >= 1981:
        return "millennial"
    elif birth_year >= 1965:
        return "gen_x"
    elif birth_year >= 1946:
        return "boomer"
    else:
        return "silent"
```

## Optional Variables

### Spiritual/Personal Development Practice
For research on wisdom, wellbeing, personal growth:

```json
"spiritual_practice": {
  "categories": {"yes": 0.50, "no": 0.50}
},
"practice_types": {
  "categories": {
    "prayer": 0.50,
    "meditation": 0.35,
    "yoga": 0.25,
    "mindfulness": 0.20,
    "other": 0.15
  }
}
```

### Income Level
```json
"income": {
  "categories": {
    "below_average": 0.30,
    "average": 0.45,
    "above_average": 0.25
  }
}
```

## Custom Configuration

Create `inputs/demographics.json` with any combination of variables above. Only include what's relevant to your research.
