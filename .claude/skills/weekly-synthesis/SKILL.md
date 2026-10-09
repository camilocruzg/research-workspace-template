---
name: weekly-synthesis
description: >
  Use this skill when the user wants a weekly review, synthesis, or summary
  of the week just completed. Trigger on: "weekly synthesis", "weekly review",
  "week summary", "end of week", "wrap up the week", "week in review", or any
  request to reflect on and record the week's progress across projects.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

Produce a synthesis of the week just completed.

## Step 1 — Week dates (use the script, not inference)

```bash
python3 .claude/skills/weekly-synthesis/scripts/get_date_info.py
```

Use `week_number`, `iso_year` and `week_range` from the output.

## Step 2 — Read (in parallel)

- This week's daily notes in `daily/YYYY/`
- `_control/projects.md`
- `_control/open-loops.md`
- `_control/context.md` (the goals section)

## Step 3 — Synthesise

A sentence or two per section unless the week warrants more:

**Week [iso_year]-[week_number] — [week_range]**

- **What moved** — concrete progress; name the project and the output.
- **What stalled** — what didn't move, and why if discernible.
- **Decisions made** — worth recording for later reference.
- **Conceptual developments** — shifts in thinking or framing.
- **Drift check** — does the week's effort match the goals in `context.md`? Name any gap plainly.
- **Open loops inherited** — key unresolved items carrying into next week.
- **Next week's shape** — what next week needs to prioritise.

## Step 4 — Confirm and save

Ask: "Save to `reviews/weekly/[iso_year]-[week_number].md`?" Write only on confirmation.

## Step 5 — Wiki consolidation (one page, once a week)

The weekly synthesis is the routine that runs when there is time to think, so consolidation happens here. Run:

```bash
python3 tools/check-wiki-drift.py
```

It ranks `wiki/concepts/` by how much has been added to each page since its opening claim was last revised, and names one target. Take that page and no others. One page a week adds up; a whole-wiki review becomes a project that does not get finished.

**Why.** Adding new material underneath a claim is the easy move, and over months it leaves the evidence growing while the argument stands still.

Read the claim against everything filed under it since, then do one of:

- **Revise the claim** — the new material has changed the argument, and the top of the page should say so. Cut the support down to what the revised claim needs.
- **Compress the support** — the claim holds, but several sections make the same point through different sources. Merge them.
- **Split the page** — it has become two arguments. Separate them and link across with `[[...]]`.

**Constraint: the page must not come out longer than it went in.** Otherwise consolidation becomes another append.

Propose the rewritten page in full and get confirmation before writing — this step deletes prose the user wrote. Update `last-updated`, and add a line to `wiki/log.md`. If the script flags nothing, say so in one line and skip the step; a week with nothing to consolidate is fine.

The script reads git history, so it needs the workspace to be a git repository with some commits. If it is not, pick the concept page with the oldest `last-updated` that has grown since, and say that is the fallback.
