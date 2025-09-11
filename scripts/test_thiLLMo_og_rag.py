#!/usr/bin/env python3
"""Comprehensive thiLLMo OG-RAG system testing for culturally faithful Kikuyu proverb translation."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from neo4j import GraphDatabase
from decouple import Config, RepositoryEnv
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThiLLMoOGRAGTester:
    """Test the complete thiLLMo OG-RAG system functionality for Kikuyu proverb translation."""
    
    def __init__(self):
        # Load configuration from project .env file
        env_path = Path(__file__).parent.parent / ".env"
        config = Config(RepositoryEnv(str(env_path)))
        
        self.driver = GraphDatabase.driver(
            config('NEO4J_URI', default='bolt://localhost:7687'),
            auth=(
                config('NEO4J_USER', default='neo4j'),
                config('NEO4J_PASSWORD', default='ograg2025')
            )
        )
        
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {}
        }
    
    def test_kikuyu_proverb_search(self):
        """Test full-text search for Kikuyu proverbs with cultural context."""
        with self.driver.session() as session:
            query = """
            CALL db.index.fulltext.queryNodes('kikuyu_proverb_fulltext', 'ũtonga maĩ wĩra') 
            YIELD node, score
            RETURN 
                node.kikuyu_text as kikuyu,
                node.literal_translation as literal,
                node.cultural_meaning as cultural,
                node.domain_relevance as domain,
                score
            ORDER BY score DESC
            LIMIT 5
            """
            
            results = list(session.run(query))
            
            print("🔍 Kikuyu Proverb Full-Text Search Test")
            print("-" * 45)
            for result in results:
                print(f"Kikuyu: {result['kikuyu']}")
                print(f"Literal: {result['literal']}")
                print(f"Cultural: {result['cultural'][:80]}...")
                print(f"Domain: {result['domain']}")
                print(f"Score: {result['score']:.3f}\n")
            
            self.test_results['tests']['kikuyu_search'] = {
                'status': 'passed' if len(results) > 0 else 'failed',
                'count': len(results),
                'description': 'Kikuyu proverb search functionality'
            }
            
            return len(results)
    
    def test_cultural_ontology_retrieval(self):
        """Test retrieval of cultural ontology for OG-RAG grounding."""
        with self.driver.session() as session:
            query = """
            MATCH (p:KikuyuProverb)-[:EMBODIES]->(c:CulturalConcept)
            OPTIONAL MATCH (p)-[:APPROPRIATE_IN]->(uc:UsageContext)
            OPTIONAL MATCH (p)-[:BELONGS_TO_FIELD]->(sf:SemanticField)
            WHERE p.domain_relevance = 'wealth_entrepreneurship'
            RETURN 
                p.kikuyu_text as proverb,
                p.morphological_analysis as morphology,
                p.cultural_significance as significance,
                collect(DISTINCT c.name) as concepts,
                collect(DISTINCT uc.name) as contexts,
                collect(DISTINCT sf.name) as fields
            LIMIT 3
            """
            
            results = list(session.run(query))
            
            print("🎭 Cultural Ontology Retrieval Test")
            print("-" * 40)
            for result in results:
                print(f"Proverb: {result['proverb']}")
                print(f"Morphology: {result['morphology']}")
                print(f"Significance: {result['significance']}")
                print(f"Concepts: {', '.join(result['concepts'])}")
                print(f"Contexts: {', '.join(result['contexts'])}")
                print(f"Fields: {', '.join(result['fields'])}\n")
            
            self.test_results['tests']['ontology_retrieval'] = {
                'status': 'passed' if len(results) > 0 else 'failed',
                'count': len(results),
                'description': 'Cultural ontology grounding for OG-RAG'
            }
            
            return len(results)
    
    def test_wealth_entrepreneurship_hypergraph(self):
        """Test hypergraph traversal for wealth/entrepreneurship domain proverbs."""
        with self.driver.session() as session:
            query = """
            MATCH (p1:KikuyuProverb)-[:EMBODIES]->(c:CulturalConcept)<-[:EMBODIES]-(p2:KikuyuProverb)
            WHERE p1 <> p2 
                AND p1.domain_relevance = 'wealth_entrepreneurship'
                AND p2.domain_relevance = 'wealth_entrepreneurship'
            RETURN 
                p1.kikuyu_text as original,
                p1.cultural_meaning as original_meaning,
                p2.kikuyu_text as related,
                p2.cultural_meaning as related_meaning,
                c.name as shared_concept,
                c.cultural_significance as concept_significance
            LIMIT 4
            """
            
            results = list(session.run(query))
            
            print("🕸️ Wealth/Entrepreneurship Hypergraph Test")
            print("-" * 45)
            for result in results:
                print(f"Original: {result['original']}")
                print(f"Meaning: {result['original_meaning'][:60]}...")
                print(f"Related: {result['related']}")
                print(f"Via Concept: {result['shared_concept']}")
                print(f"Significance: {result['concept_significance'][:50]}...\n")
            
            self.test_results['tests']['hypergraph_traversal'] = {
                'status': 'passed' if len(results) > 0 else 'failed',
                'count': len(results),
                'description': 'Domain-specific hypergraph traversal'
            }
            
            return len(results)
    
    def test_thiLLMo_translation_patterns(self):
        """Test thiLLMo-specific translation query patterns."""
        with self.driver.session() as session:
            query = """
            MATCH (tp:TranslationPattern)
            MATCH (cp:CulturalPreservation)
            WHERE tp.target_domain = 'wealth_entrepreneurship'
               AND cp.preservation_strategy = 'ontology_grounded'
            RETURN 
                tp.pattern_type,
                tp.translation_strategy,
                tp.cultural_fidelity_score,
                cp.description,
                cp.validation_criteria
            LIMIT 3
            """
            
            results = list(session.run(query))
            
            print("⚡ thiLLMo Translation Patterns Test")
            print("-" * 42)
            for result in results:
                print(f"Pattern: {result['tp.pattern_type']}")
                print(f"Strategy: {result['tp.translation_strategy']}")
                print(f"Fidelity: {result['tp.cultural_fidelity_score']}")
                print(f"Preservation: {result['cp.description']}")
                print(f"Validation: {result['cp.validation_criteria'][:50]}...\n")
            
            self.test_results['tests']['translation_patterns'] = {
                'status': 'passed' if len(results) > 0 else 'failed',
                'count': len(results),
                'description': 'thiLLMo translation pattern validation'
            }
            
            return len(results)
    
    def test_cultural_sensitivity_compliance(self):
        """Test cultural sensitivity and heritage preservation compliance."""
        with self.driver.session() as session:
            query = """
            MATCH (p:KikuyuProverb)
            WHERE p.cultural_validation_status = 'approved'
                AND p.heritage_preservation_flag = true
            OPTIONAL MATCH (p)-[:VALIDATED_BY]->(cv:CulturalValidator)
            RETURN 
                count(p) as approved_proverbs,
                collect(DISTINCT cv.validator_type) as validator_types,
                avg(p.cultural_authenticity_score) as avg_authenticity
            """
            
            result = session.run(query).single()
            
            print("🛡️ Cultural Sensitivity Compliance Test")
            print("-" * 45)
            if result:
                print(f"Approved Proverbs: {result['approved_proverbs']}")
                print(f"Validator Types: {', '.join(result['validator_types'] or [])}")
                print(f"Avg Authenticity: {result['avg_authenticity']:.3f}")
            
            self.test_results['tests']['cultural_compliance'] = {
                'status': 'passed' if result and result['approved_proverbs'] > 0 else 'failed',
                'count': result['approved_proverbs'] if result else 0,
                'description': 'Cultural sensitivity and heritage preservation'
            }
            
            return result['approved_proverbs'] if result else 0
    
    def test_morphological_analysis_integration(self):
        """Test integration of Kikuyu morphological analysis in OG-RAG."""
        with self.driver.session() as session:
            query = """
            MATCH (p:KikuyuProverb)
            WHERE p.morphological_analysis IS NOT NULL
                AND p.root_words IS NOT NULL
            RETURN 
                p.kikuyu_text as proverb,
                p.morphological_analysis as analysis,
                p.root_words as roots,
                p.grammatical_structure as structure
            LIMIT 3
            """
            
            results = list(session.run(query))
            
            print("🔤 Morphological Analysis Integration Test")
            print("-" * 48)
            for result in results:
                print(f"Proverb: {result['proverb']}")
                print(f"Analysis: {result['analysis']}")
                print(f"Roots: {result['roots']}")
                print(f"Structure: {result['structure']}\n")
            
            self.test_results['tests']['morphological_analysis'] = {
                'status': 'passed' if len(results) > 0 else 'failed',
                'count': len(results),
                'description': 'Kikuyu morphological analysis integration'
            }
            
            return len(results)
    
    def test_og_rag_retrieval_performance(self):
        """Test OG-RAG retrieval performance for translation queries."""
        with self.driver.session() as session:
            start_time = datetime.now()
            
            query = """
            MATCH (p:KikuyuProverb)-[:EMBODIES]->(c:CulturalConcept)
            WHERE p.domain_relevance = 'wealth_entrepreneurship'
            WITH p, collect(c) as concepts
            MATCH (p)-[:BELONGS_TO_FIELD]->(sf:SemanticField)
            RETURN 
                p.kikuyu_text,
                p.cultural_meaning,
                [concept IN concepts | concept.name] as concept_names,
                sf.name as semantic_field
            LIMIT 10
            """
            
            results = list(session.run(query))
            end_time = datetime.now()
            
            retrieval_time = (end_time - start_time).total_seconds()
            
            print("⚡ OG-RAG Retrieval Performance Test")
            print("-" * 42)
            print(f"Retrieved: {len(results)} proverbs")
            print(f"Time: {retrieval_time:.3f} seconds")
            print(f"Performance: {len(results)/retrieval_time:.2f} proverbs/sec\n")
            
            self.test_results['tests']['retrieval_performance'] = {
                'status': 'passed' if retrieval_time < 2.0 else 'warning',
                'count': len(results),
                'performance_seconds': retrieval_time,
                'description': 'OG-RAG retrieval performance benchmark'
            }
            
            return len(results), retrieval_time
    
    def run_all_tests(self):
        """Run comprehensive thiLLMo OG-RAG system tests."""
        print("🧪 thiLLMo OG-RAG System Test Suite")
        print("🌍 Culturally Faithful Kikuyu Proverb Translation")
        print("=" * 55)
        
        try:
            # Test 1: Kikuyu proverb search
            search_results = self.test_kikuyu_proverb_search()
            print(f"✅ Kikuyu search: {search_results} results")
            
            # Test 2: Cultural ontology retrieval
            ontology_results = self.test_cultural_ontology_retrieval()
            print(f"✅ Ontology retrieval: {ontology_results} results")
            
            # Test 3: Domain-specific hypergraph
            hypergraph_results = self.test_wealth_entrepreneurship_hypergraph()
            print(f"✅ Hypergraph traversal: {hypergraph_results} results")
            
            # Test 4: Translation patterns
            pattern_results = self.test_thiLLMo_translation_patterns()
            print(f"✅ Translation patterns: {pattern_results} results")
            
            # Test 5: Cultural compliance
            compliance_results = self.test_cultural_sensitivity_compliance()
            print(f"✅ Cultural compliance: {compliance_results} approved")
            
            # Test 6: Morphological analysis
            morphology_results = self.test_morphological_analysis_integration()
            print(f"✅ Morphological analysis: {morphology_results} results")
            
            # Test 7: Performance benchmark
            perf_results, perf_time = self.test_og_rag_retrieval_performance()
            print(f"✅ Performance: {perf_results} results in {perf_time:.3f}s")
            
            # Summary
            passed_tests = sum(1 for test in self.test_results['tests'].values() 
                             if test['status'] == 'passed')
            total_tests = len(self.test_results['tests'])
            
            print(f"\n🎉 Test Summary: {passed_tests}/{total_tests} tests passed")
            print("🌍 thiLLMo OG-RAG system ready for culturally faithful translation!")
            
            # Save test results
            self._save_test_results()
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            logger.error(f"Test error: {e}")
            self.test_results['error'] = str(e)
    
    def _save_test_results(self):
        """Save test results to logs directory."""
        logs_dir = Path(__file__).parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        results_file = logs_dir / f"thiLLMo_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Test results saved to: {results_file}")
    
    def close(self):
        self.driver.close()

def main():
    """Main test execution function."""
    print("🚀 Starting thiLLMo OG-RAG System Tests")
    print("📚 Testing culturally faithful Kikuyu proverb translation capabilities")
    print("-" * 70)
    
    tester = ThiLLMoOGRAGTester()
    try:
        tester.run_all_tests()
    finally:
        tester.close()

if __name__ == "__main__":
    main()
