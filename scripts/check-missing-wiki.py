#!/usr/bin/env python3
"""
Wiki File Checker for CIS 110

This script extracts vocabulary terms from the vocabulary.md file and 
checks which ones don't have corresponding wiki files yet.

Usage: python check-missing-wiki.py
"""

import re
import os
from pathlib import Path


def extract_vocabulary_terms(file_path):
    """
    Extract vocabulary terms from the markdown file.
    
    Returns:
        list: List of vocabulary terms
    """
    terms = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        # Pattern to match vocabulary terms: - **Term** - Definition
        term_pattern = r'^- \*\*(.*?)\*\* - (.*)$'
        
        for line in lines:
            line = line.strip()
            
            # Check if this line is a vocabulary term
            term_match = re.match(term_pattern, line)
            if term_match:
                term = term_match.group(1).strip()
                terms.append(term)
                
    except FileNotFoundError:
        print(f"Error: Could not find vocabulary file at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading vocabulary file: {e}")
        return []
        
    return terms


def term_to_filename(term):
    """
    Convert a vocabulary term to the expected wiki filename.
    
    Args:
        term (str): The vocabulary term
        
    Returns:
        str: The expected filename
    """
    # Convert to lowercase and replace spaces/special chars with hyphens
    filename = term.lower()
    filename = re.sub(r'[^a-z0-9\s\-]', '', filename)  # Remove special chars except spaces and hyphens
    filename = re.sub(r'\s+', '-', filename)  # Replace spaces with hyphens
    filename = re.sub(r'-+', '-', filename)  # Replace multiple hyphens with single
    filename = filename.strip('-')  # Remove leading/trailing hyphens
    
    return f"{filename}.md"


def get_existing_wiki_files(wiki_dir):
    """
    Get list of existing wiki files.
    
    Args:
        wiki_dir (Path): Path to the wiki directory
        
    Returns:
        set: Set of existing wiki filenames
    """
    if not wiki_dir.exists():
        return set()
    
    return {f.name for f in wiki_dir.iterdir() if f.is_file() and f.suffix == '.md'}


def main():
    """Main function to check for missing wiki files."""
    
    # Find the vocabulary file and wiki directory
    script_dir = Path(__file__).parent
    vocab_file = script_dir.parent / 'vocabulary.md'
    wiki_dir = script_dir.parent / 'wiki'
    
    if not vocab_file.exists():
        print(f"Error: Could not find vocabulary.md at {vocab_file}")
        return
    
    # Extract vocabulary terms
    print(f"Loading vocabulary from {vocab_file.name}...")
    terms = extract_vocabulary_terms(vocab_file)
    
    if not terms:
        print("Error: No vocabulary terms found in the file.")
        return
    
    print(f"Found {len(terms)} vocabulary terms.")
    
    # Get existing wiki files
    existing_files = get_existing_wiki_files(wiki_dir)
    print(f"Found {len(existing_files)} existing wiki files.")
    
    # Check for missing files
    missing_terms = []
    for term in terms:
        expected_filename = term_to_filename(term)
        if expected_filename not in existing_files:
            missing_terms.append((term, expected_filename))
    
    # Display results
    if missing_terms:
        print(f"\n=== Missing Wiki Files ({len(missing_terms)} terms) ===")
        for i, (term, filename) in enumerate(missing_terms, 1):
            print(f"{i:3d}. {term} -> {filename}")
    else:
        print("\n🎉 All vocabulary terms have corresponding wiki files!")
    
    print(f"\nSummary:")
    print(f"  Total terms: {len(terms)}")
    print(f"  Existing wiki files: {len(existing_files)}")
    print(f"  Missing wiki files: {len(missing_terms)}")


if __name__ == "__main__":
    main()
