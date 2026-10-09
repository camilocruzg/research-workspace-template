---
name: lint
description: >
  Run a health check on the workspace. Use when the user asks to "lint",
  "health check", "tidy up", "audit the workspace", or "check what's
  drifting". Also useful on Monday mornings alongside the morning brief.
  Checks open-loops.md for stale items, projects.md for inactive projects,
  projects/ for unregistered folders, _inbox/ for unprocessed files, and
  recent daily notes for missing handoffs, plus artefact registers and wiki
  links. Reports first; fixes only on approval.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

Surface what is drifting, stale or overdue — then let the user decide what to fix.

## Step 1 — Read (in parallel)

1. `_control/open-loops.md`, and run `python3 tools/check-open-loops.py`
2. `_control/projects.md`
3. The folders under `projects/`
4. `wiki/index.md` and the files in `wiki/concepts/`
5. Files in `_inbox/` (excluding `_captured/`)
6. Daily notes from the last 14 days

## Step 2 — Check

**open-loops.md**
- Anything the script reports as FAIL or WARN.
- **Expired relative dates** — "by Friday", "next week", "tomorrow" that are now in the past.
- **Long-idle items** — no date and no mention in recent daily notes for more than three weeks.
- **Overdue** — items under `⏰ Deadlined / person-waiting` whose date has passed.

**projects.md**
- **Stale projects** — Active, with no Recent entry in the last 14 days. Give the days since the last update.
- **Nothing next** — Active projects with no Next step (probably stalled).

**Unregistered projects** — any folder under `projects/` with no `README.md`, or with no entry in `projects.md`. Report what it seems to contain and ask whether to register or archive it. Do not register anything unilaterally.

**Artefacts** — projects with no `artefacts.md`; and any file in the workspace over ~10 MB, or any dataset, media or code repository inside it, which belongs in the artefacts root and the register (see `_control/schema.md`). Find large files with `find . -size +10M -not -path './.git/*'`.

**Wiki** — concept pages missing from `wiki/index.md`, and `[[links]]` that point to pages that do not exist.

**_inbox/** — count of unprocessed files; suggest `inbox-capture` if any.

**Daily notes** — working days in the last two weeks whose End of Day block is empty. A missing handoff weakens the next morning's brief.

## Step 3 — Report

- **🔴 Needs attention** — overdue items, idle items with real consequences
- **🟡 Drifting** — stale projects, uncleared items, expired relative dates, missing handoffs
- **🟢 All clear** — the checks with nothing to flag, listed briefly
- **Inbox** — count, or "clear"

Name the specific items, not just the categories.

## Step 4 — Offer fixes

Ask which to fix. Make changes only on explicit approval, piece by piece.
