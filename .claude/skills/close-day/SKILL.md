---
name: close-day
description: >
  Use this skill when the user wants to close out their working day, do an
  end-of-day review, or capture what happened today. Trigger on: "close day",
  "close the day", "end of day", "wrap up today", "day review", or any signal
  that the user is finishing work for the day and wants to tidy up.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

It's the end of the working day. Close it cleanly, leave a handoff for tomorrow, and commit.

## Step 1 — Gather

Ask: "What happened today? Meetings, decisions, things that moved, things that stalled, anything that came in. Rough notes are fine."

Also read today's daily note, `_control/open-loops.md` and `_control/projects.md` before proposing anything.

## Step 2 — Propose (show each, wait for approval, then write)

**a) End of Day block** in today's daily note:
- **Moved:** what moved forward.
- **Stalled:** what didn't, and why if known.
- **Tomorrow:** the priorities for tomorrow, with enough context that tomorrow's `morning-brief` can use them as the default Top 3. This line is the handoff; make it specific.

**b) open-loops.md updates** — as a diff: items to mark done, new items, status changes.

**c) open-loops.md subtraction — every close-day, not occasionally.**

`open-loops.md` is loaded into every session, so its length is a cost paid every time. Subtraction means items **leave the file**; moving them to another section is not subtraction.

1. **Sweep, then delete.** Move every `[x]` item into `## ✅ Recently cleared` as one dated batch for today (e.g. `- [x] 2026-07-16 — [example-project] item text`), then delete every cleared batch older than seven days. If the workspace is a git repository, git keeps them: `git log -S "<text>" -- _control/open-loops.md` recovers any of it.
2. **Expire the parking lot.** Items under `## 🗄 Parked / someday` in a sub-heading dated more than 30 days ago are removed by default. Present them as one batch with one question — "these N expire tonight, name any keepers" — never item by item. Keepers move to a fresh dated sub-heading.
3. **Verify with the script.** Run `python3 tools/check-open-loops.py`. It must exit 0 before the day is closed. FAIL means the sweep is unfinished; fix and re-run. WARNs (expired or undated parked items, a project queue over ten items) are reported to the user, not silently fixed. Report the day's net change in one line; if the file grew, say so plainly.

**d) projects.md** — propose exact text for any project whose status, recent or next step changed.

**e) Project READMEs** — for each project with meaningful work today, propose a changelog line and, if the state changed, a revised Current Status.

**f) Knowledge and artefacts**
- **Ideas:** read today's 💡 Conceptual Developments. For any idea that has come back more than once, or that changes how a project is framed, propose a new `wiki/concepts/` page or a revision to an existing one (following `wiki/concepts/example-concept.md`), plus a line in `wiki/log.md` and `wiki/index.md`. Most days nothing qualifies; say so in one line.
- **Artefacts:** if today produced, moved or superseded code, data, media or exports, propose the entry for `projects/[name]/artefacts.md`. Anything large that landed in the workspace by mistake should move to the artefacts root (see `_control/schema.md`).

**g) Tomorrow's meetings** — ask what tomorrow holds (or, only if connectors are ON in `CLAUDE.md`, read tomorrow's calendar). Surface anything that needs preparation and fold it into the Tomorrow line.

## Step 3 — Commit (if the workspace is a git repository)

1. Stage the changed workspace files.
2. Propose a one-paragraph commit message summarising the day. Show it before committing.
3. Commit, and push if a remote is configured.

Write nothing and commit nothing until each step is approved.
