#!/usr/bin/env python3
"""
Wiki Mention Graph Builder for CIS 110

This script analyzes all wiki files to build a directed graph of vocabulary term mentions.
Each edge represents one term mentioning another in its definition.

The graph is stored in wiki/graph.json in compressed format:
- Words are assigned numeric IDs 
- Edges are stored as [source_id, target_id] pairs
- Includes metadata for reconstruction

Usage: python build-mention-graph.py
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class WikiMentionGraphBuilder:
    def __init__(self):
        """Initialize the graph builder."""
        self.word_to_id = {}  # word -> numeric ID
        self.id_to_word = {}  # numeric ID -> word
        self.edges = []       # list of [source_id, target_id] pairs
        self.next_id = 0
        
        # Statistics
        self.total_files = 0
        self.total_mentions = 0
        self.self_references = 0
        
    def get_or_create_word_id(self, word: str) -> int:
        """
        Get existing ID for word or create new one.
        
        Args:
            word: The vocabulary word (normalized)
            
        Returns:
            int: Numeric ID for the word
        """
        if word not in self.word_to_id:
            word_id = self.next_id
            self.word_to_id[word] = word_id
            self.id_to_word[word_id] = word
            self.next_id += 1
            return word_id
        return self.word_to_id[word]
    
    def normalize_term(self, term: str) -> str:
        """
        Normalize a term for consistent matching.
        
        Args:
            term: Raw term from filename or content
            
        Returns:
            str: Normalized term
        """
        # Convert filename format to display format
        normalized = term.lower()
        normalized = normalized.replace('-', ' ')
        normalized = normalized.replace('_', ' ')
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def extract_wiki_links(self, content: str) -> Set[str]:
        """
        Extract [[wiki-style]] links from content.
        
        Args:
            content: Full wiki file content
            
        Returns:
            Set[str]: Set of linked terms (normalized)
        """
        # Pattern to match [[word]] or [[word-with-dashes]]
        wiki_link_pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(wiki_link_pattern, content)
        
        linked_terms = set()
        for match in matches:
            normalized = self.normalize_term(match)
            linked_terms.add(normalized)
        
        return linked_terms
    
    def extract_implicit_mentions(self, content: str, all_vocab_terms: Set[str]) -> Set[str]:
        """
        Extract implicit mentions of vocabulary terms in content.
        
        Args:
            content: Wiki file content
            all_vocab_terms: Set of all known vocabulary terms
            
        Returns:
            Set[str]: Set of implicitly mentioned terms
        """
        # Use ALL content, not just definition section
        # Remove markdown headers and formatting for cleaner matching
        clean_content = content.lower()
        
        # Remove markdown formatting that might interfere with matching
        clean_content = re.sub(r'#{1,6}\s*', '', clean_content)  # Remove headers
        clean_content = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_content)  # Remove bold
        clean_content = re.sub(r'\*([^*]+)\*', r'\1', clean_content)  # Remove italic
        clean_content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_content)  # Remove links
        
        mentioned_terms = set()
        
        for term in all_vocab_terms:
            # Skip very short terms to avoid false positives
            if len(term) < 4:
                continue
                
            # Look for the term as a whole word
            pattern = r'\b' + re.escape(term.lower()) + r'\b'
            if re.search(pattern, clean_content):
                mentioned_terms.add(term)
        
        return mentioned_terms
    
    def extract_definition_section(self, content: str) -> str:
        """
        Extract just the definition section from wiki content.
        
        Args:
            content: Full wiki file content
            
        Returns:
            str: Definition section content
        """
        lines = content.split('\n')
        in_definition = False
        definition_lines = []
        
        for line in lines:
            if line.strip() == '## Definition':
                in_definition = True
                continue
            elif in_definition:
                if line.startswith('## ') and line.strip() != '## Definition':
                    break
                elif line.strip():
                    definition_lines.append(line.strip())
        
        return ' '.join(definition_lines)
    
    def get_all_vocab_terms(self, wiki_dir: Path) -> Set[str]:
        """
        Get all vocabulary terms from wiki filenames.
        
        Args:
            wiki_dir: Path to wiki directory
            
        Returns:
            Set[str]: All vocabulary terms (normalized)
        """
        vocab_terms = set()
        
        for wiki_file in wiki_dir.glob('*.md'):
            # Skip special files
            if wiki_file.name in ['README.md', 'index.md', 'graph.json']:
                continue
                
            term = self.normalize_term(wiki_file.stem)
            vocab_terms.add(term)
        
        return vocab_terms
    
    def process_wiki_file(self, file_path: Path, all_vocab_terms: Set[str]) -> None:
        """
        Process a single wiki file to extract mentions.
        
        Args:
            file_path: Path to wiki file
            all_vocab_terms: Set of all vocabulary terms
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get the source term
            source_term = self.normalize_term(file_path.stem)
            source_id = self.get_or_create_word_id(source_term)
            
            # Extract explicit wiki links
            wiki_links = self.extract_wiki_links(content)
            
            # Extract implicit mentions
            implicit_mentions = self.extract_implicit_mentions(content, all_vocab_terms)
            
            # Combine all mentions
            all_mentions = wiki_links | implicit_mentions
            
            # Remove self-references
            if source_term in all_mentions:
                all_mentions.remove(source_term)
                self.self_references += 1
            
            # Create edges for valid mentions
            for mentioned_term in all_mentions:
                if mentioned_term in all_vocab_terms:
                    target_id = self.get_or_create_word_id(mentioned_term)
                    self.edges.append([source_id, target_id])
                    self.total_mentions += 1
            
            self.total_files += 1
            
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
    
    def build_graph(self, wiki_dir: Path) -> Dict:
        """
        Build the complete mention graph.
        
        Args:
            wiki_dir: Path to wiki directory
            
        Returns:
            Dict: Graph data structure
        """
        print("🔍 Discovering vocabulary terms...")
        all_vocab_terms = self.get_all_vocab_terms(wiki_dir)
        print(f"   Found {len(all_vocab_terms)} vocabulary terms")
        
        print("📖 Processing wiki files...")
        wiki_files = [f for f in wiki_dir.glob('*.md') 
                     if f.name not in ['README.md', 'index.md']]
        
        for i, wiki_file in enumerate(sorted(wiki_files), 1):
            if i % 20 == 0:
                print(f"   Processed {i}/{len(wiki_files)} files...")
            self.process_wiki_file(wiki_file, all_vocab_terms)
        
        print(f"   Processed {self.total_files} files")
        
        # Build the graph structure
        graph_data = {
            'metadata': {
                'total_nodes': len(self.word_to_id),
                'total_edges': len(self.edges),
                'total_files_processed': self.total_files,
                'total_mentions': self.total_mentions,
                'self_references_removed': self.self_references,
                'created_at': '2025-09-02',
                'description': 'Wiki vocabulary mention graph for CIS 110'
            },
            'nodes': {
                'id_to_word': self.id_to_word,
                'word_to_id': self.word_to_id
            },
            'edges': self.edges
        }
        
        return graph_data
    
    def calculate_graph_statistics(self, graph_data: Dict) -> Dict:
        """
        Calculate useful statistics about the graph.
        
        Args:
            graph_data: The graph structure
            
        Returns:
            Dict: Graph statistics
        """
        edges = graph_data['edges']
        nodes = graph_data['nodes']['id_to_word']
        
        # Count in-degree and out-degree for each node
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        
        for source_id, target_id in edges:
            out_degree[source_id] += 1
            in_degree[target_id] += 1
        
        # Find most referenced terms (highest in-degree)
        most_referenced = sorted(
            [(nodes[node_id], degree) for node_id, degree in in_degree.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
        
        # Find most referencing terms (highest out-degree)  
        most_referencing = sorted(
            [(nodes[node_id], degree) for node_id, degree in out_degree.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
        
        # Calculate density
        num_nodes = len(nodes)
        max_possible_edges = num_nodes * (num_nodes - 1)  # Directed graph, no self-loops
        density = len(edges) / max_possible_edges if max_possible_edges > 0 else 0
        
        return {
            'num_nodes': num_nodes,
            'num_edges': len(edges),
            'density': density,
            'average_out_degree': sum(out_degree.values()) / num_nodes if num_nodes > 0 else 0,
            'average_in_degree': sum(in_degree.values()) / num_nodes if num_nodes > 0 else 0,
            'most_referenced_terms': most_referenced,
            'most_referencing_terms': most_referencing,
            'isolated_nodes': [nodes[node_id] for node_id in nodes 
                             if node_id not in in_degree and node_id not in out_degree]
        }


def main():
    """Main function to build the mention graph."""
    
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    wiki_dir = project_dir / 'wiki'
    
    if not wiki_dir.exists():
        print("❌ Wiki directory not found!")
        return
    
    print("🕸️  Wiki Mention Graph Builder")
    print("=" * 40)
    print("Building directed graph of vocabulary term mentions...")
    print()
    
    # Build the graph
    builder = WikiMentionGraphBuilder()
    graph_data = builder.build_graph(wiki_dir)
    
    # Calculate statistics
    print("📊 Calculating graph statistics...")
    stats = builder.calculate_graph_statistics(graph_data)
    
    # Add statistics to graph data
    graph_data['statistics'] = stats
    
    # Save to JSON file
    output_file = wiki_dir / 'graph.json'
    print(f"💾 Saving graph to {output_file}...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n✅ Graph built successfully!")
    print(f"   📊 Nodes: {stats['num_nodes']}")
    print(f"   🔗 Edges: {stats['num_edges']}")
    print(f"   📈 Density: {stats['density']:.4f}")
    print(f"   ⚡ Avg Out-degree: {stats['average_out_degree']:.2f}")
    print(f"   ⚡ Avg In-degree: {stats['average_in_degree']:.2f}")
    
    print(f"\n🔝 Most Referenced Terms:")
    for term, degree in stats['most_referenced_terms'][:5]:
        print(f"   • {term}: {degree} references")
    
    print(f"\n📝 Most Referencing Terms:")
    for term, degree in stats['most_referencing_terms'][:5]:
        print(f"   • {term}: references {degree} other terms")
    
    if stats['isolated_nodes']:
        print(f"\n🏝️  Isolated Terms ({len(stats['isolated_nodes'])}):")
        for term in stats['isolated_nodes'][:5]:
            print(f"   • {term}")
        if len(stats['isolated_nodes']) > 5:
            print(f"   ... and {len(stats['isolated_nodes']) - 5} more")
    
    print(f"\n📁 Graph saved to: {output_file}")


if __name__ == "__main__":
    main()
