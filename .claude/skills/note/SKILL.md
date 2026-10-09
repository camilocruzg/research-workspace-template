---
name: note
description: >
  Fast, zero-friction note capture. Use when the user wants to jot a quick
  thought, idea, reminder, or fragment into their inbox without processing it
  now. Trigger on: "/note", "note:", "jot this down", "quick note", "make a
  note", or any short thought the user clearly wants saved for later rather
  than acted on now. Writes ONE timestamped file to _inbox/ and stops. Distinct
  from `capture` (processes input now) and `inbox-capture` (files the inbox later).
---

# Quick note → _inbox/

The goal is speed. Save the note and get out of the way. Do **not** extract decisions, propose control-file updates, or ask for approval — that is `inbox-capture`'s job, later. One file, one confirmation line.

1. **Content.** Take it from the skill arguments. If empty, ask once: "What's the note?" Preserve the user's wording exactly.
2. **Timestamp.** Run `date "+%Y-%m-%d %H%M %H:%M %A"` — do not guess the time.
3. **Title and slug.** Use the first line as the title if it is short (≤ 10 words), otherwise the first six to eight words. Slug: lowercase, hyphenated, punctuation stripped, at most ~50 characters.
4. **Project tag.** Add a project folder name to `tags` only if the note literally names it. Never guess; leave `tags: []` when in doubt.
5. **Write** `_inbox/<YYYY-MM-DD>-<HHMM>-<slug>.md`:

   ```markdown
   ---
   date: <YYYY-MM-DD>
   time: <HH:mm>
   weekday: <Weekday>
   type: note
   tags: []
   status: inbox
   ---

   # <Title>

   <the note content, verbatim>
   ```

   `status: inbox` is required — `inbox-capture` keys on it. If the filename exists, append `-2`, `-3`, …

6. **Confirm and stop:** one line naming the file, e.g. `Saved → _inbox/2026-07-16-1240-call-the-printer.md`.
