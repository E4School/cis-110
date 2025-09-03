#!/usr/bin/env python3
"""
🎯 Universal Sentence Coverage Assessor
=====================================
Evaluates any sentence file for vocabulary coverage and quality metrics.
"""

import json
import os
import re
from typing import List, Set, Dict, Tuple
from collections import defaultdict, Counter
import argparse

class UniversalSentenceAssessor:
    def __init__(self, wiki_dir: str):
        """Initialize assessor with vocabulary."""
        self.wiki_dir = wiki_dir
        self.vocabulary = self._load_vocabulary()
        self.term_aliases = self._create_comprehensive_aliases()
        
    def _load_vocabulary(self) -> List[str]:
        """Load vocabulary terms from wiki files."""
        vocabulary = []
        for filename in sorted(os.listdir(self.wiki_dir)):
            if filename.endswith('.md') and filename != 'index.md':
                term = filename[:-3].replace('-', ' ')
                vocabulary.append(term)
        return vocabulary
    
    def _create_comprehensive_aliases(self) -> Dict[str, List[str]]:
        """Create comprehensive aliases for better term detection."""
        aliases = {}
        
        for term in self.vocabulary:
            term_aliases = []
            term_lower = term.lower()
            
            # Basic variations
            term_aliases.extend([
                term_lower,
                term_lower.replace(' ', '-'),
                term_lower.replace(' ', ''),
                term.title(),
                term.upper()
            ])
            
            # Handle parenthetical expressions
            if '(' in term and ')' in term:
                # Extract content in parentheses
                paren_content = re.search(r'\(([^)]+)\)', term)
                if paren_content:
                    acronym = paren_content.group(1)
                    base_term = re.sub(r'\s*\([^)]+\)', '', term).strip()
                    term_aliases.extend([
                        acronym.lower(),
                        acronym.upper(),
                        base_term.lower(),
                        f"{base_term} ({acronym})".lower(),
                        f"{base_term} {acronym}".lower()
                    ])
            
            # Handle specific technical terms
            if 'operating system' in term_lower:
                term_aliases.extend(['os', 'operating system', 'operating systems'])
            
            if 'artificial intelligence' in term_lower:
                term_aliases.extend(['ai', 'artificial intelligence', 'machine intelligence'])
            
            if 'uniform resource locator' in term_lower:
                term_aliases.extend(['url', 'urls', 'web address', 'web addresses'])
            
            if 'hypertext transfer protocol' in term_lower:
                term_aliases.extend(['http', 'https', 'hypertext transfer protocol'])
            
            if 'world wide web' in term_lower:
                term_aliases.extend(['web', 'www', 'world wide web', 'internet'])
            
            if 'central processing unit' in term_lower or ' cpu' in term_lower:
                term_aliases.extend(['cpu', 'processor', 'central processing unit'])
            
            if 'random access memory' in term_lower or ' ram' in term_lower:
                term_aliases.extend(['ram', 'memory', 'random access memory'])
            
            # Handle compound terms
            if ' and ' in term_lower:
                parts = term_lower.split(' and ')
                term_aliases.extend(parts)
            
            # Remove duplicates and empty strings
            term_aliases = [alias for alias in set(term_aliases) if alias and len(alias) > 1]
            aliases[term] = term_aliases
        
        return aliases
    
    def extract_sentences_from_file(self, file_path: str) -> List[str]:
        """Extract sentences from various file formats."""
        sentences = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by lines and look for sentence patterns
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines, headers, separators
            if not line or line.startswith('=') or line.startswith('#') or line.startswith('🎯'):
                continue
            
            # Extract numbered sentences
            numbered_match = re.match(r'^\s*\d+\.\s*(.+)$', line)
            if numbered_match:
                sentence = numbered_match.group(1).strip()
                if sentence and len(sentence) > 10:  # Ignore very short sentences
                    sentences.append(sentence)
                continue
            
            # Extract sentences that look like proper sentences
            if (line.endswith('.') or line.endswith('!') or line.endswith('?')) and len(line) > 20:
                # Skip lines that look like metadata
                if not any(keyword in line.lower() for keyword in ['coverage', 'analysis', 'generated', 'missing', 'covered']):
                    sentences.append(line)
        
        return sentences
    
    def find_term_matches(self, sentences: List[str]) -> Dict:
        """Find which terms are covered by the sentences."""
        covered_terms = set()
        term_locations = defaultdict(list)
        coverage_details = defaultdict(list)
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            sentence_words = set(re.findall(r'\b\w+\b', sentence_lower))
            
            for term in self.vocabulary:
                found_match = False
                best_alias = None
                
                for alias in self.term_aliases[term]:
                    alias_lower = alias.lower()
                    
                    # Check for exact phrase match
                    if alias_lower in sentence_lower:
                        covered_terms.add(term)
                        term_locations[term].append(i + 1)
                        coverage_details[term].append({
                            'sentence_num': i + 1,
                            'matched_alias': alias,
                            'sentence': sentence
                        })
                        found_match = True
                        best_alias = alias
                        break
                    
                    # Check for word-based match for multi-word terms
                    elif ' ' in alias_lower:
                        alias_words = set(alias_lower.split())
                        if alias_words.issubset(sentence_words):
                            covered_terms.add(term)
                            term_locations[term].append(i + 1)
                            coverage_details[term].append({
                                'sentence_num': i + 1,
                                'matched_alias': alias,
                                'sentence': sentence
                            })
                            found_match = True
                            best_alias = alias
                            break
                
                if found_match:
                    break
        
        missing_terms = set(self.vocabulary) - covered_terms
        
        return {
            'covered_terms': covered_terms,
            'missing_terms': missing_terms,
            'term_locations': dict(term_locations),
            'coverage_details': dict(coverage_details),
            'coverage_percentage': 100 * len(covered_terms) / len(self.vocabulary)
        }
    
    def analyze_sentence_quality(self, sentences: List[str]) -> Dict:
        """Analyze quality metrics of sentences."""
        if not sentences:
            return {'error': 'No sentences found'}
        
        # Basic metrics
        total_words = sum(len(sentence.split()) for sentence in sentences)
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        
        # Language quality indicators
        articles = sum(1 for s in sentences if any(art in s.lower() for art in [' the ', ' a ', ' an ']))
        conjunctions = sum(1 for s in sentences if any(conj in s.lower() for conj in [' and ', ' or ', ' but ', ' while ', ' when ', ' where ', ' because ']))
        prepositions = sum(1 for s in sentences if any(prep in s.lower() for prep in [' in ', ' on ', ' at ', ' for ', ' with ', ' by ', ' through ', ' using ']))
        
        # Sentence variety
        first_words = [s.split()[0].lower() if s.split() else '' for s in sentences]
        first_word_counts = Counter(first_words)
        
        # Readability approximation (simplified)
        avg_sentence_length = total_words / len(sentences)
        
        return {
            'total_sentences': len(sentences),
            'total_words': total_words,
            'avg_words_per_sentence': avg_sentence_length,
            'sentence_lengths': sentence_lengths,
            'min_length': min(sentence_lengths),
            'max_length': max(sentence_lengths),
            'median_length': sorted(sentence_lengths)[len(sentence_lengths)//2],
            'language_quality': {
                'articles_pct': 100 * articles / len(sentences),
                'conjunctions_pct': 100 * conjunctions / len(sentences),
                'prepositions_pct': 100 * prepositions / len(sentences),
                'proper_endings': sum(1 for s in sentences if s.endswith(('.', '!', '?')))
            },
            'variety': {
                'unique_starters': len(set(first_words)),
                'most_common_starters': dict(first_word_counts.most_common(5)),
                'repetitive_starters': {word: count for word, count in first_word_counts.items() if count > 3}
            }
        }
    
    def generate_comprehensive_report(self, file_path: str) -> str:
        """Generate a comprehensive assessment report."""
        sentences = self.extract_sentences_from_file(file_path)
        
        if not sentences:
            return "❌ No sentences found in the file."
        
        coverage = self.find_term_matches(sentences)
        quality = self.analyze_sentence_quality(sentences)
        
        report = []
        report.append(f"📊 COMPREHENSIVE SENTENCE ASSESSMENT REPORT")
        report.append(f"File: {os.path.basename(file_path)}")
        report.append("=" * 60)
        
        # Basic Stats
        report.append(f"\n📝 Basic Statistics:")
        report.append(f"   Sentences analyzed: {len(sentences)}")
        report.append(f"   Total words: {quality['total_words']}")
        report.append(f"   Average sentence length: {quality['avg_words_per_sentence']:.1f} words")
        report.append(f"   Length range: {quality['min_length']}-{quality['max_length']} words")
        
        # Coverage Analysis
        report.append(f"\n🎯 Vocabulary Coverage:")
        report.append(f"   ✅ Covered: {len(coverage['covered_terms'])}/{len(self.vocabulary)} terms ({coverage['coverage_percentage']:.1f}%)")
        report.append(f"   ❌ Missing: {len(coverage['missing_terms'])} terms")
        
        if coverage['missing_terms']:
            report.append(f"\n📋 Missing Terms:")
            missing_sorted = sorted(coverage['missing_terms'])
            # Group missing terms for better readability
            for i in range(0, len(missing_sorted), 3):
                group = missing_sorted[i:i+3]
                report.append(f"   • {' | '.join(group)}")
        
        # Quality Analysis
        lq = quality['language_quality']
        report.append(f"\n🗣️  Language Quality:")
        report.append(f"   Articles (the/a/an): {lq['articles_pct']:.1f}%")
        report.append(f"   Conjunctions: {lq['conjunctions_pct']:.1f}%")
        report.append(f"   Prepositions: {lq['prepositions_pct']:.1f}%")
        report.append(f"   Proper endings: {lq['proper_endings']}/{len(sentences)} ({100*lq['proper_endings']/len(sentences):.1f}%)")
        
        # Variety Analysis
        variety = quality['variety']
        report.append(f"\n🎨 Sentence Variety:")
        report.append(f"   Unique sentence starters: {variety['unique_starters']}")
        
        if variety['repetitive_starters']:
            report.append(f"   ⚠️  Repetitive starters:")
            for word, count in variety['repetitive_starters'].items():
                report.append(f"      '{word}': {count} times")
        else:
            report.append(f"   ✅ Good variety in sentence starters")
        
        # Overall Assessment
        coverage_score = coverage['coverage_percentage']
        
        # Language naturalness score (0-100)
        naturalness = min(100, (lq['articles_pct'] + lq['conjunctions_pct'] + lq['prepositions_pct']) / 3)
        
        # Variety score (0-100) 
        variety_score = min(100, 100 * variety['unique_starters'] / len(sentences))
        
        # Efficiency score (more terms per sentence is better)
        efficiency = min(100, 100 * len(coverage['covered_terms']) / len(sentences) / 2)  # Normalize assuming 2 terms per sentence is excellent
        
        overall_score = (coverage_score * 0.4 + naturalness * 0.25 + variety_score * 0.20 + efficiency * 0.15)
        
        report.append(f"\n🏆 Overall Assessment:")
        report.append(f"   Coverage Score: {coverage_score:.1f}/100 (40% weight)")
        report.append(f"   Naturalness Score: {naturalness:.1f}/100 (25% weight)")
        report.append(f"   Variety Score: {variety_score:.1f}/100 (20% weight)")
        report.append(f"   Efficiency Score: {efficiency:.1f}/100 (15% weight)")
        report.append(f"   📊 OVERALL SCORE: {overall_score:.1f}/100")
        
        # Recommendations
        report.append(f"\n💡 Recommendations:")
        
        if coverage_score < 85:
            report.append(f"   • Improve vocabulary coverage (currently {coverage_score:.1f}%)")
        
        if naturalness < 60:
            report.append(f"   • Use more natural language patterns (articles, conjunctions)")
        
        if variety_score < 50:
            report.append(f"   • Increase sentence starter variety")
        
        if efficiency < 50:
            report.append(f"   • Try to include more terms per sentence where natural")
        
        if len(sentences) > 50:
            report.append(f"   • Consider reducing number of sentences for better memorability")
        
        return "\n".join(report)
    
    def save_assessment_to_file(self, file_path: str, output_path: str = None):
        """Save assessment report to a file."""
        report = self.generate_comprehensive_report(file_path)
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(self.wiki_dir, f"{base_name}-assessment.txt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return output_path

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Assess sentence files for vocabulary coverage and quality')
    parser.add_argument('file_path', help='Path to the sentence file to assess')
    parser.add_argument('--wiki-dir', default='wiki', help='Directory containing vocabulary wiki files')
    parser.add_argument('--output', help='Output file path for the assessment report')
    parser.add_argument('--print-report', action='store_true', help='Print the report to console')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"❌ File not found: {args.file_path}")
        return
    
    if not os.path.exists(args.wiki_dir):
        print(f"❌ Wiki directory not found: {args.wiki_dir}")
        return
    
    print(f"📊 Assessing sentence file: {args.file_path}")
    
    assessor = UniversalSentenceAssessor(args.wiki_dir)
    
    if args.print_report:
        report = assessor.generate_comprehensive_report(args.file_path)
        print(report)
    
    output_path = assessor.save_assessment_to_file(args.file_path, args.output)
    print(f"📁 Assessment report saved to: {output_path}")

if __name__ == "__main__":
    # If run without arguments, assess the human-crafted sentences
    import sys
    if len(sys.argv) == 1:
        wiki_dir = "wiki"
        file_path = os.path.join(wiki_dir, "human-crafted-sentences.txt")
        
        if os.path.exists(file_path):
            assessor = UniversalSentenceAssessor(wiki_dir)
            report = assessor.generate_comprehensive_report(file_path)
            print(report)
            
            # Save the report
            output_path = assessor.save_assessment_to_file(file_path)
            print(f"\n📁 Assessment saved to: {output_path}")
        else:
            print(f"❌ Default file not found: {file_path}")
    else:
        main()
