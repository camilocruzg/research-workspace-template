# Workspace template for Claude Code

A plain-folder workspace that gives Claude Code a memory of your work across days and projects. Markdown files hold the state (who you are, where each project stands, what is open), and a handful of skills run the routines that keep that state current: a morning brief, capturing notes, closing the day, and handing a project over from one session to the next.

Nothing here is an app. It is a folder of text files and instructions, so you can read, edit or delete any of it.

For the reasoning behind the design, see the accompanying write-up: [A workspace that remembers](https://gist.github.com/camilocruzg/40666a858efd22c0d4408f38d0547621).

## What you need

- [Claude Code](https://docs.claude.com/en/docs/claude-code/overview), in the terminal or the desktop app
- Python 3 (for two small scripts; preinstalled on macOS)
- git: the daily commit is your archive, and the wiki drift check reads its history
- Not needed: email and calendar connectors. They are switched off in `CLAUDE.md` by default; see Privacy before turning them on

## Quick start

0. Check that your organisation allows its work data to be used with Claude (see Privacy below).
1. Click **Use this template** on GitHub to make your own copy. **Make your copy private** — it will hold your notes, tasks and collaborators' names.
2. Clone it somewhere you work (a synced folder such as iCloud or Dropbox works if you want it on several machines).
3. Open Claude Code in that folder (`cd your-workspace && claude`). The workspace's `CLAUDE.md`, settings and skills load automatically.
4. Fill in `_control/context.md`. This matters most: it is what lets the agent push back usefully rather than generically. Fifteen minutes of honest specifics is enough to start. You can also ask Claude to interview you and draft it.
5. Replace `projects/example-project/` with a real project, and add it to `_control/projects.md` and `_control/open-loops.md`. Set your artefacts root in `_control/schema.md` (default `~/Artefacts/`).
6. Run `/morning-brief`.

## Layout

```
_control/
  context.md        who you are, goals, working style        (loaded every session)
  projects.md       where each project stands                (loaded every session)
  open-loops.md     everything pending                       (loaded every session)
  schema.md         the map: layers, filing rules, where artefacts live
daily/YYYY/         one note per working day
projects/[name]/
  README.md         status and changelog
  thread.md         handoff between working sessions
  artefacts.md      register of what the project produced and where it lives
  docs/             specs, drafts, meeting notes
  deliverables/     final submitted versions
wiki/
  concepts/         one page per idea or argument, spanning projects
  index.md, log.md
_inbox/             quick notes waiting to be processed
reviews/weekly/     weekly syntheses
templates/          daily note, project README, thread, artefacts register
tools/              check-open-loops.py, check-wiki-drift.py
.claude/
  settings.json     SessionStart hook that loads the three control files
  skills/           the routines below
CLAUDE.md           the working agreement between you and the agent
```

## The routines

| When | Skill | What it does |
|---|---|---|
| Start of day | `/morning-brief` | Reads yesterday's handoff, calendar, email and open loops; proposes today's focus and Top 3; creates the daily note |
| Any time | `/capture` | Paste meeting notes or a transcript; it extracts decisions and actions and proposes where each goes |
| Any time | `/note` | Drops a thought into `_inbox/` in seconds, unprocessed |
| When convenient | `/inbox-capture` | Works through `_inbox/`, one note at a time |
| Start of a project session | `/read-thread` | Restores where you left that project |
| End of a project session | `/update-thread` | Writes a three-part handoff: current state, live question, re-entry point |
| End of day | `/close-day` | Reflection and tomorrow's handoff, open-loop subtraction, state updates, ideas to the wiki, artefacts to the register, commit |
| End of week | `/weekly-synthesis` | What moved, what stalled, whether effort matched goals; consolidates one wiki page |
| Weekly or when it feels messy | `/lint` | Reports what is stale, drifting or unregistered |

You can also just talk to it. The skills are shortcuts for routines, not the only way in.

## Where things live

The workspace holds **documents**: the text you think with. Everything a project **produces** (code, datasets, media, exports) lives outside it, in an artefacts root (`~/Artefacts/[project]/` by default), and is listed in that project's `artefacts.md`. Governed data, such as anything covered by an ethics approval or confidentiality agreement, stays in the storage that agreement specifies; the workspace holds only a reference to it. Final submitted versions come back into `projects/[name]/deliverables/` as the record.

The point is that each kind of material sits where its visibility and storage cost suit it, while a single question ("where is X for project Y?") always has the same answer: that project's `artefacts.md`. The project folder name is the key that ties the locations together. `_control/schema.md` has the full rules.

## How ideas become knowledge

New ideas land first under 💡 in the day's note, without any judgement about whether they matter. Those that keep coming back, or that change how a project is framed, are promoted at close-day or in the weekly synthesis to a page in `wiki/concepts/`: a claim at the top, its support beneath. Once a week, `check-wiki-drift.py` names the page that has accumulated most material under a claim nobody has revisited, and the weekly synthesis revises it. The rule is that the page cannot come out longer than it went in, so the argument moves rather than only the evidence piling up.

## Two rules worth keeping

**The agent proposes, you approve.** `CLAUDE.md` tells it to show every change to your files before making it. This is slower than letting it write freely, and it is the reason the files stay trustworthy.

**Things leave `open-loops.md`.** The file is read at the start of every session, so it has to stay short. `close-day` sweeps finished items out and `tools/check-open-loops.py` checks that it did. Without this the file grows until it stops being useful.

## Growing it

Start with the daily loop for a couple of weeks before adding anything. Things that have proved worth adding later:

- **A literature folder** with an ingest routine that files reading into the wiki, alongside what work produces.
- **Brain-dump notes** read by the morning brief alongside the handoff.
- **Feeds** (a daily digest of field news) dropped into `_inbox/` by a script.
- **Your own skills.** If you find yourself asking for the same routine three times, ask Claude to write it as a skill in `.claude/skills/`.

## Privacy

**Check that the tool is allowed first.** Everything in this workspace is sent to the AI provider as you work: your notes, collaborators' names, project details. Many institutions allow work data to go only to AI tools they have approved, sometimes only at certain data classifications. Check your organisation's policy before putting work material here.

**Email and calendar are off by default.** A connector sends the content of your mail and meetings (other people's names and messages) to the provider. `CLAUDE.md` has a switch that keeps the routines from using connectors even when they are available. Turn it on only if your organisation's policy allows it. A safer pattern, if you need it, is to fetch and de-identify the data locally and give the agent only the result.

**Keep your copy private.** If you push it to GitHub, keep the repository private.

**Governed data never enters the workspace.** Participant data and anything under an ethics or confidentiality agreement belongs in the storage that agreement specifies; the workspace holds only a reference to it in `artefacts.md`.
