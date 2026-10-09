---
name: inbox-capture
description: >
  Use this skill when the user wants to process files waiting in the _inbox/
  folder. Trigger on: "process inbox", "check inbox", "what's in my inbox",
  "clear my inbox", or any request to sweep unprocessed notes into the control
  system. Extracts decisions, actions and conceptual developments from each
  file, proposes updates to the control files and daily note, then moves
  processed files to _inbox/_captured/ on approval.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

Scan `_inbox/` (not `_inbox/_captured/`) for `.md` files that are ready. A file is ready if its frontmatter has `status: inbox`, or has no `status` field at all. Skip any other status.

If nothing is ready, say the inbox is clear. If several are, list them all first so the user knows what is queued, then process them **one at a time**, finishing each before starting the next.

## For each file

1. **Extract**
   - **Decisions** — explicit choices that close a question
   - **Actions** — things to do, follow up, send or chase, tagged with the project folder name where identifiable
   - **Conceptual developments** — shifts in thinking, new framings, ideas worth keeping

2. **Propose** where each piece goes, before writing anything:
   - Actions and decisions with follow-ups → `_control/open-loops.md` (as a diff)
   - Project state changes → `_control/projects.md`
   - Conceptual developments → today's daily note under 💡 Conceptual Developments

   Some notes are just fragments to keep. It is fine to propose "nothing to file; archive as is".

3. **Write only what is approved**, piece by piece.

4. **Close the file:** set `status: captured`, add `captured: YYYY-MM-DD`, move it to `_inbox/_captured/`, and add one line to today's daily note under 🗂 Session Extracts: `Inbox captured: <filename> — <what was extracted>`.
