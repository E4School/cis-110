#!/usr/bin/env python3
"""
🎯 Optimal Vocabulary Sentence Generator
=======================================
Generates the minimum number of natural sentences that mention each vocabulary word exactly once.
Uses graph-based clustering and heuristic optimization.
"""

import json
import os
from typing import List, Set, Dict, Tuple
from collections import defaultdict
import itertools

class OptimalSentenceGenerator:
    def __init__(self, wiki_dir: str):
        """Initialize with vocabulary and relationships."""
        self.wiki_dir = wiki_dir
        self.vocabulary = self._load_vocabulary()
        self.graph_data = self._load_graph()
        self.relationships = self._extract_relationships()
        self.sentence_templates = self._create_sentence_templates()
        
    def _load_vocabulary(self) -> List[str]:
        """Load vocabulary terms from wiki files."""
        vocabulary = []
        for filename in sorted(os.listdir(self.wiki_dir)):
            if filename.endswith('.md') and filename != 'index.md':
                term = filename[:-3].replace('-', ' ')
                vocabulary.append(term)
        return vocabulary
    
    def _load_graph(self) -> Dict:
        """Load relationship graph."""
        try:
            with open(os.path.join(self.wiki_dir, 'graph.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"nodes": {"id_to_word": {}}, "edges": []}
    
    def _extract_relationships(self) -> Dict[str, Set[str]]:
        """Extract term relationships from graph."""
        relationships = defaultdict(set)
        
        if "nodes" in self.graph_data and "id_to_word" in self.graph_data["nodes"]:
            id_to_word = self.graph_data["nodes"]["id_to_word"]
            
            if "edges" in self.graph_data:
                for edge in self.graph_data["edges"]:
                    if len(edge) >= 2:
                        source_term = id_to_word.get(str(edge[0]), "")
                        target_term = id_to_word.get(str(edge[1]), "")
                        
                        if source_term and target_term and source_term in self.vocabulary and target_term in self.vocabulary:
                            relationships[source_term].add(target_term)
                            relationships[target_term].add(source_term)
        
        return dict(relationships)
    
    def _create_sentence_templates(self) -> List[Tuple[str, List[str]]]:
        """Create hand-crafted sentence templates for common term combinations."""
        templates = []
        
        # Find which terms we actually have
        vocab_set = set(self.vocabulary)
        
        # Basic computer system
        basic_computer = ["computer", "hardware", "software", "operating system os"]
        available_basic = [t for t in basic_computer if t in vocab_set]
        if len(available_basic) >= 3:
            templates.append((
                "A computer combines hardware and software components managed by an operating system (OS).",
                available_basic[:4]
            ))
        
        # Internet basics  
        internet_basics = ["internet", "world wide web web", "web browser", "url uniform resource locator", "http hypertext transfer protocol"]
        available_internet = [t for t in internet_basics if t in vocab_set]
        if len(available_internet) >= 3:
            templates.append((
                "The Internet enables the World Wide Web, where web browsers use HTTP to access URLs.",
                available_internet[:5]
            ))
        
        # Data management
        data_terms = ["data", "database", "file", "storage", "backup"]
        available_data = [t for t in data_terms if t in vocab_set]
        if len(available_data) >= 3:
            templates.append((
                "Data is organized in databases and files, stored on storage devices with backup systems for protection.",
                available_data[:5]
            ))
        
        # Security fundamentals
        security_terms = ["cybersecurity", "password", "encryption", "firewall", "malware", "virus"]
        available_security = [t for t in security_terms if t in vocab_set]
        if len(available_security) >= 3:
            templates.append((
                "Cybersecurity protects systems using passwords, encryption, and firewalls against malware and viruses.",
                available_security[:6]
            ))
        
        # Programming basics
        programming_terms = ["programming", "code", "algorithm", "function", "variable", "debugging"]
        available_programming = [t for t in programming_terms if t in vocab_set]
        if len(available_programming) >= 3:
            templates.append((
                "Programming involves writing code using algorithms, functions, and variables, then debugging to fix errors.",
                available_programming[:6]
            ))
        
        # Digital communication
        communication_terms = ["email", "instant messaging", "social media", "video conferencing", "netiquette"]
        available_communication = [t for t in communication_terms if t in vocab_set]
        if len(available_communication) >= 3:
            templates.append((
                "Digital communication includes email, instant messaging, social media, and video conferencing, all requiring good netiquette.",
                available_communication[:5]
            ))
        
        # Mobile technology
        mobile_terms = ["smart device", "wearable technology", "app store", "notification", "sync"]
        available_mobile = [t for t in mobile_terms if t in vocab_set]
        if len(available_mobile) >= 3:
            templates.append((
                "Smart devices and wearable technology connect to app stores for downloading applications that send notifications and sync data.",
                available_mobile[:5]
            ))
        
        return templates
    
    def find_optimal_clusters(self, max_cluster_size: int = 6) -> List[Set[str]]:
        """Find optimal clusters using greedy approach with relationship weights."""
        clusters = []
        remaining_terms = set(self.vocabulary)
        
        # Use pre-made templates first
        for sentence, terms in self.sentence_templates:
            available_terms = [t for t in terms if t in remaining_terms]
            if len(available_terms) >= 2:
                cluster = set(available_terms)
                clusters.append(cluster)
                remaining_terms -= cluster
                print(f"📝 Template cluster: {', '.join(sorted(cluster))}")
        
        # For remaining terms, use relationship-based clustering
        while remaining_terms:
            # Find the term with most connections to other remaining terms
            best_term = None
            best_score = -1
            
            for term in remaining_terms:
                related = self.relationships.get(term, set())
                score = len(related.intersection(remaining_terms))
                if score > best_score:
                    best_score = score
                    best_term = term
            
            if best_term is None:
                # Pick any remaining term
                best_term = next(iter(remaining_terms))
            
            # Build cluster around this term
            cluster = {best_term}
            related = self.relationships.get(best_term, set())
            
            # Add related terms up to max size
            for related_term in related:
                if related_term in remaining_terms and len(cluster) < max_cluster_size:
                    cluster.add(related_term)
            
            clusters.append(cluster)
            remaining_terms -= cluster
        
        return clusters
    
    def generate_sentence_for_cluster(self, cluster: Set[str]) -> str:
        """Generate a natural sentence for a cluster of terms."""
        terms = sorted(list(cluster))
        
        # Check if this matches one of our templates
        for template_sentence, template_terms in self.sentence_templates:
            if set(terms).issubset(set(template_terms)):
                return template_sentence
        
        # For manual generation, create context-aware sentences
        if len(terms) == 1:
            term = terms[0]
            
            # Context-specific single term sentences
            if "security" in term.lower() or "cyber" in term.lower():
                return f"Understanding {term} is crucial for protecting digital systems."
            elif "data" in term.lower() or "information" in term.lower():
                return f"Managing {term} effectively is essential in modern computing."
            elif "software" in term.lower() or "application" in term.lower():
                return f"The {term} provides essential functionality to users."
            elif "network" in term.lower() or "internet" in term.lower():
                return f"The concept of {term} connects computers worldwide."
            else:
                return f"Understanding {term} is important in computer science."
        
        # For multiple terms, create connecting sentences
        elif len(terms) == 2:
            return f"The relationship between {terms[0]} and {terms[1]} is fundamental to computing systems."
        
        elif len(terms) == 3:
            return f"In computing, {terms[0]}, {terms[1]}, and {terms[2]} work together as interconnected components."
        
        else:
            # For larger clusters, create comprehensive sentences
            if len(terms) <= 4:
                return f"Key computing concepts include {', '.join(terms[:-1])}, and {terms[-1]}."
            else:
                mid_point = len(terms) // 2
                first_part = ', '.join(terms[:mid_point])
                second_part = ', '.join(terms[mid_point:])
                return f"Computing systems integrate {first_part} with {second_part} to provide functionality."
    
    def generate_optimal_sentences(self) -> List[str]:
        """Generate the optimal set of sentences covering all vocabulary."""
        print("🎯 Generating Optimal Vocabulary Coverage Sentences")
        print("=" * 60)
        
        # Find optimal clusters
        clusters = self.find_optimal_clusters()
        
        print(f"\n📊 Clustering Results:")
        print(f"   Total clusters: {len(clusters)}")
        cluster_sizes = [len(c) for c in clusters]
        print(f"   Cluster sizes: min={min(cluster_sizes)}, max={max(cluster_sizes)}, avg={sum(cluster_sizes)/len(cluster_sizes):.1f}")
        
        # Generate sentences
        sentences = []
        print(f"\n✍️  Generating sentences:")
        
        for i, cluster in enumerate(clusters, 1):
            sentence = self.generate_sentence_for_cluster(cluster)
            sentences.append(sentence)
            terms_str = ', '.join(sorted(cluster))
            print(f"   {i:3d}. [{len(cluster)} terms] {terms_str}")
            print(f"        → {sentence}")
            print()
        
        # Verify coverage
        covered_terms = set()
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for term in self.vocabulary:
                if term.lower() in sentence_lower:
                    covered_terms.add(term)
        
        missing_terms = set(self.vocabulary) - covered_terms
        
        print(f"📊 Coverage Verification:")
        print(f"   ✅ Covered: {len(covered_terms)}/{len(self.vocabulary)} terms ({100*len(covered_terms)/len(self.vocabulary):.1f}%)")
        if missing_terms:
            print(f"   ❌ Missing: {len(missing_terms)} terms: {', '.join(sorted(missing_terms))}")
        else:
            print(f"   🎉 Perfect coverage achieved!")
        
        return sentences
    
    def save_results(self, sentences: List[str], output_file: str):
        """Save results to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("🎯 Optimal Vocabulary Coverage Sentences\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {len(sentences)} sentences covering {len(self.vocabulary)} vocabulary terms\n\n")
            
            for i, sentence in enumerate(sentences, 1):
                f.write(f"{i:3d}. {sentence}\n")
            
            # Coverage analysis
            covered_terms = set()
            for sentence in sentences:
                sentence_lower = sentence.lower()
                for term in self.vocabulary:
                    if term.lower() in sentence_lower:
                        covered_terms.add(term)
            
            missing_terms = set(self.vocabulary) - covered_terms
            
            f.write(f"\n📊 Coverage Analysis:\n")
            f.write(f"✅ Covered: {len(covered_terms)}/{len(self.vocabulary)} terms ({100*len(covered_terms)/len(self.vocabulary):.1f}%)\n")
            if missing_terms:
                f.write(f"❌ Missing: {', '.join(sorted(missing_terms))}\n")
            else:
                f.write("🎉 Perfect coverage achieved!\n")

def main():
    """Main function."""
    print("🎯 Optimal Vocabulary Sentence Generator")
    print("=" * 50)
    
    wiki_dir = "wiki"
    if not os.path.exists(wiki_dir):
        print(f"❌ Wiki directory not found: {wiki_dir}")
        return
    
    generator = OptimalSentenceGenerator(wiki_dir)
    sentences = generator.generate_optimal_sentences()
    
    # Save results
    output_file = os.path.join(wiki_dir, "optimal-coverage-sentences.txt")
    generator.save_results(sentences, output_file)
    
    print(f"\n🎉 Generated {len(sentences)} optimal coverage sentences!")
    print(f"📁 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
