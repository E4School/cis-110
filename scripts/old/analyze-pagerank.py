#!/usr/bin/env python3
"""
Wiki PageRank Analyzer for CIS 110

This script loads the mention graph and runs PageRank algorithm to find
the most "important" vocabulary terms based on how they're referenced.

Usage: python analyze-pagerank.py
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict


class WikiPageRankAnalyzer:
    def __init__(self, graph_file: Path):
        """
        Initialize analyzer with graph data.
        
        Args:
            graph_file: Path to graph.json file
        """
        print(f"📊 Loading graph from {graph_file}...")
        with open(graph_file, 'r', encoding='utf-8') as f:
            self.graph_data = json.load(f)
        
        self.id_to_word = {int(k): v for k, v in self.graph_data['nodes']['id_to_word'].items()}
        self.word_to_id = {v: int(k) for k, v in self.graph_data['nodes']['id_to_word'].items()}
        self.edges = self.graph_data['edges']
        self.num_nodes = len(self.id_to_word)
        
        print(f"   Loaded {self.num_nodes} nodes and {len(self.edges)} edges")
        
    def build_adjacency_matrix(self) -> np.ndarray:
        """
        Build adjacency matrix from edge list.
        
        Returns:
            np.ndarray: Adjacency matrix (row = source, col = target)
        """
        print("🔗 Building adjacency matrix...")
        matrix = np.zeros((self.num_nodes, self.num_nodes))
        
        for source_id, target_id in self.edges:
            matrix[source_id, target_id] = 1
        
        return matrix
    
    def compute_pagerank(self, damping_factor: float = 0.85, max_iterations: int = 100, 
                        tolerance: float = 1e-6) -> np.ndarray:
        """
        Compute PageRank scores using power iteration.
        
        Args:
            damping_factor: Probability of following links (vs random jump)
            max_iterations: Maximum number of iterations
            tolerance: Convergence tolerance
            
        Returns:
            np.ndarray: PageRank scores for each node
        """
        print(f"⚡ Computing PageRank (d={damping_factor})...")
        
        # Build transition matrix
        adj_matrix = self.build_adjacency_matrix()
        
        # Create transition matrix (column-stochastic)
        # Each column sums to 1 (outgoing probabilities from each node)
        transition_matrix = np.zeros_like(adj_matrix, dtype=float)
        
        for i in range(self.num_nodes):
            out_degree = np.sum(adj_matrix[i, :])
            if out_degree > 0:
                # Normalize outgoing edges
                transition_matrix[i, :] = adj_matrix[i, :] / out_degree
            else:
                # If no outgoing edges, uniform distribution
                transition_matrix[i, :] = 1.0 / self.num_nodes
        
        # Transpose to get column-stochastic matrix (for matrix multiplication)
        transition_matrix = transition_matrix.T
        
        # Initialize PageRank vector
        pagerank = np.ones(self.num_nodes) / self.num_nodes
        
        # Power iteration
        for iteration in range(max_iterations):
            prev_pagerank = pagerank.copy()
            
            # PageRank update formula
            pagerank = (damping_factor * transition_matrix @ pagerank + 
                       (1 - damping_factor) / self.num_nodes * np.ones(self.num_nodes))
            
            # Check convergence
            diff = np.linalg.norm(pagerank - prev_pagerank, 1)
            if diff < tolerance:
                print(f"   Converged after {iteration + 1} iterations (diff={diff:.2e})")
                break
        else:
            print(f"   Reached max iterations ({max_iterations})")
        
        return pagerank
    
    def get_top_terms(self, scores: np.ndarray, top_k: int = 20) -> List[Tuple[str, float]]:
        """
        Get top-k terms by score.
        
        Args:
            scores: Array of scores for each node
            top_k: Number of top terms to return
            
        Returns:
            List of (term, score) tuples, sorted by score descending
        """
        term_scores = [(self.id_to_word[i], scores[i]) for i in range(self.num_nodes)]
        return sorted(term_scores, key=lambda x: x[1], reverse=True)[:top_k]
    
    def analyze_centrality_measures(self) -> Dict:
        """
        Compute various centrality measures.
        
        Returns:
            Dict: Different centrality rankings
        """
        print("📈 Computing centrality measures...")
        
        # Build adjacency matrix
        adj_matrix = self.build_adjacency_matrix()
        
        # In-degree centrality (how many terms point to this term)
        in_degree = np.sum(adj_matrix, axis=0)
        in_degree_norm = in_degree / np.max(in_degree) if np.max(in_degree) > 0 else in_degree
        
        # Out-degree centrality (how many terms this term points to)
        out_degree = np.sum(adj_matrix, axis=1)
        out_degree_norm = out_degree / np.max(out_degree) if np.max(out_degree) > 0 else out_degree
        
        # PageRank
        pagerank_scores = self.compute_pagerank()
        
        return {
            'pagerank': self.get_top_terms(pagerank_scores, 20),
            'in_degree': self.get_top_terms(in_degree_norm, 20),
            'out_degree': self.get_top_terms(out_degree_norm, 20),
            'raw_scores': {
                'pagerank': pagerank_scores,
                'in_degree': in_degree,
                'out_degree': out_degree
            }
        }
    
    def find_authority_hub_terms(self, centrality_results: Dict) -> Dict:
        """
        Identify authority terms (high in-degree) and hub terms (high out-degree).
        
        Args:
            centrality_results: Results from analyze_centrality_measures
            
        Returns:
            Dict: Authority and hub classifications
        """
        in_degree_scores = centrality_results['raw_scores']['in_degree']
        out_degree_scores = centrality_results['raw_scores']['out_degree']
        
        # Thresholds for classification (top quartile)
        in_degree_threshold = np.percentile(in_degree_scores, 75)
        out_degree_threshold = np.percentile(out_degree_scores, 75)
        
        authorities = []  # High in-degree, low out-degree
        hubs = []        # High out-degree, low in-degree
        connectors = []  # High both in-degree and out-degree
        isolated = []    # Low both in-degree and out-degree
        
        for i in range(self.num_nodes):
            term = self.id_to_word[i]
            in_deg = in_degree_scores[i]
            out_deg = out_degree_scores[i]
            
            high_in = in_deg >= in_degree_threshold
            high_out = out_deg >= out_degree_threshold
            
            if high_in and high_out:
                connectors.append((term, in_deg, out_deg))
            elif high_in and not high_out:
                authorities.append((term, in_deg, out_deg))
            elif not high_in and high_out:
                hubs.append((term, in_deg, out_deg))
            elif in_deg == 0 and out_deg == 0:
                isolated.append((term, in_deg, out_deg))
        
        return {
            'authorities': sorted(authorities, key=lambda x: x[1], reverse=True)[:10],
            'hubs': sorted(hubs, key=lambda x: x[2], reverse=True)[:10],
            'connectors': sorted(connectors, key=lambda x: x[1] + x[2], reverse=True)[:10],
            'isolated': isolated[:10]
        }
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive analysis report.
        
        Returns:
            str: Formatted report text
        """
        centrality_results = self.analyze_centrality_measures()
        authority_hub_results = self.find_authority_hub_terms(centrality_results)
        
        report = []
        report.append("🏆 WIKI VOCABULARY PAGERANK ANALYSIS")
        report.append("=" * 50)
        
        # Graph overview
        stats = self.graph_data.get('statistics', {})
        report.append(f"📊 Graph Overview:")
        report.append(f"   Nodes: {stats.get('num_nodes', 'N/A')}")
        report.append(f"   Edges: {stats.get('num_edges', 'N/A')}")
        report.append(f"   Density: {stats.get('density', 0):.4f}")
        report.append("")
        
        # PageRank results
        report.append("🥇 TOP TERMS BY PAGERANK:")
        report.append("   (Most 'important' terms based on reference network)")
        for i, (term, score) in enumerate(centrality_results['pagerank'][:10], 1):
            report.append(f"   {i:2d}. {term:<25} ({score:.4f})")
        report.append("")
        
        # Most referenced terms (authorities)
        report.append("📚 AUTHORITY TERMS:")
        report.append("   (Most referenced by other terms)")
        for i, (term, in_deg, out_deg) in enumerate(authority_hub_results['authorities'][:10], 1):
            report.append(f"   {i:2d}. {term:<25} (referenced {int(in_deg)} times)")
        report.append("")
        
        # Hub terms
        report.append("🔗 HUB TERMS:")
        report.append("   (Reference many other terms)")
        for i, (term, in_deg, out_deg) in enumerate(authority_hub_results['hubs'][:10], 1):
            report.append(f"   {i:2d}. {term:<25} (references {int(out_deg)} terms)")
        report.append("")
        
        # Connector terms
        if authority_hub_results['connectors']:
            report.append("🌐 CONNECTOR TERMS:")
            report.append("   (Both reference and are referenced heavily)")
            for i, (term, in_deg, out_deg) in enumerate(authority_hub_results['connectors'][:5], 1):
                report.append(f"   {i:2d}. {term:<25} (in:{int(in_deg)}, out:{int(out_deg)})")
            report.append("")
        
        # Isolated terms
        if authority_hub_results['isolated']:
            report.append("🏝️  ISOLATED TERMS:")
            report.append("   (No connections to other terms)")
            isolated_terms = [term for term, _, _ in authority_hub_results['isolated']]
            report.append(f"   {', '.join(isolated_terms[:10])}")
            if len(authority_hub_results['isolated']) > 10:
                report.append(f"   ... and {len(authority_hub_results['isolated']) - 10} more")
            report.append("")
        
        return "\n".join(report)


def main():
    """Main function to analyze PageRank."""
    
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    wiki_dir = project_dir / 'wiki'
    graph_file = wiki_dir / 'graph.json'
    
    if not graph_file.exists():
        print("❌ Graph file not found! Run build-mention-graph.py first.")
        return
    
    print("📊 Wiki PageRank Analyzer")
    print("=" * 30)
    
    # Analyze the graph
    analyzer = WikiPageRankAnalyzer(graph_file)
    report = analyzer.generate_report()
    
    # Print report
    print("\n" + report)
    
    # Save report to file
    report_file = wiki_dir / 'pagerank-analysis.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📁 Full report saved to: {report_file}")


if __name__ == "__main__":
    main()
