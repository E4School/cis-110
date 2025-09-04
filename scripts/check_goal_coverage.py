#!/usr/bin/env python
"""Check coverage of learning goals in main.md.

Reads learning goals from learning-goals.md, extracts every bullet goal line,
and reports whether each appears (case-insensitive substring match) in main.md.

Usage (from repo root or cis-110-ai-redo directory):
  python scripts/check_goal_coverage.py            # human-readable table
  python scripts/check_goal_coverage.py --json     # machine-readable JSON

Exit code: 0 always (non-invasive); coverage info printed to stdout.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

BASE = Path(__file__).resolve().parent.parent  # cis-110-ai-redo directory
LEARNING_GOALS_FILE = BASE / "learning-goals.md"
MAIN_FILE = BASE / "main.md"


@dataclass
class Goal:
    section: str
    text: str  # Raw goal text (without leading dash)
    present: bool = False


def normalize(s: str) -> str:
    # Lowercase, collapse whitespace, remove markdown bold markup and backticks
    s = s.lower()
    s = s.replace("**", "")
    s = s.replace("`", "")
    # Remove paired parentheses content? Keep content; just normalize spaces.
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_learning_goals(path: Path) -> List[Goal]:
    goals: List[Goal] = []
    current_section = "(Uncategorized)"
    bullet_pattern = re.compile(r"^\s*-\s+")
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("## "):
                current_section = line[3:].strip()
                continue
            if line.strip().startswith("- "):
                text = line.strip()[2:].strip()
                if text:  # ignore empty bullets
                    goals.append(Goal(section=current_section, text=text))
    return goals


def mark_presence(goals: List[Goal], main_text: str) -> None:
    norm_main = normalize(main_text)
    for g in goals:
        # Search normalized substring; ensure punctuation differences don't break matches
        candidate = normalize(g.text)
        g.present = candidate in norm_main


def format_table(goals: List[Goal]) -> str:
    # Determine column widths
    rows = [(g.section, g.text, "YES" if g.present else "NO") for g in goals]
    # Include header prototype with 3 elements to avoid IndexError
    header_tuple = ("Section", "Learning Goal", "Present")
    sec_w = max(len(r[0]) for r in rows + [header_tuple])
    goal_w = max(len(r[1]) for r in rows + [header_tuple])
    status_w = len(header_tuple[2])
    header = f"{'Section'.ljust(sec_w)} | {'Learning Goal'.ljust(goal_w)} | Present"
    sep = f"{'-'*sec_w}-+-{'-'*goal_w}-+-{'-'*status_w}"
    lines = [header, sep]
    for sec, goal, present in rows:
        lines.append(f"{sec.ljust(sec_w)} | {goal.ljust(goal_w)} | {present}")
    # Summary
    total = len(goals)
    covered = sum(g.present for g in goals)
    lines.append("")
    lines.append(f"Coverage: {covered}/{total} ({covered/total:.1%})")
    missing = [g for g in goals if not g.present]
    if missing:
        lines.append("Missing goals (by section):")
        by_section: dict[str, List[str]] = {}
        for m in missing:
            by_section.setdefault(m.section, []).append(m.text)
        for sec in sorted(by_section):
            lines.append(f"  {sec}:")
            for t in by_section[sec]:
                lines.append(f"    - {t}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check coverage of learning goals in main.md")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of table")
    args = parser.parse_args()

    if not LEARNING_GOALS_FILE.exists():
        raise SystemExit(f"Missing learning goals file: {LEARNING_GOALS_FILE}")
    if not MAIN_FILE.exists():
        raise SystemExit(f"Missing main file: {MAIN_FILE}")

    goals = load_learning_goals(LEARNING_GOALS_FILE)
    main_text = MAIN_FILE.read_text(encoding="utf-8")
    mark_presence(goals, main_text)

    if args.json:
        data = {
            "summary": {
                "total": len(goals),
                "covered": sum(g.present for g in goals),
            },
            "goals": [
                {
                    "section": g.section,
                    "goal": g.text,
                    "present": g.present,
                }
                for g in goals
            ],
        }
        print(json.dumps(data, indent=2))
    else:
        print(format_table(goals))


if __name__ == "__main__":  # pragma: no cover
    main()
