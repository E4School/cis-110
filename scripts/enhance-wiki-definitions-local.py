#!/usr/bin/env python3
"""
Wiki Definition Template Enhancer for CIS 110

This script enhances wiki definitions using predefined templates and patterns
rather than AI. It's a fallback option when AI enhancement isn't available.

Usage: python enhance-wiki-definitions-local.py
"""

import re
from pathlib import Path
from typing import Optional, Dict


class LocalDefinitionEnhancer:
    def __init__(self):
        """Initialize the local enhancer with templates."""
        self.enhancement_count = 0
        self.error_count = 0
        
        # Define enhancement patterns for different types of terms
        self.enhancement_templates = {
            'hardware': "A {term} is a physical component of a computer system. {definition} It is an essential piece of hardware that enables computers to function properly and interact with users or other systems.",
            
            'software': "A {term} is a type of software application or program. {definition} It represents a crucial category of software that helps users accomplish specific tasks on computer systems.",
            
            'concept': "A {term} is a fundamental concept in computer science and information technology. {definition} Understanding this concept is essential for students learning about computing systems and digital technology.",
            
            'process': "A {term} is a process or methodology used in computing and information systems. {definition} This process is important for effective computer operation and user interaction with technology.",
            
            'technology': "A {term} is a technology or technical approach used in modern computing. {definition} This technology plays a significant role in how we interact with and utilize computer systems today.",
            
            'default': "A {term} is an important concept in computer and information sciences. {definition} This concept is fundamental to understanding how modern computing systems work and how they impact our daily lives."
        }
        
        # Keywords to categorize terms
        self.category_keywords = {
            'hardware': ['cpu', 'processor', 'ram', 'memory', 'storage', 'hardware', 'device', 'computer', 'motherboard', 'disk'],
            'software': ['software', 'program', 'application', 'app', 'operating system', 'os', 'browser', 'email'],
            'process': ['programming', 'algorithm', 'debugging', 'testing', 'process', 'method', 'procedure'],
            'technology': ['internet', 'web', 'cloud', 'network', 'wifi', 'encryption', 'cybersecurity', 'artificial intelligence'],
            'concept': ['data', 'information', 'file', 'folder', 'bit', 'byte', 'binary', 'digital']
        }

    def categorize_term(self, term: str, definition: str) -> str:
        """
        Categorize a term based on keywords in the term and definition.
        
        Args:
            term: The vocabulary term
            definition: Current definition
            
        Returns:
            str: Category name
        """
        term_lower = term.lower()
        definition_lower = definition.lower()
        combined_text = f"{term_lower} {definition_lower}"
        
        # Count matches for each category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in combined_text)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score, or default
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        return 'default'

    def enhance_definition(self, term: str, current_definition: str) -> str:
        """
        Enhance a definition using local templates and rules.
        
        Args:
            term: The vocabulary term
            current_definition: Current definition text
            
        Returns:
            str: Enhanced definition
        """
        # Clean up the current definition
        cleaned_definition = current_definition.strip()
        if cleaned_definition.endswith('.'):
            cleaned_definition = cleaned_definition[:-1]
        
        # Categorize the term
        category = self.categorize_term(term, current_definition)
        
        # Get template
        template = self.enhancement_templates.get(category, self.enhancement_templates['default'])
        
        # Apply template
        enhanced = template.format(
            term=term.lower(),
            definition=cleaned_definition
        )
        
        # Additional enhancements based on length
        if len(current_definition) < 50:
            enhanced += " This term is essential for students beginning their study of computer and information sciences."
        
        return enhanced

    def extract_current_definition(self, content: str) -> Optional[str]:
        """Extract the current definition from wiki content."""
        lines = content.split('\n')
        in_definition = False
        definition_lines = []
        
        for line in lines:
            if line.strip() == '## Definition':
                in_definition = True
                continue
            elif in_definition:
                if line.startswith('## ') or (line.strip() == '' and definition_lines):
                    break
                elif line.strip():
                    definition_lines.append(line.strip())
        
        if definition_lines:
            return ' '.join(definition_lines)
        return None

    def update_definition_in_content(self, content: str, new_definition: str) -> str:
        """Update the definition section in wiki content."""
        lines = content.split('\n')
        result_lines = []
        in_definition = False
        definition_replaced = False
        
        for line in lines:
            if line.strip() == '## Definition':
                result_lines.append(line)
                result_lines.append(new_definition)
                in_definition = True
                definition_replaced = True
                continue
            elif in_definition:
                if line.startswith('## ') or not line.strip():
                    in_definition = False
                    if line.strip():
                        result_lines.append('')
                        result_lines.append(line)
                else:
                    continue
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)

    def process_wiki_file(self, file_path: Path) -> bool:
        """Process a single wiki file to enhance its definition."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract term name
            term = file_path.stem.replace('-', ' ').title()
            
            # Extract current definition
            current_definition = self.extract_current_definition(content)
            if not current_definition:
                print(f"  Warning: No definition found in {file_path.name}")
                return False
            
            # Enhance the definition
            enhanced_definition = self.enhance_definition(term, current_definition)
            
            # Update content
            updated_content = self.update_definition_in_content(content, enhanced_definition)
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            self.enhancement_count += 1
            return True
            
        except Exception as e:
            print(f"  Error processing {file_path.name}: {e}")
            self.error_count += 1
            return False

    def enhance_all_wiki_files(self, wiki_dir: Path):
        """Enhance definitions in all wiki files."""
        wiki_files = list(wiki_dir.glob('*.md'))
        
        if not wiki_files:
            print("No wiki files found!")
            return
        
        print(f"🚀 Enhancing definitions in {len(wiki_files)} wiki files using local templates...")
        
        for i, wiki_file in enumerate(sorted(wiki_files), 1):
            print(f"[{i:3d}/{len(wiki_files)}] Enhancing {wiki_file.name}...")
            self.process_wiki_file(wiki_file)
            
            if i % 20 == 0:
                print(f"  ✅ Enhanced {self.enhancement_count} definitions so far...")
        
        print(f"\n🎉 Enhancement complete!")
        print(f"  ✅ Successfully enhanced: {self.enhancement_count}")
        print(f"  ❌ Errors encountered: {self.error_count}")


def main():
    """Main function."""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    wiki_dir = project_dir / 'wiki'
    
    if not wiki_dir.exists():
        print("❌ Wiki directory not found!")
        return
    
    print("🤖 Local Wiki Definition Enhancer")
    print("=" * 40)
    print("This will enhance all wiki definitions using local templates.")
    print()
    
    response = input("Proceed with enhancement? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    enhancer = LocalDefinitionEnhancer()
    enhancer.enhance_all_wiki_files(wiki_dir)


if __name__ == "__main__":
    main()
