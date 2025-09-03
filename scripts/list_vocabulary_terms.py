#!/usr/bin/env python3
"""Extract all vocabulary terms from vocabulary.md and print them on one line, each in single quotes.

Adds the immediate category (the nearest preceding level-3 heading '###') inside the quotes, e.g.:
    'Field [Databases and Structured Data]'

Detection pattern for terms: markdown bullet lines like:
    - **Term** - Definition text

Category detection: lines that start with '### ' (optionally with bold ** markers). The raw heading text is cleaned:
    - Remove surrounding **
    - Collapse whitespace
    - Replace '&' with 'and'

Usage:
    python scripts/list_vocabulary_terms.py
Optional:
    --separator " , "   # custom separator placed between quoted items (default: space)
    --no-dedupe          # include duplicates in order (default removes duplicates preserving first occurrence)
    --no-category        # omit category suffix (reverts to original behavior)
"""
from __future__ import annotations
import re
import argparse
from pathlib import Path

def clean_category(raw: str) -> str:
    raw = raw.strip().strip('#').strip()
    # Remove wrapping ** if present
    if raw.startswith('**') and raw.endswith('**'):
        raw = raw[2:-2]
    # Collapse whitespace
    raw = re.sub(r"\s+", " ", raw)
    # Replace & with 'and'
    raw = raw.replace('&', 'and')
    return raw.strip()


def extract_terms_with_categories(markdown_text: str, dedupe: bool = True) -> list[tuple[str, str]]:
    term_pattern = re.compile(r"^\s*- \*\*(.+?)\*\*\s*- ")
    category_pattern = re.compile(r"^###\s+(.*)$")
    items: list[tuple[str, str]] = []
    seen = set()
    current_category = ""
    for line in markdown_text.splitlines():
        cat_match = category_pattern.match(line)
        if cat_match:
            current_category = clean_category(cat_match.group(1))
            continue
        term_match = term_pattern.match(line)
        if term_match:
            term = term_match.group(1).strip()
            if dedupe and term in seen:
                continue
            seen.add(term)
            items.append((term, current_category))
    return items

def main():
    parser = argparse.ArgumentParser(description="List vocabulary terms (with categories) from vocabulary.md")
    parser.add_argument("--separator", "-s", default=" ", help="Separator between quoted terms (default: space)")
    parser.add_argument("--no-dedupe", action="store_true", help="Do not remove duplicate terms")
    parser.add_argument("--no-category", action="store_true", help="Do not append category labels")
    args = parser.parse_args()

    # Assume script resides in scripts/ and vocabulary.md is one directory up
    vocab_path = Path(__file__).resolve().parent.parent / "vocabulary.md"
    if not vocab_path.exists():
        raise SystemExit(f"vocabulary.md not found at expected path: {vocab_path}")

    text = vocab_path.read_text(encoding="utf-8")
    items = extract_terms_with_categories(text, dedupe=not args.no_dedupe)

    if args.no_category:
        line = args.separator.join(f"'{term}'" for term, _cat in items)
    else:
        line = args.separator.join(
            f"'{term} [{cat}]'" if cat else f"'{term}'" for term, cat in items
        )
    print(line)

if __name__ == "__main__":
    main()
