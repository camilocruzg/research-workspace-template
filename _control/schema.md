---
title: Workspace Schema
type: living-document
last-updated: YYYY-MM-DD
review-cadence: monthly
---

# Workspace Schema

*The structure of the workspace: what lives where, how things get filed, how to find them. `CLAUDE.md` carries the working agreement; this file carries the map. Read it when you need to understand the workspace itself, not just its current state. Change it deliberately — when the schema and the folders disagree, fix one of them.*

---

## The join key

**The project folder name is the join key across every location.** `projects/example-project/`, the artefacts root `~/Artefacts/example-project/`, the `[example-project]` tag in `open-loops.md`, and the `## [example-project]` entry in `projects.md` all use the same string. Never abbreviate it. That one convention is what lets the agent follow a project from a task to its documents to its code.

---

## Layers

| Layer | Location | Who writes | Holds |
|---|---|---|---|
| Control | `_control/` | Agent, on approval | Operational state: what is open, active, in motion. Loaded every session. |
| Daily | `daily/YYYY/` | Agent + you | The log: what happened, what was decided, tomorrow's handoff |
| Projects | `projects/[name]/` | Agent + you | Operational documents per project: status, handoff, specs, drafts |
| Knowledge | `wiki/` | Agent, on approval | Synthesis that outlasts any one project: concepts, arguments, positions |

The daily note is where things happen; the control files record where things stand; the wiki records what you have come to think.

---

## Folder map

### `_control/`
| File | Purpose | Cadence |
|---|---|---|
| `context.md` | Who you are, goals, working style | Monthly |
| `projects.md` | Where each project stands (single source of truth) | As things change |
| `open-loops.md` | Everything pending | Daily, with subtraction at close-day |
| `schema.md` | This file | When the structure changes |

### `daily/YYYY/YYYY-MM-DD.md`
One note per working day, from `templates/daily-note.md`. The **💡 Conceptual Developments** section is where new ideas land first, before any decision about whether they are worth keeping. The **End of Day → Tomorrow** line is the handoff the next morning's brief starts from.

### `projects/[name]/`
| File | Purpose |
|---|---|
| `README.md` | Objectives, current status, changelog |
| `thread.md` | Session handoff: current state, live question, re-entry point. Replaced, not appended. |
| `artefacts.md` | Register of everything the project produced that lives outside the workspace |
| `docs/` | Specs, drafts, meeting notes, design documents |
| `deliverables/` | Final, submitted versions: documents of record |

### `wiki/`
| Path | Purpose |
|---|---|
| `concepts/` | One page per idea, argument or position, spanning projects. Claim first, support beneath. |
| `index.md` | Entry point: one line per concept page |
| `log.md` | Append-only record of what was filed to the wiki and why |

Link between pages with `[[page-name]]`. Concept pages link to the projects that feed them; project READMEs link to the concepts they contribute to.

### Other
- `_inbox/` — quick notes (`status: inbox`) waiting for `inbox-capture`; processed notes move to `_inbox/_captured/`.
- `reviews/weekly/` — weekly syntheses.
- `templates/` — daily note, project README, thread, artefacts register.
- `tools/` — `check-open-loops.py` (close-day, lint), `check-wiki-drift.py` (weekly-synthesis).

---

## How ideas become knowledge

1. **Emerge.** An idea surfaces while working — in a conversation, a meeting, a draft. It is logged under 💡 Conceptual Developments in that day's note. No judgement yet.
2. **Promote.** At close-day or weekly synthesis, ideas that keep coming back, or that change how a project is framed, are proposed as a new wiki concept page or as a revision to an existing one.
3. **Revise, don't pile up.** A concept page states its claim at the top. New material should be able to change that claim. Once a week, `check-wiki-drift.py` names the one page that has accumulated most under an unexamined claim; the weekly synthesis revises the claim, compresses the support, or splits the page. **The page must not come out longer than it went in.**

The wiki is fed by work. A literature layer (sources ingested into concept pages) can be added later; it is not needed to start.

---

## Artefact storage: study and workshop

**Principle.** The workspace stores *documents* — text and small assets, the things you think with. What projects *produce* — code, datasets, media, exports, experiments — lives outside it and is **registered** in the project's `artefacts.md`. An artefact that is not registered does not officially exist.

One decision per file: **is this a document I think with, or a thing the project produced?**

| Kind | Where it lives | Visibility | Storage |
|---|---|---|---|
| Documents (notes, specs, drafts, threads) | The workspace | Private repo; synced across your machines | Small, text |
| Artefacts (code, data, media, exports) | Artefacts root: `~/Artefacts/[project-name]/` | Local, not synced; code may have its own repo | Heavy |
| Governed data (participant data, anything under an ethics or confidentiality agreement) | The storage that agreement specifies | As the agreement requires | Never the workspace or the artefacts root — register only the reference |
| Remote material (servers, shared drives) | Where it already is | As set by its owner | The register points to it |
| Final deliverables (submitted PDFs, final reports) | `projects/[name]/deliverables/` | With the workspace | Small, immutable, worth keeping with the record |

*Set your artefacts root here if it differs from `~/Artefacts/`.*

Inside the artefacts root, `code/`, `data/`, `media/` and `outputs/` subfolders are a helpful default, not a rule. The register, not the folder layout, is how things get found.

**Size rule.** Anything over ~10 MB, any dataset, any code repository and any media goes to its home outside the workspace and is registered.

**Lifecycle.** Register entries move `working` → `current` → `archived`. When something is superseded, mark it archived rather than deleting the entry; that keeps the trail of which version produced which result.

**Starting from a mess.** Register before moving. List scattered artefacts where they currently sit (Desktop, Downloads, shared drives) in `artefacts.md` without moving anything; move each one to its home the next time you touch it.

---

## Filing rules

| Content | Destination |
|---|---|
| Meeting notes | Daily note Log → project `docs/` if substantial |
| Decisions | Daily note Decisions Made + `open-loops.md` if action follows |
| New tasks | `open-loops.md` under the project heading |
| Project state change | `projects.md` (Status / Recent / Next) + README Current Status |
| New idea, framing, shift in thinking | Daily note 💡 → wiki concept page if it holds |
| Specs, drafts, design docs | `projects/[name]/docs/` |
| Code, data, media, large files | Artefacts root + register in `projects/[name]/artefacts.md` |
| Governed data | Approved storage + register the reference only |
| Final deliverables | `projects/[name]/deliverables/` |
| Quick fragments | `_inbox/` via `note` |

---

## Navigation

- **Where does project X stand?** → `projects.md`, then `projects/[name]/README.md`
- **What do I need to do?** → `open-loops.md`
- **Where did I leave X?** → `projects/[name]/thread.md`
- **Where is the dataset / code / recording for X?** → `projects/[name]/artefacts.md`, always, wherever the thing physically sits
- **What do I think about Y?** → `wiki/index.md`, then `wiki/concepts/`
- **What happened this week?** → `daily/`, or `reviews/weekly/`
