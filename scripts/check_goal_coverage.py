#!/usr/bin/env python
"""Check coverage of learning goals across the modular section files referenced by main.md.

Process:
    1. Parse `learning-goals.md` for bullet goals grouped under section headings (## lines).
    2. Parse `main.md` and collect every markdown link target or plain path containing `content/` and ending in `.md`.
         (Supports formats like `content/01-file.md`, `[text](content/01-file.md)`, or indented paths.)
    3. Concatenate the contents of those files (in the order they appear) into a single corpus.
         If none are found, fall back to scanning `main.md` itself.
    4. Perform case-insensitive, whitespace-normalized substring matching for each goal.
    5. Output a table (default) or JSON with `--json`.

Usage:
    python scripts/check_goal_coverage.py            # human-readable table
    python scripts/check_goal_coverage.py --json     # machine-readable JSON

Exit code: 0 always (non-invasive); coverage info printed to stdout.
"""

from __future__ import annotations

import argparse
import json
import re
from itertools import groupby
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


LINK_PATTERN = re.compile(r"content/[A-Za-z0-9_.\-]+\.md")


def extract_content_files(main_text: str) -> List[Path]:
    """Return list of Paths for content markdown files referenced in main.md.

    Accepts both markdown link syntax and bare paths. Keeps first-seen order and de-duplicates.
    """
    seen = []
    for match in LINK_PATTERN.finditer(main_text):
        rel = match.group(0)
        p = (BASE / rel).resolve()
        if p.exists() and p.suffix.lower() == '.md' and p not in seen:
            seen.append(p)
    return seen


def load_aggregated_content() -> tuple[str, list[Path]]:
    text = MAIN_FILE.read_text(encoding="utf-8")
    files = extract_content_files(text)
    if not files:  # fallback legacy behavior
        return text, []
    parts = []
    for fp in files:
        try:
            parts.append(fp.read_text(encoding="utf-8"))
        except Exception as e:
            parts.append(f"\n<!-- Error reading {fp.name}: {e} -->\n")
    return "\n\n".join(parts), files


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
    aggregated_text, files = load_aggregated_content()
    mark_presence(goals, aggregated_text)

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
        covered = sum(g.present for g in goals)
        if files:
            print(f"\nScanned {len(files)} content file(s) referenced in main.md.")
        else:
            print("\nNo content/ files referenced; scanned main.md body.")
        print(f"Covered {covered}/{len(goals)} goals.")


if __name__ == "__main__":  # pragma: no cover
    main()
