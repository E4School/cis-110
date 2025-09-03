#!/usr/bin/env python3
"""
🎯 Improved Sentence Coverage Assessor
====================================
Fixed version with much better term detection and debugging capabilities.
"""

import json
import os
import re
from typing import List, Set, Dict, Tuple
from collections import defaultdict, Counter
import argparse

class ImprovedSentenceAssessor:
    def __init__(self, wiki_dir: str):
        """Initialize assessor with vocabulary."""
        self.wiki_dir = wiki_dir
        self.vocabulary = self._load_vocabulary()
        self.debug_mode = False
        
    def _load_vocabulary(self) -> List[str]:
        """Load vocabulary terms from wiki files."""
        vocabulary = []
        for filename in sorted(os.listdir(self.wiki_dir)):
            if filename.endswith('.md') and filename != 'index.md':
                term = filename[:-3].replace('-', ' ')
                vocabulary.append(term)
        return vocabulary
    
    def extract_sentences_from_file(self, file_path: str) -> List[str]:
        """Extract sentences from file."""
        sentences = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines, headers, separators
            if not line or line.startswith('=') or line.startswith('#') or '🎯' in line or '📊' in line:
                continue
            
            # Extract numbered sentences
            numbered_match = re.match(r'^\s*\d+\.\s*(.+)$', line)
            if numbered_match:
                sentence = numbered_match.group(1).strip()
                if sentence and len(sentence) > 5:
                    sentences.append(sentence)
                continue
            
            # Extract sentences that look like proper sentences
            if (line.endswith('.') or line.endswith('!') or line.endswith('?')) and len(line) > 10:
                if not any(keyword in line.lower() for keyword in ['coverage', 'analysis', 'generated', 'missing', 'covered', 'method:', 'file:']):
                    sentences.append(line)
        
        return sentences
    
    def normalize_term(self, term: str) -> str:
        """Normalize a term for comparison."""
        # Remove punctuation, convert to lowercase, normalize spaces
        normalized = re.sub(r'[^\w\s]', '', term.lower())
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def create_term_variations(self, term: str) -> Set[str]:
        """Create all possible variations of a term for matching."""
        variations = set()
        term_lower = term.lower()
        
        # Add the basic term
        variations.add(term_lower)
        variations.add(self.normalize_term(term))
        
        # Handle parenthetical expressions like "artificial intelligence (ai)"
        if '(' in term and ')' in term:
            # Extract the acronym and base term
            paren_match = re.search(r'^(.+?)\s*\(([^)]+)\)(.*)$', term)
            if paren_match:
                base_part = paren_match.group(1).strip()
                acronym = paren_match.group(2).strip()
                suffix_part = paren_match.group(3).strip()
                
                # Add variations
                variations.add(base_part.lower())
                variations.add(acronym.lower())
                variations.add(acronym.upper())
                variations.add(f"{base_part} {acronym}".lower())
                variations.add(f"{base_part} ({acronym})".lower())
                if suffix_part:
                    variations.add(f"{base_part} {suffix_part}".lower())
        
        # Handle hyphens and spaces
        if ' ' in term_lower:
            variations.add(term_lower.replace(' ', '-'))
            variations.add(term_lower.replace(' ', ''))
            # Add individual words for multi-word terms
            words = term_lower.split()
            if len(words) <= 3:  # Only for reasonable length terms
                variations.update(words)
        
        # Handle common technical abbreviations
        tech_mappings = {
            'operating system': ['os', 'operating system'],
            'artificial intelligence': ['ai', 'artificial intelligence'],
            'uniform resource locator': ['url', 'web address'],
            'hypertext transfer protocol': ['http', 'https'],
            'world wide web': ['web', 'www', 'world wide web'],
            'central processing unit': ['cpu', 'processor'],
            'random access memory': ['ram', 'memory'],
            'read only memory': ['rom'],
            'application programming interface': ['api'],
            'structured query language': ['sql'],
            'hypertext markup language': ['html'],
            'cascading style sheets': ['css'],
            'domain name system': ['dns'],
            'internet service provider': ['isp'],
            'virtual private network': ['vpn'],
            'user interface': ['ui'],
            'user experience': ['ux'],
            'frequently asked questions': ['faq'],
            'portable document format': ['pdf'],
            'two factor authentication': ['2fa', 'two factor auth'],
            'virtual reality': ['vr'],
            'augmented reality': ['ar'],
            'internet of things': ['iot'],
            'quality assurance': ['qa'],
        }
        
        for full_term, abbrevs in tech_mappings.items():
            if full_term in term_lower:
                variations.update(abbrevs)
        
        # Remove empty variations
        variations = {v for v in variations if v and len(v) > 0}
        
        return variations
    
    def find_term_in_sentence(self, term: str, sentence: str) -> Tuple[bool, str, str]:
        """Find if a term appears in a sentence. Returns (found, matched_variation, context)."""
        sentence_lower = sentence.lower()
        sentence_normalized = self.normalize_term(sentence)
        
        variations = self.create_term_variations(term)
        
        for variation in variations:
            variation_normalized = self.normalize_term(variation)
            
            # Try exact phrase match first
            if variation_normalized in sentence_normalized:
                return True, variation, f"Exact match: '{variation_normalized}'"
            
            # Try word boundary match for shorter terms
            if len(variation.split()) <= 2:
                pattern = r'\b' + re.escape(variation) + r'\b'
                if re.search(pattern, sentence_lower):
                    return True, variation, f"Word boundary match: '{variation}'"
        
        return False, "", ""
    
    def find_all_term_matches(self, sentences: List[str]) -> Dict:
        """Find all term matches with detailed debugging."""
        covered_terms = set()
        term_locations = defaultdict(list)
        coverage_details = defaultdict(list)
        debug_info = []
        
        for i, sentence in enumerate(sentences):
            sentence_matches = []
            
            for term in self.vocabulary:
                found, matched_variation, context = self.find_term_in_sentence(term, sentence)
                
                if found:
                    covered_terms.add(term)
                    term_locations[term].append(i + 1)
                    coverage_details[term].append({
                        'sentence_num': i + 1,
                        'matched_variation': matched_variation,
                        'context': context,
                        'sentence': sentence
                    })
                    sentence_matches.append(f"{term} ({matched_variation})")
            
            if self.debug_mode and sentence_matches:
                debug_info.append(f"Sentence {i+1}: {len(sentence_matches)} matches - {', '.join(sentence_matches)}")
        
        missing_terms = set(self.vocabulary) - covered_terms
        
        return {
            'covered_terms': covered_terms,
            'missing_terms': missing_terms,
            'term_locations': dict(term_locations),
            'coverage_details': dict(coverage_details),
            'coverage_percentage': 100 * len(covered_terms) / len(self.vocabulary),
            'debug_info': debug_info
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
        
        return {
            'total_sentences': len(sentences),
            'total_words': total_words,
            'avg_words_per_sentence': total_words / len(sentences),
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
    
    def generate_comprehensive_report(self, file_path: str, debug: bool = False) -> str:
        """Generate a comprehensive assessment report."""
        self.debug_mode = debug
        sentences = self.extract_sentences_from_file(file_path)
        
        if not sentences:
            return "❌ No sentences found in the file."
        
        coverage = self.find_all_term_matches(sentences)
        quality = self.analyze_sentence_quality(sentences)
        
        report = []
        report.append(f"📊 IMPROVED SENTENCE ASSESSMENT REPORT")
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
        
        # Show some example matches
        if coverage['coverage_details']:
            report.append(f"\n🔍 Sample Term Matches:")
            sample_matches = list(coverage['coverage_details'].items())[:10]
            for term, matches in sample_matches:
                match = matches[0]  # Show first match
                report.append(f"   • '{term}' → found as '{match['matched_variation']}' in sentence {match['sentence_num']}")
        
        # Debug info if requested
        if debug and coverage['debug_info']:
            report.append(f"\n🐛 Debug Info (first 10 sentences):")
            for debug_line in coverage['debug_info'][:10]:
                report.append(f"   {debug_line}")
        
        if coverage['missing_terms']:
            report.append(f"\n📋 Missing Terms (first 30):")
            missing_sorted = sorted(coverage['missing_terms'])[:30]
            for i in range(0, len(missing_sorted), 3):
                group = missing_sorted[i:i+3]
                report.append(f"   • {' | '.join(group)}")
            if len(coverage['missing_terms']) > 30:
                report.append(f"   ... and {len(coverage['missing_terms']) - 30} more")
        
        # Quality Analysis
        lq = quality['language_quality']
        report.append(f"\n🗣️  Language Quality:")
        report.append(f"   Articles (the/a/an): {lq['articles_pct']:.1f}%")
        report.append(f"   Conjunctions: {lq['conjunctions_pct']:.1f}%")
        report.append(f"   Prepositions: {lq['prepositions_pct']:.1f}%")
        report.append(f"   Proper endings: {lq['proper_endings']}/{len(sentences)} ({100*lq['proper_endings']/len(sentences):.1f}%)")
        
        # Overall Assessment
        coverage_score = coverage['coverage_percentage']
        naturalness = min(100, (lq['articles_pct'] + lq['conjunctions_pct'] + lq['prepositions_pct']) / 3)
        variety_score = min(100, 100 * quality['variety']['unique_starters'] / len(sentences))
        efficiency = min(100, 100 * len(coverage['covered_terms']) / len(sentences) / 2)
        
        overall_score = (coverage_score * 0.4 + naturalness * 0.25 + variety_score * 0.20 + efficiency * 0.15)
        
        report.append(f"\n🏆 Overall Assessment:")
        report.append(f"   Coverage Score: {coverage_score:.1f}/100 (40% weight)")
        report.append(f"   Naturalness Score: {naturalness:.1f}/100 (25% weight)")
        report.append(f"   Variety Score: {variety_score:.1f}/100 (20% weight)")
        report.append(f"   Efficiency Score: {efficiency:.1f}/100 (15% weight)")
        report.append(f"   📊 OVERALL SCORE: {overall_score:.1f}/100")
        
        return "\n".join(report)

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Assess sentence files with improved term detection')
    parser.add_argument('file_path', help='Path to the sentence file to assess')
    parser.add_argument('--wiki-dir', default='wiki', help='Directory containing vocabulary wiki files')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(f"❌ File not found: {args.file_path}")
        return
    
    if not os.path.exists(args.wiki_dir):
        print(f"❌ Wiki directory not found: {args.wiki_dir}")
        return
    
    print(f"📊 Assessing sentence file: {args.file_path}")
    
    assessor = ImprovedSentenceAssessor(args.wiki_dir)
    report = assessor.generate_comprehensive_report(args.file_path, debug=args.debug)
    print(report)
    
    # Save the report
    base_name = os.path.splitext(os.path.basename(args.file_path))[0]
    output_path = f"coverage-documents/{base_name}-improved-assessment.txt"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📁 Assessment saved to: {output_path}")

if __name__ == "__main__":
    # If run without arguments, assess the random sentences
    import sys
    if len(sys.argv) == 1:
        file_path = "coverage-documents/random-path-50-5-sentences.txt"
        
        if os.path.exists(file_path):
            assessor = ImprovedSentenceAssessor("wiki")
            report = assessor.generate_comprehensive_report(file_path, debug=True)
            print(report)
        else:
            print(f"❌ Default file not found: {file_path}")
    else:
        main()
