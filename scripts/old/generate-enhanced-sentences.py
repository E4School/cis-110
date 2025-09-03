#!/usr/bin/env python3
"""
🎯 Enhanced Sentence Coverage Generator
=====================================
Generates improved sentences with better naturalness and variety.
"""

import json
import os
from typing import List, Set, Dict, Tuple
from collections import defaultdict
import random

class EnhancedSentenceGenerator:
    def __init__(self, wiki_dir: str):
        """Initialize with vocabulary and relationships."""
        self.wiki_dir = wiki_dir
        self.vocabulary = self._load_vocabulary()
        self.graph_data = self._load_graph()
        self.relationships = self._extract_relationships()
        
        # Sentence starters for variety
        self.sentence_starters = [
            "Modern computing relies on",
            "Digital systems utilize", 
            "Technology professionals work with",
            "Computer science encompasses",
            "Information systems feature",
            "Software development involves",
            "Cybersecurity specialists focus on",
            "Data management requires",
            "Network administrators handle",
            "Web developers create",
            "System administrators maintain",
            "Database designers implement",
            "Mobile applications incorporate",
            "Cloud computing platforms provide",
            "Artificial intelligence systems use",
        ]
        
        # Context-specific templates
        self.context_templates = {
            'security': [
                "Cybersecurity professionals use {terms} to protect digital assets.",
                "Security systems implement {terms} for comprehensive protection.",
                "Modern security frameworks incorporate {terms} as essential components."
            ],
            'data': [
                "Data scientists work with {terms} to extract meaningful insights.",
                "Information systems manage {terms} through sophisticated processes.",
                "Database administrators utilize {terms} for efficient data handling."
            ],
            'network': [
                "Network engineers configure {terms} to ensure reliable connectivity.",
                "Internet infrastructure depends on {terms} for seamless communication.",
                "Communication protocols utilize {terms} to facilitate data exchange."
            ],
            'software': [
                "Software developers implement {terms} to create robust applications.",
                "Programming languages provide {terms} as fundamental building blocks.",
                "Application frameworks incorporate {terms} for enhanced functionality."
            ],
            'hardware': [
                "Computer systems integrate {terms} to deliver processing capabilities.",
                "Hardware components include {terms} as essential elements.",
                "Computing devices utilize {terms} for optimal performance."
            ]
        }
    
    def _load_vocabulary(self) -> List[str]:
        """Load vocabulary terms."""
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
        """Extract term relationships."""
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
    
    def categorize_term(self, term: str) -> str:
        """Categorize a term by its domain."""
        term_lower = term.lower()
        
        if any(keyword in term_lower for keyword in ['security', 'cyber', 'password', 'encryption', 'firewall', 'virus', 'malware', 'privacy']):
            return 'security'
        elif any(keyword in term_lower for keyword in ['data', 'database', 'information', 'file', 'storage', 'backup']):
            return 'data'
        elif any(keyword in term_lower for keyword in ['internet', 'web', 'network', 'http', 'url', 'browser', 'email', 'wifi']):
            return 'network'
        elif any(keyword in term_lower for keyword in ['software', 'application', 'program', 'code', 'programming', 'algorithm']):
            return 'software'
        elif any(keyword in term_lower for keyword in ['hardware', 'cpu', 'ram', 'rom', 'processor', 'device', 'computer']):
            return 'hardware'
        else:
            return 'general'
    
    def find_enhanced_clusters(self, max_cluster_size: int = 5) -> List[Tuple[Set[str], str]]:
        """Find clusters with category information."""
        clusters = []
        remaining_terms = set(self.vocabulary)
        
        # Hand-crafted high-quality clusters
        quality_clusters = [
            ({"computer", "hardware", "software", "operating system os"}, "hardware", 
             "A computer combines hardware and software components managed by an operating system (OS)."),
            
            ({"internet", "world wide web web", "web browser", "url uniform resource locator", "http hypertext transfer protocol"}, "network",
             "The Internet enables the World Wide Web, where web browsers use HTTP protocols to access URLs."),
            
            ({"data", "database", "file", "storage", "backup"}, "data",
             "Data management involves organizing information in databases and files, with storage systems and backup procedures."),
            
            ({"cybersecurity", "password", "encryption", "firewall", "malware", "virus"}, "security",
             "Cybersecurity professionals use passwords, encryption, and firewalls to defend against malware and viruses."),
            
            ({"programming", "code", "algorithm", "function", "variable", "debugging"}, "software",
             "Programming involves writing code with algorithms, functions, and variables, then debugging to resolve issues."),
            
            ({"email", "instant messaging", "social media", "video conferencing", "netiquette"}, "network",
             "Digital communication encompasses email, instant messaging, social media, and video conferencing, all requiring proper netiquette."),
            
            ({"analytics", "big data", "data mining", "machine learning", "artificial intelligence ai"}, "data",
             "Advanced analytics processes big data through data mining and machine learning algorithms in artificial intelligence (AI) systems."),
        ]
        
        for cluster_terms, category, sentence in quality_clusters:
            available_terms = cluster_terms.intersection(remaining_terms)
            if len(available_terms) >= 3:
                clusters.append((available_terms, category, sentence))
                remaining_terms -= available_terms
        
        # For remaining terms, create relationship-based clusters
        while remaining_terms:
            # Find most connected term
            best_term = max(remaining_terms, 
                          key=lambda t: len(self.relationships.get(t, set()).intersection(remaining_terms)))
            
            # Build cluster
            cluster = {best_term}
            category = self.categorize_term(best_term)
            related = self.relationships.get(best_term, set())
            
            # Add related terms from same category when possible
            for related_term in related:
                if (related_term in remaining_terms and 
                    len(cluster) < max_cluster_size and
                    (self.categorize_term(related_term) == category or len(cluster) < 3)):
                    cluster.add(related_term)
            
            clusters.append((cluster, category, None))
            remaining_terms -= cluster
        
        return clusters
    
    def generate_enhanced_sentence(self, cluster: Set[str], category: str, template_sentence: str = None) -> str:
        """Generate an enhanced sentence with better naturalness."""
        terms = sorted(list(cluster))
        
        if template_sentence:
            return template_sentence
        
        # Use context-specific templates
        if category in self.context_templates:
            template = random.choice(self.context_templates[category])
            if len(terms) <= 3:
                terms_str = ", ".join(terms[:-1]) + f", and {terms[-1]}" if len(terms) > 1 else terms[0]
            else:
                mid = len(terms) // 2
                terms_str = f"{', '.join(terms[:mid])}, and {', '.join(terms[mid:])}"
            
            return template.format(terms=terms_str)
        
        # Fallback with varied starters
        if len(terms) == 1:
            starters = [
                f"The concept of {terms[0]} is fundamental in computing.",
                f"Understanding {terms[0]} helps students grasp digital systems.",
                f"Modern technology relies on {terms[0]} for essential functionality.",
                f"Computer science students learn about {terms[0]} as a core topic.",
                f"Information systems incorporate {terms[0]} as a key component."
            ]
            return random.choice(starters)
        
        elif len(terms) == 2:
            starters = [
                f"The relationship between {terms[0]} and {terms[1]} illustrates key computing principles.",
                f"Computer systems integrate {terms[0]} with {terms[1]} for enhanced capabilities.",
                f"Students explore how {terms[0]} and {terms[1]} work together in digital environments."
            ]
            return random.choice(starters)
        
        else:
            starter = random.choice(self.sentence_starters)
            if len(terms) <= 4:
                terms_str = ", ".join(terms[:-1]) + f", and {terms[-1]}"
            else:
                mid = len(terms) // 2
                terms_str = f"{', '.join(terms[:mid])}, along with {', '.join(terms[mid:])}"
            
            return f"{starter} {terms_str} as essential components."
    
    def generate_enhanced_sentences(self) -> List[str]:
        """Generate enhanced sentences with better quality."""
        print("🎯 Generating Enhanced Vocabulary Coverage Sentences")
        print("=" * 60)
        
        clusters = self.find_enhanced_clusters()
        sentences = []
        
        print(f"📊 Generated {len(clusters)} clusters")
        print("\n✍️  Creating enhanced sentences:")
        
        for i, (cluster, category, template) in enumerate(clusters, 1):
            sentence = self.generate_enhanced_sentence(cluster, category, template)
            sentences.append(sentence)
            
            terms_str = ', '.join(sorted(cluster))
            print(f"   {i:3d}. [{category}] {terms_str}")
            print(f"        → {sentence}")
            print()
        
        return sentences
    
    def save_enhanced_results(self, sentences: List[str], output_file: str):
        """Save enhanced results."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("🎯 Enhanced Vocabulary Coverage Sentences\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {len(sentences)} high-quality sentences covering {len(self.vocabulary)} vocabulary terms\n\n")
            
            for i, sentence in enumerate(sentences, 1):
                f.write(f"{i:3d}. {sentence}\n")

def main():
    """Generate enhanced sentences."""
    print("🎯 Enhanced Sentence Coverage Generator")
    print("=" * 50)
    
    wiki_dir = "wiki"
    generator = EnhancedSentenceGenerator(wiki_dir)
    sentences = generator.generate_enhanced_sentences()
    
    # Save results
    output_file = os.path.join(wiki_dir, "enhanced-coverage-sentences.txt")
    generator.save_enhanced_results(sentences, output_file)
    
    print(f"\n🎉 Generated {len(sentences)} enhanced coverage sentences!")
    print(f"📁 Results saved to: {output_file}")

if __name__ == "__main__":
    main()
