#!/usr/bin/env python3
"""
Script to run the Enhanced Translation Comparison System with sample data.
Creates sample benchmark data and demonstrates the full pipeline.
"""

import pandas as pd
from pathlib import Path
import asyncio
import sys
import json
import logging

# Check for required packages
try:
    import openai
    import google.generativeai as genai
    TRANSLATION_CLIENTS_AVAILABLE = True
except ImportError as e:
    TRANSLATION_CLIENTS_AVAILABLE = False
    print(f"⚠️ Warning: Some translation clients not available: {e}")
    print("   Install missing packages: pip install openai google-generativeai")

# Add src to path for evaluation framework imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from scripts.enhanced_translation_comparison import EnhancedTranslationComparisonSystem
    COMPARISON_SYSTEM_AVAILABLE = True
except ImportError as e:
    COMPARISON_SYSTEM_AVAILABLE = False
    print(f"❌ Error: Could not import comparison system: {e}")
    print("   Please ensure all dependencies are installed: pip install -r requirements.txt")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_sample_benchmark_data():
    """Create sample benchmark data with proper Kikuyu proverbs."""
    
    sample_data = [
        {
            'proverb_id': 'KP001',
            'kikuyu_proverb': 'Mũndũ akua na ũkĩa',
            'expert_translation': 'A person dies from overeating',
            'expert_cultural_meaning': 'Warns against excess and the importance of moderation in all aspects of life',
            'expert_business_relevance': 'In business: Avoid overexpansion and maintain sustainable growth practices'
        },
        {
            'proverb_id': 'KP002',
            'kikuyu_proverb': 'Kĩhonia kĩa njamba kĩrĩa kĩndũ',
            'expert_translation': 'A hyena\'s friend is another hyena',
            'expert_cultural_meaning': 'People naturally associate with those who share similar values and characteristics',
            'expert_business_relevance': 'Business partnerships work best when values and goals are aligned'
        },
        {
            'proverb_id': 'KP003',
            'kikuyu_proverb': 'Njũgũma ĩrĩa ĩtatuĩkaga mũti',
            'expert_translation': 'The seed that doesn\'t become a tree',
            'expert_cultural_meaning': 'Emphasizes the importance of nurturing potential and creating conditions for growth',
            'expert_business_relevance': 'Investment in people and ideas requires patience and proper conditions to flourish'
        },
        {
            'proverb_id': 'KP004',
            'kikuyu_proverb': 'Mũgambo wa nyoni ũiguagwo rũciinĩ',
            'expert_translation': 'The bird\'s song is heard in the morning',
            'expert_cultural_meaning': 'Early action and preparation lead to the best opportunities',
            'expert_business_relevance': 'Early market entry and preparation give competitive advantages'
        },
        {
            'proverb_id': 'KP005',
            'kikuyu_proverb': 'Kanyaga karĩa kau',
            'expert_translation': 'Step on what is on the ground',
            'expert_cultural_meaning': 'Use available resources wisely rather than yearning for what you don\'t have',
            'expert_business_relevance': 'Successful businesses work with available resources and optimize what they have'
        },
        {
            'proverb_id': 'KP006',
            'kikuyu_proverb': 'Gĩkeno kĩa mũndũ nĩ kĩrĩa ekwenda',
            'expert_translation': 'A person\'s joy is what they desire',
            'expert_cultural_meaning': 'True satisfaction comes from pursuing one\'s authentic goals and values',
            'expert_business_relevance': 'Business success should align with personal values and meaningful objectives'
        },
        {
            'proverb_id': 'KP007',
            'kikuyu_proverb': 'Mũgũnda ũtarĩmwo ndũciaraga',
            'expert_translation': 'An untilled field bears nothing',
            'expert_cultural_meaning': 'Success requires consistent effort and preparation',
            'expert_business_relevance': 'Business requires continuous investment in planning and execution'
        },
        {
            'proverb_id': 'KP008',
            'kikuyu_proverb': 'Ũthoni wa mũndũ nĩ kĩrĩa endaga',
            'expert_translation': 'A person\'s wealth is what they want',
            'expert_cultural_meaning': 'True wealth is defined by individual values and priorities',
            'expert_business_relevance': 'Business value should be measured by meaningful metrics not just profit'
        },
        {
            'proverb_id': 'KP009',
            'kikuyu_proverb': 'Kĩrĩa kĩgooka na maai kĩthiiaga na maai',
            'expert_translation': 'What comes with water goes with water',
            'expert_cultural_meaning': 'Easy gains can be easily lost without proper foundation',
            'expert_business_relevance': 'Quick business wins need sustainable foundations to maintain success'
        },
        {
            'proverb_id': 'KP010',
            'kikuyu_proverb': 'Mũndũ akĩrĩra ndagĩaga na marĩa',
            'expert_translation': 'When a person eats they are not alone with food',
            'expert_cultural_meaning': 'Sharing resources strengthens community bonds and ensures collective prosperity',
            'expert_business_relevance': 'Collaborative business approaches often yield better long-term results'
        }
    ]
    
    # Create output directory
    output_dir = Path("data/evaluation/benchmark")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save sample benchmark data
    sample_df = pd.DataFrame(sample_data)
    sample_file = output_dir / "sample_translation_benchmark.csv"
    sample_df.to_csv(sample_file, index=False, encoding='utf-8')
    
    logger.info(f"✅ Created sample benchmark data: {sample_file}")
    logger.info(f"📊 Sample contains {len(sample_df)} Kikuyu proverbs")
    
    return str(sample_file)

async def run_demo_comparison():
    """Run demonstration of the Enhanced Translation Comparison System."""
    
    logger.info("🚀 Starting Enhanced Translation Comparison System Demo")
    
    # Step 1: Create sample benchmark data
    logger.info("Step 1: Creating sample benchmark data...")
    sample_benchmark_file = create_sample_benchmark_data()
    
    # Step 2: Initialize comparison system
    logger.info("Step 2: Initializing comparison system...")
    comparison_system = EnhancedTranslationComparisonSystem()
    
    try:
        # Step 3: Generate OG-RAG translations
        logger.info("Step 3: Generating OG-RAG translations with metadata...")
        og_rag_df = await comparison_system.generate_og_rag_translations_with_metadata(
            sample_benchmark_file
        )
        
        # Step 4: Generate Raw LLM translations
        logger.info("Step 4: Generating raw LLM translations...")
        raw_llm_df = await comparison_system.generate_raw_llm_translations_for_comparison(
            sample_benchmark_file
        )
        
        # Step 5: Create comprehensive comparison dataset
        logger.info("Step 5: Creating comprehensive comparison dataset...")
        comparison_df = await comparison_system.create_comprehensive_comparison_dataset()
        
        # Step 6: Run LLM as a Judge evaluation (if LLM clients available)
        if comparison_system.llm_evaluator.configurator.primary_provider:
            logger.info("Step 6: Running LLM as a Judge evaluation...")
            llm_judge_results = await comparison_system.run_llm_judge_evaluation()
        else:
            logger.warning("Step 6: Skipping LLM Judge evaluation - no LLM providers configured")
            llm_judge_results = {"status": "skipped", "reason": "No LLM providers available"}
        
        # Step 7: Generate comprehensive summary
        logger.info("Step 7: Generating summary report...")
        summary_report = comparison_system._generate_pipeline_summary(
            og_rag_df, raw_llm_df, comparison_df, llm_judge_results
        )
        
        # Display results
        print("\\n" + "="*60)
        print("🎯 ENHANCED TRANSLATION COMPARISON DEMO RESULTS")
        print("="*60)
        print(f"📊 Total proverbs processed: {len(comparison_df)}")
        print(f"🔄 OG-RAG translations: {len(og_rag_df)}")
        print(f"🤖 Raw LLM translations: {len(raw_llm_df)}")
        print(f"📋 Comparison pairs created: {len(comparison_df)}")
        
        if comparison_df['evaluation_priority'].value_counts().to_dict():
            priority_counts = comparison_df['evaluation_priority'].value_counts().to_dict()
            print(f"🎯 High priority evaluations: {priority_counts.get('high', 0)}")
            print(f"🔍 Medium priority evaluations: {priority_counts.get('medium', 0)}")
            print(f"📝 Low priority evaluations: {priority_counts.get('low', 0)}")
        
        print(f"\\n💾 Output directory: {comparison_system.output_dir}")
        print("\\n📁 Generated files:")
        for file_type, file_path in summary_report["output_files"].items():
            if Path(file_path).exists():
                print(f"  ✅ {file_type}: {file_path}")
            else:
                print(f"  ❌ {file_type}: {file_path}")
        
        if llm_judge_results.get("status") != "skipped":
            print("\\n🤖 LLM Judge Evaluation: ✅ Completed")
        else:
            print("\\n🤖 LLM Judge Evaluation: ⚠️ Skipped (configure API keys in .env)")
        
        print("\\n🎉 Demo completed successfully!")
        print("\\n💡 Next steps:")
        print("  1. Configure API keys in .env file for full LLM evaluation")
        print("  2. Replace sample data with actual Kikuyu proverb dataset")
        print("  3. Integrate with your Neo4j ontology for enhanced context retrieval")
        print("  4. Run comparative analysis on larger datasets")
        
        return summary_report
        
    except Exception as e:
        logger.error(f"Demo execution failed: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        return None

def main():
    """Main demo runner."""
    print("🌟 Enhanced Translation Comparison System Demo")
    print("This demo shows the integration of LLM as a Judge with translation comparison.")
    print()
    
    # Check for required dependencies
    if not COMPARISON_SYSTEM_AVAILABLE:
        print("❌ Cannot run demo - comparison system not available")
        print("💡 Install dependencies: pip install -r requirements.txt")
        return 1
    
    if not TRANSLATION_CLIENTS_AVAILABLE:
        print("⚠️ Running demo in limited mode - some translation clients not available")
        print("💡 For full functionality: pip install openai google-generativeai")
        print()
    
    try:
        summary = asyncio.run(run_demo_comparison())
        
        if summary:
            print("\\n✅ Demo completed successfully!")
            return 0
        else:
            print("\\n❌ Demo failed - check logs for details")
            return 1
            
    except KeyboardInterrupt:
        print("\\n🛑 Demo interrupted by user")
        return 130
    except Exception as e:
        print(f"\\n💥 Demo failed with error: {e}")
        if "--verbose" in sys.argv:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())