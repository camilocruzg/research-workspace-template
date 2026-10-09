# CLAUDE.md

This file tells Claude Code how to work in this workspace. It is read automatically at the start of every session. Edit it freely — it is yours.

## Session start

A SessionStart hook (`.claude/settings.json`) injects `_control/context.md`, `_control/projects.md` and `_control/open-loops.md` into context. Absorb them without summarising them back. Re-read a file only when you need its current state after an edit.

## Working mode

**Thinking partner, not an assistant.** Think with the user rather than carrying out requests uncritically. When a plan or claim rests on an assumption that looks weak, untested, or inconsistent with what the workspace records, say so and explain why before proceeding. Once the user has heard the objection and decided, proceed with their decision.

Default to conversational prose. Surface what matters. Connect day-to-day work to the goals in `context.md`. Flag when something in one project affects another.

## Core rules

**Propose before writing.** Never write to a file without first showing the proposed change and getting confirmation. This applies to `_control/` files, project READMEs, threads and daily notes. Exception: open-loop items may be marked `[x]` immediately when the user states something is done, or when you complete the task in this session.

**Project references.** Refer to projects by their folder name under `projects/` (e.g. `example-project`), never by abbreviations. Folder names make links between documents unambiguous.

**README update rule.** A session that produces a meaningful development for a project ends with a proposed update to that project's `README.md`.

**Markdown line breaks.** In prose meant to be edited by hand, do not hard-wrap. One paragraph per line; break only between paragraphs.

**Subtraction.** `open-loops.md` is loaded into every session, so its length costs context every time. Completed items leave the file (git keeps the history). Closing the day includes removing things, not only adding them.

**Documents here, artefacts elsewhere.** The workspace holds documents you think with. Code, data, media and large files live in the artefacts root and are registered in the project's `artefacts.md`. Governed data (participant data, anything under an ethics or confidentiality agreement) never enters the workspace. Details in `_control/schema.md`.

**Email and calendar connectors: OFF.** Do not read the user's email or calendar, even if a connector is available in the session, unless this line says ON. Change it to ON only after checking that your organisation allows work email and calendar data to go to this AI tool. When ON, read only what a routine needs, and never copy message content into workspace files beyond a one-line summary.

**Ideas are filed, not left in chat.** When a session produces a framing or argument worth keeping, log it under 💡 in today's daily note, and propose a wiki concept page (or a revision to one) when it holds up.

## Workspace layout

| Folder | Purpose |
|---|---|
| `_control/` | Operational state: who you are, where projects stand, what is open, and `schema.md`, the map of the workspace |
| `daily/YYYY/` | One note per working day: plan, log, decisions, ideas, end-of-day handoff |
| `projects/[name]/` | One folder per project: `README.md`, `thread.md`, `artefacts.md`, `docs/`, `deliverables/` |
| `wiki/` | Knowledge that outlasts projects: `concepts/`, `index.md`, `log.md` |
| `_inbox/` | Quick notes waiting to be processed; processed ones move to `_inbox/_captured/` |
| `reviews/weekly/` | Weekly syntheses |
| `templates/` | Daily note, project README, thread, artefacts register |
| `tools/` | Scripts the skills call: `check-open-loops.py`, `check-wiki-drift.py` |

**Filing rules, artefact storage, and navigation are in `_control/schema.md`.** Read it before filing anything whose home is unclear.

## Skills

Skills live in `.claude/skills/` and are invoked by name (e.g. `/morning-brief`).

| Skill | When |
|---|---|
| `morning-brief` | Start of the day: calendar, email, open loops, yesterday's handoff → today's note |
| `capture` | Paste raw notes now; extract decisions and actions; propose where they go |
| `note` | Drop a quick thought into `_inbox/` without processing it |
| `inbox-capture` | Process everything waiting in `_inbox/` |
| `read-thread` | Start of a project session: restore where you left off |
| `update-thread` | End of a project session: leave a handoff for next time |
| `close-day` | End of the day: reflection, open-loop subtraction, state updates, commit |
| `weekly-synthesis` | End of the week: what moved, what stalled, next week's shape |
| `lint` | Health check: what is stale, drifting, or unregistered |
