#!/usr/bin/env python3
"""
🎯 Random Graph Path Sentence Generator
=====================================
Generates random "sentences" by following graph paths from random starting nodes.
"""

import json
import os
import random
from collections import deque
from typing import List, Set, Dict, Tuple

class RandomPathGenerator:
    def __init__(self, wiki_dir: str):
        """Initialize with vocabulary graph."""
        self.wiki_dir = wiki_dir
        self.graph_data = self._load_graph()
        self.id_to_word = {}
        self.word_to_id = {}
        self.adjacency_list = {}
        self._build_graph_structures()
        
    def _load_graph(self) -> Dict:
        """Load the vocabulary relationship graph."""
        try:
            with open(os.path.join(self.wiki_dir, 'graph.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"nodes": {"id_to_word": {}}, "edges": []}
    
    def _build_graph_structures(self):
        """Build convenient graph structures for path finding."""
        if "nodes" not in self.graph_data or "id_to_word" not in self.graph_data["nodes"]:
            print("❌ Invalid graph structure")
            return
        
        # Build ID to word mapping
        self.id_to_word = self.graph_data["nodes"]["id_to_word"]
        self.word_to_id = {word: node_id for node_id, word in self.id_to_word.items()}
        
        # Build adjacency list
        self.adjacency_list = {node_id: [] for node_id in self.id_to_word.keys()}
        
        if "edges" in self.graph_data:
            for edge in self.graph_data["edges"]:
                if len(edge) >= 2:
                    source_id = str(edge[0])
                    target_id = str(edge[1])
                    
                    if source_id in self.adjacency_list and target_id in self.adjacency_list:
                        self.adjacency_list[source_id].append(target_id)
                        # Add reverse edge for undirected traversal
                        self.adjacency_list[target_id].append(source_id)
        
        print(f"📊 Graph loaded: {len(self.id_to_word)} nodes, {sum(len(adj) for adj in self.adjacency_list.values())//2} edges")
    
    def find_paths_bfs(self, start_node_id: str, path_length: int, max_paths: int = 100) -> List[List[str]]:
        """Find unique paths of specified length using BFS from start node."""
        if start_node_id not in self.adjacency_list:
            return []
        
        paths = []
        queue = deque([(start_node_id, [start_node_id])])  # (current_node, path_so_far)
        visited_paths = set()
        
        while queue and len(paths) < max_paths:
            current_node, path = queue.popleft()
            
            # If we've reached the desired path length
            if len(path) == path_length:
                path_tuple = tuple(path)
                if path_tuple not in visited_paths:
                    visited_paths.add(path_tuple)
                    paths.append(path[:])  # Copy the path
                continue
            
            # If path is not yet full, explore neighbors
            if len(path) < path_length:
                for neighbor_id in self.adjacency_list[current_node]:
                    # Avoid immediate backtracking (but allow revisiting nodes later in path)
                    if len(path) < 2 or neighbor_id != path[-2]:
                        new_path = path + [neighbor_id]
                        queue.append((neighbor_id, new_path))
        
        return paths
    
    def generate_random_path_sentences(self, num_sentences: int, path_length: int) -> List[str]:
        """Generate random path sentences."""
        print(f"🎲 Generating {num_sentences} random path sentences of length {path_length}")
        
        sentences = []
        node_ids = list(self.id_to_word.keys())
        
        attempts = 0
        max_attempts = num_sentences * 10  # Prevent infinite loops
        
        while len(sentences) < num_sentences and attempts < max_attempts:
            attempts += 1
            
            # Pick random starting node
            start_node = random.choice(node_ids)
            
            # Find paths from this node
            paths = self.find_paths_bfs(start_node, path_length, max_paths=20)
            
            if paths:
                # Pick a random path from the found paths
                chosen_path = random.choice(paths)
                
                # Convert node IDs to words
                words = [self.id_to_word[node_id] for node_id in chosen_path]
                
                # Create a "sentence" by joining the words
                sentence = " ".join(words) + "."
                
                # Avoid duplicates
                if sentence not in sentences:
                    sentences.append(sentence)
                    print(f"   {len(sentences):2d}. {sentence}")
        
        if len(sentences) < num_sentences:
            print(f"⚠️  Only generated {len(sentences)} sentences (attempted {attempts} times)")
        
        return sentences
    
    def save_sentences(self, sentences: List[str], filename: str):
        """Save sentences to file."""
        output_path = os.path.join("coverage-documents", filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"🎲 Random Graph Path Sentences\n")
            f.write("=" * 40 + "\n")
            f.write(f"Generated: {len(sentences)} sentences using BFS paths of length {len(sentences[0].split()) - 1 if sentences else 0}\n")
            f.write(f"Method: Breadth-first search from random starting nodes\n\n")
            
            for i, sentence in enumerate(sentences, 1):
                f.write(f"{i:2d}. {sentence}\n")
        
        print(f"📁 Sentences saved to: {output_path}")
        return output_path

def main():
    """Generate random path sentences."""
    print("🎲 Random Graph Path Sentence Generator")
    print("=" * 50)
    
    wiki_dir = "wiki"
    if not os.path.exists(wiki_dir):
        print(f"❌ Wiki directory not found: {wiki_dir}")
        return
    
    # Ensure coverage-documents directory exists
    os.makedirs("coverage-documents", exist_ok=True)
    
    generator = RandomPathGenerator(wiki_dir)
    
    # Generate 50 sentences with paths of length 5
    sentences = generator.generate_random_path_sentences(num_sentences=50, path_length=5)
    
    # Save to file
    filename = "random-path-50-5-sentences.txt"
    output_path = generator.save_sentences(sentences, filename)
    
    print(f"\n🎉 Generated {len(sentences)} random path sentences!")
    print(f"📁 Saved to: {output_path}")
    
    # Also assess them immediately
    print(f"\n📊 Running assessment on generated sentences...")
    
    import subprocess
    import sys
    
    try:
        result = subprocess.run([
            sys.executable, 
            "scripts/assess-sentence-coverage.py", 
            output_path
        ], capture_output=True, text=True, cwd=".")
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"⚠️  Could not run assessment: {e}")

if __name__ == "__main__":
    main()
