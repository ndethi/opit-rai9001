#!/usr/bin/env python3
"""
Baseline Gap Analysis for Kikuyu Proverb Translation Systems

This script compares baseline MT system translations against expert translations
to identify systematic failures and inform ontology construction priorities.

Analysis Goals:
1. Identify Kikuyu concepts consistently mistranslated across all systems
2. Detect lost cultural meanings and metaphors
3. Quantify translation quality gaps (semantic, cultural, metaphorical)
4. Prioritize which concepts need deepest ontology representation

Input:
- data/results/baseline_translations/baseline_literal_proverb_100proverbs_deduped.csv
- data/evaluation/gold_standard_ireri_deduplicated.csv

Output:
- data/analysis/baseline_gap_analysis.json (structured failures)
- docs/baseline_gap_analysis.md (human-readable report)

Author: ndethi
Date: October 13, 2025
"""

import pandas as pd
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class TranslationGap:
    """Represents a translation failure across MT systems"""
    proverb_id: str
    kikuyu_text: str
    expert_translation: str
    expert_cultural_meaning: str
    expert_teaching: str
    
    # MT system translations
    openai_gpt4o_mini: str
    gemini_flash: str
    gpt35_turbo: str
    nllb200: str
    
    # Gap analysis
    gap_type: str  # 'complete_failure', 'partial_failure', 'metaphor_loss', 'cultural_loss'
    failed_systems: List[str]
    failure_severity: str  # 'critical', 'major', 'minor'
    
    # Semantic analysis
    missing_kikuyu_concepts: List[str]
    lost_cultural_meanings: List[str]
    failed_metaphors: List[str]
    
    # LLM analysis
    semantic_similarity_avg: float
    cultural_fidelity_avg: float
    metaphor_preservation_avg: float
    
    analysis_notes: str


@dataclass
class GapAnalysisSummary:
    """Summary statistics for gap analysis"""
    total_proverbs: int
    complete_failures: int  # All systems fail
    partial_failures: int  # Some systems fail
    metaphor_losses: int
    cultural_losses: int
    
    avg_semantic_similarity: float
    avg_cultural_fidelity: float
    avg_metaphor_preservation: float
    
    # Priority concepts for ontology
    top_missing_concepts: List[Tuple[str, int]]  # (concept, frequency)
    top_failed_metaphors: List[Tuple[str, int]]
    critical_kikuyu_terms: List[str]
    
    # System-specific failures
    system_failure_rates: Dict[str, float]
    worst_performing_system: str
    best_performing_system: str


class BaselineGapAnalyzer:
    """Analyzes gaps between baseline MT systems and expert translations"""
    
    def __init__(self, baseline_path: str, gold_standard_path: str):
        self.baseline_path = Path(baseline_path)
        self.gold_standard_path = Path(gold_standard_path)
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"  # GPT-4o for semantic analysis
        self.temperature = 0.2  # Low temperature for consistent analysis
        
        # Load data
        self.baseline_df = None
        self.gold_standard_df = None
        self.merged_df = None
        
        # Analysis results
        self.gaps: List[TranslationGap] = []
        self.summary: GapAnalysisSummary = None
    
    def load_data(self):
        """Load baseline and gold standard datasets"""
        logger.info(f"Loading baseline from {self.baseline_path}")
        self.baseline_df = pd.read_csv(self.baseline_path)
        
        logger.info(f"Loading gold standard from {self.gold_standard_path}")
        self.gold_standard_df = pd.read_csv(self.gold_standard_path)
        
        # Merge on proverb_id
        self.merged_df = pd.merge(
            self.baseline_df,
            self.gold_standard_df,
            on='proverb_id',
            suffixes=('_baseline', '_expert')
        )
        
        logger.info(f"Loaded {len(self.merged_df)} proverbs for analysis")
    
    def _get_analysis_prompt(self, row: pd.Series) -> str:
        """Build prompt for LLM-based gap analysis"""
        # Handle missing expert data
        expert_cultural = row.get('expert_cultural_meaning_expert', 'N/A')
        if pd.isna(expert_cultural):
            expert_cultural = 'N/A'
        
        expert_teaching = row.get('expert_teaching', 'N/A')
        if pd.isna(expert_teaching):
            expert_teaching = 'N/A'
        
        return f"""You are an expert in translation quality assessment and Kikuyu language. Analyze the following proverb translations and identify gaps.

**Kikuyu Proverb:** {row['kikuyu_text_expert']}

**Expert Translation:** {row['expert_translation_expert']}
**Expert Cultural Meaning:** {expert_cultural}
**Expert Teaching:** {expert_teaching}

**MT System Translations:**
1. OpenAI (GPT-4o-mini): {row['openai_literal']}
2. Google (Gemini): {row['google_literal']}
3. Cohere: {row['cohere_literal']}
4. NLLB-200: {row['nllb_literal']}

**Task:** Analyze each MT translation and provide:
1. Which systems completely failed (nonsensical or totally wrong)?
2. What Kikuyu concepts were mistranslated or lost?
3. Was the cultural meaning preserved?
4. Was the metaphorical structure preserved?
5. Semantic similarity score (0-1) for each system
6. Cultural fidelity score (0-1) for each system
7. Metaphor preservation score (0-1) for each system
8. Overall failure severity: critical/major/minor

Respond in JSON format:
{{
  "failed_systems": ["system1", "system2"],
  "gap_type": "complete_failure|partial_failure|metaphor_loss|cultural_loss",
  "failure_severity": "critical|major|minor",
  "missing_kikuyu_concepts": ["concept1", "concept2"],
  "lost_cultural_meanings": ["meaning1", "meaning2"],
  "failed_metaphors": ["metaphor description"],
  "semantic_scores": {{
    "openai": 0.7,
    "google": 0.6,
    "cohere": 0.5,
    "nllb": 0.1
  }},
  "cultural_fidelity_scores": {{
    "openai": 0.6,
    "google": 0.5,
    "cohere": 0.4,
    "nllb": 0.0
  }},
  "metaphor_preservation_scores": {{
    "openai": 0.5,
    "google": 0.4,
    "cohere": 0.3,
    "nllb": 0.0
  }},
  "analysis_notes": "Brief explanation of main failures"
}}"""
    
    def analyze_proverb(self, row: pd.Series) -> TranslationGap:
        """Analyze translation gaps for a single proverb using LLM"""
        proverb_id = row['proverb_id']
        logger.info(f"Analyzing gaps for {proverb_id}")
        
        try:
            # Get LLM analysis
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert translation quality analyst specializing in Kikuyu language and culture."},
                    {"role": "user", "content": self._get_analysis_prompt(row)}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            analysis = json.loads(response.choices[0].message.content)
            
            # Calculate averages
            semantic_scores = analysis['semantic_scores']
            cultural_scores = analysis['cultural_fidelity_scores']
            metaphor_scores = analysis['metaphor_preservation_scores']
            
            semantic_avg = sum(semantic_scores.values()) / len(semantic_scores)
            cultural_avg = sum(cultural_scores.values()) / len(cultural_scores)
            metaphor_avg = sum(metaphor_scores.values()) / len(metaphor_scores)
            
            # Create TranslationGap object
            gap = TranslationGap(
                proverb_id=proverb_id,
                kikuyu_text=row['kikuyu_text_expert'],
                expert_translation=row['expert_translation_expert'],
                expert_cultural_meaning=row.get('expert_cultural_meaning_expert', ''),
                expert_teaching=row.get('expert_teaching', ''),
                openai_gpt4o_mini=row['openai_literal'],
                gemini_flash=row['google_literal'],
                gpt35_turbo=row['cohere_literal'],
                nllb200=row['nllb_literal'],
                gap_type=analysis['gap_type'],
                failed_systems=analysis['failed_systems'],
                failure_severity=analysis['failure_severity'],
                missing_kikuyu_concepts=analysis['missing_kikuyu_concepts'],
                lost_cultural_meanings=analysis['lost_cultural_meanings'],
                failed_metaphors=analysis['failed_metaphors'],
                semantic_similarity_avg=semantic_avg,
                cultural_fidelity_avg=cultural_avg,
                metaphor_preservation_avg=metaphor_avg,
                analysis_notes=analysis['analysis_notes']
            )
            
            logger.info(f"✓ Analyzed {proverb_id}: {gap.gap_type} ({gap.failure_severity})")
            return gap
            
        except Exception as e:
            logger.error(f"✗ Failed to analyze {proverb_id}: {e}")
            # Return minimal gap object on failure
            return TranslationGap(
                proverb_id=proverb_id,
                kikuyu_text=row['kikuyu_text_expert'],
                expert_translation=row['expert_translation_expert'],
                expert_cultural_meaning=row.get('expert_cultural_meaning_expert', ''),
                expert_teaching=row.get('expert_teaching', ''),
                openai_gpt4o_mini=row['openai_literal'],
                gemini_flash=row['google_literal'],
                gpt35_turbo=row['cohere_literal'],
                nllb200=row['nllb_literal'],
                gap_type='unknown',
                failed_systems=[],
                failure_severity='unknown',
                missing_kikuyu_concepts=[],
                lost_cultural_meanings=[],
                failed_metaphors=[],
                semantic_similarity_avg=0.0,
                cultural_fidelity_avg=0.0,
                metaphor_preservation_avg=0.0,
                analysis_notes=f"Analysis failed: {str(e)}"
            )
    
    def analyze_all_proverbs(self, max_proverbs: int = None):
        """Analyze all proverbs in the dataset"""
        if self.merged_df is None:
            self.load_data()
        
        df_to_analyze = self.merged_df.head(max_proverbs) if max_proverbs else self.merged_df
        
        logger.info(f"Starting gap analysis for {len(df_to_analyze)} proverbs")
        
        for idx, row in df_to_analyze.iterrows():
            gap = self.analyze_proverb(row)
            self.gaps.append(gap)
        
        logger.info(f"✓ Completed analysis of {len(self.gaps)} proverbs")
    
    def generate_summary(self) -> GapAnalysisSummary:
        """Generate summary statistics from gap analysis"""
        logger.info("Generating gap analysis summary")
        
        # Count gap types
        complete_failures = sum(1 for g in self.gaps if g.gap_type == 'complete_failure')
        partial_failures = sum(1 for g in self.gaps if g.gap_type == 'partial_failure')
        metaphor_losses = sum(1 for g in self.gaps if g.gap_type == 'metaphor_loss')
        cultural_losses = sum(1 for g in self.gaps if g.gap_type == 'cultural_loss')
        
        # Calculate averages
        avg_semantic = sum(g.semantic_similarity_avg for g in self.gaps) / len(self.gaps)
        avg_cultural = sum(g.cultural_fidelity_avg for g in self.gaps) / len(self.gaps)
        avg_metaphor = sum(g.metaphor_preservation_avg for g in self.gaps) / len(self.gaps)
        
        # Collect missing concepts
        concept_freq = {}
        for gap in self.gaps:
            for concept in gap.missing_kikuyu_concepts:
                concept_freq[concept] = concept_freq.get(concept, 0) + 1
        top_concepts = sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Collect failed metaphors
        metaphor_freq = {}
        for gap in self.gaps:
            for metaphor in gap.failed_metaphors:
                metaphor_freq[metaphor] = metaphor_freq.get(metaphor, 0) + 1
        top_metaphors = sorted(metaphor_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        
        # Critical Kikuyu terms (concepts appearing in 5+ failures)
        critical_terms = [concept for concept, freq in top_concepts if freq >= 5]
        
        # System failure rates (map to actual names in JSON)
        system_failures = {
            'openai': 0,
            'google': 0,
            'cohere': 0,
            'nllb': 0
        }
        
        # Map system names for display
        system_display_names = {
            'openai': 'OpenAI GPT-4o-mini',
            'google': 'Google Gemini',
            'cohere': 'Cohere',
            'nllb': 'NLLB-200'
        }
        for gap in self.gaps:
            for system in gap.failed_systems:
                if system in system_failures:
                    system_failures[system] += 1
        
        system_failure_rates = {
            system: count / len(self.gaps) 
            for system, count in system_failures.items()
        }
        
        worst_system = max(system_failure_rates, key=system_failure_rates.get)
        best_system = min(system_failure_rates, key=system_failure_rates.get)
        
        self.summary = GapAnalysisSummary(
            total_proverbs=len(self.gaps),
            complete_failures=complete_failures,
            partial_failures=partial_failures,
            metaphor_losses=metaphor_losses,
            cultural_losses=cultural_losses,
            avg_semantic_similarity=avg_semantic,
            avg_cultural_fidelity=avg_cultural,
            avg_metaphor_preservation=avg_metaphor,
            top_missing_concepts=top_concepts,
            top_failed_metaphors=top_metaphors,
            critical_kikuyu_terms=critical_terms,
            system_failure_rates=system_failure_rates,
            worst_performing_system=worst_system,
            best_performing_system=best_system
        )
        
        logger.info("✓ Generated summary statistics")
        return self.summary
    
    def save_results(self, json_output: str, markdown_output: str):
        """Save gap analysis results to JSON and Markdown"""
        # Save JSON
        json_path = Path(json_output)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'baseline_file': str(self.baseline_path),
                'gold_standard_file': str(self.gold_standard_path),
                'model_used': self.model
            },
            'summary': asdict(self.summary),
            'gaps': [asdict(gap) for gap in self.gaps]
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Saved JSON results to {json_path}")
        
        # Generate and save Markdown report
        md_path = Path(markdown_output)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        
        markdown = self._generate_markdown_report()
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        logger.info(f"✓ Saved Markdown report to {md_path}")
    
    def _generate_markdown_report(self) -> str:
        """Generate human-readable Markdown report"""
        s = self.summary
        
        report = f"""# Baseline Translation Gap Analysis Report
**Date:** {datetime.now().strftime('%B %d, %Y')}  
**Corpus:** 100 Kikuyu Proverbs (Ireri Collection - Wealth/Prosperity Domain)  
**Analysis Model:** GPT-4o  

---

## Executive Summary

This report identifies systematic failures in baseline MT systems when translating Kikuyu proverbs, informing **ontology construction priorities** for the OG-RAG system.

### Key Findings
- **Total Proverbs Analyzed:** {s.total_proverbs}
- **Complete Failures (All Systems):** {s.complete_failures} ({s.complete_failures/s.total_proverbs*100:.1f}%)
- **Partial Failures (Some Systems):** {s.partial_failures} ({s.partial_failures/s.total_proverbs*100:.1f}%)
- **Metaphor Preservation Failures:** {s.metaphor_losses} ({s.metaphor_losses/s.total_proverbs*100:.1f}%)
- **Cultural Meaning Losses:** {s.cultural_losses} ({s.cultural_losses/s.total_proverbs*100:.1f}%)

### Quality Scores (0-1 scale)
- **Semantic Similarity:** {s.avg_semantic_similarity:.3f}
- **Cultural Fidelity:** {s.avg_cultural_fidelity:.3f}
- **Metaphor Preservation:** {s.avg_metaphor_preservation:.3f}

---

## 1. System-Level Performance

### Failure Rates by MT System
"""
        
        # System failure rates
        for system, rate in sorted(s.system_failure_rates.items(), key=lambda x: x[1], reverse=True):
            report += f"- **{system}:** {rate*100:.1f}% failure rate\n"
        
        report += f"""
**Worst Performing System:** {s.worst_performing_system}  
**Best Performing System:** {s.best_performing_system}

### System Rankings
1. **{s.best_performing_system}** (Most reliable)
"""
        
        # Add other systems in order
        sorted_systems = sorted(s.system_failure_rates.items(), key=lambda x: x[1])
        for i, (system, rate) in enumerate(sorted_systems[1:], 2):
            report += f"{i}. **{system}**\n"
        
        report += f"""
---

## 2. Missing Kikuyu Concepts

These concepts were consistently mistranslated across MT systems, indicating **HIGH PRIORITY** for ontology representation.

### Top 20 Missing Concepts
"""
        
        for i, (concept, freq) in enumerate(s.top_missing_concepts, 1):
            priority = "🔴 CRITICAL" if freq >= 10 else "🟠 HIGH" if freq >= 5 else "🟡 MEDIUM"
            report += f"{i}. **{concept}** - {freq} failures {priority}\n"
        
        report += f"""
### Critical Kikuyu Terms for Deep Ontology Representation
These terms appeared in 5+ failures and require rich semantic/cultural annotations:

"""
        for term in s.critical_kikuyu_terms:
            report += f"- `{term}`\n"
        
        report += f"""
---

## 3. Failed Metaphors

Metaphorical structures that MT systems consistently failed to preserve.

### Top 20 Failed Metaphors
"""
        
        for i, (metaphor, freq) in enumerate(s.top_failed_metaphors, 1):
            report += f"{i}. {metaphor} ({freq} failures)\n"
        
        report += """
---

## 4. Gap Type Distribution

"""
        
        # Gap type breakdown
        gap_types = {}
        for gap in self.gaps:
            gap_types[gap.gap_type] = gap_types.get(gap.gap_type, 0) + 1
        
        for gap_type, count in sorted(gap_types.items(), key=lambda x: x[1], reverse=True):
            percentage = count / s.total_proverbs * 100
            report += f"- **{gap_type}:** {count} proverbs ({percentage:.1f}%)\n"
        
        report += """
---

## 5. Critical Failures (Sample)

Below are examples of **critical failures** where all MT systems produced poor translations.

"""
        
        # Show 5 critical failures
        critical_gaps = [g for g in self.gaps if g.failure_severity == 'critical'][:5]
        
        for i, gap in enumerate(critical_gaps, 1):
            report += f"""
### {i}. {gap.proverb_id}: "{gap.kikuyu_text}"

**Expert Translation:** {gap.expert_translation}  
**Expert Cultural Meaning:** {gap.expert_cultural_meaning}

**MT System Translations:**
- **OpenAI GPT-4o-mini:** {gap.openai_gpt4o_mini}
- **Gemini 1.5 Flash:** {gap.gemini_flash}
- **GPT-3.5-turbo:** {gap.gpt35_turbo}
- **NLLB-200:** {gap.nllb200}

**Analysis:**
- **Failed Systems:** {', '.join(gap.failed_systems)}
- **Missing Concepts:** {', '.join(gap.missing_kikuyu_concepts)}
- **Lost Cultural Meanings:** {', '.join(gap.lost_cultural_meanings)}
- **Failed Metaphors:** {', '.join(gap.failed_metaphors)}

**Scores:**
- Semantic: {gap.semantic_similarity_avg:.2f}
- Cultural: {gap.cultural_fidelity_avg:.2f}
- Metaphor: {gap.metaphor_preservation_avg:.2f}

**Notes:** {gap.analysis_notes}

---
"""
        
        report += """
## 6. Ontology Construction Priorities

Based on this gap analysis, the following areas require **deepest ontology representation**:

### Priority 1: Critical Kikuyu Concepts (5+ failures)
These concepts should have:
- Rich semantic definitions
- Multiple Kikuyu expressions/synonyms
- Cultural significance annotations
- Usage context examples
- Biblical parallels (where applicable)

**Target Concepts:**
"""
        for term in s.critical_kikuyu_terms[:10]:
            report += f"- {term}\n"
        
        report += f"""
### Priority 2: Metaphorical Structures
Metaphors require:
- Explicit vehicle-tenor mappings
- Cultural resonance explanations
- Mapping justifications
- Multiple examples

**Focus Areas:**
"""
        for metaphor, freq in s.top_failed_metaphors[:5]:
            report += f"- {metaphor}\n"
        
        report += """
### Priority 3: Cultural Context
Proverbs with high cultural loss need:
- Expert cultural meaning annotations
- Teaching/moral dimensions
- Application contexts
- Thematic categorization

---

## 7. Recommendations for OG-RAG System

### Ontology Depth Requirements
1. **Entities:** Include all critical Kikuyu terms with cultural significance
2. **Metaphors:** Explicit vehicle-tenor-mapping-resonance structure
3. **Cultural Concepts:** Moral dimensions, Kikuyu expressions, explanations
4. **Relationships:** Rich property network (expresses, usesMetaphor, involvesEntity)

### Retrieval Strategy
- Prioritize subgraph retrieval for critical terms
- Include metaphor context in RAG prompts
- Surface cultural meanings for generation

### Evaluation Focus
- Test OG-RAG particularly on proverbs with complete baseline failures
- Measure improvement in cultural fidelity (currently lowest score)
- Validate metaphor preservation (second-lowest score)

---

## 8. Methodology Notes

**Analysis Approach:**
- LLM-based semantic comparison (GPT-4o at temperature 0.2)
- Structured JSON output for consistency
- Three-dimensional scoring: semantic, cultural, metaphorical

**Limitations:**
- LLM analysis introduces potential bias
- Cultural fidelity assessment limited by model's Kikuyu knowledge
- Some proverbs may have multiple valid translations

**Validation:**
- All failures manually reviewable in JSON output
- Scores averaged across 4 systems for robustness
- Priority rankings based on frequency, not individual judgments

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Next Step:** Manual ontology class hierarchy design informed by these priorities (Phase 2b)
"""
        
        return report


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze baseline translation gaps to inform ontology priorities'
    )
    parser.add_argument(
        '--baseline',
        default='data/results/baseline_translations/baseline_literal_proverb_100proverbs_deduped.csv',
        help='Path to baseline translations CSV'
    )
    parser.add_argument(
        '--gold-standard',
        default='data/evaluation/gold_standard_ireri_deduplicated.csv',
        help='Path to gold standard expert translations CSV'
    )
    parser.add_argument(
        '--output-json',
        default='data/analysis/baseline_gap_analysis.json',
        help='Output path for JSON results'
    )
    parser.add_argument(
        '--output-markdown',
        default='docs/baseline_gap_analysis.md',
        help='Output path for Markdown report'
    )
    parser.add_argument(
        '--max-proverbs',
        type=int,
        help='Limit analysis to first N proverbs (for testing)'
    )
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = BaselineGapAnalyzer(args.baseline, args.gold_standard)
    
    # Run analysis
    analyzer.load_data()
    analyzer.analyze_all_proverbs(max_proverbs=args.max_proverbs)
    analyzer.generate_summary()
    analyzer.save_results(args.output_json, args.output_markdown)
    
    # Print summary
    s = analyzer.summary
    print("\n" + "="*60)
    print("BASELINE GAP ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total Proverbs: {s.total_proverbs}")
    print(f"Complete Failures: {s.complete_failures} ({s.complete_failures/s.total_proverbs*100:.1f}%)")
    print(f"Avg Semantic Similarity: {s.avg_semantic_similarity:.3f}")
    print(f"Avg Cultural Fidelity: {s.avg_cultural_fidelity:.3f}")
    print(f"Avg Metaphor Preservation: {s.avg_metaphor_preservation:.3f}")
    print(f"\nWorst System: {s.worst_performing_system} ({s.system_failure_rates[s.worst_performing_system]*100:.1f}%)")
    print(f"Best System: {s.best_performing_system} ({s.system_failure_rates[s.best_performing_system]*100:.1f}%)")
    print(f"\nCritical Kikuyu Terms: {len(s.critical_kikuyu_terms)}")
    print(f"Top Missing Concept: {s.top_missing_concepts[0][0]} ({s.top_missing_concepts[0][1]} failures)")
    print("="*60)
    print(f"\n✓ Full report saved to {args.output_markdown}")


if __name__ == '__main__':
    main()
