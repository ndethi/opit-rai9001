#!/usr/bin/env python3
"""
LLM as a Judge Evaluation Interface for thiLLMo

Unified interface for running LLM-based evaluation of Kikuyu proverb translations
with support for single evaluations, comparative analysis, and ensemble assessment.
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path
import json

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from evaluation.llm_config import DynamicLLMConfigurator
from evaluation.llm_judge import LLMJudgeEvaluator
from evaluation.comparative_pipeline import ComparativeEvaluationPipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_argument_parser():
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="LLM as a Judge Evaluation System for thiLLMo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test configuration
  python run_llm_evaluation.py --mode config --show-summary
  
  # Single translation evaluation
  python run_llm_evaluation.py --mode single \\
    --kikuyu "Mũndũ mũgeni nĩ kĩara kĩa kũingĩrwo nĩ maĩ" \\
    --translation "A visitor is like a vessel that should be filled with water" \\
    --system og_rag
  
  # Comparative evaluation
  python run_llm_evaluation.py --mode comparative \\
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \\
    --sample-size 10 --enable-ensemble
  
  # Full pipeline evaluation
  python run_llm_evaluation.py --mode pipeline \\
    --benchmark-file data/evaluation/benchmark/translation_evaluation_benchmark.csv \\
    --output-dir outputs/evaluation/full_run
        """
    )
    
    # Mode selection
    parser.add_argument(
        '--mode', 
        choices=['config', 'single', 'comparative', 'pipeline'],
        required=True,
        help='Evaluation mode to run'
    )
    
    # Configuration options
    parser.add_argument('--config-file', help='Path to configuration .env file')
    parser.add_argument('--show-summary', action='store_true', help='Show configuration summary')
    
    # Single evaluation options
    parser.add_argument('--kikuyu', help='Kikuyu proverb text')
    parser.add_argument('--translation', help='English translation to evaluate')
    parser.add_argument('--system', choices=['og_rag', 'raw_llm'], help='Translation system type')
    parser.add_argument('--proverb-id', help='Proverb identifier')
    
    # Comparative and pipeline options
    parser.add_argument('--benchmark-file', help='Path to benchmark CSV file')
    parser.add_argument('--sample-size', type=int, help='Number of evaluations to run (default: all)')
    parser.add_argument('--enable-ensemble', action='store_true', help='Enable ensemble evaluation')
    parser.add_argument('--output-dir', help='Output directory for results')
    
    # General options
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode')
    
    return parser

async def run_config_mode(args):
    """Run configuration testing mode."""
    print("=== LLM as a Judge Configuration ===\\n")
    
    try:
        configurator = DynamicLLMConfigurator(args.config_file)
        
        if args.show_summary:
            config_summary = configurator.get_configuration_summary()
            print(json.dumps(config_summary, indent=2))
        else:
            # Basic configuration check
            primary_model = configurator.get_primary_model()
            if primary_model:
                print(f"✅ Primary Model: {primary_model.provider.value}:{primary_model.model_name}")
            else:
                print("❌ No primary model configured")
                
            fallback_models = configurator.get_fallback_models()
            if fallback_models:
                print(f"✅ Fallback Models: {len(fallback_models)} available")
                for model in fallback_models:
                    print(f"   - {model.provider.value}:{model.model_name}")
            else:
                print("⚠️  No fallback models configured")
                
            ensemble_models = configurator.get_ensemble_models()
            print(f"🔧 Ensemble Models: {len(ensemble_models)} available")
            
            print(f"\\n📊 Evaluation Weights:")
            eval_config = configurator.evaluation_config
            print(f"   Cultural Faithfulness: {eval_config.cultural_weight}")
            print(f"   Translation Accuracy: {eval_config.translation_weight}")
            print(f"   Business Relevance: {eval_config.business_weight}")
            print(f"   Overall Fluency: {eval_config.fluency_weight}")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return 1
        
    return 0

async def run_single_mode(args):
    """Run single translation evaluation mode."""
    if not all([args.kikuyu, args.translation, args.system]):
        print("❌ Single mode requires --kikuyu, --translation, and --system arguments")
        return 1
        
    print("=== Single Translation Evaluation ===\\n")
    
    try:
        evaluator = LLMJudgeEvaluator(args.config_file)
        
        print(f"Evaluating {args.system.upper()} translation...")
        print(f"Kikuyu: {args.kikuyu}")
        print(f"English: {args.translation}\\n")
        
        evaluation = await evaluator.evaluate_single_translation(
            args.kikuyu,
            args.translation,
            args.system,
            args.proverb_id or "single_eval"
        )
        
        print("=== Evaluation Results ===")
        print(f"Weighted Score: {evaluation.weighted_score:.2f}/5.0")
        print(f"Cultural Faithfulness: {evaluation.evaluation_criteria.cultural_faithfulness:.1f}/5.0")
        print(f"Translation Accuracy: {evaluation.evaluation_criteria.translation_accuracy:.1f}/5.0")
        print(f"Business Relevance: {evaluation.evaluation_criteria.business_relevance:.1f}/5.0")
        print(f"Overall Fluency: {evaluation.evaluation_criteria.overall_fluency:.1f}/5.0")
        print(f"Confidence: {evaluation.evaluation_criteria.confidence_score:.2f}")
        print(f"\\nDetailed Feedback:")
        print(evaluation.evaluation_criteria.detailed_feedback)
        
        # Save result if output directory specified
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            result_file = output_dir / f"single_evaluation_{args.proverb_id or 'result'}.json"
            with open(result_file, 'w') as f:
                import dataclasses
                result_dict = dataclasses.asdict(evaluation)
                result_dict['evaluation_timestamp'] = evaluation.evaluation_timestamp.isoformat()
                json.dump(result_dict, f, indent=2)
                
            print(f"\\n💾 Results saved to {result_file}")
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return 1
        
    return 0

async def run_comparative_mode(args):
    """Run comparative evaluation mode."""
    if not args.benchmark_file:
        print("❌ Comparative mode requires --benchmark-file argument")
        return 1
        
    print("=== Comparative Evaluation ===\\n")
    
    try:
        pipeline = ComparativeEvaluationPipeline(args.benchmark_file, args.config_file)
        
        print(f"Loading benchmark from: {args.benchmark_file}")
        if args.sample_size:
            print(f"Sample size: {args.sample_size}")
        print(f"Ensemble evaluation: {'Enabled' if args.enable_ensemble else 'Disabled'}\\n")
        
        results = await pipeline.run_comparative_evaluation(
            sample_size=args.sample_size,
            enable_ensemble=args.enable_ensemble
        )
        
        print("=== Evaluation Complete ===")
        print(f"Total evaluations: {results['evaluation_metadata']['total_evaluations']}")
        
        # Show key findings
        if 'key_findings' in results:
            print("\\n📊 Key Findings:")
            for finding in results['key_findings']:
                print(f"  • {finding}")
                
        # Show recommendations
        if 'recommendations' in results:
            print("\\n💡 Recommendations:")
            for rec in results['recommendations'][:3]:  # Show first 3
                print(f"  • {rec}")
                
        # Statistical summary
        stats = results.get('statistical_analysis', {})
        if 'overall_scores' in stats:
            og_rag_mean = stats['overall_scores']['og_rag']['mean']
            raw_llm_mean = stats['overall_scores']['raw_llm']['mean']
            print(f"\\n📈 Mean Scores:")
            print(f"  OG-RAG: {og_rag_mean:.2f}")
            print(f"  Raw LLM: {raw_llm_mean:.2f}")
            
        print(f"\\n💾 Full results saved to: outputs/evaluation/comparative/")
        
    except Exception as e:
        print(f"❌ Comparative evaluation failed: {e}")
        return 1
        
    return 0

async def run_pipeline_mode(args):
    """Run full pipeline evaluation mode."""
    print("=== Full Pipeline Evaluation ===\\n")
    
    # This would integrate with the full thiLLMo pipeline
    # For now, delegate to comparative mode
    return await run_comparative_mode(args)

async def main():
    """Main entry point."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
        
    # Route to appropriate mode
    try:
        if args.mode == 'config':
            return await run_config_mode(args)
        elif args.mode == 'single':
            return await run_single_mode(args)
        elif args.mode == 'comparative':
            return await run_comparative_mode(args)
        elif args.mode == 'pipeline':
            return await run_pipeline_mode(args)
        else:
            print(f"❌ Unknown mode: {args.mode}")
            return 1
            
    except KeyboardInterrupt:
        print("\\n🛑 Evaluation interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)