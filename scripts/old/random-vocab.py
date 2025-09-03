#!/usr/bin/env python3
"""
Random Vocabulary Partitioner for CIS 110

This script extracts vocabulary terms from the vocabulary.md file and 
randomly partitions them into groups of n terms each.

Usage: python random-vocab.py <group_size>
Example: python random-vocab.py 10
"""

import sys
import re
import random
import os
from pathlib import Path


def extract_vocabulary_terms(file_path):
    """
    Extract vocabulary terms from the markdown file with their categories.
    
    Returns:
        list: List of tuples containing (term, definition, category)
    """
    terms = []
    current_category = "Unknown"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        # Pattern to match vocabulary terms: - **Term** - Definition
        term_pattern = r'^- \*\*(.*?)\*\* - (.*)$'
        # Pattern to match category headers: ### **Category Name**
        category_pattern = r'^### \*\*(.*?)\*\*'
        
        for line in lines:
            line = line.strip()
            
            # Check if this line is a category header
            category_match = re.match(category_pattern, line)
            if category_match:
                current_category = category_match.group(1).strip()
                continue
            
            # Check if this line is a vocabulary term
            term_match = re.match(term_pattern, line)
            if term_match:
                term = term_match.group(1).strip()
                definition = term_match.group(2).strip()
                terms.append((term, definition, current_category))
                
    except FileNotFoundError:
        print(f"Error: Could not find vocabulary file at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading vocabulary file: {e}")
        sys.exit(1)
        
    return terms


def partition_vocabulary(terms, group_size):
    """
    Randomly partition vocabulary terms into groups of specified size.
    
    Args:
        terms (list): List of (term, definition, category) tuples
        group_size (int): Number of terms per group
        
    Returns:
        list: List of groups, where each group is a list of (term, definition, category) tuples
    """
    # Shuffle the terms randomly
    shuffled_terms = terms.copy()
    random.shuffle(shuffled_terms)
    
    # Partition into groups
    groups = []
    for i in range(0, len(shuffled_terms), group_size):
        group = shuffled_terms[i:i + group_size]
        groups.append(group)
    
    return groups


def format_group_output(groups):
    """
    Format the partitioned groups for output.
    
    Args:
        groups (list): List of groups, each containing (term, definition, category) tuples
    """
    total_terms = sum(len(group) for group in groups)
    print(f"\n=== Vocabulary Partitioned into {len(groups)} Groups ===")
    print(f"Total terms: {total_terms}")
    print()
    
    for group_num, group in enumerate(groups, 1):
        print(f"--- GROUP {group_num} ({len(group)} terms) ---")
        for i, (term, definition, category) in enumerate(group, 1):
            print(f"{i:2d}. **{term}** ({category}) - {definition}")
        print()  # Extra space between groups


def main():
    """Main function to handle command line arguments and execute the script."""
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python random-vocab.py <group_size>")
        print("Example: python random-vocab.py 10")
        sys.exit(1)
    
    try:
        group_size = int(sys.argv[1])
        if group_size <= 0:
            print("Error: Group size must be a positive integer.")
            sys.exit(1)
    except ValueError:
        print("Error: Please provide a valid integer for the group size.")
        sys.exit(1)
    
    # Find the vocabulary file (assume it's in the parent directory)
    script_dir = Path(__file__).parent
    vocab_file = script_dir.parent / 'vocabulary.md'
    
    if not vocab_file.exists():
        print(f"Error: Could not find vocabulary.md at {vocab_file}")
        print("Make sure the vocabulary.md file exists in the project root.")
        sys.exit(1)
    
    # Extract vocabulary terms
    print(f"Loading vocabulary from {vocab_file.name}...")
    terms = extract_vocabulary_terms(vocab_file)
    
    if not terms:
        print("Error: No vocabulary terms found in the file.")
        sys.exit(1)
    
    print(f"Found {len(terms)} vocabulary terms.")
    
    # Partition vocabulary into groups
    groups = partition_vocabulary(terms, group_size)
    
    # Display results
    format_group_output(groups)


if __name__ == "__main__":
    main()
