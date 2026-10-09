---
name: update-thread
description: >
  Update the thread.md for the current project at the end of a working session.
  Use when the user says "update thread", "close session", "wrap up this project",
  or wants to capture where they're leaving a project before switching context.
  Produces a three-block handoff note: current state, live question, re-entry point.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

You're closing a working session on one project. Leave a precise handoff for the next session — not a summary of what happened, but where things are, what is live, and exactly where to start next time.

## Step 1 — Identify the project

If it is clear from the session, proceed. Otherwise ask: "Which project are we closing?"

## Step 2 — Gather (in parallel)

- `projects/[name]/README.md`
- `projects/[name]/thread.md` (if it exists)
- Today's daily note
- This project's items in `_control/open-loops.md`

## Step 3 — Draft the thread

Three blocks, following `templates/thread.md`. Be specific; vague entries are useless on re-entry. Write in the first person, as a note to yourself.

- **Current State** — two or three sentences on what is true now. Name the file, result or decision that marks where you are.
- **Live Question** — one or two sentences: the question or hypothesis being worked through.
- **Re-entry Point** — one sentence: the first action next time, specific enough to start without reading anything else.

## Step 4 — Confirm and write

Show the draft and ask: "Does this capture where you're leaving it?" Adjust, then write `projects/[name]/thread.md`, **replacing it entirely** — the thread is current state, not a log. Update the `_Last updated:_` date.

## Step 5 — README (if warranted)

If the session produced something significant — a decision, a finished piece, a milestone — propose a dated changelog line for `projects/[name]/README.md`, and a revised Current Status if it changed. Show before writing. Skip this step after exploratory sessions with no clear output.
