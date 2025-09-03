#!/usr/bin/env python3
"""
🎯 Vocabulary Analysis for Sentence Coverage
===========================================
Analyzes vocabulary terms and their relationships to plan optimal sentence coverage.
"""

import json
import os
import re
from typing import List, Set, Dict, Tuple
from collections import defaultdict, Counter

class VocabularyAnalyzer:
    def __init__(self, wiki_dir: str):
        """Initialize with vocabulary from wiki directory."""
        self.wiki_dir = wiki_dir
        self.vocabulary = self._load_vocabulary()
        self.graph_data = self._load_graph()
        self.term_relationships = self._extract_relationships()
        
    def _load_vocabulary(self) -> List[str]:
        """Load all vocabulary terms from wiki files."""
        vocabulary = []
        
        for filename in sorted(os.listdir(self.wiki_dir)):
            if filename.endswith('.md') and filename != 'index.md':
                # Convert filename to term (remove .md, replace hyphens with spaces)
                term = filename[:-3].replace('-', ' ')
                vocabulary.append(term)
        
        return vocabulary
    
    def _load_graph(self) -> Dict:
        """Load the vocabulary relationship graph."""
        try:
            with open(os.path.join(self.wiki_dir, 'graph.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"nodes": [], "edges": []}
    
    def _extract_relationships(self) -> Dict[str, Set[str]]:
        """Extract which terms are related to each other from the graph."""
        relationships = defaultdict(set)
        
        # Handle the actual graph structure from our files
        if "nodes" in self.graph_data and "id_to_word" in self.graph_data["nodes"]:
            # Map node IDs to terms
            id_to_word = self.graph_data["nodes"]["id_to_word"]
            
            # Build relationships from edges (which are arrays of [source_id, target_id])
            if "edges" in self.graph_data:
                for edge in self.graph_data["edges"]:
                    if len(edge) >= 2:
                        source_id = str(edge[0])
                        target_id = str(edge[1])
                        
                        source_term = id_to_word.get(source_id, "")
                        target_term = id_to_word.get(target_id, "")
                        
                        if source_term and target_term:
                            relationships[source_term].add(target_term)
                            relationships[target_term].add(source_term)
        
        return dict(relationships)
    
    def analyze_vocabulary_categories(self) -> Dict[str, List[str]]:
        """Categorize vocabulary terms by topic."""
        categories = {
            'hardware': [],
            'software': [],
            'internet_web': [],
            'security': [],
            'data': [],
            'programming': [],
            'devices': [],
            'general': []
        }
        
        # Keywords for each category
        hardware_keywords = ['hardware', 'cpu', 'ram', 'rom', 'processor', 'device', 'storage']
        software_keywords = ['software', 'application', 'program', 'os', 'operating system']
        internet_keywords = ['internet', 'web', 'http', 'url', 'browser', 'email', 'wifi', 'network']
        security_keywords = ['security', 'cyber', 'password', 'encryption', 'firewall', 'virus', 'malware', 'privacy']
        data_keywords = ['data', 'database', 'information', 'file', 'storage', 'backup']
        programming_keywords = ['code', 'programming', 'algorithm', 'function', 'variable', 'loop']
        device_keywords = ['smartphone', 'tablet', 'computer', 'device', 'wearable', 'smart']
        
        for term in self.vocabulary:
            term_lower = term.lower()
            categorized = False
            
            for keyword in hardware_keywords:
                if keyword in term_lower:
                    categories['hardware'].append(term)
                    categorized = True
                    break
            
            if not categorized:
                for keyword in software_keywords:
                    if keyword in term_lower:
                        categories['software'].append(term)
                        categorized = True
                        break
            
            if not categorized:
                for keyword in internet_keywords:
                    if keyword in term_lower:
                        categories['internet_web'].append(term)
                        categorized = True
                        break
            
            if not categorized:
                for keyword in security_keywords:
                    if keyword in term_lower:
                        categories['security'].append(term)
                        categorized = True
                        break
            
            if not categorized:
                for keyword in data_keywords:
                    if keyword in term_lower:
                        categories['data'].append(term)
                        categorized = True
                        break
            
            if not categorized:
                for keyword in programming_keywords:
                    if keyword in term_lower:
                        categories['programming'].append(term)
                        categorized = True
                        break
            
            if not categorized:
                for keyword in device_keywords:
                    if keyword in term_lower:
                        categories['devices'].append(term)
                        categorized = True
                        break
            
            if not categorized:
                categories['general'].append(term)
        
        return categories
    
    def find_term_clusters(self, max_cluster_size: int = 6) -> List[Set[str]]:
        """Find clusters of related terms based on graph relationships."""
        clusters = []
        used_terms = set()
        
        # Get connectivity for each term
        connectivity = {}
        for term in self.vocabulary:
            related = self.term_relationships.get(term, set())
            # Only count relationships with terms in our vocabulary
            vocab_related = related.intersection(set(self.vocabulary))
            connectivity[term] = len(vocab_related)
        
        # Sort by connectivity (most connected first)
        sorted_terms = sorted(self.vocabulary, key=lambda t: connectivity[t], reverse=True)
        
        for term in sorted_terms:
            if term in used_terms:
                continue
            
            # Start new cluster
            cluster = {term}
            related = self.term_relationships.get(term, set())
            vocab_related = related.intersection(set(self.vocabulary))
            
            # Add related terms up to max size
            for related_term in vocab_related:
                if related_term not in used_terms and len(cluster) < max_cluster_size:
                    cluster.add(related_term)
            
            clusters.append(cluster)
            used_terms.update(cluster)
        
        # Add remaining terms as singleton clusters
        for term in self.vocabulary:
            if term not in used_terms:
                clusters.append({term})
        
        return clusters
    
    def create_manual_sentence_templates(self) -> List[Tuple[str, Set[str]]]:
        """Create manual sentence templates for common term combinations."""
        templates = []
        
        # Hardware sentence
        hardware_terms = {'computer', 'hardware', 'processor cpu', 'ram random access memory', 'storage'}
        available_hardware = hardware_terms.intersection(set(self.vocabulary))
        if len(available_hardware) >= 2:
            templates.append((
                "A computer's hardware includes the processor (CPU), RAM for temporary storage, and various storage devices.",
                available_hardware
            ))
        
        # Software sentence
        software_terms = {'software', 'application software', 'operating system os', 'programming'}
        available_software = software_terms.intersection(set(self.vocabulary))
        if len(available_software) >= 2:
            templates.append((
                "Software includes the operating system (OS), application software, and programming tools.",
                available_software
            ))
        
        # Internet sentence
        internet_terms = {'internet', 'world wide web web', 'web browser', 'url uniform resource locator', 'http hypertext transfer protocol'}
        available_internet = internet_terms.intersection(set(self.vocabulary))
        if len(available_internet) >= 2:
            templates.append((
                "The Internet enables the World Wide Web, where web browsers use HTTP to access URLs.",
                available_internet
            ))
        
        # Security sentence
        security_terms = {'cybersecurity', 'password', 'encryption', 'firewall', 'malware', 'virus'}
        available_security = security_terms.intersection(set(self.vocabulary))
        if len(available_security) >= 2:
            templates.append((
                "Cybersecurity involves using passwords, encryption, and firewalls to protect against malware and viruses.",
                available_security
            ))
        
        return templates
    
    def analyze_vocabulary(self):
        """Perform comprehensive vocabulary analysis."""
        print(f"📚 Vocabulary Analysis")
        print("=" * 50)
        print(f"Total terms: {len(self.vocabulary)}")
        
        # Categories
        categories = self.analyze_vocabulary_categories()
        print(f"\n🏷️  Term Categories:")
        for category, terms in categories.items():
            if terms:
                print(f"   {category.replace('_', ' ').title()}: {len(terms)} terms")
                print(f"      Sample: {', '.join(terms[:3])}{'...' if len(terms) > 3 else ''}")
        
        # Relationships
        print(f"\n🔗 Relationship Analysis:")
        relationship_counts = [len(self.term_relationships.get(term, set())) for term in self.vocabulary]
        if relationship_counts:
            avg_connections = sum(relationship_counts) / len(relationship_counts)
            max_connections = max(relationship_counts)
            print(f"   Average connections per term: {avg_connections:.1f}")
            print(f"   Most connected term has: {max_connections} connections")
            
            # Find most connected terms
            most_connected = sorted(self.vocabulary, 
                                  key=lambda t: len(self.term_relationships.get(t, set())), 
                                  reverse=True)[:5]
            print(f"   Most connected terms: {', '.join(most_connected)}")
        
        # Clustering analysis
        clusters = self.find_term_clusters()
        print(f"\n🧩 Clustering Analysis:")
        print(f"   Found {len(clusters)} potential clusters")
        cluster_sizes = [len(c) for c in clusters]
        print(f"   Cluster sizes: min={min(cluster_sizes)}, max={max(cluster_sizes)}, avg={sum(cluster_sizes)/len(cluster_sizes):.1f}")
        
        # Estimate sentence count
        estimated_sentences = len([c for c in clusters if len(c) > 1]) + len([c for c in clusters if len(c) == 1])
        print(f"   Estimated sentences needed: {estimated_sentences}")
        
        # Show sample clusters
        print(f"\n📝 Sample Term Clusters:")
        large_clusters = [c for c in clusters if len(c) > 2][:5]
        for i, cluster in enumerate(large_clusters, 1):
            print(f"   {i}. {', '.join(sorted(cluster))}")
        
        return {
            'total_terms': len(self.vocabulary),
            'categories': categories,
            'clusters': clusters,
            'estimated_sentences': estimated_sentences
        }

def main():
    """Main function to analyze vocabulary."""
    print("🎯 Vocabulary Analysis for Sentence Coverage")
    print("=" * 60)
    
    wiki_dir = "wiki"
    if not os.path.exists(wiki_dir):
        print(f"❌ Wiki directory not found: {wiki_dir}")
        return
    
    analyzer = VocabularyAnalyzer(wiki_dir)
    results = analyzer.analyze_vocabulary()
    
    print(f"\n🎯 Summary:")
    print(f"   {results['total_terms']} vocabulary terms")
    print(f"   ~{results['estimated_sentences']} sentences estimated")
    print(f"   {len(results['clusters'])} term clusters identified")

if __name__ == "__main__":
    main()
