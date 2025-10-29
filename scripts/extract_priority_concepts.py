#!/usr/bin/env python3
"""
Extract Priority Concepts from Baseline Gap Analysis
====================================================
Phase 3 of Day 1: Foundation Setup

Extracts the top 20 cultural concepts from baseline gap analysis
that had the most translation failures. These become the priority
concepts for ontology population.

Input:  data/analysis/baseline_gap_analysis.json
Output: data/processed/priority_concepts.csv
"""

import json
import csv
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

def extract_priority_concepts(gap_file: Path, output_file: Path, top_n: int = 20):
    """Extract top N priority concepts from gap analysis."""
    
    print("="*70)
    print("PRIORITY CONCEPT EXTRACTION")
    print("="*70)
    print(f"\n📖 Input: {gap_file}")
    print(f"📝 Output: {output_file}")
    print(f"🎯 Target: Top {top_n} concepts\n")
    
    # Load gap analysis
    with open(gap_file) as f:
        data = json.load(f)
    
    gaps = data['gaps']
    print(f"📊 Analyzing {len(gaps)} proverbs with translation failures...\n")
    
    # Track concept frequencies and severity
    concept_failures = Counter()
    concept_severity = defaultdict(list)
    concept_proverbs = defaultdict(list)
    concept_metaphors = defaultdict(set)
    concept_cultural_meanings = defaultdict(set)
    
    # Extract concepts from all gaps
    for gap in gaps:
        proverb_id = gap['proverb_id']
        severity = gap['failure_severity']
        
        # Count missing concepts
        for concept in gap.get('missing_kikuyu_concepts', []):
            concept_clean = concept.strip().lower()
            concept_failures[concept_clean] += 1
            concept_severity[concept_clean].append(severity)
            concept_proverbs[concept_clean].append(proverb_id)
            
            # Track related metaphors and meanings
            for metaphor in gap.get('failed_metaphors', []):
                concept_metaphors[concept_clean].add(metaphor)
            for meaning in gap.get('lost_cultural_meanings', []):
                concept_cultural_meanings[concept_clean].add(meaning)
    
    print(f"🔍 Found {len(concept_failures)} unique concepts across failures\n")
    
    # Calculate importance scores
    concept_data = []
    for concept, count in concept_failures.items():
        severities = concept_severity[concept]
        
        # Calculate severity weight (critical=3, high=2, medium=1)
        severity_weight = sum(
            3 if s == 'critical' else 2 if s == 'high' else 1 
            for s in severities
        )
        
        # Importance score = frequency * average severity weight
        importance_score = count * (severity_weight / len(severities))
        
        # Get domain from concept keywords
        domain = categorize_concept(concept)
        
        concept_data.append({
            'concept_name': concept,
            'failure_count': count,
            'importance_score': round(importance_score, 2),
            'domain': domain,
            'critical_failures': severities.count('critical'),
            'high_failures': severities.count('high'),
            'medium_failures': severities.count('medium'),
            'example_proverbs': ','.join(concept_proverbs[concept][:3]),
            'failed_metaphors_count': len(concept_metaphors[concept]),
            'lost_meanings_count': len(concept_cultural_meanings[concept]),
            'priority': 0  # Will be assigned after sorting
        })
    
    # Sort by importance score (descending)
    concept_data.sort(key=lambda x: x['importance_score'], reverse=True)
    
    # Assign priority ranks
    for i, concept in enumerate(concept_data[:top_n], 1):
        concept['priority'] = i
    
    # Print top concepts
    print("🏆 TOP 20 PRIORITY CONCEPTS:")
    print("-" * 70)
    print(f"{'Rank':<6}{'Concept':<25}{'Failures':<10}{'Score':<10}{'Domain':<15}")
    print("-" * 70)
    
    for concept in concept_data[:top_n]:
        print(f"{concept['priority']:<6}"
              f"{concept['concept_name']:<25}"
              f"{concept['failure_count']:<10}"
              f"{concept['importance_score']:<10}"
              f"{concept['domain']:<15}")
    
    # Save to CSV
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'priority', 'concept_name', 'failure_count', 'importance_score',
            'domain', 'critical_failures', 'high_failures', 'medium_failures',
            'example_proverbs', 'failed_metaphors_count', 'lost_meanings_count'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(concept_data[:top_n])
    
    print("-" * 70)
    print(f"\n✅ Saved {top_n} priority concepts to: {output_file}")
    
    # Summary statistics
    total_failures = sum(c['failure_count'] for c in concept_data[:top_n])
    avg_score = sum(c['importance_score'] for c in concept_data[:top_n]) / top_n
    
    print(f"\n📈 STATISTICS:")
    print(f"   Total failures covered: {total_failures}")
    print(f"   Average importance score: {avg_score:.2f}")
    print(f"   Top concept: {concept_data[0]['concept_name']} ({concept_data[0]['failure_count']} failures)")
    print(f"   Domains represented: {len(set(c['domain'] for c in concept_data[:top_n]))}")
    
    print("\n" + "="*70)
    print("✅ PRIORITY CONCEPT EXTRACTION COMPLETE!")
    print("="*70)
    
    return concept_data[:top_n]


def categorize_concept(concept: str) -> str:
    """Categorize concept into domain based on keywords."""
    
    # Domain keyword mappings
    domains = {
        'wealth': ['wealth', 'money', 'riches', 'prosperity', 'fortune', 'utonga', 'mbeca'],
        'poverty': ['poverty', 'poor', 'lack', 'scarcity', 'thiini'],
        'social': ['community', 'family', 'kinship', 'relationships', 'social', 'unity'],
        'wisdom': ['wisdom', 'knowledge', 'understanding', 'intelligence', 'ũũgĩ'],
        'work': ['work', 'labor', 'effort', 'industry', 'diligence', 'wĩra'],
        'morality': ['morality', 'ethics', 'character', 'virtue', 'honesty', 'integrity'],
        'nature': ['nature', 'animals', 'land', 'seasons', 'agriculture', 'farming'],
        'leadership': ['leadership', 'authority', 'power', 'governance', 'elder'],
        'conflict': ['conflict', 'dispute', 'quarrel', 'disagreement', 'war'],
        'values': ['respect', 'honor', 'shame', 'pride', 'humility', 'patience']
    }
    
    concept_lower = concept.lower()
    
    # Check each domain
    for domain, keywords in domains.items():
        if any(keyword in concept_lower for keyword in keywords):
            return domain
    
    # Default to 'general'
    return 'general'


if __name__ == '__main__':
    # File paths
    project_root = Path(__file__).parent.parent
    gap_file = project_root / 'data/analysis/baseline_gap_analysis.json'
    output_file = project_root / 'data/processed/priority_concepts.csv'
    
    # Extract priority concepts
    priority_concepts = extract_priority_concepts(gap_file, output_file, top_n=20)
    
    print(f"\n📝 Next steps:")
    print(f"   1. Review priority concepts in: {output_file}")
    print(f"   2. Proceed to Phase 4: Populate proverb nodes")
    print(f"   3. Proceed to Phase 5: Create concept nodes")
    print(f"   4. Proceed to Phase 6: Link proverbs to concepts\n")
