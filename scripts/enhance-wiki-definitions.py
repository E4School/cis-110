#!/usr/bin/env python3
"""
Wiki Definition Enhancer for CIS 110

This script batch processes all wiki files and enhances their definitions 
by sending them to ChatGPT with appropriate enhancement prompts.

Requirements:
- pip install openai
- Set OPENAI_API_KEY environment variable

Usage: python enhance-wiki-definitions.py
"""

import os
import re
import time
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI library not available. Install with: pip install openai")


class WikiDefinitionEnhancer:
    def __init__(self, prompt_override: Optional[str] = None, append_mode: bool = False, model: str = "gpt-4o"):
        """
        Initialize the enhancer with OpenAI client.
        
        Args:
            prompt_override: Custom prompt to use instead of default enhancement prompt
            append_mode: If True, append responses to files instead of replacing definitions
            model: OpenAI model to use (default: gpt-4o)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library is required. Install with: pip install openai")
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        self.enhancement_count = 0
        self.error_count = 0
        self.prompt_override = prompt_override
        self.append_mode = append_mode
        self.model = model
        
        print(f"🤖 Using model: {model}")
        
    def create_enhancement_prompt(self, term: str, current_definition: str) -> str:
        """
        Create an enhancement prompt for ChatGPT.
        
        Args:
            term: The vocabulary term
            current_definition: The current definition to enhance
            
        Returns:
            str: The enhancement prompt
        """
        # Use prompt override if provided
        if self.prompt_override:
            # Replace placeholders in custom prompt
            custom_prompt = self.prompt_override.replace("{term}", term)
            custom_prompt = custom_prompt.replace("{current_definition}", current_definition)
            return custom_prompt
        
        # Use default enhancement prompt
        return f"""You are enhancing a vocabulary definition for a CIS 110 (Computer and Information Sciences) introductory course. 

TERM: {term}

CURRENT DEFINITION:
{current_definition}

Please enhance this definition to be:
1. **Clear and accessible** - Written for beginning CIS students with no prior technical knowledge
2. **Comprehensive** - Covers the essential aspects of the concept
3. **Educational** - Helps students understand the concept's importance in computing
4. **Practical** - Includes relevant real-world context or examples when helpful
5. **Concise** - Detailed but not overly verbose (2-4 sentences typically)

IMPORTANT: 
- Return ONLY the enhanced definition text
- Do NOT include any headers, formatting, or extra commentary
- Do NOT include phrases like "Here's an enhanced definition" or similar
- Make it suitable for a university-level introductory course

Enhanced definition:"""

    def enhance_definition(self, term: str, current_definition: str) -> Optional[str]:
        """
        Send definition to ChatGPT for enhancement.
        
        Args:
            term: The vocabulary term
            current_definition: Current definition text
            
        Returns:
            str: Enhanced definition or None if failed
        """
        try:
            prompt = self.create_enhancement_prompt(term, current_definition)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,  # Increased for better models
                temperature=0.7
            )
            
            enhanced_definition = response.choices[0].message.content.strip()
            
            # Basic validation - ensure we got a reasonable response
            if len(enhanced_definition) < 20:
                print(f"  Warning: Enhanced definition for '{term}' seems too short")
                return None
            
            return enhanced_definition
            
        except Exception as e:
            print(f"  Error enhancing '{term}': {e}")
            return None

    def extract_current_definition(self, content: str) -> Optional[str]:
        """
        Extract the current definition from wiki content.
        
        Args:
            content: Full wiki file content
            
        Returns:
            str: Current definition text or None if not found
        """
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
                elif line.strip():  # Non-empty line
                    definition_lines.append(line)
        
        if definition_lines:
            return '\n'.join(definition_lines).strip()
        return None

    def update_definition_in_content(self, content: str, new_definition: str) -> str:
        """
        Update the definition section in wiki content.
        
        Args:
            content: Original wiki content
            new_definition: Enhanced definition to insert
            
        Returns:
            str: Updated content
        """
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
                # Skip lines until we hit the next section or end
                if line.startswith('## ') or not line.strip():
                    in_definition = False
                    if line.strip():  # Next section
                        result_lines.append('')
                        result_lines.append(line)
                else:
                    continue  # Skip old definition lines
            else:
                result_lines.append(line)
        
        if not definition_replaced:
            # If no definition section found, add one after the title
            if len(result_lines) >= 3:
                result_lines.insert(3, '')
                result_lines.insert(4, '## Definition')
                result_lines.insert(5, new_definition)
        
        return '\n'.join(result_lines)

    def append_to_wiki_file(self, content: str, response: str) -> str:
        """
        Append response to wiki file with timestamp.
        
        Args:
            content: Original wiki content
            response: Response from ChatGPT to append
            
        Returns:
            str: Updated content with appended response
        """
        import datetime
        
        # Generate timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Clean up content (remove trailing whitespace)
        content = content.rstrip()
        
        # Append new section
        appended_content = f"""{content}

## {timestamp}
{response}
"""
        
        return appended_content

    def process_wiki_file(self, file_path: Path) -> bool:
        """
        Process a single wiki file to enhance its definition or append custom content.
        
        Args:
            file_path: Path to the wiki file
            
        Returns:
            bool: True if file was successfully processed
        """
        try:
            # Read current content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract term name from filename
            term = file_path.stem.replace('-', ' ').title()
            
            # Extract current definition
            current_definition = self.extract_current_definition(content)
            if not current_definition:
                print(f"  Warning: No definition found in {file_path.name}")
                if not self.append_mode:
                    return False
                # For append mode, use the whole content as "definition"
                current_definition = content
            
            # Get response from ChatGPT
            response = self.enhance_definition(term, current_definition)
            if not response:
                self.error_count += 1
                return False
            
            # Update content based on mode
            if self.append_mode:
                # Append response to end of file with timestamp
                updated_content = self.append_to_wiki_file(content, response)
            else:
                # Replace definition (original behavior)
                updated_content = self.update_definition_in_content(content, response)
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            self.enhancement_count += 1
            return True
            
        except Exception as e:
            print(f"  Error processing {file_path.name}: {e}")
            self.error_count += 1
            return False

    def enhance_all_wiki_files(self, wiki_dir: Path, max_files: Optional[int] = None, start_from: Optional[str] = None):
        """
        Enhance definitions in all wiki files.
        
        Args:
            wiki_dir: Path to wiki directory
            max_files: Optional limit on number of files to process
            start_from: Optional filename to start from (inclusive)
        """
        wiki_files = list(wiki_dir.glob('*.md'))
        
        if not wiki_files:
            print("No wiki files found!")
            return
        
        # Sort files alphabetically
        wiki_files = sorted(wiki_files)
        
        # Filter to start from specific file if requested
        if start_from:
            start_index = None
            for i, wiki_file in enumerate(wiki_files):
                if wiki_file.name == start_from:
                    start_index = i
                    break
            
            if start_index is not None:
                wiki_files = wiki_files[start_index:]
                print(f"📍 Starting from {start_from} (found at position {start_index + 1})")
                print(f"📋 Remaining files to process: {len(wiki_files)}")
            else:
                print(f"⚠️  Warning: Start file '{start_from}' not found, processing all files")
        
        if max_files:
            wiki_files = wiki_files[:max_files]
            print(f"Processing first {max_files} files (limit applied)...")
        
        print(f"🚀 Enhancing definitions in {len(wiki_files)} wiki files...")
        print("⚠️  This will use OpenAI API calls - ensure you have sufficient credits")
        print()
        
        for i, wiki_file in enumerate(wiki_files, 1):
            print(f"[{i:3d}/{len(wiki_files)}] Enhancing {wiki_file.name}...")
            
            success = self.process_wiki_file(wiki_file)
            
            if success and i % 10 == 0:
                print(f"  ✅ Enhanced {self.enhancement_count} definitions so far...")
                # Small delay to be respectful to API
                time.sleep(1)
            
            # Add small delay between requests
            time.sleep(0.5)
        
        print(f"\n🎉 Enhancement complete!")
        print(f"  ✅ Successfully enhanced: {self.enhancement_count}")
        print(f"  ❌ Errors encountered: {self.error_count}")
        print(f"  📊 Success rate: {(self.enhancement_count/(self.enhancement_count + self.error_count)*100):.1f}%")


def main():
    """Main function to enhance all wiki definitions."""
    
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI library not available. Install with: pip install openai")
        return
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY environment variable is required")
        print("   Set it with: $env:OPENAI_API_KEY='your-api-key-here'")
        return
    
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    wiki_dir = project_dir / 'wiki'
    
    if not wiki_dir.exists():
        print("❌ Wiki directory not found!")
        return
    
    print("🤖 Wiki Definition Enhancer - AI-Powered Definition Enhancement")
    print("=" * 65)
    print("This will enhance all wiki definitions using ChatGPT.")
    print("Each definition will be made more comprehensive and educational.")
    print()
    print("⚠️  WARNING: This will make API calls to OpenAI (costs money)")
    print()
    
    # Model selection
    print("🧠 Model Options:")
    print("   1. gpt-4o (newest, most capable, higher cost)")
    print("   2. gpt-4 (very capable, moderate cost)")
    print("   3. gpt-3.5-turbo (fast, lower cost)")
    print()
    model_choice = input("Choose model (1, 2, or 3) [default: 1]: ").strip() or "1"
    
    model_map = {
        "1": "gpt-4o",
        "2": "gpt-4", 
        "3": "gpt-3.5-turbo"
    }
    
    selected_model = model_map.get(model_choice, "gpt-4o")
    print(f"🧠 Selected model: {selected_model}")
    print()
    
    # Option for custom prompt
    print("💬 Prompt Options:")
    print("   1. Use default enhancement prompt")
    print("   2. Use custom prompt (will append results to files)")
    print()
    prompt_choice = input("Choose prompt option (1 or 2): ").strip()
    
    prompt_override = None
    append_mode = False
    
    if prompt_choice == "2":
        print("\nCustom prompt mode enabled!")
        print("Available placeholders: {term}, {current_definition}")
        print("Example: 'For the term {term}, create 3 exam questions about: {current_definition}'")
        print()
        prompt_override = input("Enter your custom prompt: ").strip()
        if not prompt_override:
            print("❌ No prompt provided, exiting.")
            return
        append_mode = True
        print(f"\n📝 Custom prompt: {prompt_override[:100]}{'...' if len(prompt_override) > 100 else ''}")
        print("🔄 Mode: Append responses to files with timestamps")
    else:
        print("📝 Using default enhancement prompt")
        print("🔄 Mode: Replace definitions in-place")
    
    # Option to start from specific file
    start_from_input = input("Start from specific file? (enter filename or press Enter for all): ").strip()
    start_from = start_from_input if start_from_input else None
    
    # Option to limit files for testing
    test_mode = input("Run in test mode? (process only 5 files) (y/N): ").strip().lower()
    max_files = 5 if test_mode in ['y', 'yes'] else None
    
    if not test_mode and not start_from:
        response = input("Are you sure you want to enhance ALL definitions? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    elif start_from and not test_mode:
        response = input(f"Enhance definitions starting from {start_from}? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    try:
        enhancer = WikiDefinitionEnhancer(
            prompt_override=prompt_override, 
            append_mode=append_mode,
            model=selected_model
        )
        enhancer.enhance_all_wiki_files(wiki_dir, max_files, start_from)
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
