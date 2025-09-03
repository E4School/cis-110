#!/usr/bin/env python3
"""
Wiki Stub Generator for CIS 110

This script generates wiki page stubs for any missing vocabulary terms.
It uses the existing check-missing-wiki.py logic to find missing terms
and creates basic wiki files with the term definition from vocabulary.md.

Usage: python generate-wiki-stubs.py
"""

import re
import os
from pathlib import Path
from datetime import datetime


def extract_vocabulary_terms_with_definitions(file_path):
    """
    Extract vocabulary terms and their definitions from the markdown file.
    
    Returns:
        dict: Dictionary mapping term names to their definitions
    """
    terms = {}
    
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
                definition = term_match.group(2).strip()
                terms[term] = definition
                
    except FileNotFoundError:
        print(f"Error: Could not find vocabulary file at {file_path}")
        return {}
    except Exception as e:
        print(f"Error reading vocabulary file: {e}")
        return {}
        
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


def generate_wiki_stub(term, definition, wiki_dir):
    """
    Generate a wiki stub file for a term.
    
    Args:
        term (str): The vocabulary term
        definition (str): The term definition
        wiki_dir (Path): Path to the wiki directory
        
    Returns:
        bool: True if file was created successfully, False otherwise
    """
    filename = term_to_filename(term)
    filepath = wiki_dir / filename
    
    # Generate the wiki content
    content = f"""# {term}

{definition}

"""
    
    try:
        # Ensure the wiki directory exists
        wiki_dir.mkdir(parents=True, exist_ok=True)
        
        # Write the wiki file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Created wiki stub: {filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating {filename}: {e}")
        return False


def main():
    """Main function to generate wiki stubs for missing files."""
    
    # Find the vocabulary file and wiki directory
    script_dir = Path(__file__).parent
    vocab_file = script_dir.parent / 'vocabulary.md'
    wiki_dir = script_dir.parent / 'wiki'
    
    if not vocab_file.exists():
        print(f"Error: Could not find vocabulary.md at {vocab_file}")
        return
    
    # Extract vocabulary terms with definitions
    print(f"Loading vocabulary from {vocab_file.name}...")
    terms_with_definitions = extract_vocabulary_terms_with_definitions(vocab_file)
    
    if not terms_with_definitions:
        print("Error: No vocabulary terms found in the file.")
        return
    
    print(f"Found {len(terms_with_definitions)} vocabulary terms.")
    
    # Get existing wiki files
    existing_files = get_existing_wiki_files(wiki_dir)
    print(f"Found {len(existing_files)} existing wiki files.")
    
    # Find missing files
    missing_terms = []
    for term, definition in terms_with_definitions.items():
        expected_filename = term_to_filename(term)
        if expected_filename not in existing_files:
            missing_terms.append((term, definition, expected_filename))
    
    # Generate stubs for missing files
    if missing_terms:
        print(f"\n=== Generating Wiki Stubs ({len(missing_terms)} terms) ===")
        
        created_count = 0
        for term, definition, filename in missing_terms:
            if generate_wiki_stub(term, definition, wiki_dir):
                created_count += 1
        
        print(f"\n=== Summary ===")
        print(f"Terms processed: {len(missing_terms)}")
        print(f"Stubs created: {created_count}")
        print(f"Errors: {len(missing_terms) - created_count}")
        
    else:
        print("\n🎉 All vocabulary terms already have corresponding wiki files!")
    
    print(f"\nFinal Summary:")
    print(f"  Total terms: {len(terms_with_definitions)}")
    print(f"  Existing wiki files: {len(existing_files)}")
    print(f"  Missing wiki files: {len(missing_terms)}")


if __name__ == "__main__":
    main()
