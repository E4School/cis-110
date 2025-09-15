#!/usr/bin/env python3
"""
Script to list all questions from concept-map.yml files.

This script scans all concept-map.yml files in the textbook content directories
and outputs all the questions they reference, showing the chapter, question file,
and the first 80 characters of each question.
"""

import yaml
import os
import glob
import argparse
import sys

def list_questions(textbook_path="public/textbook", verbose=False, full_question=False):
    """
    List all questions from concept-map.yml files.
    
    Args:
        textbook_path: Path to the textbook directory
        verbose: Show additional details
        full_question: Show full question text instead of truncated
    """
    pattern = os.path.join(textbook_path, "content/overviews/*/concept-map.yml")
    concept_files = glob.glob(pattern)
    
    if not concept_files:
        print(f"No concept-map.yml files found in {pattern}")
        return
    
    total_questions = 0
    
    for concept_file in sorted(concept_files):
        if verbose:
            print(f"\n--- Processing: {concept_file} ---")
        
        try:
            with open(concept_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading {concept_file}: {e}")
            continue
        
        if 'concept_map' not in data:
            if verbose:
                print(f"No concept_map found in {concept_file}")
            continue
        
        chapter = concept_file.split(os.sep)[-2]  # Get chapter directory name
        chapter_questions = 0
        
        for category in data['concept_map']:
            for concept in category.get('concepts', []):
                for q_file in concept.get('exam_questions', []):
                    q_path = os.path.join(os.path.dirname(concept_file), q_file)
                    
                    if not os.path.exists(q_path):
                        if verbose:
                            print(f"Question file not found: {q_path}")
                        continue
                    
                    try:
                        with open(q_path, 'r', encoding='utf-8') as qf:
                            q_data = yaml.safe_load(qf)
                        
                        question_text = q_data.get('question', 'No question field')
                        if full_question:
                            display_text = question_text
                        else:
                            display_text = question_text[:80] + '...' if len(question_text) > 80 else question_text
                        
                        print(f"{chapter}/{q_file}: {display_text}")
                        chapter_questions += 1
                        total_questions += 1
                        
                    except Exception as e:
                        print(f"Error reading question file {q_path}: {e}")
        
        if verbose and chapter_questions > 0:
            print(f"Chapter {chapter}: {chapter_questions} questions")
    
    print(f"\nTotal questions found: {total_questions}")

def main():
    parser = argparse.ArgumentParser(description="List all questions from concept-map.yml files")
    parser.add_argument(
        '--textbook-path', 
        default='public/textbook',
        help='Path to the textbook directory (default: public/textbook)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output with processing details'
    )
    parser.add_argument(
        '--full', '-f',
        action='store_true',
        help='Show full question text instead of truncated'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.textbook_path):
        print(f"Error: Textbook path '{args.textbook_path}' does not exist")
        sys.exit(1)
    
    list_questions(args.textbook_path, args.verbose, args.full)

if __name__ == "__main__":
    main()
