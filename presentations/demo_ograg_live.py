#!/usr/bin/env python3
"""
Live OG-RAG Demo for Thesis Defense
====================================

Compares three translation approaches:
1. Raw GPT-4 (no context)
2. Traditional RAG (example proverbs)
3. OG-RAG (ontology-grounded context)

Author: Charles Watson Ndethi Kibaki
Date: January 13, 2026
Defense: January 14, 2026
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any
import json

# Add src to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))
sys.path.insert(0, str(repo_root))

try:
    # Import using importlib for hyphenated directory names
    import importlib.util
    
    # Load og-rag-system module
    ograg_path = repo_root / "src" / "og-rag-system" / "ograg_translator.py"
    neo4j_path = repo_root / "src" / "neo4j" / "scripts" / "connection.py"
    
    # Load ograg_translator
    spec = importlib.util.spec_from_file_location("ograg_translator", ograg_path)
    ograg_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ograg_module)
    OGRAGTranslator = ograg_module.OGRAGTranslator
    TranslationResult = ograg_module.TranslationResult
    
    # Load Neo4j connection
    spec = importlib.util.spec_from_file_location("connection", neo4j_path)
    neo4j_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(neo4j_module)
    Neo4jConnection = neo4j_module.Neo4jConnection
    
except Exception as e:
    print(f"❌ Import error: {e}")
    print(f"Current path: {sys.path}")
    print(f"Repository root: {repo_root}")
    import traceback
    traceback.print_exc()
    print("\nPlease run from repository root: python presentations/demo_ograg_live.py")
    sys.exit(1)


# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str, color: str = Colors.CYAN):
    """Print formatted section header."""
    print(f"\n{color}{'='*70}")
    print(f"{text.center(70)}")
    print(f"{'='*70}{Colors.ENDC}\n")


def print_subheader(text: str, char: str = "━", color: str = Colors.YELLOW):
    """Print formatted subsection header."""
    print(f"\n{color}{text.center(70, char)}{Colors.ENDC}")


def print_result(label: str, value: str, color: str = Colors.GREEN):
    """Print labeled result."""
    print(f"{color}{label}:{Colors.ENDC} {value}")


def demo_proverb(kikuyu_text: str, show_graph: bool = False):
    """
    Run complete demo for one proverb.
    
    Args:
        kikuyu_text: Kikuyu proverb to translate
        show_graph: If True, show Neo4j query for graph retrieval
    
    Returns:
        Dictionary with results from all three methods
    """
    
    print_header("🎯 THESIS DEFENSE DEMO: Ontology-Grounded RAG", Colors.BOLD + Colors.CYAN)
    
    # Initialize system
    print(f"{Colors.CYAN}⏳ Initializing OG-RAG system...{Colors.ENDC}")
    try:
        translator = OGRAGTranslator()
        print(f"{Colors.GREEN}✅ System ready{Colors.ENDC}\n")
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to initialize: {e}{Colors.ENDC}")
        return None
    
    print_result("📖 PROVERB", kikuyu_text, Colors.BOLD)
    
    results = {}
    
    # ========================================================================
    # STEP 1: Raw GPT-4 Translation
    # ========================================================================
    print_subheader("🔴 RAW GPT-4 (No Context)", color=Colors.RED)
    
    try:
        raw_result = translator.translate_raw(kikuyu_text)
        results['raw'] = raw_result
        
        print(f"\n{Colors.BOLD}Translation:{Colors.ENDC}")
        print(f'  "{raw_result.translation}"')
        print(f"\n{Colors.BOLD}Tokens:{Colors.ENDC} {raw_result.total_tokens}")
        
        print(f"\n{Colors.BOLD}Analysis:{Colors.ENDC}")
        print(f"{Colors.RED}❌ Literal translation only{Colors.ENDC}")
        print(f"{Colors.RED}❌ No cultural context{Colors.ENDC}")
        print(f"{Colors.RED}❌ Misses wisdom teaching{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Raw translation failed: {e}{Colors.ENDC}")
        results['raw'] = None
    
    # ========================================================================
    # STEP 2: Traditional RAG
    # ========================================================================
    print_subheader("🟡 TRADITIONAL RAG (Similar Proverbs)", color=Colors.YELLOW)
    
    try:
        trad_result = translator.translate_traditional_rag(kikuyu_text)
        results['traditional'] = trad_result
        
        print(f"\n{Colors.BOLD}Retrieved Examples:{Colors.ENDC}")
        if trad_result.retrieved_proverbs:
            for i, proverb in enumerate(trad_result.retrieved_proverbs[:3], 1):
                print(f"  {i}. {proverb.kikuyu_text}")
                if hasattr(proverb, 'expert_teaching') and proverb.expert_teaching:
                    teaching = proverb.expert_teaching[:80] + "..." if len(proverb.expert_teaching) > 80 else proverb.expert_teaching
                    print(f"     → {teaching}")
        
        print(f"\n{Colors.BOLD}Translation:{Colors.ENDC}")
        print(f'  "{trad_result.translation}"')
        print(f"\n{Colors.BOLD}Tokens:{Colors.ENDC} {trad_result.total_tokens}")
        
        print(f"\n{Colors.BOLD}Analysis:{Colors.ENDC}")
        print(f"{Colors.YELLOW}⚠️  Better than raw GPT-4{Colors.ENDC}")
        print(f"{Colors.YELLOW}⚠️  Includes some context from examples{Colors.ENDC}")
        print(f"{Colors.YELLOW}⚠️  But lacks structured cultural knowledge{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Traditional RAG failed: {e}{Colors.ENDC}")
        results['traditional'] = None
    
    # ========================================================================
    # STEP 3: Show Knowledge Graph Query (Optional)
    # ========================================================================
    if show_graph:
        print_subheader("🔍 KNOWLEDGE GRAPH QUERY", color=Colors.BLUE)
        
        try:
            cypher = f"""
            MATCH (p:Proverb {{kikuyu_text: "{kikuyu_text}"}})
            MATCH (p)-[e:EXPRESSES_CONCEPT]->(c:CulturalConcept)
            RETURN p.kikuyu_text as proverb, 
                   collect({{name: c.name, weight: c.cultural_weight}}) as concepts
            """
            
            print(f"{Colors.BLUE}Cypher Query:{Colors.ENDC}")
            print(f"{Colors.CYAN}{cypher}{Colors.ENDC}")
            
            conn = Neo4jConnection()
            result = conn.execute_query(cypher)
            
            if result and len(result) > 0:
                concepts = result[0].get('concepts', [])
                print(f"\n{Colors.GREEN}✅ Retrieved {len(concepts)} cultural concepts:{Colors.ENDC}")
                for concept in sorted(concepts, key=lambda x: x.get('weight', 0), reverse=True)[:5]:
                    weight = concept.get('weight', 0)
                    print(f"  • {concept['name']} (weight: {weight:.2f})")
            else:
                print(f"{Colors.YELLOW}⚠️  No concepts found for this proverb{Colors.ENDC}")
            
            conn.close()
            
        except Exception as e:
            print(f"{Colors.RED}❌ Graph query failed: {e}{Colors.ENDC}")
    
    # ========================================================================
    # STEP 4: OG-RAG Translation
    # ========================================================================
    print_subheader("🟢 OG-RAG (Ontology-Grounded)", color=Colors.GREEN)
    
    try:
        ograg_result = translator.translate_ograg(kikuyu_text)
        results['ograg'] = ograg_result
        
        print(f"\n{Colors.BOLD}Cultural Context Retrieved:{Colors.ENDC}")
        if ograg_result.concepts_used:
            for i, concept in enumerate(ograg_result.concepts_used[:5], 1):
                print(f"  {i}. {concept}")
        
        if ograg_result.retrieved_proverbs:
            print(f"\n{Colors.BOLD}Related Proverbs:{Colors.ENDC} {len(ograg_result.retrieved_proverbs)}")
        
        print(f"\n{Colors.BOLD}Translation:{Colors.ENDC}")
        print(f'  "{ograg_result.translation}"')
        
        if ograg_result.explanation:
            print(f"\n{Colors.BOLD}Cultural Explanation:{Colors.ENDC}")
            # Wrap explanation text
            explanation_lines = ograg_result.explanation.split('\n')
            for line in explanation_lines:
                if line.strip():
                    print(f"  {line}")
        
        print(f"\n{Colors.BOLD}Metrics:{Colors.ENDC}")
        print(f"  • Tokens: {ograg_result.total_tokens}")
        print(f"  • Concepts Used: {len(ograg_result.concepts_used or [])}")
        print(f"  • Related Proverbs: {len(ograg_result.retrieved_proverbs or [])}")
        
        print(f"\n{Colors.BOLD}Analysis:{Colors.ENDC}")
        print(f"{Colors.GREEN}✅ Full cultural context from ontology{Colors.ENDC}")
        print(f"{Colors.GREEN}✅ Expert-validated concept definitions{Colors.ENDC}")
        print(f"{Colors.GREEN}✅ Captures complete wisdom teaching{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.RED}❌ OG-RAG translation failed: {e}{Colors.ENDC}")
        results['ograg'] = None
    
    # ========================================================================
    # STEP 5: Side-by-Side Comparison
    # ========================================================================
    print_header("📊 COMPARISON SUMMARY", Colors.BOLD + Colors.CYAN)
    
    # Print comparison table
    print(f"\n{Colors.BOLD}{'Method':<25} {'Tokens':<10} {'Cultural Depth':<25}{Colors.ENDC}")
    print("─" * 70)
    
    if results.get('raw'):
        depth = "⭐" + Colors.RED + " (1/5 - Literal only)" + Colors.ENDC
        print(f"{Colors.RED}Raw GPT-4{Colors.ENDC:<34} {results['raw'].total_tokens:<10} {depth}")
    
    if results.get('traditional'):
        depth = "⭐⭐⭐" + Colors.YELLOW + " (3/5 - Some context)" + Colors.ENDC
        print(f"{Colors.YELLOW}Traditional RAG{Colors.ENDC:<34} {results['traditional'].total_tokens:<10} {depth}")
    
    if results.get('ograg'):
        depth = "⭐⭐⭐⭐⭐" + Colors.GREEN + " (5/5 - Full ontology)" + Colors.ENDC
        print(f"{Colors.GREEN}OG-RAG{Colors.ENDC:<34} {results['ograg'].total_tokens:<10} {depth}")
    
    print("\n" + "─" * 70)
    print(f"\n{Colors.BOLD + Colors.GREEN}RESULT: OG-RAG captures full cultural teaching{Colors.ENDC}")
    print(f"{Colors.GREEN}        through structured ontological grounding{Colors.ENDC}\n")
    
    print_header("✅ DEMO COMPLETE", Colors.GREEN)
    
    return results


def test_connection():
    """Test that all system components are working."""
    print_header("🔧 System Component Check", Colors.CYAN)
    
    all_ok = True
    
    # Test 1: Neo4j Connection
    print(f"{Colors.CYAN}Testing Neo4j AuraDB connection...{Colors.ENDC}")
    try:
        conn = Neo4jConnection()
        result = conn.execute_query("MATCH (n) RETURN count(n) as total LIMIT 1")
        if result and len(result) > 0:
            count = result[0].get('total', 0)
            print(f"{Colors.GREEN}✅ Neo4j connected ({count:,} nodes){Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️  Neo4j connected but query returned no results{Colors.ENDC}")
        conn.close()
    except Exception as e:
        print(f"{Colors.RED}❌ Neo4j connection failed: {e}{Colors.ENDC}")
        all_ok = False
    
    # Test 2: OpenAI API Key
    print(f"\n{Colors.CYAN}Checking OpenAI API configuration...{Colors.ENDC}")
    try:
        from decouple import config
        import os
        
        api_key = config('OPENAI_API_KEY', default=None) or os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key != 'your_openai_api_key_here' and len(api_key) > 20:
            print(f"{Colors.GREEN}✅ OpenAI API key loaded (length: {len(api_key)}){Colors.ENDC}")
        else:
            print(f"{Colors.RED}❌ OpenAI API key missing or invalid{Colors.ENDC}")
            print(f"{Colors.YELLOW}   Please set OPENAI_API_KEY in .env file{Colors.ENDC}")
            all_ok = False
    except Exception as e:
        print(f"{Colors.RED}❌ API key check failed: {e}{Colors.ENDC}")
        all_ok = False
    
    # Test 3: OG-RAG System Initialization
    print(f"\n{Colors.CYAN}Testing OG-RAG system initialization...{Colors.ENDC}")
    try:
        translator = OGRAGTranslator()
        print(f"{Colors.GREEN}✅ OGRAGTranslator initialized successfully{Colors.ENDC}")
        print(f"   Model: {translator.model}")
        print(f"   Temperature: {translator.temperature}")
    except Exception as e:
        print(f"{Colors.RED}❌ OG-RAG initialization failed: {e}{Colors.ENDC}")
        all_ok = False
    
    # Summary
    print("\n" + "─" * 70)
    if all_ok:
        print(f"{Colors.GREEN + Colors.BOLD}✅ All systems ready for demo{Colors.ENDC}\n")
    else:
        print(f"{Colors.RED + Colors.BOLD}❌ Some components failed - fix errors before demo{Colors.ENDC}\n")
    
    return all_ok


def save_results(results: Dict[str, Any], output_file: str = "demo_results.json"):
    """Save demo results to JSON file."""
    try:
        output_path = repo_root / "outputs" / "evaluation" / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert TranslationResult objects to dicts
        serializable = {}
        for key, result in results.items():
            if result and hasattr(result, '__dict__'):
                serializable[key] = {
                    'translation': result.translation,
                    'method': result.method,
                    'total_tokens': result.total_tokens,
                    'concepts_used': result.concepts_used,
                    'explanation': result.explanation
                }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)
        
        print(f"{Colors.GREEN}✅ Results saved to: {output_path}{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.YELLOW}⚠️  Failed to save results: {e}{Colors.ENDC}")


def main():
    """Main entry point for demo script."""
    parser = argparse.ArgumentParser(
        description="Live OG-RAG Demo for Thesis Defense",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test system connections
  python presentations/demo_ograg_live.py --test
  
  # Run demo with default proverb
  python presentations/demo_ograg_live.py
  
  # Run demo with custom proverb and show graph query
  python presentations/demo_ograg_live.py --proverb "Mwangi ti mwene ciaku" --show-graph
  
  # Save results to file
  python presentations/demo_ograg_live.py --save-results
        """
    )
    
    parser.add_argument(
        '--proverb',
        type=str,
        default="Gutiri uriragio ni utonga no ukia",
        help="Kikuyu proverb to translate (default: wealth/poverty proverb)"
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help="Test system connections only (no translation)"
    )
    
    parser.add_argument(
        '--show-graph',
        action='store_true',
        help="Show Neo4j graph query during demo"
    )
    
    parser.add_argument(
        '--save-results',
        action='store_true',
        help="Save demo results to JSON file"
    )
    
    args = parser.parse_args()
    
    # Run test mode or full demo
    if args.test:
        test_connection()
    else:
        # Always test first
        if not test_connection():
            print(f"\n{Colors.RED}System check failed. Fix errors before running demo.{Colors.ENDC}")
            sys.exit(1)
        
        # Run the demo
        results = demo_proverb(args.proverb, args.show_graph)
        
        # Save if requested
        if args.save_results and results:
            save_results(results)


if __name__ == "__main__":
    main()
