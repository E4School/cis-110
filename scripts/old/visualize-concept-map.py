#!/usr/bin/env python3
"""
Wiki Concept Territory Visualizer for CIS 110

This script creates an interactive visualization of the vocabulary mention graph,
showing conceptual relationships, PageRank importance, and domain clustering.

Requirements:
- pip install networkx matplotlib plotly pandas

Usage: python visualize-concept-map.py
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import colorsys

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import pandas as pd
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Visualization libraries not available. Install with:")
    print("pip install networkx matplotlib plotly pandas")


class ConceptTerritoryVisualizer:
    def __init__(self, graph_file: Path):
        """Initialize visualizer with graph data."""
        print(f"📊 Loading graph from {graph_file}...")
        with open(graph_file, 'r', encoding='utf-8') as f:
            self.graph_data = json.load(f)
        
        self.id_to_word = {int(k): v for k, v in self.graph_data['nodes']['id_to_word'].items()}
        self.word_to_id = {v: int(k) for k, v in self.graph_data['nodes']['id_to_word'].items()}
        self.edges = self.graph_data['edges']
        self.num_nodes = len(self.id_to_word)
        
        # Create NetworkX graph
        self.G = nx.DiGraph()
        
        # Add nodes
        for node_id, word in self.id_to_word.items():
            self.G.add_node(node_id, word=word)
        
        # Add edges
        for source_id, target_id in self.edges:
            if self.G.has_edge(source_id, target_id):
                self.G[source_id][target_id]['weight'] += 1
            else:
                self.G.add_edge(source_id, target_id, weight=1)
        
        print(f"   Created graph with {self.G.number_of_nodes()} nodes and {self.G.number_of_edges()} edges")
        
        # Compute metrics
        self.compute_graph_metrics()
        
    def compute_graph_metrics(self):
        """Compute various graph metrics for visualization."""
        print("📈 Computing graph metrics...")
        
        # PageRank
        self.pagerank = nx.pagerank(self.G)
        
        # Centrality measures
        self.degree_centrality = nx.degree_centrality(self.G)
        self.betweenness_centrality = nx.betweenness_centrality(self.G)
        self.closeness_centrality = nx.closeness_centrality(self.G)
        
        # Community detection
        # Convert to undirected for community detection
        G_undirected = self.G.to_undirected()
        self.communities = nx.community.greedy_modularity_communities(G_undirected)
        
        # Create community mapping
        self.node_to_community = {}
        for i, community in enumerate(self.communities):
            for node in community:
                self.node_to_community[node] = i
        
        print(f"   Found {len(self.communities)} conceptual communities")
    
    def categorize_terms(self) -> Dict[str, List[str]]:
        """Categorize terms into conceptual domains."""
        categories = {
            'Hardware': ['computer', 'processor', 'cpu', 'memory', 'ram', 'rom', 'storage', 'hardware', 'device', 'input device', 'output device'],
            'Software': ['software', 'program', 'application', 'code', 'programming', 'algorithm', 'function', 'variable', 'loop', 'conditional'],
            'Networks': ['internet', 'network', 'web', 'protocol', 'wifi', 'router', 'dns', 'http', 'https', 'url'],
            'Data': ['data', 'information', 'database', 'file', 'folder', 'analytics', 'big data', 'query', 'record', 'field'],
            'Security': ['cybersecurity', 'encryption', 'password', 'malware', 'virus', 'firewall', 'privacy', 'authentication'],
            'Web': ['web browser', 'website', 'html', 'css', 'javascript', 'web application', 'web server'],
            'Social': ['social media', 'social network', 'blog', 'email', 'instant messaging', 'collaboration tools'],
            'Systems': ['operating system', 'file system', 'backup', 'installation', 'troubleshooting', 'documentation']
        }
        
        # Create reverse mapping
        term_categories = {}
        for category, terms in categories.items():
            for term in terms:
                if term in self.word_to_id:
                    term_categories[term] = category
        
        return term_categories
    
    def create_interactive_network(self) -> go.Figure:
        """Create interactive network visualization using Plotly."""
        print("🎨 Creating interactive network visualization...")
        
        # Use spring layout for positioning
        pos = nx.spring_layout(self.G, k=3, iterations=50, seed=42)
        
        # Prepare node data
        node_trace = go.Scatter(
            x=[],
            y=[],
            mode='markers+text',
            text=[],
            textposition="middle center",
            textfont=dict(size=8),
            marker=dict(
                size=[],
                color=[],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="PageRank Score"),
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'PageRank: %{customdata[1]:.4f}<br>' +
                         'Community: %{customdata[2]}<br>' +
                         'Degree: %{customdata[3]}<extra></extra>',
            customdata=[]
        )
        
        # Prepare edge data
        edge_trace = go.Scatter(
            x=[],
            y=[],
            mode='lines',
            line=dict(width=0.5, color='rgba(125,125,125,0.3)'),
            hoverinfo='none'
        )
        
        # Add edges
        for edge in self.G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)
        
        # Add nodes
        term_categories = self.categorize_terms()
        
        for node in self.G.nodes():
            x, y = pos[node]
            word = self.id_to_word[node]
            pagerank_score = self.pagerank[node]
            community = self.node_to_community.get(node, 0)
            degree = self.G.degree(node)
            
            node_trace['x'] += (x,)
            node_trace['y'] += (y,)
            
            # Size based on PageRank
            size = 10 + 50 * pagerank_score
            node_trace['marker']['size'] += (size,)
            
            # Color based on PageRank
            node_trace['marker']['color'] += (pagerank_score,)
            
            # Show only important terms as text
            if pagerank_score > 0.01:  # Only show high PageRank terms
                node_trace['text'] += (word,)
            else:
                node_trace['text'] += ('',)
            
            # Custom data for hover
            category = term_categories.get(word, f'Community {community}')
            node_trace['customdata'] += ((word, pagerank_score, category, degree),)
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title=dict(
                               text='CIS 110 Vocabulary Concept Map<br><sub>Node size = PageRank importance, Color = PageRank score</sub>',
                               font=dict(size=16)
                           ),
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           annotations=[ dict(
                               text="Drag to pan, scroll to zoom. Hover for details.",
                               showarrow=False,
                               xref="paper", yref="paper",
                               x=0.005, y=-0.002,
                               xanchor='left', yanchor='bottom',
                               font=dict(color="#888888", size=12)
                           )],
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           width=1200,
                           height=800
                       ))
        
        return fig
    
    def create_community_analysis(self) -> go.Figure:
        """Create community analysis visualization."""
        print("🧩 Analyzing conceptual communities...")
        
        # Analyze communities
        community_data = []
        term_categories = self.categorize_terms()
        
        for i, community in enumerate(self.communities):
            community_words = [self.id_to_word[node] for node in community]
            total_pagerank = sum(self.pagerank[node] for node in community)
            avg_pagerank = total_pagerank / len(community)
            
            # Categorize community
            categories = defaultdict(int)
            for word in community_words:
                category = term_categories.get(word, 'Other')
                categories[category] += 1
            
            dominant_category = max(categories.items(), key=lambda x: x[1])[0] if categories else 'Other'
            
            community_data.append({
                'Community': f'Community {i+1}',
                'Size': len(community),
                'Total PageRank': total_pagerank,
                'Avg PageRank': avg_pagerank,
                'Dominant Category': dominant_category,
                'Top Terms': ', '.join(sorted(community_words, key=lambda w: self.pagerank[self.word_to_id[w]], reverse=True)[:5])
            })
        
        # Create subplot figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Community Sizes', 'Community PageRank Totals', 'Category Distribution', 'Top Communities by Importance'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "table"}]]
        )
        
        # Community sizes
        fig.add_trace(
            go.Bar(x=[d['Community'] for d in community_data],
                   y=[d['Size'] for d in community_data],
                   name='Size'),
            row=1, col=1
        )
        
        # Community PageRank
        fig.add_trace(
            go.Bar(x=[d['Community'] for d in community_data],
                   y=[d['Total PageRank'] for d in community_data],
                   name='PageRank'),
            row=1, col=2
        )
        
        # Category distribution
        category_counts = defaultdict(int)
        for d in community_data:
            category_counts[d['Dominant Category']] += 1
        
        fig.add_trace(
            go.Pie(labels=list(category_counts.keys()),
                   values=list(category_counts.values()),
                   name="Categories"),
            row=2, col=1
        )
        
        # Top communities table
        top_communities = sorted(community_data, key=lambda x: x['Total PageRank'], reverse=True)[:8]
        fig.add_trace(
            go.Table(
                header=dict(values=['Community', 'Size', 'Category', 'Top Terms'],
                           fill_color='lightblue'),
                cells=dict(values=[
                    [d['Community'] for d in top_communities],
                    [d['Size'] for d in top_communities],
                    [d['Dominant Category'] for d in top_communities],
                    [d['Top Terms'] for d in top_communities]
                ],
                fill_color='white')
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, title_text="Conceptual Community Analysis")
        return fig
    
    def create_centrality_comparison(self) -> go.Figure:
        """Create centrality measures comparison."""
        print("📊 Comparing centrality measures...")
        
        # Get top terms by different centrality measures
        top_n = 15
        
        pagerank_top = sorted(self.pagerank.items(), key=lambda x: x[1], reverse=True)[:top_n]
        degree_top = sorted(self.degree_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
        betweenness_top = sorted(self.betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
        closeness_top = sorted(self.closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        # Create comparison data
        measures = ['PageRank', 'Degree', 'Betweenness', 'Closeness']
        top_terms = [pagerank_top, degree_top, betweenness_top, closeness_top]
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=measures,
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        positions = [(1,1), (1,2), (2,1), (2,2)]
        
        for i, (measure, top_list) in enumerate(zip(measures, top_terms)):
            row, col = positions[i]
            
            terms = [self.id_to_word[node_id] for node_id, score in top_list]
            scores = [score for node_id, score in top_list]
            
            fig.add_trace(
                go.Bar(x=terms, y=scores, name=measure, showlegend=False),
                row=row, col=col
            )
            
            # Rotate x-axis labels
            fig.update_xaxes(tickangle=45, row=row, col=col)
        
        fig.update_layout(height=800, title_text="Centrality Measures Comparison")
        return fig
    
    def generate_insights(self) -> str:
        """Generate textual insights about the concept map."""
        insights = []
        insights.append("🗺️  CONCEPT MAP INSIGHTS")
        insights.append("=" * 40)
        
        # Top terms by PageRank
        top_pagerank = sorted(self.pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
        insights.append("🏆 Most Central Concepts (PageRank):")
        for i, (node_id, score) in enumerate(top_pagerank, 1):
            word = self.id_to_word[node_id]
            insights.append(f"   {i:2d}. {word:<20} ({score:.4f})")
        insights.append("")
        
        # Community analysis
        insights.append(f"🧩 Conceptual Communities: {len(self.communities)}")
        community_sizes = [len(community) for community in self.communities]
        insights.append(f"   Largest community: {max(community_sizes)} terms")
        insights.append(f"   Smallest community: {min(community_sizes)} terms")
        insights.append(f"   Average community size: {sum(community_sizes)/len(community_sizes):.1f}")
        insights.append("")
        
        # Network properties
        density = nx.density(self.G)
        avg_clustering = nx.average_clustering(self.G.to_undirected())
        
        insights.append("📈 Network Properties:")
        insights.append(f"   Density: {density:.4f}")
        insights.append(f"   Average clustering: {avg_clustering:.4f}")
        insights.append(f"   Number of strongly connected components: {nx.number_strongly_connected_components(self.G)}")
        insights.append("")
        
        # Bridge terms (high betweenness centrality)
        top_betweenness = sorted(self.betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        insights.append("🌉 Bridge Terms (High Betweenness):")
        for i, (node_id, score) in enumerate(top_betweenness, 1):
            word = self.id_to_word[node_id]
            insights.append(f"   {i}. {word:<20} ({score:.4f})")
        insights.append("")
        
        return "\n".join(insights)


def main():
    """Main function to create concept territory visualization."""
    
    if not VISUALIZATION_AVAILABLE:
        print("❌ Visualization libraries not available!")
        return
    
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    wiki_dir = project_dir / 'wiki'
    graph_file = wiki_dir / 'graph.json'
    
    if not graph_file.exists():
        print("❌ Graph file not found! Run build-mention-graph.py first.")
        return
    
    print("🗺️  Wiki Concept Territory Visualizer")
    print("=" * 40)
    
    try:
        visualizer = ConceptTerritoryVisualizer(graph_file)
        
        # Create visualizations
        print("\n🎨 Creating visualizations...")
        
        # 1. Interactive network map
        network_fig = visualizer.create_interactive_network()
        network_file = wiki_dir / 'concept-network.html'
        network_fig.write_html(str(network_file))
        print(f"   📊 Network map saved to: {network_file}")
        
        # 2. Community analysis
        community_fig = visualizer.create_community_analysis()
        community_file = wiki_dir / 'community-analysis.html'
        community_fig.write_html(str(community_file))
        print(f"   🧩 Community analysis saved to: {community_file}")
        
        # 3. Centrality comparison
        centrality_fig = visualizer.create_centrality_comparison()
        centrality_file = wiki_dir / 'centrality-comparison.html'
        centrality_fig.write_html(str(centrality_file))
        print(f"   📈 Centrality comparison saved to: {centrality_file}")
        
        # 4. Generate insights
        insights = visualizer.generate_insights()
        print("\n" + insights)
        
        # Save insights
        insights_file = wiki_dir / 'concept-insights.txt'
        with open(insights_file, 'w', encoding='utf-8') as f:
            f.write(insights)
        print(f"\n📁 Insights saved to: {insights_file}")
        
        print(f"\n✨ Concept territory mapped successfully!")
        print(f"   Open {network_file} in your browser to explore the interactive map!")
        
    except Exception as e:
        print(f"❌ Error during visualization: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
