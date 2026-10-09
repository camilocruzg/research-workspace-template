---
name: morning-brief
description: >
  Use this skill when the user wants a morning overview of their day, asks
  what's pressing or urgent, wants to start their working day, or asks for
  a daily briefing. Trigger on: "morning brief", "what's on today",
  "what's pressing", "start my day", "daily briefing", "what should I
  focus on today", or any similar opening-of-day prompt. Works from the
  previous day's handoff and open loops; reads calendar and email only if
  connectors are switched ON in CLAUDE.md.
---

All paths are relative to the workspace root (the folder containing `CLAUDE.md`).

Produce a verified morning brief and create today's daily note.

## Step 0 — Date, note check, and yesterday's handoff

Get today's date and weekday (run `date "+%Y-%m-%d %A"` if not in context). Check whether `daily/YYYY/YYYY-MM-DD.md` already exists.

**Read the most recent previous daily note** — the latest file in `daily/`, which is not necessarily yesterday (weekends, gaps, leave). From it, take:

- **`# End of Day` → Tomorrow** — the priorities the user set for themselves at close of day, when they had the most context. **These are the default Top 3.**
- **`# End of Day` → Stalled** — what didn't move, and why.
- **`# Top 3`** — any item the Log and End of Day do not show as moved.

This handoff outranks everything gathered in Step 1. Calendar, email and open loops describe what is arriving; the handoff describes what the user already decided mattered. Do not re-derive priorities from scratch when a handoff exists. Displace a carried item only when something in Step 1 genuinely overrides it, and say so in one clause.

If there is no previous note, or its End of Day is blank, say so in one line — a missing handoff is worth knowing about — and derive priorities from Step 1.

## Step 1 — Gather (in parallel)

1. **Open loops:** read `_control/open-loops.md`. Note items in `⏰ Deadlined / person-waiting` that are due this week or overdue.
2. **Meetings:** ask the user once, briefly, what is in today's calendar — unless connectors are switched ON in `CLAUDE.md`.
3. **Calendar and email — only if `CLAUDE.md` says connectors are ON:**
   - Calendar: today's events. Drop declined events; note any awaiting a response.
   - Email: inbox threads from the last two days, excluding promotions, social and no-reply senders. Triage on sender and subject; open only the few that look actionable, and check whether the user has already replied. Mark each **needs reply** or **already replied**. Do not copy message content into the daily note.

If connectors are OFF, never call them, even if they are available in the session. The brief works from the handoff and open loops alone.

## Step 2 — Verify before presenting

Show only confirmed events, only threads with no reply found, and only loops that are still open.

## Step 3 — Present the brief

**Calendar** — today's meetings, in order.

**Email** (connectors ON only) — at most three items that genuinely need attention. If none, say so.

**Due** — open-loop items due or overdue.

**Carried forward** — what the last note handed to today: the Tomorrow line, plus anything stalled. Two or three items at most.

**One strategic move** — the single highest-leverage thing to do today, connected to the goals in `context.md` where possible.

Keep it readable in under a minute. Omit empty sections.

## Step 4 — Build the daily note

Build today's note from `templates/daily-note.md`:

- Frontmatter: `date` and `weekday`; meetings pre-filled from the calendar or from what the user said (time and title only).
- Propose a **Strategic Focus** (one or two sentences) and **Top 3**, starting from the carried-forward block — Step 1 only amends it.
- Leave the other sections blank.

**If the note already exists:** propose the Strategic Focus and Top 3 only, and add them on confirmation.

**If it does not exist:** show the full note and its path (`daily/YYYY/YYYY-MM-DD.md`, creating the year folder if needed) and ask "Save this?". Write only on confirmation.
