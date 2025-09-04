#!/usr/bin/env python
"""Split `main.md` into individual section markdown files.

Rules:
  - Identify sections by lines starting with '## '. Ignore the first '# ' title.
  - Capture everything from a section header until (but not including) the next '## ' header or EOF.
  - Create output directory `content/` if missing.
  - File naming: two-digit incremental index (01..10) plus a normalized slug from the section title text.
      * Title text is everything after the leading '## ' trimmed.
      * Slug rules: lowercase, keep alphanumerics, replace spaces/separators with '-', collapse repeats, trim '-'.
      * Limit slug length to 40 chars.
  - Write each file with a first-level heading '# <Original Section Title>' so each file is standalone.
  - Do not overwrite existing files unless --force specified.
  - Print a summary table of index -> filename.

Usage:
  python scripts/split_main_sections.py            # dry run (no files written) -- shows planned mapping
  python scripts/split_main_sections.py --write    # actually write files
  python scripts/split_main_sections.py --force --write  # overwrite existing

Exit codes: 0 success, non-zero on structural errors (e.g., < 1 section found).
"""
from __future__ import annotations
import re
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List

BASE = Path(__file__).resolve().parent.parent
MAIN = BASE / 'main.md'
OUT_DIR = BASE / 'content'

SECTION_RE = re.compile(r'^##\s+(.*)')
TITLE_RE = re.compile(r'^#\s+')

@dataclass
class Section:
    index: int
    title: str
    lines: List[str]


def slugify(title: str, max_len: int = 40) -> str:
    t = title.lower()
    # Remove trailing parenthetical clarifiers for brevity? keep them but strip punctuation.
    t = re.sub(r'[^a-z0-9]+', '-', t)
    t = re.sub(r'-{2,}', '-', t).strip('-')
    return t[:max_len].rstrip('-') or 'section'


def parse_sections(text: str) -> List[Section]:
    lines = text.splitlines()
    sections: List[Section] = []
    current: Section | None = None
    for line in lines:
        if TITLE_RE.match(line):
            # Skip the top-level title line entirely
            continue
        m = SECTION_RE.match(line)
        if m:
            # Start new section
            if current:
                sections.append(current)
            current = Section(index=len(sections)+1, title=m.group(1).strip(), lines=[line])
        else:
            if current:
                current.lines.append(line)
    if current:
        sections.append(current)
    return sections


def write_sections(sections: List[Section], write: bool, force: bool) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    rows = []
    for sec in sections:
        slug = slugify(sec.title)
        filename = f"{sec.index:02d}-{slug}.md"
        path = OUT_DIR / filename
        content_lines = [f"# {sec.title}\n"]
        # Keep original lines but upgrade first '##' to '#'
        started = False
        for line in sec.lines[1:]:  # skip the original section header (we replaced it)
            content_lines.append(line + ("\n" if not line.endswith('\n') else ''))
        content = ''.join(content_lines).rstrip() + '\n'
        exists = path.exists()
        status = 'SKIP' if exists and not force and write else 'WRITE'
        if write and (not exists or force):
            path.write_text(content, encoding='utf-8')
        rows.append((sec.index, sec.title, filename, status))
    # Print summary table
    col_w = [0,0,0,0]
    for r in rows:
        col_w = [max(col_w[i], len(str(r[i]))) for i in range(4)]
    header = ('Idx','Title','File','Action')
    print(f"{header[0].ljust(col_w[0])} | {header[1].ljust(col_w[1])} | {header[2].ljust(col_w[2])} | {header[3].ljust(col_w[3])}")
    print('-'*col_w[0] + '-+-' + '-'*col_w[1] + '-+-' + '-'*col_w[2] + '-+-' + '-'*col_w[3])
    for r in rows:
        print(f"{str(r[0]).ljust(col_w[0])} | {r[1].ljust(col_w[1])} | {r[2].ljust(col_w[2])} | {r[3].ljust(col_w[3])}")
    print(f"\nSections found: {len(sections)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='Write files (otherwise dry run)')
    ap.add_argument('--force', action='store_true', help='Overwrite existing files when used with --write')
    args = ap.parse_args()

    if not MAIN.exists():
        raise SystemExit(f"Missing main file: {MAIN}")

    text = MAIN.read_text(encoding='utf-8')
    sections = parse_sections(text)
    if len(sections) != 10:
        print(f"Warning: expected 10 sections, found {len(sections)}")
    if len(sections) == 0:
        raise SystemExit('No sections parsed.')
    write_sections(sections, write=args.write, force=args.force)

if __name__ == '__main__':
    main()
