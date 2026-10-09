---
name: read-thread
description: >
  Read the thread.md for a project to re-enter a working session quickly.
  Use when the user says "read thread", "catch me up on [project]",
  "where were we on [project]", or is starting a project session and
  wants to re-establish context before diving in.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

You're re-entering a working session on one project. Surface the handoff left by the last session — no more, no less — plus the open tasks, so work can start without reading anything else.

## Step 1 — Identify the project

If the project is given as an argument or clear from context, proceed. Otherwise ask: "Which project are we picking up?" Use the folder name under `projects/`.

## Step 2 — Gather (in parallel)

- `projects/[name]/thread.md` — the handoff from the last session
- `projects/[name]/README.md` — current status
- `projects/[name]/artefacts.md` — where the project's code, data and outputs live
- `_control/open-loops.md` — open items for this project

If `thread.md` does not exist, say so and suggest running `update-thread` at the end of this session to start one. If `artefacts.md` does not exist, skip it silently.

## Step 3 — Present

Render the thread's three blocks (Current State, Live Question, Re-entry Point), verbatim or lightly condensed. Then add:

**Artefacts** — from `artefacts.md`, only the entries the re-entry point needs (the repo, the dataset, the current output), one line each.

**Open loops** — the three to five most actionable open items for this project, in priority order. If none, say so.

Keep it short enough to read before starting. No interpretation or recommendations — just the thread and the loops.

This skill is read-only.
