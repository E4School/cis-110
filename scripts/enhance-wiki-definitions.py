#!/usr/bin/env python3
"""
Wiki Definition Enhancer for CIS 110

This script batch processes all wiki files and enhances their definitions 
by sending them to ChatGPT with appropriate enhancement prompts.

Requirements:
- pip install openai python-dotenv
- Create a .env file with OPENAI_API_KEY=your-key-here

Usage: python enhance-wiki-definitions.py
"""

import os
import re
import time
import argparse
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI library not available. Install with: pip install openai")

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("python-dotenv library not available. Install with: pip install python-dotenv")


def load_api_key() -> Optional[str]:
    """
    Load the OpenAI API key from .env file or environment variable.
    
    Returns:
        str: API key if found, None otherwise
    """
    # Try to load from .env file first
    if DOTENV_AVAILABLE:
        # Look for .env file in script directory or parent directory
        script_dir = Path(__file__).parent
        env_paths = [
            script_dir / '.env',
            script_dir.parent / '.env'
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                print(f"📄 Loaded environment from {env_path}")
                break
        else:
            # Try loading from current directory
            load_dotenv()
    
    # Get API key from environment (either from .env or system env)
    api_key = os.getenv('OPENAI_API_KEY')
    return api_key


class WikiDefinitionEnhancer:
    def __init__(self, prompt_override: Optional[str] = None, append_mode: bool = False, model: str = "gpt-5", concept_list: Optional[str] = None):
        """
        Initialize the enhancer with OpenAI client.
        
        Args:
            prompt_override: Custom prompt to use instead of default enhancement prompt
            append_mode: If True, append responses to files instead of replacing definitions
            model: OpenAI model to use (default: gpt-5)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library is required. Install with: pip install openai")
        
        # Load API key from .env file or environment
        api_key = load_api_key()
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found. Create a .env file with OPENAI_API_KEY=your-key-here")

        self.client = OpenAI(api_key=api_key)
        self.enhancement_count = 0
        self.error_count = 0
        self.prompt_override = prompt_override
        self.append_mode = append_mode
        self.model = model
        # Large external list of concepts (optional). If provided and custom prompt contains
        # {concept_list} it will be substituted; otherwise appended under a heading.
        self.concept_list = concept_list

        print(f"🤖 Using model: {model}")
        
    def create_enhancement_prompt(self, term: str, current_definition: str, source_file: Optional[Path] = None) -> str:
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
            # Start with the raw override template
            custom_prompt = self.prompt_override

            # Basic placeholders
            custom_prompt = custom_prompt.replace("{term}", term)
            custom_prompt = custom_prompt.replace("{current_definition}", current_definition)

            # File include placeholders: {FILE:relative/path.txt}
            # We allow relative to project root (script_dir.parent) or absolute paths (discouraged)
            file_pattern = re.compile(r"\{FILE:([^}]+)\}")
            script_dir = Path(__file__).parent
            project_dir = script_dir.parent
            source_dir = source_file.parent if source_file else None  # e.g., wiki/
            term_subdir = None
            if source_file is not None:
                # wiki/term.md -> wiki/term/
                term_subdir = source_file.parent / source_file.stem

            def replace_file(match):
                rel_path = match.group(1).strip()
                # If path starts with ./ or ../ and we have a source_dir, resolve relative to the wiki file's directory
                base_path: Path
                if rel_path.startswith('./') and term_subdir is not None:
                    base_path = term_subdir / rel_path[2:]
                elif source_dir and rel_path.startswith('../'):
                    base_path = (term_subdir or source_dir) / rel_path  # normal parent traversal
                elif term_subdir is not None:
                    # Try term-specific file first if it's a simple relative name (no leading slash)
                    if not rel_path.startswith('/') and not re.match(r'^[A-Za-z]:\\', rel_path):
                        candidate_first = (term_subdir / rel_path).resolve()
                        if candidate_first.exists():
                            base_path = candidate_first
                        else:
                            base_path = project_dir / rel_path
                    else:
                        base_path = project_dir / rel_path
                else:
                    base_path = project_dir / rel_path
                # Prevent directory traversal outside project (normalize and ensure within project)
                try:
                    candidate = base_path if isinstance(base_path, Path) else Path(base_path)
                    candidate = candidate.resolve()
                    if not str(candidate).startswith(str(project_dir.resolve())):
                        raise ValueError(f"Included file path outside project: {rel_path}")
                    if not candidate.exists():
                        raise FileNotFoundError(f"Included file not found: {rel_path}")
                    text = candidate.read_text(encoding='utf-8')
                    # Limit very large files
                    max_chars = 8000
                    if len(text) > max_chars:
                        text = text[:max_chars] + "\n...[TRUNCATED]"
                    return f"\n[FILE: {rel_path}]\n{text}\n[END FILE]\n"
                except Exception as e:
                    # Re-raise to surface the error to caller so processing halts for this term
                    raise

            if '{FILE:' in custom_prompt:
                custom_prompt = file_pattern.sub(replace_file, custom_prompt)

            # Concept list placeholder
            if "{concept_list}" in custom_prompt:
                custom_prompt = custom_prompt.replace("{concept_list}", self.concept_list or "(no concept list provided)")
                return custom_prompt
            # If concept list provided but no placeholder, append it for convenience
            if self.concept_list:
                return custom_prompt + "\n\nConcept List (for reference):\n" + self.concept_list
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

    def enhance_definition(self, term: str, current_definition: str, source_path: Optional[Path] = None) -> Optional[str]:
        """
        Send definition to ChatGPT for enhancement.
        
        Args:
            term: The vocabulary term
            current_definition: Current definition text
            
        Returns:
            str: Enhanced definition or None if failed
        """
        try:
            prompt = self.create_enhancement_prompt(term, current_definition, source_path)
            
            # Use different API calls based on model
            if self.model.startswith("gpt-5"):
                # GPT-5 uses the Responses API
                response = self.client.responses.create(
                    model=self.model,
                    input=prompt,
                    reasoning={"effort": "low"}  # Optional parameter for GPT-5
                )
                enhanced_definition = response.output_text.strip()
            else:
                # Other models use Chat Completions API
                api_params = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.7
                }
                response = self.client.chat.completions.create(**api_params)
                enhanced_definition = response.choices[0].message.content.strip()
            
            # Basic validation - ensure we got a reasonable response
            if len(enhanced_definition) < 20:
                print(f"  Warning: Enhanced definition for '{term}' seems too short ({len(enhanced_definition)} chars)")
                # For debugging purposes, let's accept short responses for now
                if len(enhanced_definition) == 0:
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
        
        # First, try to find a formal "## Definition" section
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
        
        # If no formal definition section found, look for simple format:
        # Title followed by definition text
        if len(lines) >= 3:
            # Check if we have: # Title, empty line, definition text
            if lines[0].startswith('# ') and lines[1].strip() == '' and lines[2].strip():
                definition_text = lines[2].strip()
                # Make sure it's not another heading
                if not definition_text.startswith('#'):
                    return definition_text
        
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

    def write_to_nested_file(self, base_file_path: Path, output_filename: str, term: str, response: str) -> bool:
        """
        Write response to a nested file structure: wiki/term-name/output-filename.md
        
        Args:
            base_file_path: Path to the original wiki file
            output_filename: Name of the output file (without .md extension)
            term: The vocabulary term
            response: Response from ChatGPT to write
            
        Returns:
            bool: True if file was written successfully
        """
        import datetime
        
        try:
            # Create nested directory based on the base filename (without extension)
            base_name = base_file_path.stem  # e.g., "algorithm" from "algorithm.md"
            nested_dir = base_file_path.parent / base_name
            nested_dir.mkdir(exist_ok=True)
            
            # Create the output file path
            if not output_filename.endswith('.md'):
                output_filename += '.md'
            output_path = nested_dir / output_filename
            
            # Generate timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare content
            content = f"""# {term} - {output_filename.replace('.md', '').replace('-', ' ').title()}

{response}
"""
            
            # If file exists, append with separator
            if output_path.exists():
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
                
                content = f"""{existing_content}

---

## {timestamp}

{response}
"""
            
            # Write the file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  📁 Written to: {nested_dir.name}/{output_filename}")
            return True
            
        except Exception as e:
            print(f"  ❌ Error writing to nested file: {e}")
            return False

    def process_wiki_file(self, file_path: Path, output_filename: Optional[str] = None) -> bool:
        """
        Process a single wiki file to enhance its definition or create custom content.
        
        Args:
            file_path: Path to the wiki file
            output_filename: If provided, write to nested file instead of modifying original
            
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
                if not self.append_mode and not output_filename:
                    return False
                # Use the whole content as "definition" for custom prompts
                current_definition = content
            
            # Get response from ChatGPT
            response = self.enhance_definition(term, current_definition, file_path)
            if not response:
                self.error_count += 1
                return False
            
            # Handle output based on mode
            if output_filename:
                # Write to nested file structure
                success = self.write_to_nested_file(file_path, output_filename, term, response)
                if success:
                    self.enhancement_count += 1
                else:
                    self.error_count += 1
                return success
            elif self.append_mode:
                # Original append behavior (for backward compatibility)
                updated_content = self.append_to_wiki_file(content, response)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            else:
                # Replace definition (original behavior)
                updated_content = self.update_definition_in_content(content, response)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            self.enhancement_count += 1
            return True
            
        except Exception as e:
            print(f"  Error processing {file_path.name}: {e}")
            self.error_count += 1
            return False

    def enhance_all_wiki_files(self, wiki_dir: Path, max_files: Optional[int] = None, start_from: Optional[str] = None, output_filename: Optional[str] = None):
        """
        Enhance definitions in all wiki files.
        
        Args:
            wiki_dir: Path to wiki directory
            max_files: Optional limit on number of files to process
            start_from: Optional filename to start from (inclusive)
            output_filename: If provided, write to nested files instead of modifying originals
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
        
        mode_description = "nested files" if output_filename else ("appending" if self.append_mode else "enhancing definitions")
        print(f"🚀 {mode_description.title()} in {len(wiki_files)} wiki files...")
        print("⚠️  This will use OpenAI API calls - ensure you have sufficient credits")
        print()
        
        for i, wiki_file in enumerate(wiki_files, 1):
            action = f"Creating {output_filename}" if output_filename else "Enhancing"
            print(f"[{i:3d}/{len(wiki_files)}] {action} {wiki_file.name}...")
            
            success = self.process_wiki_file(wiki_file, output_filename)
            
            if success and i % 10 == 0:
                print(f"  ✅ Processed {self.enhancement_count} files so far...")
                # Small delay to be respectful to API
                time.sleep(2)
            
            # Add longer delay between requests for GPT-5
            if self.model.startswith("gpt-5"):
                time.sleep(2)
            else:
                time.sleep(0.5)
        
        print(f"\n🎉 Processing complete!")
        print(f"  ✅ Successfully processed: {self.enhancement_count}")
        print(f"  ❌ Errors encountered: {self.error_count}")
        
        # Calculate success rate, avoiding division by zero
        total_processed = self.enhancement_count + self.error_count
        if total_processed > 0:
            success_rate = (self.enhancement_count / total_processed) * 100
            print(f"  📊 Success rate: {success_rate:.1f}%")
        else:
            print(f"  📊 Success rate: N/A (no files processed)")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Wiki Definition Enhancer - AI-Powered Definition Enhancement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhance-wiki-definitions.py --model gpt-4o --test
  python enhance-wiki-definitions.py --model gpt-5 --start-from algorithm.md
  python enhance-wiki-definitions.py --custom-prompt "Create 3 exam questions about: {current_definition}" --output-file "exam-questions"
  python enhance-wiki-definitions.py --model gpt-3.5-turbo --max-files 10
  python enhance-wiki-definitions.py --custom-prompt "Generate study guide for: {current_definition}" --output-file "study-guide" --test
        """
    )
    
    parser.add_argument(
        "--model", "-m",
        choices=["gpt-5", "gpt-4o", "gpt-4", "gpt-3.5-turbo"],
        default=None,
        help="Model to use (default: gpt-5)"
    )
    
    parser.add_argument(
        "--custom-prompt", "-p",
        type=str,
        default=None,
        help="Custom prompt to use. Use {term} and {current_definition} as placeholders."
    )
    
    parser.add_argument(
        "--output-file", "-o",
        type=str,
        default=None,
        help="Output filename for custom prompt results (required when using --custom-prompt)"
    )
    
    parser.add_argument(
        "--start-from", "-s",
        type=str,
        default=None,
        help="Start processing from a specific filename (inclusive)"
    )
    
    parser.add_argument(
        "--max-files", "-n",
        type=int,
        default=None,
        help="Maximum number of files to process (for testing)"
    )
    
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run in test mode (process only 5 files)"
    )
    
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip confirmation prompts and proceed automatically"
    )

    parser.add_argument(
        "--concept-list-file",
        type=str,
        default=None,
        help="(Optional) Path to a text file containing a list of concepts to inject via {concept_list}. If omitted and {concept_list} is present, the list is auto-generated."
    )
    parser.add_argument(
        "--auto-concept-list",
        action="store_true",
        help="Force auto-generation of concept list from scripts/list_vocabulary_terms.py even if {concept_list} not explicitly in custom prompt."
    )
    
    return parser.parse_args()


def main():
    """Main function to enhance all wiki definitions."""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Validate arguments
    if args.custom_prompt and not args.output_file:
        print("❌ Error: --output-file is required when using --custom-prompt")
        print("   Example: --custom-prompt 'Create questions' --output-file 'exam-questions'")
        return
    
    if args.output_file and not args.custom_prompt:
        print("❌ Error: --output-file can only be used with --custom-prompt")
        return
    
    if not OPENAI_AVAILABLE:
        print("❌ OpenAI library not available. Install with: pip install openai")
        return
    
    if not DOTENV_AVAILABLE:
        print("⚠️  python-dotenv library not available. Install with: pip install python-dotenv")
        print("   (Will try to use system environment variables)")
    
    # Check for API key
    api_key = load_api_key()
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        print("   Create a .env file in the project directory with:")
        print("   OPENAI_API_KEY=your-api-key-here")
        print("   Or set it as an environment variable:")
        print("   $env:OPENAI_API_KEY='your-api-key-here'")
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
    
    # Model selection (use CLI arg or prompt)
    if args.model:
        selected_model = args.model
        print(f"🧠 Using model: {selected_model} (from command line)")
    else:
        print("🧠 Model Options:")
        print("   1. gpt-5 (newest, most advanced, highest cost)")
        print("   2. gpt-4o (very capable, higher cost)")
        print("   3. gpt-4 (very capable, moderate cost)")
        print("   4. gpt-3.5-turbo (fast, lower cost)")
        print()
        model_choice = input("Choose model (1, 2, 3, or 4) [default: 1]: ").strip() or "1"
        
        model_map = {
            "1": "gpt-5",
            "2": "gpt-4o",
            "3": "gpt-4", 
            "4": "gpt-3.5-turbo"
        }
        
        selected_model = model_map.get(model_choice, "gpt-5")
    
    print(f"🧠 Selected model: {selected_model}")
    print()
    
    # Prepare concept list (file or auto-generate)
    concept_list_text = None
    need_concepts = False
    if args.custom_prompt and '{concept_list}' in args.custom_prompt:
        need_concepts = True
    if args.auto_concept_list:
        need_concepts = True

    if args.concept_list_file:
        try:
            concept_path = Path(args.concept_list_file)
            if not concept_path.is_absolute():
                concept_path = project_dir / args.concept_list_file
            concept_list_text = concept_path.read_text(encoding='utf-8').strip()
            print(f"📚 Loaded concept list from {concept_path} ({len(concept_list_text)} chars)")
        except Exception as e:
            print(f"⚠️  Failed to load concept list file: {e}")
            concept_list_text = None
            need_concepts = True  # fallback to auto

    if need_concepts and concept_list_text is None:
        list_script = project_dir / 'scripts' / 'list_vocabulary_terms.py'
        if list_script.exists():
            try:
                cmd = [sys.executable, str(list_script)]
                # We want categories included (default behavior). Capture output.
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                concept_list_text = result.stdout.strip()
                print(f"🛠️  Auto-generated concept list from list_vocabulary_terms.py ({len(concept_list_text)} chars)")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  Failed to auto-generate concept list: {e}")
        else:
            print("⚠️  list_vocabulary_terms.py not found; cannot auto-generate concept list")

    # Prompt options (use CLI arg or prompt)
    if args.custom_prompt:
        prompt_override = args.custom_prompt
        output_filename = args.output_file
        append_mode = False  # We don't append anymore, we create nested files
        print(f"📝 Custom prompt: {prompt_override[:100]}{'...' if len(prompt_override) > 100 else ''}")
        print(f"� Output to nested files: {output_filename}.md")
    else:
        output_filename = None
        if not args.yes:  # Only ask if not in auto-yes mode
            print("💬 Prompt Options:")
            print("   1. Use default enhancement prompt")
            print("   2. Use custom prompt (will create nested files)")
            print()
            prompt_choice = input("Choose prompt option (1 or 2): ").strip()
            
            if prompt_choice == "2":
                print("\nCustom prompt mode enabled!")
                print("Available placeholders: {term}, {current_definition}")
                print("Example: 'For the term {term}, create 3 exam questions about: {current_definition}'")
                print()
                prompt_override = input("Enter your custom prompt: ").strip()
                if not prompt_override:
                    print("❌ No prompt provided, exiting.")
                    return
                
                output_filename = input("Enter output filename (without .md): ").strip()
                if not output_filename:
                    print("❌ No output filename provided, exiting.")
                    return
                
                append_mode = False
                print(f"\n📝 Custom prompt: {prompt_override[:100]}{'...' if len(prompt_override) > 100 else ''}")
                print(f"� Output to nested files: {output_filename}.md")
            else:
                prompt_override = None
                append_mode = False
                print("📝 Using default enhancement prompt")
                print("🔄 Mode: Replace definitions in-place")
        else:
            prompt_override = None
            append_mode = False
            print("📝 Using default enhancement prompt (auto mode)")
            print("🔄 Mode: Replace definitions in-place")
    
    # File selection options
    start_from = args.start_from
    if start_from and not args.yes:
        print(f"📍 Starting from: {start_from}")
    elif not start_from and not args.yes:
        start_from_input = input("Start from specific file? (enter filename or press Enter for all): ").strip()
        start_from = start_from_input if start_from_input else None
    
    # Test mode / max files
    if args.test:
        max_files = 5
        print("🧪 Test mode: processing only 5 files")
    elif args.max_files:
        max_files = args.max_files
        print(f"📊 Processing maximum {max_files} files")
    else:
        if not args.yes:
            test_mode = input("Run in test mode? (process only 5 files) (y/N): ").strip().lower()
            max_files = 5 if test_mode in ['y', 'yes'] else None
        else:
            max_files = None
    
    # Confirmation (unless auto-yes mode)
    if not args.yes:
        if not max_files and not start_from:
            response = input("Are you sure you want to enhance ALL definitions? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("Operation cancelled.")
                return
        elif start_from and not max_files:
            response = input(f"Enhance definitions starting from {start_from}? (y/N): ").strip().lower()
            if response not in ['y', 'yes']:
                print("Operation cancelled.")
                return
    
    try:
        enhancer = WikiDefinitionEnhancer(
            prompt_override=prompt_override, 
            append_mode=append_mode,
            model=selected_model,
            concept_list=concept_list_text
        )
        enhancer.enhance_all_wiki_files(wiki_dir, max_files, start_from, output_filename)
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
