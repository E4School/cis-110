#!/usr/bin/env python3
"""
Quick GPT-4o Wiki Enhancer

This script runs the wiki enhancer with GPT-4o and a predefined good prompt
for quick high-quality enhancement without interactive prompts.

Usage: python quick-gpt4o-enhance.py [start_file]
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from enhance_wiki_definitions import WikiDefinitionEnhancer, OPENAI_AVAILABLE
except ImportError:
    print("❌ Could not import enhance_wiki_definitions module")
    sys.exit(1)


def main():
    """Quick enhancement with GPT-4o."""
    
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
    
    # Get start file from command line if provided
    start_from = None
    if len(sys.argv) > 1:
        start_from = sys.argv[1]
        if not start_from.endswith('.md'):
            start_from += '.md'
    
    print("🚀 Quick GPT-4o Wiki Enhancement")
    print("=" * 35)
    print("🧠 Model: gpt-4o (most capable)")
    print("📝 Mode: Default enhancement (replace definitions)")
    if start_from:
        print(f"📍 Starting from: {start_from}")
    print()
    print("⚠️  WARNING: This will make API calls to OpenAI (costs money)")
    print()
    
    response = input("Proceed with GPT-4o enhancement? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    try:
        enhancer = WikiDefinitionEnhancer(
            prompt_override=None,  # Use default enhancement prompt
            append_mode=False,     # Replace definitions
            model="gpt-4o"        # Use best model
        )
        enhancer.enhance_all_wiki_files(wiki_dir, start_from=start_from)
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
