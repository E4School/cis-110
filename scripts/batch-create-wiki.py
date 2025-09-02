#!/usr/bin/env python3
"""
Batch Wiki Creator for CIS 110

This script creates comprehensive wiki pages for all missing vocabulary terms
from the vocabulary.md file.

Usage: python batch-create-wiki.py
"""

import re
import os
from pathlib import Path
import json


def extract_vocabulary_terms_with_definitions(file_path):
    """
    Extract vocabulary terms from the markdown file with their definitions and categories.
    
    Returns:
        dict: Dictionary mapping terms to their info (definition, category)
    """
    terms = {}
    current_category = "General"
    
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
                terms[term] = {
                    'definition': definition,
                    'category': current_category
                }
                
    except FileNotFoundError:
        print(f"Error: Could not find vocabulary file at {file_path}")
        return {}
    except Exception as e:
        print(f"Error reading vocabulary file: {e}")
        return {}
        
    return terms


def term_to_filename(term):
    """Convert a vocabulary term to the expected wiki filename."""
    filename = term.lower()
    filename = re.sub(r'[^a-z0-9\s\-]', '', filename)
    filename = re.sub(r'\s+', '-', filename)
    filename = re.sub(r'-+', '-', filename)
    filename = filename.strip('-')
    return f"{filename}.md"


def get_existing_wiki_files(wiki_dir):
    """Get set of existing wiki filenames."""
    if not wiki_dir.exists():
        return set()
    return {f.name for f in wiki_dir.iterdir() if f.is_file() and f.suffix == '.md'}


def generate_wiki_content(term, definition, category):
    """
    Generate comprehensive wiki content for a term based on its definition and category.
    """
    
    # Create related terms section based on the term's category and common relationships
    related_terms = generate_related_terms(term, category)
    
    # Generate examples based on the term
    examples = generate_examples(term, definition)
    
    # Generate key characteristics or components
    key_info = generate_key_info(term, definition, category)
    
    content = f"""# {term}

{definition}

## Definition
{generate_expanded_definition(term, definition, category)}

{key_info}

{examples}

## Related Terms
{related_terms}

{generate_additional_sections(term, category)}
"""
    
    return content


def generate_expanded_definition(term, definition, category):
    """Generate an expanded definition based on the term and category."""
    
    # Common expanded definition patterns based on categories
    if "Software" in category or "Application" in category:
        return f"{term} refers to {definition.lower()} This type of software plays an important role in computer systems by providing specific functionality to users or other programs."
    
    elif "Hardware" in category or "Device" in category:
        return f"{term} is {definition.lower()} As a hardware component, it works in conjunction with other computer parts to enable the overall functionality of computer systems."
    
    elif "Internet" in category or "Web" in category:
        return f"{term} is {definition.lower()} It is an essential component of internet infrastructure that enables global communication and information sharing."
    
    elif "Security" in category or "Cybersecurity" in category:
        return f"{term} refers to {definition.lower()} This security concept is crucial for protecting digital systems and data from various threats and unauthorized access."
    
    elif "Programming" in category:
        return f"{term} is {definition.lower()} It is a fundamental concept in computer programming and software development."
    
    elif "Data" in category or "Database" in category:
        return f"{term} refers to {definition.lower()} It plays a key role in data management and information systems."
    
    elif "Digital Communication" in category or "Social Media" in category:
        return f"{term} is {definition.lower()} It represents an important aspect of modern digital communication and online interaction."
    
    else:
        return f"{term} is {definition.lower()} This concept is important in understanding modern technology and computer systems."


def generate_key_info(term, definition, category):
    """Generate key characteristics, types, or components section."""
    
    if "Software" in category:
        return """## Key Characteristics
- **Functionality** - Provides specific capabilities to users or systems
- **Digital** - Exists as code and instructions rather than physical components
- **Interactive** - Responds to user input and system events
- **Updatable** - Can be modified and improved over time"""
    
    elif "Hardware" in category:
        return """## Key Characteristics
- **Physical** - Tangible component that can be touched
- **Electronic** - Uses electrical circuits and components
- **Durable** - Designed for long-term operation
- **Interconnected** - Works with other hardware components"""
    
    elif "Internet" in category or "Web" in category:
        return """## Key Characteristics
- **Networked** - Operates across interconnected computer systems
- **Global** - Accessible from around the world
- **Protocol-based** - Uses standardized communication rules
- **Scalable** - Can handle varying amounts of traffic and data"""
    
    elif "Security" in category:
        return """## Key Characteristics
- **Protective** - Designed to prevent unauthorized access
- **Proactive** - Anticipates and prevents potential threats
- **Layered** - Works as part of comprehensive security systems
- **Adaptive** - Evolves to address new types of threats"""
    
    elif "Data" in category:
        return """## Key Characteristics
- **Structured** - Organized in a systematic way
- **Accessible** - Can be retrieved and used when needed
- **Persistent** - Stored for future use and reference
- **Valuable** - Contains important information for decision-making"""
    
    else:
        return """## Key Characteristics
- **Digital** - Exists in electronic form
- **Functional** - Serves specific purposes in computer systems
- **Interactive** - Can be used and manipulated by users
- **Essential** - Important for modern computing and technology"""


def generate_examples(term, definition):
    """Generate relevant examples based on the term."""
    
    # Common examples based on term patterns
    if "software" in term.lower() or "application" in term.lower():
        return """## Examples
- Popular applications in this category
- Common use cases and scenarios
- Industry-standard implementations
- Open-source alternatives"""
    
    elif "device" in term.lower() or "hardware" in term.lower():
        return """## Examples
- Common types and models
- Different manufacturers and brands
- Various specifications and capabilities
- Consumer and professional versions"""
    
    elif "protocol" in term.lower() or "standard" in term.lower():
        return """## Examples
- Real-world implementations
- Different versions and variations
- Compatible systems and platforms
- Industry adoption and usage"""
    
    else:
        return """## Applications
- Common use cases
- Real-world implementations
- Industry applications
- Consumer and business usage"""


def generate_related_terms(term, category):
    """Generate related terms with wiki links."""
    
    # Define common relationships between terms
    base_terms = [
        "[[Computer]]", "[[Software]]", "[[Hardware]]", "[[Internet]]", 
        "[[Programming]]", "[[Data]]", "[[Cybersecurity]]"
    ]
    
    # Category-specific related terms
    if "Software" in category:
        return "- [[Software]] - General category of computer programs\n- [[Operating System (OS)]] - System software that manages resources\n- [[Application Software]] - Programs for end-users\n- [[Programming]] - Process of creating software"
    
    elif "Hardware" in category:
        return "- [[Hardware]] - Physical computer components\n- [[Computer]] - Complete system including hardware\n- [[Processor (CPU)]] - Central processing unit\n- [[Operating System (OS)]] - Software that manages hardware"
    
    elif "Internet" in category or "Web" in category:
        return "- [[Internet]] - Global network infrastructure\n- [[World Wide Web (Web)]] - System of interlinked documents\n- [[Web Browser]] - Software for accessing web content\n- [[URL (Uniform Resource Locator)]] - Web addresses"
    
    elif "Security" in category:
        return "- [[Cybersecurity]] - Practice of protecting digital systems\n- [[Malware]] - Malicious software threats\n- [[Encryption]] - Data protection method\n- [[Password]] - Authentication mechanism"
    
    elif "Programming" in category:
        return "- [[Programming]] - Process of creating software\n- [[Algorithm]] - Step-by-step problem-solving procedure\n- [[Code]] - Instructions written in programming languages\n- [[Software]] - Programs created through programming"
    
    elif "Data" in category:
        return "- [[Data]] - Raw facts and information\n- [[Database]] - Organized collection of data\n- [[Information]] - Processed data with meaning\n- [[Analytics]] - Process of examining data"
    
    else:
        return f"- [[Computer]] - Basic computing system\n- [[Software]] - Computer programs and applications\n- [[Technology]] - Applied scientific knowledge\n- [[Digital]] - Electronic and computer-based systems"


def generate_additional_sections(term, category):
    """Generate additional relevant sections based on category."""
    
    if "Security" in category:
        return """## Security Considerations
- **Risk Assessment** - Understanding potential vulnerabilities
- **Best Practices** - Recommended implementation approaches
- **Compliance** - Meeting regulatory and industry standards
- **Monitoring** - Ongoing surveillance and threat detection

## Implementation
- **Planning** - Proper design and strategy development
- **Deployment** - Careful rollout and configuration
- **Testing** - Verification of security effectiveness
- **Maintenance** - Regular updates and improvements"""
    
    elif "Programming" in category:
        return """## Usage in Programming
- **Syntax** - How it's written in code
- **Best Practices** - Recommended usage patterns
- **Common Patterns** - Typical implementation approaches
- **Debugging** - Troubleshooting and error handling

## Learning Resources
- **Tutorials** - Step-by-step learning materials
- **Documentation** - Official references and guides
- **Examples** - Sample code and implementations
- **Practice** - Exercises and projects"""
    
    elif "Internet" in category or "Web" in category:
        return """## Technical Details
- **Standards** - Official specifications and protocols
- **Implementation** - How it works in practice
- **Compatibility** - Support across different systems
- **Performance** - Speed and efficiency considerations

## Evolution
- **History** - Development and adoption timeline
- **Current Status** - Present-day usage and features
- **Future Trends** - Expected developments and improvements
- **Industry Impact** - Effect on business and society"""
    
    else:
        return """## Importance
This concept is significant in modern computing and technology, contributing to the overall functionality and user experience of digital systems.

## Future Developments
As technology continues to evolve, this area is likely to see continued innovation and improvement, adapting to new requirements and capabilities."""


def main():
    """Main function to batch create missing wiki files."""
    
    # Setup paths
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    vocab_file = project_dir / 'vocabulary.md'
    wiki_dir = project_dir / 'wiki'
    
    # Ensure wiki directory exists
    wiki_dir.mkdir(exist_ok=True)
    
    print("Loading vocabulary terms...")
    terms_info = extract_vocabulary_terms_with_definitions(vocab_file)
    
    if not terms_info:
        print("Error: No vocabulary terms found.")
        return
    
    print(f"Found {len(terms_info)} vocabulary terms.")
    
    # Get existing wiki files
    existing_files = get_existing_wiki_files(wiki_dir)
    print(f"Found {len(existing_files)} existing wiki files.")
    
    # Find missing terms
    missing_terms = []
    for term in terms_info:
        expected_filename = term_to_filename(term)
        if expected_filename not in existing_files:
            missing_terms.append(term)
    
    if not missing_terms:
        print("🎉 All vocabulary terms already have wiki files!")
        return
    
    print(f"Creating {len(missing_terms)} missing wiki files...")
    
    # Create missing wiki files
    created_count = 0
    for term in missing_terms:
        try:
            filename = term_to_filename(term)
            filepath = wiki_dir / filename
            
            # Generate content
            term_info = terms_info[term]
            content = generate_wiki_content(
                term, 
                term_info['definition'], 
                term_info['category']
            )
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_count += 1
            if created_count % 10 == 0:
                print(f"  Created {created_count}/{len(missing_terms)} files...")
                
        except Exception as e:
            print(f"Error creating {filename}: {e}")
    
    print(f"✅ Successfully created {created_count} wiki files!")
    print(f"📁 Wiki files are located in: {wiki_dir}")
    
    # Final verification
    final_existing = get_existing_wiki_files(wiki_dir)
    final_missing = len(terms_info) - len(final_existing)
    
    print(f"\n📊 Final Status:")
    print(f"  Total terms: {len(terms_info)}")
    print(f"  Wiki files created: {len(final_existing)}")
    print(f"  Still missing: {final_missing}")


if __name__ == "__main__":
    main()
