---
name: capture
description: >
  Use this skill when the user wants to capture and process raw input —
  meeting notes, rough notes, voice memo transcripts, email threads, or
  anything pasted for extraction and filing. Trigger on: "capture this",
  "process these notes", "I have meeting notes", "extract decisions",
  "here are my notes", or any time the user shares unstructured input and
  wants it turned into decisions, actions, and updates to the control files.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

The input is raw notes: meeting notes, a voice-memo transcript, an email thread. If it is already in the arguments or the preceding message, process it; otherwise ask for it once.

1. **Decisions** — extract explicit choices that close a question.
2. **Actions** — extract things to do, follow up, send or chase. Tag each with the project folder name if identifiable (e.g. `[example-project]`).
3. **Conceptual developments** — extract shifts in thinking, new framings, ideas worth keeping.
4. **Propose where each piece goes:**
   - Decisions → today's daily note under Decisions Made, and `_control/open-loops.md` if an action follows
   - Actions → `_control/open-loops.md` (show exactly where, as a diff)
   - Project state changes → `_control/projects.md` (show the proposed text)
   - Conceptual developments → today's daily note under 💡 Conceptual Developments
5. **Show all proposed changes before writing anything.** Write only what the user approves, piece by piece.
6. Add one line to today's daily note under 🗂 Session Extracts: what was captured and where it went.
