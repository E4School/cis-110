#!/usr/bin/env python3
"""
🎯 Sentence Coverage Evaluator
============================
Evaluates sentence coverage and provides metrics for quality assessment.
"""

import json
import os
import re
from typing import List, Set, Dict, Tuple
from collections import defaultdict

class SentenceCoverageEvaluator:
    def __init__(self, wiki_dir: str):
        """Initialize evaluator."""
        self.wiki_dir = wiki_dir
        self.vocabulary = self._load_vocabulary()
        self.term_aliases = self._create_term_aliases()
        
    def _load_vocabulary(self) -> List[str]:
        """Load vocabulary terms."""
        vocabulary = []
        for filename in sorted(os.listdir(self.wiki_dir)):
            if filename.endswith('.md') and filename != 'index.md':
                term = filename[:-3].replace('-', ' ')
                vocabulary.append(term)
        return vocabulary
    
    def _create_term_aliases(self) -> Dict[str, List[str]]:
        """Create aliases for terms to improve detection."""
        aliases = {}
        
        for term in self.vocabulary:
            term_aliases = [term.lower()]
            
            # Add common variations
            if ' os' in term:
                term_aliases.append(term.replace(' os', ' (OS)').lower())
                term_aliases.append(term.replace(' os', '').lower())
            
            if ' ai' in term:
                term_aliases.append(term.replace(' ai', ' (AI)').lower())
                term_aliases.append(term.replace(' ai', '').lower())
            
            if ' url ' in term or term.endswith(' url'):
                term_aliases.append(term.replace(' url', ' URL').lower())
                term_aliases.append('url')
            
            if ' http ' in term or term.startswith('http '):
                term_aliases.append(term.replace(' http ', ' HTTP ').lower())
                term_aliases.append('http')
            
            if 'world wide web web' in term:
                term_aliases.extend(['world wide web', 'web', 'www'])
            
            # Add hyphenated versions
            term_aliases.append(term.replace(' ', '-').lower())
            
            # Add versions without common words
            clean_term = term.lower()
            for remove_word in ['the ', 'a ', 'an ']:
                if clean_term.startswith(remove_word):
                    term_aliases.append(clean_term[len(remove_word):])
            
            aliases[term] = list(set(term_aliases))
        
        return aliases
    
    def verify_coverage_detailed(self, sentences: List[str]) -> Dict:
        """Detailed coverage verification with better term matching."""
        covered_terms = set()
        term_locations = defaultdict(list)
        
        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            
            for term in self.vocabulary:
                for alias in self.term_aliases[term]:
                    if alias in sentence_lower:
                        covered_terms.add(term)
                        term_locations[term].append((i + 1, sentence, alias))
                        break
        
        missing_terms = set(self.vocabulary) - covered_terms
        
        return {
            'covered_terms': covered_terms,
            'missing_terms': missing_terms,
            'term_locations': dict(term_locations),
            'coverage_percentage': 100 * len(covered_terms) / len(self.vocabulary)
        }
    
    def evaluate_sentence_quality(self, sentences: List[str]) -> Dict:
        """Evaluate various quality metrics for the sentences."""
        metrics = {
            'total_sentences': len(sentences),
            'total_words': sum(len(s.split()) for s in sentences),
            'avg_words_per_sentence': sum(len(s.split()) for s in sentences) / len(sentences),
            'sentence_lengths': [len(s.split()) for s in sentences],
            'readability_scores': [],
            'natural_language_indicators': {}
        }
        
        # Sentence length analysis
        lengths = metrics['sentence_lengths']
        metrics['min_length'] = min(lengths)
        metrics['max_length'] = max(lengths)
        metrics['median_length'] = sorted(lengths)[len(lengths)//2]
        
        # Natural language indicators
        natural_indicators = {
            'uses_articles': sum(1 for s in sentences if any(article in s.lower() for article in [' the ', ' a ', ' an '])),
            'uses_conjunctions': sum(1 for s in sentences if any(conj in s.lower() for conj in [' and ', ' or ', ' but ', ' while ', ' when ', ' where '])),
            'uses_prepositions': sum(1 for s in sentences if any(prep in s.lower() for prep in [' in ', ' on ', ' at ', ' for ', ' with ', ' by '])),
            'proper_capitalization': sum(1 for s in sentences if s[0].isupper() and s.endswith('.')),
            'varied_sentence_starters': len(set(s.split()[0].lower() for s in sentences if s.split()))
        }
        
        metrics['natural_language_indicators'] = natural_indicators
        
        # Repetition analysis
        sentence_starts = [s.split()[0] if s.split() else '' for s in sentences]
        start_counts = defaultdict(int)
        for start in sentence_starts:
            start_counts[start.lower()] += 1
        
        metrics['repetitive_starts'] = {k: v for k, v in start_counts.items() if v > 3}
        
        return metrics
    
    def generate_quality_report(self, sentences: List[str]) -> str:
        """Generate a comprehensive quality report."""
        coverage = self.verify_coverage_detailed(sentences)
        quality = self.evaluate_sentence_quality(sentences)
        
        report = []
        report.append("📊 SENTENCE COVERAGE QUALITY REPORT")
        report.append("=" * 50)
        
        # Coverage Analysis
        report.append(f"\n🎯 Coverage Analysis:")
        report.append(f"   ✅ Covered: {len(coverage['covered_terms'])}/{len(self.vocabulary)} terms ({coverage['coverage_percentage']:.1f}%)")
        
        if coverage['missing_terms']:
            report.append(f"   ❌ Missing terms ({len(coverage['missing_terms'])}):")
            for term in sorted(coverage['missing_terms']):
                report.append(f"      • {term}")
        else:
            report.append("   🎉 Perfect coverage achieved!")
        
        # Quality Metrics
        report.append(f"\n📝 Sentence Quality Metrics:")
        report.append(f"   Total sentences: {quality['total_sentences']}")
        report.append(f"   Total words: {quality['total_words']}")
        report.append(f"   Average words per sentence: {quality['avg_words_per_sentence']:.1f}")
        report.append(f"   Sentence length range: {quality['min_length']}-{quality['max_length']} words")
        report.append(f"   Median sentence length: {quality['median_length']} words")
        
        # Natural Language Quality
        nl = quality['natural_language_indicators']
        report.append(f"\n🗣️  Natural Language Quality:")
        report.append(f"   Uses articles (the/a/an): {nl['uses_articles']}/{quality['total_sentences']} ({100*nl['uses_articles']/quality['total_sentences']:.1f}%)")
        report.append(f"   Uses conjunctions: {nl['uses_conjunctions']}/{quality['total_sentences']} ({100*nl['uses_conjunctions']/quality['total_sentences']:.1f}%)")
        report.append(f"   Uses prepositions: {nl['uses_prepositions']}/{quality['total_sentences']} ({100*nl['uses_prepositions']/quality['total_sentences']:.1f}%)")
        report.append(f"   Proper capitalization: {nl['proper_capitalization']}/{quality['total_sentences']} ({100*nl['proper_capitalization']/quality['total_sentences']:.1f}%)")
        report.append(f"   Varied sentence starters: {nl['varied_sentence_starters']} unique")
        
        # Repetition Issues
        if quality['repetitive_starts']:
            report.append(f"\n⚠️  Repetition Issues:")
            for start, count in quality['repetitive_starts'].items():
                report.append(f"   '{start}' starts {count} sentences")
        
        # Recommendations
        report.append(f"\n💡 Recommendations:")
        
        if coverage['coverage_percentage'] < 100:
            report.append(f"   • Fix missing term coverage ({len(coverage['missing_terms'])} terms)")
        
        if quality['avg_words_per_sentence'] > 25:
            report.append(f"   • Consider shortening sentences (avg {quality['avg_words_per_sentence']:.1f} words)")
        elif quality['avg_words_per_sentence'] < 8:
            report.append(f"   • Consider combining some short sentences for better flow")
        
        if nl['uses_articles'] / quality['total_sentences'] < 0.5:
            report.append(f"   • Increase use of articles (the/a/an) for more natural language")
        
        if quality['repetitive_starts']:
            report.append(f"   • Vary sentence starters to avoid repetition")
        
        # Overall Score
        coverage_score = coverage['coverage_percentage']
        naturalness_score = 100 * min(1.0, (nl['uses_articles'] + nl['uses_conjunctions'] + nl['uses_prepositions']) / (3 * quality['total_sentences']))
        variety_score = 100 * min(1.0, nl['varied_sentence_starters'] / (quality['total_sentences'] * 0.3))
        
        overall_score = (coverage_score * 0.5 + naturalness_score * 0.3 + variety_score * 0.2)
        
        report.append(f"\n🏆 Overall Quality Score: {overall_score:.1f}/100")
        report.append(f"   Coverage: {coverage_score:.1f}/100 (50% weight)")
        report.append(f"   Naturalness: {naturalness_score:.1f}/100 (30% weight)")
        report.append(f"   Variety: {variety_score:.1f}/100 (20% weight)")
        
        return "\n".join(report)
    
    def suggest_improvements(self, sentences: List[str]) -> List[str]:
        """Suggest specific improvements for the sentences."""
        coverage = self.verify_coverage_detailed(sentences)
        suggestions = []
        
        # Fix missing terms
        if coverage['missing_terms']:
            suggestions.append("Missing Term Fixes:")
            for term in sorted(coverage['missing_terms']):
                suggestions.append(f"  • Add '{term}' to an appropriate sentence")
        
        # Improve repetitive sentences
        quality = self.evaluate_sentence_quality(sentences)
        if quality['repetitive_starts']:
            suggestions.append("\nSentence Variety Improvements:")
            for start, count in quality['repetitive_starts'].items():
                suggestions.append(f"  • Vary the {count} sentences starting with '{start}'")
        
        return suggestions

def main():
    """Evaluate the generated sentences."""
    print("📊 Sentence Coverage Evaluator")
    print("=" * 40)
    
    wiki_dir = "wiki"
    sentences_file = os.path.join(wiki_dir, "optimal-coverage-sentences.txt")
    
    if not os.path.exists(sentences_file):
        print(f"❌ Sentences file not found: {sentences_file}")
        return
    
    # Load sentences
    sentences = []
    with open(sentences_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # Extract sentences from numbered lines
            if re.match(r'^\s*\d+\.\s+', line):
                sentence = re.sub(r'^\s*\d+\.\s+', '', line).strip()
                if sentence:
                    sentences.append(sentence)
    
    print(f"📚 Loaded {len(sentences)} sentences for evaluation")
    
    # Evaluate
    evaluator = SentenceCoverageEvaluator(wiki_dir)
    report = evaluator.generate_quality_report(sentences)
    
    print(report)
    
    # Save detailed report
    report_file = os.path.join(wiki_dir, "sentence-quality-report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📁 Detailed report saved to: {report_file}")

if __name__ == "__main__":
    main()
