#!/usr/bin/env python3
"""Structural check on _control/open-loops.md.

Prose rules do not enforce themselves. This script turns the close-day
subtraction rule into checks that either pass or do not:

  FAIL  completed [x] items still sitting in active sections (the sweep did not happen)
  FAIL  "Recently cleared" batches older than 7 days (git is the archive)
  WARN  parked items past the 30-day expiry, or under an undated sub-heading
  WARN  a project queue (under the 🏗 section) with more than 10 items

It also reports the day's flow — items added, removed and net change since the
last git commit — because a file that grows a little every day is the failure
mode, not any single level.

Exit code 0 = clean, 1 = violations found. Run from close-day or lint.
"""

import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOOPS = ROOT / "_control" / "open-loops.md"
REL = "_control/open-loops.md"

CLEARED_HEADING = "## ✅ Recently cleared"
PARKED_HEADING = "## 🗄 Parked / someday"

PROJECT_SECTION_MAX = 10  # a project sub-section above this is a dev backlog re-forming
CLEARED_RETENTION_DAYS = 7  # git is the archive; a second copy in context is not free
PARKED_EXPIRY_DAYS = 30  # parked longer than this is removed by default

DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def today():
    return date.today()


def parse_date(text):
    m = DATE_RE.search(text)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").date()
    except ValueError:
        return None


def item_key(raw):
    """Normalised identity for an item, for add/remove diffing across versions."""
    s = re.sub(r"^\s*- \[[ x]\]\s*", "", raw)
    s = re.sub(r"[*_`\[\]]", "", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s[:60]


def split_regions(text):
    """Return (active, parked, cleared) source blocks."""
    cleared = ""
    parked = ""
    head = text
    if CLEARED_HEADING in head:
        head, cleared = head.split(CLEARED_HEADING, 1)
    if PARKED_HEADING in head:
        head, parked = head.split(PARKED_HEADING, 1)
    return head, parked, cleared


def parse_items(block):
    """Top-level checkbox items only — nested detail lines are not items."""
    out = []
    for raw in block.split("\n"):
        if re.match(r"^- \[[ x]\]", raw):
            out.append(raw)
    return out


def count_open(text):
    """Open items across active + parked, keyed for diffing."""
    active, parked, _ = split_regions(text)
    keys = set()
    for block in (active, parked):
        for raw in parse_items(block):
            if "[x]" not in raw:
                keys.add(item_key(raw))
    return keys


def parse_active_sections(active):
    section = sub = None
    sections = {}
    done = []
    for raw in active.split("\n"):
        if raw.startswith("## "):
            section, sub = raw[3:].strip(), None
        elif raw.startswith("### "):
            sub = raw[4:].strip()
        elif re.match(r"\s*- \[", raw):
            key = f"{section} / {sub}" if sub else str(section)
            sections[key] = sections.get(key, 0) + 1
            if "[x]" in raw:
                done.append((key, re.sub(r"^\s*- \[x\]\s*", "", raw)[:80]))
    return done, sections


def git_head_version():
    try:
        out = subprocess.run(
            ["git", "show", f"HEAD:{REL}"],
            cwd=ROOT, capture_output=True, text=True, timeout=10,
        )
        return out.stdout if out.returncode == 0 else None
    except Exception:
        return None


def main():
    if not LOOPS.exists():
        print(f"FAIL  {LOOPS} not found")
        return 1

    text = LOOPS.read_text()
    for heading in (CLEARED_HEADING, PARKED_HEADING):
        if heading not in text:
            print(f"FAIL  '{heading}' heading missing — cannot tell active from archived")
            return 1

    active, parked, cleared = split_regions(text)
    active_done, sections = parse_active_sections(active)

    active_open = sum(sections.values()) - len(active_done)
    parked_open = sum(1 for raw in parse_items(parked) if "[x]" not in raw)

    errors = []
    warnings = []

    # --- Hard failure 1: the sweep did not happen -------------------------
    if active_done:
        errors.append(
            f"{len(active_done)} completed item(s) still sitting in active sections "
            f"— close-day did not subtract:"
        )
        for key, snippet in active_done:
            errors.append(f"    [{key}] {snippet}")

    # --- Hard failure 2: cleared items never left the file ----------------
    stale_batches = []
    for raw in parse_items(cleared):
        d = parse_date(raw)
        if d and (today() - d).days > CLEARED_RETENTION_DAYS:
            stale_batches.append((d, (today() - d).days))
    if stale_batches:
        errors.append(
            f"{len(stale_batches)} cleared batch(es) older than {CLEARED_RETENTION_DAYS} days "
            f"still in the file — delete them; git is the archive:"
        )
        for d, age in sorted(stale_batches):
            errors.append(f"    batch {d} ({age} days old)  →  git log -S '<text>' -- {REL}")

    # --- Warning: the parking lot has expired stock -----------------------
    expired = []
    undated = []
    sub = None
    sub_date = None
    for raw in parked.split("\n"):
        if raw.startswith("### "):
            sub = raw[4:].strip()
            sub_date = parse_date(sub)
        elif re.match(r"^- \[ \]", raw):
            if sub_date is None:
                undated.append(sub or "(no sub-heading)")
            elif (today() - sub_date).days > PARKED_EXPIRY_DAYS:
                expired.append((sub, (today() - sub_date).days))

    if expired:
        by_sub = {}
        for name, age in expired:
            by_sub.setdefault((name, age), 0)
            by_sub[(name, age)] += 1
        warnings.append(
            f"{len(expired)} parked item(s) past the {PARKED_EXPIRY_DAYS}-day expiry "
            f"— propose as ONE batch, default remove, user names keepers:"
        )
        for (name, age), n in sorted(by_sub.items(), key=lambda i: -i[0][1]):
            warnings.append(f"    {name}: {n} item(s), parked {age} days ago")

    if undated:
        seen = sorted(set(undated))
        warnings.append(
            f"{len(undated)} parked item(s) under sub-heading(s) with no date "
            f"— cannot expire automatically; date the heading or clear it:"
        )
        for name in seen:
            warnings.append(f"    {name}")

    # --- Warning: a development backlog is re-forming ---------------------
    fat = {k: n for k, n in sections.items() if k.startswith("🏗") and n > PROJECT_SECTION_MAX}
    if fat:
        warnings.append(
            f"project sub-section(s) over {PROJECT_SECTION_MAX} items "
            f"— check whether a development backlog is re-forming:"
        )
        for key, n in sorted(fat.items(), key=lambda i: -i[1]):
            name = key.split("/")[-1].strip()
            warnings.append(f"    {key}: {n} items → if any are undated and unblocked, move them to projects/{name}/backlog.md")

    # --- Flow, not level --------------------------------------------------
    print(f"open items: {active_open} actionable + {parked_open} parked = {active_open + parked_open}")

    head = git_head_version()
    if head is None:
        print("flow: (no committed version to compare against)")
    else:
        before, now = count_open(head), count_open(text)
        added, removed = now - before, before - now
        net = len(now) - len(before)
        arrow = "+" if net > 0 else ""
        print(f"flow: {len(added)} added, {len(removed)} removed, net {arrow}{net} since last commit")
        if net > 0:
            print(f"      the file grew today — subtraction did not keep up with intake")

    if warnings:
        print("\nWARN")
        for line in warnings:
            print("  " + line)

    if errors:
        print("\nFAIL")
        for line in errors:
            print("  " + line)
        return 1

    print("\nPASS  nothing completed left in active sections; no cleared batch past retention")
    return 0


if __name__ == "__main__":
    sys.exit(main())
