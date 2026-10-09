---
title: Artefacts Register — example-project
type: artefacts-register
last-updated: YYYY-MM-DD
---

# Artefacts Register — example-project

Everything this project produced that lives outside the workspace: where it is, who owns it, which version is current. An artefact that is not registered here does not officially exist. Update at the end of any session that produces, moves or supersedes one.

**Artefacts root:** `~/Artefacts/example-project/`

Lifecycle: **working** (in development) → **current** (the version in use for a stated purpose) → **archived** (superseded; kept for the record, never deleted from the register).

*The entries below are illustrative. Replace them with your own.*

---

## Code

### analysis-scripts
- **Location:** `~/Artefacts/example-project/code/analysis-scripts/` (own git repository)
- **Status:** current
- **Notes:** `python run.py --input ../data/survey-clean.csv` produces the figures under Outputs.

---

## Data

### survey responses (raw)
- **Location:** Institutional research storage, `[project storage reference]`
- **Origin:** Online survey, collected YYYY-MM to YYYY-MM
- **Governance:** Covered by ethics approval `[number]`; identifiable data, must stay in approved storage. Only this reference lives in the workspace.
- **Status:** current

### survey responses (de-identified)
- **Location:** `~/Artefacts/example-project/data/survey-clean.csv`
- **Origin:** Produced from the raw responses by `analysis-scripts/deidentify.py`
- **Governance:** De-identified working copy, as permitted by the approval
- **Status:** current

---

## Media

### site photographs
- **Location:** `~/Artefacts/example-project/media/site-visit-YYYY-MM-DD/`
- **Status:** current

---

## Outputs

*Exports, figures, decks. Final submitted versions go to `projects/example-project/deliverables/` in the workspace.*

| Purpose | Artefact | Location | Version / date | Status |
|---|---|---|---|---|
| Paper, Figure 2 | response distribution chart | `~/Artefacts/example-project/outputs/fig2-v2.pdf` | v2, YYYY-MM-DD | current |
| Paper, Figure 2 | response distribution chart | `~/Artefacts/example-project/outputs/fig2-v1.pdf` | v1, YYYY-MM-DD | archived |
| Progress meeting | slide deck | `~/Artefacts/example-project/outputs/progress-deck.pdf` | YYYY-MM-DD | current |
