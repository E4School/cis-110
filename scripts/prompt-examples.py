#!/usr/bin/env python3
"""
Custom Prompt Examples for Wiki Enhancement

This file contains example prompts that can be used with the enhanced 
enhance-wiki-definitions.py script in custom prompt mode.

Usage: Copy any prompt and paste it when the script asks for a custom prompt.
"""

# Example prompts for different use cases
EXAMPLE_PROMPTS = {
    "exam_questions": """For the term {term}, create 3 multiple-choice exam questions based on: {current_definition}. Include the correct answer and brief explanations for each question.""",
    
    "real_world_examples": """For the term {term}, provide 3 specific real-world examples where this concept is used, based on: {current_definition}. Focus on concrete applications students might encounter.""",
    
    "common_misconceptions": """For the term {term}, identify and explain 2-3 common misconceptions students might have about: {current_definition}. Provide clear corrections for each misconception.""",
    
    "comparison_analysis": """For the term {term}, compare and contrast it with 2 related concepts, using this definition: {current_definition}. Explain the key differences and similarities.""",
    
    "troubleshooting_guide": """For the term {term}, create a troubleshooting guide that helps students understand when and why problems might occur with: {current_definition}. Include common issues and solutions.""",
    
    "beginner_explanation": """For the term {term}, rewrite this definition in the simplest possible terms for someone who has never used a computer: {current_definition}. Use analogies and avoid all technical jargon.""",
    
    "advanced_concepts": """For the term {term}, explain advanced concepts and implications that build upon: {current_definition}. Focus on topics a student might encounter in higher-level courses.""",
    
    "historical_context": """For the term {term}, provide historical context about how this concept developed over time, building on: {current_definition}. Include key milestones and influential figures.""",
    
    "critical_thinking": """For the term {term}, pose 3 critical thinking questions that encourage deeper analysis of: {current_definition}. Questions should promote discussion and reflection.""",
    
    "industry_perspective": """For the term {term}, explain how this concept is viewed and used in the current tech industry, based on: {current_definition}. Include trends, challenges, and opportunities.""",
    
    "study_tips": """For the term {term}, create study tips and memory aids to help students remember and understand: {current_definition}. Include mnemonics, visual aids, or practice exercises.""",
    
    "ethical_considerations": """For the term {term}, discuss potential ethical considerations and implications related to: {current_definition}. Focus on responsible use and potential concerns."""
}

def print_examples():
    """Print all example prompts with descriptions."""
    print("🎯 Custom Prompt Examples for Wiki Enhancement")
    print("=" * 50)
    print("Copy any prompt below and use it in the enhance-wiki-definitions.py script")
    print()
    
    for name, prompt in EXAMPLE_PROMPTS.items():
        print(f"📝 {name.replace('_', ' ').title()}:")
        print(f"   {prompt}")
        print()

if __name__ == "__main__":
    print_examples()
