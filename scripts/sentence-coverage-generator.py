#!/usr/bin/env python3
"""
🎯 Vocabulary Sentence Coverage Generator
=========================================
Finds the minimum number of natural sentences that mention each vocabulary word exactly once.
This is a set cover optimization problem with natural language constraints.
"""

import json
import os
import sys
from typing import List, Set, Dict, Tuple
import itertools
from collections import defaultdict
import openai
import re

class VocabularyCoverageOptimizer:
    def __init__(self, wiki_dir: str):
        """Initialize with vocabulary from wiki directory."""
        self.wiki_dir = wiki_dir
        self.vocabulary = self._load_vocabulary()
        self.graph_data = self._load_graph()
        self.term_relationships = self._extract_relationships()
        
        print(f"📚 Loaded {len(self.vocabulary)} vocabulary terms")
        
    def _load_vocabulary(self) -> Set[str]:
        """Load all vocabulary terms from wiki files."""
        vocabulary = set()
        
        for filename in os.listdir(self.wiki_dir):
            if filename.endswith('.md') and filename != 'index.md':
                # Convert filename to term (remove .md, replace hyphens with spaces)
                term = filename[:-3].replace('-', ' ')
                # Handle special cases like acronyms
                if term.endswith(' ai'):
                    term = term[:-3] + ' (AI)'
                elif term.endswith(' ar'):
                    term = term[:-3] + ' (AR)'
                elif term.endswith(' vr'):
                    term = term[:-3] + ' (VR)'
                elif term.endswith(' iot'):
                    term = term[:-4] + ' (IoT)'
                elif term.endswith(' 2fa'):
                    term = term[:-4] + ' (2FA)'
                elif ' api ' in term or term.endswith(' api'):
                    term = term.replace(' api', ' API')
                elif ' url ' in term or term.endswith(' url'):
                    term = term.replace(' url', ' URL')
                elif ' html ' in term or term.endswith(' html'):
                    term = term.replace(' html', ' HTML')
                elif ' css ' in term or term.endswith(' css'):
                    term = term.replace(' css', ' CSS')
                elif ' http ' in term or term.endswith(' http'):
                    term = term.replace(' http', ' HTTP')
                elif ' https' in term:
                    term = term.replace(' https', ' HTTPS')
                elif ' dns ' in term or term.endswith(' dns'):
                    term = term.replace(' dns', ' DNS')
                elif ' ip ' in term or term.startswith('ip '):
                    term = term.replace(' ip ', ' IP ').replace('ip ', 'IP ')
                elif ' os ' in term or term.endswith(' os'):
                    term = term.replace(' os', ' OS')
                elif ' cpu' in term:
                    term = term.replace(' cpu', ' CPU')
                elif ' ram ' in term or term.endswith(' ram'):
                    term = term.replace(' ram', ' RAM')
                elif ' rom ' in term or term.endswith(' rom'):
                    term = term.replace(' rom', ' ROM')
                elif ' sql ' in term or term.endswith(' sql'):
                    term = term.replace(' sql', ' SQL')
                elif ' nosql' in term:
                    term = term.replace(' nosql', ' NoSQL')
                elif ' pdf ' in term or term.endswith(' pdf'):
                    term = term.replace(' pdf', ' PDF')
                elif ' qr ' in term or term.startswith('qr '):
                    term = term.replace(' qr ', ' QR ').replace('qr ', 'QR ')
                elif ' vpn ' in term or term.endswith(' vpn'):
                    term = term.replace(' vpn', ' VPN')
                elif ' wifi' in term or term == 'wifi':
                    term = term.replace('wifi', 'Wi-Fi')
                elif ' ux' in term:
                    term = term.replace(' ux', ' UX')
                elif ' ui' in term:
                    term = term.replace(' ui', ' UI')
                elif ' isp ' in term or term.endswith(' isp'):
                    term = term.replace(' isp', ' ISP')
                elif ' faq ' in term or term.endswith(' faq'):
                    term = term.replace(' faq', ' FAQ')
                
                vocabulary.add(term)
        
        return vocabulary
    
    def _load_graph(self) -> Dict:
        """Load the vocabulary relationship graph."""
        try:
            with open(os.path.join(self.wiki_dir, 'graph.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  No graph.json found, proceeding without relationship data")
            return {"nodes": [], "edges": []}
    
    def _extract_relationships(self) -> Dict[str, Set[str]]:
        """Extract which terms are related to each other from the graph."""
        relationships = defaultdict(set)
        
        # Create mapping from node IDs to clean terms
        node_map = {}
        for node in self.graph_data.get("nodes", []):
            clean_term = node["id"].replace("-", " ")
            node_map[node["id"]] = clean_term
        
        # Build relationships from edges
        for edge in self.graph_data.get("edges", []):
            source_term = node_map.get(edge["source"], "")
            target_term = node_map.get(edge["target"], "")
            
            if source_term and target_term:
                relationships[source_term].add(target_term)
                relationships[target_term].add(source_term)
        
        return dict(relationships)
    
    def find_related_clusters(self, max_cluster_size: int = 8) -> List[Set[str]]:
        """Find clusters of related terms that could naturally appear in the same sentence."""
        print(f"🔍 Finding related term clusters (max size: {max_cluster_size})...")
        
        clusters = []
        used_terms = set()
        
        # Sort terms by number of relationships (most connected first)
        term_connectivity = [(term, len(self.term_relationships.get(term, set()))) 
                           for term in self.vocabulary]
        term_connectivity.sort(key=lambda x: x[1], reverse=True)
        
        for term, connectivity in term_connectivity:
            if term in used_terms:
                continue
                
            # Start a new cluster with this term
            cluster = {term}
            related = self.term_relationships.get(term, set())
            
            # Add related terms that haven't been used yet
            for related_term in related:
                if (related_term in self.vocabulary and 
                    related_term not in used_terms and 
                    len(cluster) < max_cluster_size):
                    cluster.add(related_term)
            
            if len(cluster) > 1:
                clusters.append(cluster)
                used_terms.update(cluster)
            else:
                # Single term cluster
                clusters.append({term})
                used_terms.add(term)
        
        # Add any remaining terms as single-term clusters
        for term in self.vocabulary:
            if term not in used_terms:
                clusters.append({term})
        
        print(f"📊 Created {len(clusters)} clusters")
        cluster_sizes = [len(c) for c in clusters]
        print(f"   Cluster sizes: min={min(cluster_sizes)}, max={max(cluster_sizes)}, avg={sum(cluster_sizes)/len(cluster_sizes):.1f}")
        
        return clusters
    
    def generate_sentence_for_cluster(self, cluster: Set[str], context: str = "") -> str:
        """Generate a natural sentence that mentions all terms in the cluster."""
        terms_list = sorted(list(cluster))
        
        # Create a prompt for GPT to generate a natural sentence
        if len(terms_list) == 1:
            prompt = f"""Create a single, natural, factually correct, and memorable sentence that mentions the term "{terms_list[0]}" in the context of computer science or information technology.

The sentence should:
- Be educational and informative
- Sound natural and flow well
- Be factually accurate
- Be memorable for students
- Be appropriate for a CIS 110 introductory course

Term to include: {terms_list[0]}

Generate just the sentence, no explanation."""
        else:
            prompt = f"""Create a single, natural, factually correct, and memorable sentence that mentions ALL of these terms: {', '.join(terms_list)}

The sentence should:
- Include every term from the list exactly once
- Sound natural and flow well (not forced or awkward)
- Be factually accurate about computer science/IT concepts
- Be educational and memorable for students
- Be appropriate for a CIS 110 introductory course
- Connect the terms in a logical, meaningful way

Terms to include (ALL must appear): {', '.join(terms_list)}

Generate just the sentence, no explanation."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            sentence = response.choices[0].message.content.strip()
            
            # Clean up the sentence
            if sentence.startswith('"') and sentence.endswith('"'):
                sentence = sentence[1:-1]
            
            return sentence
            
        except Exception as e:
            print(f"❌ Error generating sentence for {terms_list}: {e}")
            # Fallback: create a simple sentence
            if len(terms_list) == 1:
                return f"Understanding {terms_list[0]} is important in computer science."
            else:
                return f"In computing, {', '.join(terms_list[:-1])}, and {terms_list[-1]} are all interconnected concepts."
    
    def verify_coverage(self, sentences: List[str]) -> Tuple[Set[str], Set[str]]:
        """Verify which terms are covered by the sentences and which are missing."""
        covered_terms = set()
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for term in self.vocabulary:
                term_lower = term.lower()
                # Check for exact matches and common variations
                if (term_lower in sentence_lower or 
                    term_lower.replace(" ", "-") in sentence_lower or
                    term_lower.replace(" ", "") in sentence_lower):
                    covered_terms.add(term)
        
        missing_terms = self.vocabulary - covered_terms
        return covered_terms, missing_terms
    
    def optimize_coverage(self) -> List[str]:
        """Generate optimized sentence coverage for all vocabulary terms."""
        print("🎯 Optimizing vocabulary coverage...")
        
        # Find related clusters
        clusters = self.find_related_clusters()
        
        sentences = []
        
        print("✍️  Generating sentences for clusters...")
        for i, cluster in enumerate(clusters, 1):
            print(f"   Cluster {i}/{len(clusters)}: {', '.join(sorted(cluster))}")
            sentence = self.generate_sentence_for_cluster(cluster)
            sentences.append(sentence)
            print(f"   → {sentence}")
        
        # Verify coverage
        covered, missing = self.verify_coverage(sentences)
        
        print(f"\n📊 Coverage Analysis:")
        print(f"   ✅ Covered: {len(covered)}/{len(self.vocabulary)} terms")
        print(f"   ❌ Missing: {len(missing)} terms")
        
        if missing:
            print(f"   Missing terms: {', '.join(sorted(missing))}")
            
            # Generate additional sentences for missing terms
            print("✍️  Generating additional sentences for missing terms...")
            for term in missing:
                sentence = self.generate_sentence_for_cluster({term})
                sentences.append(sentence)
                print(f"   → {sentence}")
        
        return sentences
    
    def save_results(self, sentences: List[str], output_file: str):
        """Save the optimized sentences to a file."""
        with open(output_file, 'w') as f:
            f.write("🎯 Optimized Vocabulary Coverage Sentences\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {len(sentences)} sentences covering {len(self.vocabulary)} terms\n\n")
            
            for i, sentence in enumerate(sentences, 1):
                f.write(f"{i:2d}. {sentence}\n")
            
            # Add coverage verification
            covered, missing = self.verify_coverage(sentences)
            f.write(f"\n📊 Coverage Verification:\n")
            f.write(f"✅ Covered: {len(covered)}/{len(self.vocabulary)} terms\n")
            if missing:
                f.write(f"❌ Missing: {', '.join(sorted(missing))}\n")
            else:
                f.write("🎉 All vocabulary terms covered!\n")
        
        print(f"💾 Results saved to: {output_file}")

def main():
    """Main function to run the vocabulary coverage optimization."""
    print("🎯 Vocabulary Sentence Coverage Generator")
    print("=" * 50)
    
    wiki_dir = "wiki"
    if not os.path.exists(wiki_dir):
        print(f"❌ Wiki directory not found: {wiki_dir}")
        return
    
    # Check for OpenAI API key
    if not openai.api_key:
        print("⚠️  OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        return
    
    optimizer = VocabularyCoverageOptimizer(wiki_dir)
    
    # Generate optimized coverage
    sentences = optimizer.optimize_coverage()
    
    # Save results
    output_file = os.path.join(wiki_dir, "vocabulary-coverage-sentences.txt")
    optimizer.save_results(sentences, output_file)
    
    print(f"\n🎉 Generated {len(sentences)} sentences for vocabulary coverage!")
    print(f"📁 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
