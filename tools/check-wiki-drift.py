#!/usr/bin/env python3
"""Measure synthesis drift across wiki/concepts/.

A concept page is supposed to hold an argument. Over months it tends to
accumulate evidence filed underneath a claim that is never re-examined: each
new source is appended as its own section, the page only ever grows, and the
opening claim stays where it was.

This script ranks concept pages by ONE thing: how much has been appended since
the last time the opening claim was actually revised. The "head" of a page is
its title and everything through the end of its first `## ` section (the
claim); everything after is support. Frontmatter is ignored, so bumping
`last-updated:` does not count as revising the claim.

It reads git history, so the workspace must be a git repository with commits.
wiki/projects/ is excluded: project pages are chronologies by design.

Used by the weekly-synthesis skill to pick ONE page per week to consolidate.
Exit code is always 0: it reports, it does not gate.
"""

import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONCEPTS = ROOT / "wiki" / "concepts"

# Two ways to earn a consolidation pass. A page is flagged if it meets EITHER.
#
#   1. A lot has been added recently under an unexamined claim.
#   2. A moderate amount has been added under a claim left alone for much longer.
#
# The second pair exists so that staleness can earn a pass on its own: with a
# single threshold, a page sitting just under it could only cross by
# accumulating MORE unexamined material.
#
# Still deliberately excluded: a stale claim with nothing added under it. That
# is a settled page, not a drifting one.
STALE_DAYS = 21   # claim age, paired with FAT_APPEND
FAT_APPEND = 60   # lines appended since the last head revision
OLD_DAYS = 45     # claim age, paired with MODEST_APPEND
MODEST_APPEND = 30


def flagged(r):
    """Does this page have earned a consolidation pass?"""
    return (r["appended"] >= FAT_APPEND and r["age"] >= STALE_DAYS) or (
        r["appended"] >= MODEST_APPEND and r["age"] >= OLD_DAYS
    )


def git(*args, text=True):
    try:
        out = subprocess.run(
            ["git", *args], cwd=ROOT, capture_output=True, text=text, timeout=20
        )
        return out.stdout if out.returncode == 0 else None
    except Exception:
        return None


def head_text(content):
    """Everything through the end of the first '## ' section: the claim.

    Frontmatter is stripped first. It sits above the title and would otherwise
    count as part of the claim — so bumping `last-updated:` while appending a
    literature section would reset the drift clock without the argument having
    been re-examined. That would let good hygiene defeat the detector, which is
    the wrong way round.
    """
    lines = content.split("\n")

    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                lines = lines[i + 1:]
                break

    seen_first = False
    out = []
    for line in lines:
        if line.startswith("## "):
            if seen_first:
                break
            seen_first = True
        out.append(line)
    return "\n".join(out)


def history(relpath):
    """[(date, total_lines, head_changed)] oldest first."""
    log = git("log", "--format=%H %ad", "--date=short", "--follow", "--reverse", "--", relpath)
    if not log:
        return []
    rows = []
    prev_head = None
    for line in log.strip().split("\n"):
        if not line.strip():
            continue
        sha, _, when = line.partition(" ")
        content = git("show", f"{sha}:{relpath}")
        if content is None:
            continue
        h = head_text(content)
        rows.append((when.strip(), len(content.split("\n")), h != prev_head))
        prev_head = h
    return rows


def main():
    if not CONCEPTS.is_dir():
        print(f"FAIL  {CONCEPTS} not found")
        return 0

    today = date.today()
    report = []

    for path in sorted(CONCEPTS.glob("*.md")):
        rel = str(path.relative_to(ROOT))
        rows = history(rel)
        if not rows:
            continue

        last_head_i = max(i for i, r in enumerate(rows) if r[2])
        last_head_date, lines_then, _ = rows[last_head_i]
        when, total, _ = rows[-1]

        try:
            age = (today - datetime.strptime(last_head_date, "%Y-%m-%d").date()).days
        except ValueError:
            age = 0

        appended = total - lines_then
        commits_since = len(rows) - 1 - last_head_i

        report.append({
            "name": path.name,
            "total": total,
            "head_date": last_head_date,
            "age": age,
            "appended": appended,
            "commits_since": commits_since,
        })

    # Rank by what the consolidation pass is for: most material added under an
    # unexamined claim. Age breaks ties — a stale claim with nothing added under
    # it is just a settled page, which is fine.
    report.sort(key=lambda r: (-r["appended"], -r["age"]))

    print(f"wiki/concepts — {len(report)} pages, synthesis drift\n")
    print(f"{'appended':>9} {'since':>11} {'age':>6} {'commits':>8} {'total':>6}  page")
    print(f"{'-'*9} {'-'*11} {'-'*6} {'-'*8} {'-'*6}  {'-'*40}")
    for r in report:
        flag = "  ←" if flagged(r) else ""
        print(
            f"{r['appended']:>+9} {r['head_date']:>11} {r['age']:>5}d "
            f"{r['commits_since']:>8} {r['total']:>6}  {r['name']}{flag}"
        )

    hits = [r for r in report if flagged(r)]
    print()
    if hits:
        top = hits[0]
        print(
            f"{len(hits)} page(s) flagged "
            f"(≥{FAT_APPEND} lines under a claim ≥{STALE_DAYS}d unexamined, "
            f"or ≥{MODEST_APPEND} lines under a claim ≥{OLD_DAYS}d unexamined)."
        )
        print(f"\nThis week's consolidation target: {top['name']}")
        print(
            f"  {top['appended']} lines added across {top['commits_since']} commit(s) "
            f"since the claim was last revised on {top['head_date']}."
        )
        print("  Re-read the opening claim against what has been filed under it.")
        print("  The page must not come out longer than it went in.")
    else:
        print("No page flagged — nothing to consolidate this week.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
