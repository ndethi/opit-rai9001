#!/usr/bin/env python3
"""Create comprehensive evaluation benchmark framework for thiLLMo OG-RAG translation quality assessment.

This script creates the evaluation infrastructure and benchmark dataset structure
before expert feedback collection, ensuring standardized evaluation methodology.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import logging
import argparse
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EvaluationBenchmarkCreator:
    """Create comprehensive evaluation benchmark framework for AI translation quality assessment."""
    
    def __init__(self, proverbs_file: str = "data/proverbs/extracted_proverbs.csv"):
        """Initialize with existing proverb data."""
        self.proverbs_file = Path(proverbs_file)
        if not self.proverbs_file.exists():
            raise FileNotFoundError(f"Proverbs file not found: {proverbs_file}")
        
        self.df = pd.read_csv(proverbs_file)
        logger.info(f"Loaded {len(self.df)} proverbs from {proverbs_file}")
        
        # Evaluation framework configuration
        self.evaluation_config = self._create_evaluation_config()
        
        # Output directories
        self.output_dir = Path("data/evaluation")
        self.benchmark_dir = self.output_dir / "benchmark"
        self.metrics_dir = self.output_dir / "metrics"
        self.templates_dir = self.output_dir / "templates"
        
        # Create directories
        for directory in [self.output_dir, self.benchmark_dir, self.metrics_dir, self.templates_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _create_evaluation_config(self) -> Dict[str, Any]:
        """Define comprehensive evaluation framework configuration."""
        return {
            "evaluation_methodology": {
                "approach": "comparative_analysis",
                "systems": ["og_rag", "raw_llm", "expert_gold_standard"],
                "evaluation_type": "human_expert_assessment"
            },
            "quality_dimensions": {
                "cultural_faithfulness": {
                    "description": "Preservation of cultural meaning and context",
                    "scale": "1-5 (1=Poor, 5=Excellent)",
                    "weight": 0.4,
                    "criteria": [
                        "Cultural concepts preserved",
                        "Traditional context maintained", 
                        "Metaphorical meaning captured",
                        "Cultural authenticity"
                    ]
                },
                "translation_accuracy": {
                    "description": "Linguistic accuracy and semantic correctness",
                    "scale": "1-5 (1=Poor, 5=Excellent)", 
                    "weight": 0.3,
                    "criteria": [
                        "Semantic equivalence",
                        "Grammatical correctness",
                        "Vocabulary appropriateness",
                        "Idiomatic naturalness"
                    ]
                },
                "business_relevance": {
                    "description": "Modern business application appropriateness",
                    "scale": "1-5 (1=Poor, 5=Excellent)",
                    "weight": 0.2,
                    "criteria": [
                        "Modern context applicability",
                        "Business scenario relevance",
                        "Professional appropriateness",
                        "Practical utility"
                    ]
                },
                "overall_fluency": {
                    "description": "Natural English expression and readability",
                    "scale": "1-5 (1=Poor, 5=Excellent)",
                    "weight": 0.1,
                    "criteria": [
                        "Natural expression",
                        "Readability",
                        "Flow and coherence",
                        "Target audience appropriateness"
                    ]
                }
            },
            "expert_qualifications": {
                "required": [
                    "Native or near-native Kikuyu speaker",
                    "Academic background in African studies, linguistics, or related field",
                    "Familiarity with traditional Kikuyu culture and proverbs"
                ],
                "preferred": [
                    "PhD in relevant field",
                    "Published research on Kikuyu culture or language",
                    "Experience with translation or cultural preservation"
                ]
            },
            "evaluation_process": {
                "blind_evaluation": True,
                "randomized_order": True,
                "multiple_evaluators": True,
                "inter_rater_reliability": True,
                "evaluation_sessions": {
                    "max_proverbs_per_session": 10,
                    "break_duration": "15 minutes",
                    "max_daily_sessions": 3
                }
            }
        }
    
    def create_benchmark_structure(self) -> str:
        """Create the benchmark dataset structure with existing proverbs."""
        
        logger.info("🏗️ Creating evaluation benchmark structure...")
        
        # Filter authentic proverbs (assuming we have some quality indicators)
        # For now, we'll use all proverbs but add placeholders for expert evaluation
        benchmark_records = []
        
        for idx, row in self.df.iterrows():
            # Create comprehensive benchmark record structure
            benchmark_record = {
                # Source Information
                'proverb_id': f"EVAL_{idx+1:04d}",
                'source_id': row.get('id', f"SRC_{idx+1}"),
                'kikuyu_text': row.get('kikuyu_text', '').strip(),
                'initial_translation': row.get('english_translation', '').strip(),
                'cultural_meaning': row.get('cultural_meaning', '').strip(),
                'traditional_usage': row.get('traditional_usage', '').strip(),
                
                # Expert Gold Standard (to be populated)
                'expert_translation': '',
                'expert_cultural_explanation': '',
                'expert_business_application': '',
                'expert_traditional_context': '',
                'expert_modern_relevance': '',
                
                # Expert Quality Scores (to be populated)
                'expert_cultural_faithfulness': None,
                'expert_translation_accuracy': None,
                'expert_business_relevance': None,
                'expert_overall_fluency': None,
                'expert_overall_score': None,
                
                # System Translations (to be generated)
                'og_rag_translation': '',
                'og_rag_cultural_explanation': '',
                'og_rag_business_application': '',
                'og_rag_confidence_score': 0.0,
                'og_rag_retrieval_context': '',
                
                'raw_llm_translation': '',
                'raw_llm_cultural_explanation': '',
                'raw_llm_business_application': '',
                'raw_llm_confidence_score': 0.0,
                
                # Evaluation Metadata
                'expert_evaluator_id': '',
                'evaluation_session_id': '',
                'evaluation_date': '',
                'evaluation_duration_minutes': None,
                'evaluation_notes': '',
                
                # Quality Control
                'validation_status': 'pending',
                'inter_rater_reliability': None,
                'consensus_required': False,
                'final_approval': False,
                
                # Benchmark Metadata
                'creation_date': datetime.now().isoformat(),
                'benchmark_version': '1.0',
                'data_source': str(self.proverbs_file)
            }
            
            # Only include records with meaningful content
            if benchmark_record['kikuyu_text'] and len(benchmark_record['kikuyu_text']) > 5:
                benchmark_records.append(benchmark_record)
        
        # Create benchmark DataFrame
        benchmark_df = pd.DataFrame(benchmark_records)
        
        # Save benchmark structure
        benchmark_file = self.benchmark_dir / "translation_evaluation_benchmark.csv"
        benchmark_df.to_csv(benchmark_file, index=False, encoding='utf-8')
        
        logger.info(f"✅ Created benchmark structure with {len(benchmark_records)} evaluation cases")
        logger.info(f"📁 Saved to: {benchmark_file}")
        
        return str(benchmark_file)
    
    def create_evaluation_templates(self) -> Dict[str, str]:
        """Create evaluation templates and instructions for experts."""
        
        logger.info("📋 Creating evaluation templates...")
        
        templates = {}
        
        # 1. Expert Evaluation Spreadsheet Template
        eval_template_data = {
            'proverb_id': ['EVAL_0001', 'EVAL_0002'],
            'kikuyu_text': ['Example proverb 1', 'Example proverb 2'],
            'system_translation_a': ['System A translation', 'System A translation'],
            'system_translation_b': ['System B translation', 'System B translation'],
            'expert_preferred_translation': ['', ''],
            'cultural_faithfulness_a': [None, None],
            'cultural_faithfulness_b': [None, None],
            'translation_accuracy_a': [None, None],
            'translation_accuracy_b': [None, None],
            'business_relevance_a': [None, None],
            'business_relevance_b': [None, None],
            'overall_fluency_a': [None, None],
            'overall_fluency_b': [None, None],
            'preferred_system': ['', ''],
            'expert_comments': ['', '']
        }
        
        eval_template_df = pd.DataFrame(eval_template_data)
        eval_template_file = self.templates_dir / "expert_evaluation_template.xlsx"
        
        with pd.ExcelWriter(eval_template_file, engine='openpyxl') as writer:
            eval_template_df.to_excel(writer, sheet_name='Evaluation', index=False)
            
            # Add instructions sheet
            instructions_df = pd.DataFrame({
                'Evaluation Guidelines': [
                    '1. Evaluate each translation on 4 dimensions (1-5 scale)',
                    '2. Cultural Faithfulness: How well cultural meaning is preserved',
                    '3. Translation Accuracy: Linguistic and semantic correctness',
                    '4. Business Relevance: Modern business application appropriateness',
                    '5. Overall Fluency: Natural English expression',
                    '6. Provide your own preferred translation',
                    '7. Indicate which system (A or B) performs better overall',
                    '8. Add detailed comments explaining your evaluation'
                ]
            })
            instructions_df.to_excel(writer, sheet_name='Instructions', index=False)
        
        templates['evaluation_template'] = str(eval_template_file)
        
        # 2. Expert Instructions Document
        instructions_content = self._create_detailed_instructions()
        instructions_file = self.templates_dir / "expert_evaluation_instructions.md"
        with open(instructions_file, 'w', encoding='utf-8') as f:
            f.write(instructions_content)
        templates['instructions'] = str(instructions_file)
        
        # 3. Evaluation Session Protocol
        protocol_content = self._create_evaluation_protocol()
        protocol_file = self.templates_dir / "evaluation_session_protocol.md"
        with open(protocol_file, 'w', encoding='utf-8') as f:
            f.write(protocol_content)
        templates['protocol'] = str(protocol_file)
        
        logger.info(f"✅ Created evaluation templates:")
        for template_type, file_path in templates.items():
            logger.info(f"   • {template_type}: {file_path}")
        
        return templates
    
    def _create_detailed_instructions(self) -> str:
        """Create detailed evaluation instructions for experts."""
        return """# Expert Evaluation Instructions for thiLLMo Translation Quality Assessment

## Overview

You are participating in a comparative evaluation of AI translation systems for Kikuyu proverbs. Your expertise in Kikuyu culture and language is crucial for assessing translation quality.

## Evaluation Process

### 1. Translation Comparison
- You will see pairs of translations (System A vs System B) for the same Kikuyu proverb
- Systems are anonymized to ensure unbiased evaluation
- One system uses Ontology-Grounded RAG, the other uses raw LLM translation

### 2. Evaluation Dimensions

#### Cultural Faithfulness (Weight: 40%)
**Question**: How well does the translation preserve the cultural meaning and context?

**Criteria**:
- Cultural concepts are accurately represented
- Traditional context is maintained
- Metaphorical meaning is captured appropriately
- Cultural authenticity is preserved

**Scale**:
- 5 = Excellent: Perfect cultural preservation
- 4 = Very Good: Minor cultural nuances missing
- 3 = Good: Adequate cultural representation
- 2 = Fair: Some cultural meaning lost
- 1 = Poor: Significant cultural distortion

#### Translation Accuracy (Weight: 30%)
**Question**: How linguistically accurate and semantically correct is the translation?

**Criteria**:
- Semantic equivalence to original meaning
- Grammatical correctness in English
- Appropriate vocabulary choices
- Natural idiomatic expression

#### Business Relevance (Weight: 20%)
**Question**: How appropriate is the translation for modern business contexts?

**Criteria**:
- Applicable to modern workplace scenarios
- Relevant to business situations
- Professional appropriateness
- Practical utility for business communication

#### Overall Fluency (Weight: 10%)
**Question**: How natural and readable is the English expression?

**Criteria**:
- Natural English expression
- Good readability and flow
- Coherent presentation
- Appropriate for target audience

### 3. Your Expert Input

#### Preferred Translation
Provide your own translation that you consider optimal, incorporating:
- Cultural authenticity
- Linguistic accuracy  
- Modern relevance
- Natural expression

#### Detailed Comments
Explain your evaluation decisions, including:
- Specific cultural elements preserved or lost
- Translation strengths and weaknesses
- Suggestions for improvement
- Cultural context that may not be obvious

## Quality Standards

### Excellent Translation (Score 4-5)
- Preserves essential cultural meaning
- Linguistically accurate and natural
- Appropriate for intended context
- Minor improvements possible

### Good Translation (Score 3)
- Generally accurate with some limitations
- Cultural meaning mostly preserved
- Understandable and usable
- Noticeable room for improvement

### Poor Translation (Score 1-2)
- Significant cultural meaning lost
- Linguistic inaccuracies or unnaturalness
- Inappropriate for intended context
- Major improvements needed

## Important Notes

- Evaluation is blind - you won't know which system produced which translation
- Focus on the translation quality, not your preference for either system
- Consider both traditional cultural accuracy and modern applicability
- Your expertise is invaluable - trust your cultural and linguistic knowledge
- Take breaks between sessions to maintain evaluation quality

## Contact Information

For questions or clarifications during evaluation:
- Project Lead: [Contact Information]
- Technical Support: [Contact Information]
- Cultural Consultation: [Contact Information]

Thank you for your valuable contribution to preserving and modernizing Kikuyu cultural heritage through technology!
"""
    
    def _create_evaluation_protocol(self) -> str:
        """Create evaluation session protocol."""
        return """# Evaluation Session Protocol

## Session Setup

### Pre-Session (5 minutes)
1. Verify expert comfort and readiness
2. Review evaluation criteria and scale
3. Confirm understanding of blind evaluation process
4. Set up evaluation materials and recording (if consented)

### Session Structure (45-60 minutes)
1. **Warm-up Phase** (5 minutes)
   - Review 1-2 example evaluations
   - Clarify any questions about criteria
   
2. **Evaluation Phase** (35-45 minutes)
   - Evaluate 8-10 proverb translation pairs
   - 4-5 minutes per proverb pair maximum
   - Encourage thinking aloud for qualitative insights
   
3. **Break** (5-10 minutes if needed)
   - Refresh and maintain focus
   - Discuss any emerging patterns or concerns

### Post-Session (5 minutes)
1. Review completed evaluations for completeness
2. Gather feedback on evaluation process
3. Schedule next session if applicable
4. Thank expert for participation

## Quality Control

### During Session
- Monitor for evaluator fatigue
- Ensure consistent application of criteria
- Note any cultural insights or explanations
- Address questions or concerns immediately

### After Session
- Review evaluations for completeness
- Check for consistency patterns
- Document session notes and insights
- Prepare materials for next session

## Inter-Rater Reliability

### Overlap Samples
- Include 2-3 overlapping proverbs between experts
- Calculate agreement scores
- Identify areas needing clarification

### Consensus Building
- Review significant disagreements
- Facilitate discussion for consensus
- Document reasoning for final decisions

## Documentation

### Required Records
- Evaluation scores and comments
- Session duration and conditions
- Expert feedback and insights
- Technical issues or concerns
- Cultural context explanations

### Privacy and Consent
- Obtain consent for recording (optional)
- Anonymize expert identifiers
- Secure storage of evaluation data
- Respect confidentiality preferences
"""
    
    def create_evaluation_metrics(self) -> str:
        """Create comprehensive evaluation metrics framework."""
        
        logger.info("📊 Creating evaluation metrics framework...")
        
        metrics_framework = {
            "primary_metrics": {
                "cultural_faithfulness_score": {
                    "description": "Average cultural faithfulness across all evaluations",
                    "calculation": "mean(expert_cultural_faithfulness)",
                    "range": [1, 5],
                    "target": "≥ 4.0"
                },
                "translation_accuracy_score": {
                    "description": "Average translation accuracy across all evaluations", 
                    "calculation": "mean(expert_translation_accuracy)",
                    "range": [1, 5],
                    "target": "≥ 4.0"
                },
                "overall_quality_score": {
                    "description": "Weighted average of all quality dimensions",
                    "calculation": "0.4*cultural_faithfulness + 0.3*translation_accuracy + 0.2*business_relevance + 0.1*fluency",
                    "range": [1, 5],
                    "target": "≥ 4.0"
                }
            },
            "comparative_metrics": {
                "og_rag_vs_raw_llm": {
                    "preference_rate": "% of cases where OG-RAG preferred",
                    "quality_difference": "mean(og_rag_scores) - mean(raw_llm_scores)",
                    "cultural_advantage": "cultural_faithfulness difference",
                    "accuracy_advantage": "translation_accuracy difference"
                }
            },
            "reliability_metrics": {
                "inter_rater_agreement": {
                    "description": "Agreement between multiple experts",
                    "calculation": "Krippendorff's alpha or ICC",
                    "target": "≥ 0.7"
                },
                "internal_consistency": {
                    "description": "Consistency within expert evaluations",
                    "calculation": "Cronbach's alpha",
                    "target": "≥ 0.8"
                }
            },
            "efficiency_metrics": {
                "evaluation_time": {
                    "description": "Average time per evaluation",
                    "target": "≤ 5 minutes per proverb"
                },
                "expert_fatigue": {
                    "description": "Quality degradation over session",
                    "measurement": "Score variance by session position"
                }
            }
        }
        
        # Save metrics framework
        metrics_file = self.metrics_dir / "evaluation_metrics_framework.json"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics_framework, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Created evaluation metrics framework: {metrics_file}")
        return str(metrics_file)
    
    def create_benchmark_metadata(self, benchmark_file: str) -> Dict[str, Any]:
        """Create comprehensive metadata about the evaluation benchmark."""
        
        logger.info("📋 Creating benchmark metadata...")
        
        benchmark_df = pd.read_csv(benchmark_file)
        
        metadata = {
            "benchmark_info": {
                "version": "1.0",
                "creation_date": datetime.now().isoformat(),
                "total_evaluation_cases": len(benchmark_df),
                "data_source": str(self.proverbs_file),
                "benchmark_file": benchmark_file
            },
            "evaluation_framework": self.evaluation_config,
            "data_statistics": {
                "proverbs_with_kikuyu_text": len(benchmark_df[benchmark_df['kikuyu_text'].notna()]),
                "proverbs_with_initial_translation": len(benchmark_df[benchmark_df['initial_translation'].notna()]),
                "proverbs_with_cultural_meaning": len(benchmark_df[benchmark_df['cultural_meaning'].notna()]),
                "average_kikuyu_text_length": benchmark_df['kikuyu_text'].astype(str).str.len().mean(),
                "average_translation_length": benchmark_df['initial_translation'].astype(str).str.len().mean()
            },
            "quality_targets": {
                "minimum_expert_score": 4.0,
                "target_cultural_faithfulness": 4.2,
                "target_translation_accuracy": 4.0,
                "target_overall_quality": 4.0,
                "minimum_inter_rater_agreement": 0.7
            },
            "evaluation_status": {
                "benchmark_created": True,
                "templates_created": True,
                "expert_recruitment": "pending",
                "evaluation_sessions": "pending",
                "data_collection": "pending",
                "analysis": "pending"
            }
        }
        
        # Save metadata
        metadata_file = self.benchmark_dir / "benchmark_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Created benchmark metadata: {metadata_file}")
        return metadata
    
    def generate_benchmark_report(self, metadata: Dict[str, Any]) -> str:
        """Generate comprehensive benchmark creation report."""
        
        report_content = f"""# thiLLMo Evaluation Benchmark Creation Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Benchmark Overview

### Framework Design
- **Approach**: Comparative evaluation (OG-RAG vs Raw LLM vs Expert Gold Standard)
- **Evaluation Type**: Human expert assessment with blind evaluation
- **Quality Dimensions**: 4 weighted dimensions (Cultural Faithfulness: 40%, Translation Accuracy: 30%, Business Relevance: 20%, Overall Fluency: 10%)

### Dataset Statistics
- **Total Evaluation Cases**: {metadata['benchmark_info']['total_evaluation_cases']}
- **Data Source**: {metadata['benchmark_info']['data_source']}
- **Proverbs with Kikuyu Text**: {metadata['data_statistics']['proverbs_with_kikuyu_text']}
- **Proverbs with Initial Translations**: {metadata['data_statistics']['proverbs_with_initial_translation']}
- **Average Kikuyu Text Length**: {metadata['data_statistics']['average_kikuyu_text_length']:.1f} characters
- **Average Translation Length**: {metadata['data_statistics']['average_translation_length']:.1f} characters

## Quality Framework

### Evaluation Dimensions
{self._format_quality_dimensions()}

### Expert Qualifications
- Native or near-native Kikuyu speakers
- Academic background in African studies, linguistics, or related fields
- Familiarity with traditional Kikuyu culture and proverbs
- Preferably PhD-level with published research

### Quality Targets
- **Minimum Expert Score**: {metadata['quality_targets']['minimum_expert_score']}
- **Target Cultural Faithfulness**: {metadata['quality_targets']['target_cultural_faithfulness']}
- **Target Translation Accuracy**: {metadata['quality_targets']['target_translation_accuracy']}
- **Minimum Inter-Rater Agreement**: {metadata['quality_targets']['minimum_inter_rater_agreement']}

## Evaluation Process

### Session Structure
- **Maximum proverbs per session**: 10
- **Session duration**: 45-60 minutes
- **Break duration**: 15 minutes
- **Maximum daily sessions**: 3

### Quality Control
- Blind evaluation (systems anonymized)
- Randomized presentation order
- Multiple evaluators for reliability
- Inter-rater reliability measurement
- Consensus building for disagreements

## Next Steps

### Phase 1: Expert Recruitment (Immediate)
1. Identify qualified Kikuyu cultural experts
2. Recruit 3-5 expert evaluators
3. Conduct evaluator training and calibration
4. Pilot test with small sample

### Phase 2: System Implementation (Parallel)
1. Implement OG-RAG translation system
2. Generate OG-RAG translations for benchmark proverbs
3. Generate Raw LLM translations for comparison
4. Prepare evaluation materials with anonymized systems

### Phase 3: Data Collection (After Phases 1-2)
1. Conduct expert evaluation sessions
2. Collect detailed quality assessments
3. Monitor inter-rater reliability
4. Build consensus for final gold standard

### Phase 4: Analysis and Reporting (Final)
1. Calculate comparative performance metrics
2. Analyze cultural faithfulness preservation
3. Generate comprehensive evaluation report
4. Publish benchmark dataset for research community

## Files Created

### Benchmark Structure
- `{metadata['benchmark_info']['benchmark_file']}` - Main benchmark dataset
- `{self.benchmark_dir}/benchmark_metadata.json` - Comprehensive metadata

### Evaluation Templates
- `{self.templates_dir}/expert_evaluation_template.xlsx` - Expert evaluation spreadsheet
- `{self.templates_dir}/expert_evaluation_instructions.md` - Detailed instructions
- `{self.templates_dir}/evaluation_session_protocol.md` - Session protocol

### Metrics Framework
- `{self.metrics_dir}/evaluation_metrics_framework.json` - Metrics definitions

## Success Criteria

The benchmark will be considered successful if:
1. **Cultural Faithfulness**: OG-RAG achieves ≥4.2 average score vs Raw LLM
2. **Translation Quality**: Overall quality score ≥4.0 for OG-RAG system
3. **Expert Agreement**: Inter-rater reliability ≥0.7 (substantial agreement)
4. **Comparative Advantage**: OG-RAG significantly outperforms Raw LLM (p<0.05)

## Expected Outcomes

Based on ontology-grounded RAG research, we expect:
- **55% increase** in factual accuracy through ontology grounding
- **40% improvement** in response correctness
- **Superior cultural preservation** compared to raw LLM translation
- **Measurable quality improvement** in business context applications

---

*This benchmark framework provides the foundation for rigorous evaluation of culturally faithful AI translation systems for Kikuyu proverbs.*
"""
        
        # Save report
        report_file = self.output_dir / f"benchmark_creation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"📄 Generated benchmark creation report: {report_file}")
        return str(report_file)
    
    def _format_quality_dimensions(self) -> str:
        """Format quality dimensions for report."""
        formatted = []
        for dim_name, dim_config in self.evaluation_config['quality_dimensions'].items():
            formatted.append(f"**{dim_name.replace('_', ' ').title()}** (Weight: {int(dim_config['weight']*100)}%)")
            formatted.append(f"- {dim_config['description']}")
            formatted.append(f"- Scale: {dim_config['scale']}")
            formatted.append("")
        return "\n".join(formatted)
    
    def create_complete_benchmark(self) -> Dict[str, str]:
        """Create complete evaluation benchmark framework."""
        
        logger.info("🚀 Creating complete evaluation benchmark framework...")
        
        results = {}
        
        # 1. Create benchmark structure
        benchmark_file = self.create_benchmark_structure()
        results['benchmark_file'] = benchmark_file
        
        # 2. Create evaluation templates
        templates = self.create_evaluation_templates()
        results.update(templates)
        
        # 3. Create metrics framework
        metrics_file = self.create_evaluation_metrics()
        results['metrics_framework'] = metrics_file
        
        # 4. Create metadata
        metadata = self.create_benchmark_metadata(benchmark_file)
        results['metadata'] = metadata
        
        # 5. Generate report
        report_file = self.generate_benchmark_report(metadata)
        results['report'] = report_file
        
        logger.info("✅ Complete evaluation benchmark framework created!")
        logger.info(f"📊 {metadata['benchmark_info']['total_evaluation_cases']} evaluation cases prepared")
        logger.info(f"📁 Output directory: {self.output_dir}")
        
        return results


def main():
    """Create comprehensive evaluation benchmark framework."""
    
    parser = argparse.ArgumentParser(description='Create evaluation benchmark framework for thiLLMo')
    parser.add_argument('--proverbs-file', default='data/proverbs/extracted_proverbs.csv',
                       help='Path to proverbs CSV file')
    parser.add_argument('--output-dir', default='data/evaluation',
                       help='Output directory for benchmark files')
    
    args = parser.parse_args()
    
    try:
        # Create benchmark creator
        creator = EvaluationBenchmarkCreator(args.proverbs_file)
        
        # Create complete benchmark framework
        results = creator.create_complete_benchmark()
        
        # Print summary
        print("\n" + "="*80)
        print("🎯 EVALUATION BENCHMARK FRAMEWORK CREATED SUCCESSFULLY!")
        print("="*80)
        print(f"📊 Total Evaluation Cases: {results['metadata']['benchmark_info']['total_evaluation_cases']}")
        print(f"📁 Output Directory: {creator.output_dir}")
        print("\n📋 Key Files Created:")
        print(f"   • Benchmark Dataset: {results['benchmark_file']}")
        print(f"   • Evaluation Templates: {results['evaluation_template']}")
        print(f"   • Expert Instructions: {results['instructions']}")
        print(f"   • Session Protocol: {results['protocol']}")
        print(f"   • Metrics Framework: {results['metrics_framework']}")
        print(f"   • Creation Report: {results['report']}")
        
        print("\n🎯 Next Steps:")
        print("   1. Review benchmark framework and evaluation criteria")
        print("   2. Recruit qualified Kikuyu cultural experts")
        print("   3. Implement OG-RAG and Raw LLM translation systems")
        print("   4. Conduct expert evaluation sessions")
        print("   5. Analyze results and publish benchmark")
        
        print("\n✅ Framework ready for expert recruitment and system implementation!")
        
    except Exception as e:
        logger.error(f"❌ Failed to create evaluation benchmark: {e}")
        raise


if __name__ == "__main__":
    main()