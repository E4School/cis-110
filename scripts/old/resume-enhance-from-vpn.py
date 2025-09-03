#!/usr/bin/env python3
"""
Resume Wiki Enhancement from VPN

This script automatically runs the wiki definition enhancer starting from
vpn-virtual-private-network.md and proceeding alphabetically.

Usage: python resume-enhance-from-vpn.py
"""

import os
import sys
from pathlib import Path

# Add scripts directory to path so we can import the enhancer
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from enhance_wiki_definitions import WikiDefinitionEnhancer, OPENAI_AVAILABLE
except ImportError:
    # Try alternative import method
    try:
        import enhance_wiki_definitions as ewd
        WikiDefinitionEnhancer = ewd.WikiDefinitionEnhancer
        OPENAI_AVAILABLE = ewd.OPENAI_AVAILABLE
    except ImportError:
        print("❌ Could not import enhance_wiki_definitions module")
        sys.exit(1)


def main():
    """Main function to resume enhancement from VPN."""
    
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
    
    print("🤖 Resume Wiki Definition Enhancement from VPN")
    print("=" * 50)
    print("This will enhance wiki definitions starting from vpn-virtual-private-network.md")
    print("and continue alphabetically through the remaining files.")
    print()
    print("⚠️  WARNING: This will make API calls to OpenAI (costs money)")
    print()
    
    # Check if the VPN file exists
    vpn_file = wiki_dir / 'vpn-virtual-private-network.md'
    if not vpn_file.exists():
        print("❌ vpn-virtual-private-network.md not found!")
        return
    
    # Get list of remaining files
    all_files = sorted(list(wiki_dir.glob('*.md')))
    start_index = None
    
    for i, wiki_file in enumerate(all_files):
        if wiki_file.name == 'vpn-virtual-private-network.md':
            start_index = i
            break
    
    if start_index is None:
        print("❌ Could not find vpn-virtual-private-network.md in file list!")
        return
    
    remaining_files = all_files[start_index:]
    print(f"📋 Files to process: {len(remaining_files)}")
    print(f"📍 Starting from: {remaining_files[0].name}")
    if len(remaining_files) > 1:
        print(f"📄 Ending with: {remaining_files[-1].name}")
    print()
    
    response = input("Proceed with enhancement? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    try:
        enhancer = WikiDefinitionEnhancer()
        enhancer.enhance_all_wiki_files(wiki_dir, start_from='vpn-virtual-private-network.md')
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
