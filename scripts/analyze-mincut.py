#!/usr/bin/env python3
"""
Wiki Min-Cut Analyzer for CIS 110

This script analyzes minimum cuts in the vocabulary mention graph to identify
critical terms that connect different conceptual areas.

Usage: python analyze-mincut.py
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict, deque
import heapq


class WikiMinCutAnalyzer:
    def __init__(self, graph_file: Path):
        """Initialize analyzer with graph data."""
        print(f"📊 Loading graph from {graph_file}...")
        with open(graph_file, 'r', encoding='utf-8') as f:
            self.graph_data = json.load(f)
        
        self.id_to_word = {int(k): v for k, v in self.graph_data['nodes']['id_to_word'].items()}
        self.word_to_id = {v: int(k) for k, v in self.graph_data['nodes']['id_to_word'].items()}
        self.edges = self.graph_data['edges']
        self.num_nodes = len(self.id_to_word)
        
        # Build adjacency representation
        self.graph = defaultdict(list)
        self.capacity = defaultdict(int)
        
        for source_id, target_id in self.edges:
            self.graph[source_id].append(target_id)
            self.capacity[(source_id, target_id)] += 1
        
        print(f"   Loaded {self.num_nodes} nodes and {len(self.edges)} edges")
    
    def bfs_find_path(self, source: int, sink: int, parent: Dict[int, int]) -> bool:
        """
        BFS to find augmenting path in residual graph.
        
        Args:
            source: Source node
            sink: Sink node  
            parent: Dictionary to store path
            
        Returns:
            bool: True if path exists
        """
        visited = set([source])
        queue = deque([source])
        
        while queue:
            u = queue.popleft()
            
            for v in self.graph[u]:
                if v not in visited and self.capacity[(u, v)] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False
    
    def max_flow_min_cut(self, source: int, sink: int) -> Tuple[int, Set[int], Set[int]]:
        """
        Compute maximum flow and minimum cut using Ford-Fulkerson.
        
        Args:
            source: Source node
            sink: Sink node
            
        Returns:
            Tuple of (max_flow_value, source_partition, sink_partition)
        """
        # Create residual graph
        residual_capacity = self.capacity.copy()
        parent = {}
        max_flow_value = 0
        
        # Find augmenting paths
        while self.bfs_find_path(source, sink, parent):
            # Find minimum capacity along the path
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, residual_capacity[(parent[s], s)])
                s = parent[s]
            
            # Add path flow to overall flow
            max_flow_value += path_flow
            
            # Update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                residual_capacity[(u, v)] -= path_flow
                residual_capacity[(v, u)] += path_flow
                v = parent[v]
            
            parent = {}
        
        # Find minimum cut by doing BFS from source in residual graph
        self.capacity = residual_capacity  # Update for BFS
        visited = set()
        queue = deque([source])
        visited.add(source)
        
        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if v not in visited and self.capacity[(u, v)] > 0:
                    visited.add(v)
                    queue.append(v)
        
        source_partition = visited
        sink_partition = set(range(self.num_nodes)) - source_partition
        
        return max_flow_value, source_partition, sink_partition
    
    def find_articulation_points(self) -> Set[int]:
        """
        Find articulation points (nodes whose removal increases connected components).
        
        Returns:
            Set of articulation point node IDs
        """
        visited = [False] * self.num_nodes
        disc = [0] * self.num_nodes
        low = [0] * self.num_nodes
        parent = [-1] * self.num_nodes
        articulation_points = set()
        time = [0]  # Use list for mutable reference
        
        def bridge_util(u):
            children = 0
            visited[u] = True
            disc[u] = low[u] = time[0]
            time[0] += 1
            
            for v in self.graph[u]:
                if not visited[v]:
                    children += 1
                    parent[v] = u
                    bridge_util(v)
                    
                    low[u] = min(low[u], low[v])
                    
                    # Root of DFS tree is articulation point if it has more than 1 child
                    if parent[u] == -1 and children > 1:
                        articulation_points.add(u)
                    
                    # Non-root node is articulation point if removing it disconnects subtree
                    if parent[u] != -1 and low[v] >= disc[u]:
                        articulation_points.add(u)
                        
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])
        
        # Run DFS from each unvisited node
        for i in range(self.num_nodes):
            if not visited[i]:
                bridge_util(i)
        
        return articulation_points
    
    def analyze_critical_terms(self) -> Dict:
        """
        Analyze which terms are critical for graph connectivity.
        
        Returns:
            Dict with analysis results
        """
        print("🔍 Finding articulation points...")
        articulation_points = self.find_articulation_points()
        
        print("🎯 Analyzing high-centrality min-cuts...")
        # Get top terms by PageRank/centrality for min-cut analysis
        top_terms = ['data', 'information', 'software', 'computer', 'field', 'internet', 'code', 'programming']
        
        min_cut_results = []
        
        for i, term1 in enumerate(top_terms):
            for term2 in top_terms[i+1:]:
                if term1 in self.word_to_id and term2 in self.word_to_id:
                    source = self.word_to_id[term1]
                    sink = self.word_to_id[term2]
                    
                    try:
                        flow_value, source_partition, sink_partition = self.max_flow_min_cut(source, sink)
                        
                        # Find the actual cut edges
                        cut_edges = []
                        for u in source_partition:
                            for v in sink_partition:
                                if v in self.graph[u]:
                                    cut_edges.append((self.id_to_word[u], self.id_to_word[v]))
                        
                        min_cut_results.append({
                            'source_term': term1,
                            'sink_term': term2,
                            'cut_value': flow_value,
                            'cut_edges': cut_edges,
                            'source_partition_size': len(source_partition),
                            'sink_partition_size': len(sink_partition)
                        })
                    except Exception as e:
                        print(f"   Error analyzing {term1} -> {term2}: {e}")
        
        return {
            'articulation_points': [self.id_to_word[node] for node in articulation_points],
            'min_cuts': sorted(min_cut_results, key=lambda x: x['cut_value'])[:10],
            'total_articulation_points': len(articulation_points)
        }
    
    def identify_conceptual_domains(self, results: Dict) -> Dict:
        """
        Identify conceptual domains based on min-cut analysis.
        
        Args:
            results: Results from analyze_critical_terms
            
        Returns:
            Dict with domain analysis
        """
        print("🧩 Identifying conceptual domains...")
        
        # Analyze partition patterns from min-cuts
        domain_indicators = defaultdict(list)
        
        for cut in results['min_cuts'][:5]:  # Use top 5 cuts
            source_term = cut['source_term']
            sink_term = cut['sink_term']
            cut_edges = cut['cut_edges']
            
            # Categorize cut edges by likely domains
            for source_edge, target_edge in cut_edges:
                # Simple domain classification based on term characteristics
                if any(keyword in source_edge.lower() for keyword in ['hardware', 'cpu', 'memory', 'storage', 'device']):
                    domain_indicators['hardware'].append(source_edge)
                elif any(keyword in source_edge.lower() for keyword in ['software', 'program', 'application', 'code']):
                    domain_indicators['software'].append(source_edge)
                elif any(keyword in source_edge.lower() for keyword in ['network', 'internet', 'web', 'protocol']):
                    domain_indicators['networking'].append(source_edge)
                elif any(keyword in source_edge.lower() for keyword in ['data', 'information', 'database', 'analytics']):
                    domain_indicators['data_management'].append(source_edge)
                elif any(keyword in source_edge.lower() for keyword in ['security', 'privacy', 'encryption', 'malware']):
                    domain_indicators['security'].append(source_edge)
        
        return dict(domain_indicators)
    
    def generate_report(self) -> str:
        """Generate comprehensive min-cut analysis report."""
        results = self.analyze_critical_terms()
        domains = self.identify_conceptual_domains(results)
        
        report = []
        report.append("🔪 WIKI VOCABULARY MIN-CUT ANALYSIS")
        report.append("=" * 50)
        
        # Graph overview
        stats = self.graph_data.get('statistics', {})
        report.append(f"📊 Graph Overview:")
        report.append(f"   Nodes: {self.num_nodes}")
        report.append(f"   Edges: {len(self.edges)}")
        report.append(f"   Density: {len(self.edges) / (self.num_nodes * (self.num_nodes - 1)):.4f}")
        report.append("")
        
        # Articulation points
        report.append("🎯 ARTICULATION POINTS:")
        report.append("   (Terms whose removal would fragment the graph)")
        if results['articulation_points']:
            for i, term in enumerate(results['articulation_points'][:15], 1):
                report.append(f"   {i:2d}. {term}")
        else:
            report.append("   No articulation points found (strongly connected)")
        report.append("")
        
        # Min-cut analysis
        report.append("✂️  MINIMUM CUTS (Between Important Terms):")
        report.append("   (Smallest number of connections to separate key concepts)")
        for i, cut in enumerate(results['min_cuts'][:8], 1):
            report.append(f"   {i}. {cut['source_term']} ↔ {cut['sink_term']}")
            report.append(f"      Cut value: {cut['cut_value']}")
            report.append(f"      Partitions: {cut['source_partition_size']} | {cut['sink_partition_size']} nodes")
            if cut['cut_edges']:
                report.append(f"      Key cut edges: {', '.join([f'{s}→{t}' for s, t in cut['cut_edges'][:3]])}")
            report.append("")
        
        # Conceptual domains
        report.append("🧩 CONCEPTUAL DOMAIN BRIDGES:")
        report.append("   (Terms that connect different CS domains)")
        for domain, terms in domains.items():
            if terms:
                unique_terms = list(set(terms))
                report.append(f"   {domain.replace('_', ' ').title()}: {', '.join(unique_terms[:5])}")
        report.append("")
        
        # Implications
        report.append("💡 EDUCATIONAL IMPLICATIONS:")
        report.append("   • Articulation points are critical foundational concepts")
        report.append("   • Low min-cut values indicate tightly coupled concept clusters")
        report.append("   • High cut values suggest independent conceptual domains")
        report.append("   • Bridge terms are essential for curriculum connectivity")
        
        return "\n".join(report)


def main():
    """Main function to analyze min-cuts."""
    
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    wiki_dir = project_dir / 'wiki'
    graph_file = wiki_dir / 'graph.json'
    
    if not graph_file.exists():
        print("❌ Graph file not found! Run build-mention-graph.py first.")
        return
    
    print("🔪 Wiki Min-Cut Analyzer")
    print("=" * 30)
    
    try:
        analyzer = WikiMinCutAnalyzer(graph_file)
        report = analyzer.generate_report()
        
        # Print report
        print("\n" + report)
        
        # Save report to file
        report_file = wiki_dir / 'mincut-analysis.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📁 Full report saved to: {report_file}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
