#!/usr/bin/env python3
"""LLM-Enhanced Ontology Concept Extraction for Kikuyu Proverbs.

This script uses GPT-4 to extract structured semantic concepts from expert annotations
in the gold standard dataset. It builds on the existing ontology infrastructure while
adding AI-powered semantic extraction capabilities.

METHODOLOGICAL NOTE:
This script uses ONLY expert annotations (expert_cultural_meaning, expert_teaching)
as the knowledge source - NOT baseline translations. This maintains research integrity
by building the ontology from authoritative cultural knowledge, not MT outputs.

Data Flow:
    Input: data/evaluation/gold_standard_ireri_deduplicated.csv
    Process: GPT-4 semantic extraction from expert annotations
    Output: data/ontology/extracted_concepts_100proverbs.json

Extracted Concepts:
    - Kikuyu Entities (physical things: mbia, njuu, ngigi, andu, indo)
    - Actions (verbs: aikaragia, ruuga, etc.)
    - Cultural Concepts (abstract: greed, trust, patience, community)
    - Metaphors (vehicle→tenor mappings with cultural explanations)
    - Thematic Categories (from expert annotations)
    
Usage:
    python scripts/extract_ontology_concepts_with_llm.py
    python scripts/extract_ontology_concepts_with_llm.py --max-proverbs 10 --test-mode

Author: ndethi
Project: thiLLMo - OPIT RAI9001 Research Project
Created: October 2025
"""

import argparse
import csv
import json
import logging
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class KikuyuEntity:
    """Represents a Kikuyu entity (noun/object) with linguistic metadata."""
    kikuyu_term: str
    english_translation: str
    category: str  # animal, object, person, place, abstract_concept
    cultural_significance: str
    example_usage: str


@dataclass
class KikuyuAction:
    """Represents a Kikuyu action (verb) with usage context."""
    kikuyu_verb: str
    english_translation: str
    action_type: str  # physical, mental, social, economic
    cultural_context: str


@dataclass
class CulturalConcept:
    """Represents an abstract cultural concept."""
    concept_name: str  # e.g., "greed", "generosity", "patience"
    kikuyu_expressions: List[str]  # Kikuyu words/phrases expressing this
    cultural_explanation: str
    moral_dimension: str  # positive, negative, neutral, contextual


@dataclass
class ProverbMetaphor:
    """Represents metaphorical structure of a proverb."""
    vehicle: str  # Concrete thing used (e.g., "storks pursuing locusts")
    tenor: str  # Abstract concept represented (e.g., "relentless pursuit of wealth")
    mapping_explanation: str  # How vehicle maps to tenor culturally
    cultural_resonance: str  # Why this metaphor works in Kikuyu culture


@dataclass
class ExtractedConcepts:
    """Complete concept extraction for a single proverb."""
    proverb_id: str
    kikuyu_text: str
    expert_translation: str
    expert_cultural_meaning: str
    expert_teaching: str
    thematic_category: str
    
    # Extracted linguistic elements
    entities: List[KikuyuEntity] = field(default_factory=list)
    actions: List[KikuyuAction] = field(default_factory=list)
    cultural_concepts: List[CulturalConcept] = field(default_factory=list)
    metaphor: Optional[ProverbMetaphor] = None
    
    # Extraction metadata
    extraction_confidence: float = 0.0
    extraction_notes: str = ""
    extracted_at: str = field(default_factory=lambda: datetime.now().isoformat())


class OntologyConceptExtractor:
    """Extracts structured concepts from expert proverb annotations using GPT-4."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client with API key."""
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"  # GPT-4o supports JSON mode + good reasoning
        self.extracted_concepts: List[ExtractedConcepts] = []
        
    def extract_concepts_from_proverb(
        self, 
        proverb_row: Dict[str, Any]
    ) -> ExtractedConcepts:
        """Extract structured concepts from a single proverb using GPT-4.
        
        Args:
            proverb_row: Dictionary containing proverb data with keys:
                - proverb_id, kikuyu_text, expert_translation,
                - expert_cultural_meaning, expert_teaching, thematic_category
        
        Returns:
            ExtractedConcepts object with structured linguistic and cultural data
        """
        logger.info(f"Extracting concepts for {proverb_row['proverb_id']}")
        
        prompt = self._build_extraction_prompt(proverb_row)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for consistent extraction
                response_format={"type": "json_object"}
            )
            
            extracted_data = json.loads(response.choices[0].message.content)
            
            # Parse response into structured dataclasses
            concepts = self._parse_extraction_response(
                proverb_row, 
                extracted_data
            )
            
            logger.info(
                f"✓ Extracted {len(concepts.entities)} entities, "
                f"{len(concepts.actions)} actions, "
                f"{len(concepts.cultural_concepts)} concepts for "
                f"{proverb_row['proverb_id']}"
            )
            
            return concepts
            
        except Exception as e:
            logger.error(
                f"Error extracting concepts for {proverb_row['proverb_id']}: {e}"
            )
            # Return empty concepts with error note
            return ExtractedConcepts(
                proverb_id=proverb_row['proverb_id'],
                kikuyu_text=proverb_row['kikuyu_text'],
                expert_translation=proverb_row.get('expert_translation', ''),
                expert_cultural_meaning=proverb_row.get(
                    'expert_cultural_meaning', ''
                ),
                expert_teaching=proverb_row.get('expert_teaching', ''),
                thematic_category=proverb_row.get('thematic_category', ''),
                extraction_confidence=0.0,
                extraction_notes=f"Extraction failed: {str(e)}"
            )
    
    def _get_system_prompt(self) -> str:
        """Get system prompt defining the extraction task."""
        return """You are an expert linguist and cultural anthropologist specializing in Kikuyu language and East African proverbs. Your task is to extract structured linguistic and cultural concepts from Kikuyu proverbs based on expert annotations.

You will analyze:
1. The original Kikuyu proverb text
2. Expert-provided English translation
3. Expert-provided cultural meaning
4. Expert-provided moral teaching

Extract these structured concepts:

**Entities**: Physical or abstract things mentioned in the proverb
- kikuyu_term: Original Kikuyu word
- english_translation: English equivalent
- category: animal/object/person/place/abstract_concept
- cultural_significance: Why this entity matters in Kikuyu culture
- example_usage: How it's used in the proverb

**Actions**: Verbs and behaviors in the proverb
- kikuyu_verb: Original Kikuyu verb
- english_translation: English equivalent
- action_type: physical/mental/social/economic
- cultural_context: Cultural nuances of this action

**Cultural Concepts**: Abstract ideas expressed
- concept_name: e.g., greed, generosity, patience
- kikuyu_expressions: Kikuyu words expressing this concept
- cultural_explanation: What this means in Kikuyu culture
- moral_dimension: positive/negative/neutral/contextual

**Metaphor** (if present): Metaphorical structure
- vehicle: Concrete thing used (e.g., "storks pursuing locusts")
- tenor: Abstract concept represented (e.g., "pursuit of wealth")
- mapping_explanation: How vehicle maps to tenor
- cultural_resonance: Why this works in Kikuyu culture

Return valid JSON only. Be thorough but accurate - base ALL extractions on the expert annotations provided, not your assumptions."""
    
    def _build_extraction_prompt(self, proverb_row: Dict[str, Any]) -> str:
        """Build extraction prompt for a specific proverb."""
        return f"""Analyze this Kikuyu proverb and extract structured concepts:

**Proverb ID**: {proverb_row['proverb_id']}

**Kikuyu Text**: {proverb_row['kikuyu_text']}

**Expert Translation**: {proverb_row.get('expert_translation', 'Not provided')}

**Expert Cultural Meaning**: {proverb_row.get('expert_cultural_meaning', 'Not provided')}

**Expert Teaching**: {proverb_row.get('expert_teaching', 'Not provided')}

**Thematic Category**: {proverb_row.get('thematic_category', 'Not provided')}

Extract and return a JSON object with this structure:
{{
    "entities": [
        {{
            "kikuyu_term": "mbia",
            "english_translation": "money/wealth/valuables",
            "category": "object",
            "cultural_significance": "Central to wealth discussions in Kikuyu culture",
            "example_usage": "Used in proverb to represent material wealth"
        }}
    ],
    "actions": [
        {{
            "kikuyu_verb": "aikaragia",
            "english_translation": "guards/pursues/protects",
            "action_type": "physical",
            "cultural_context": "Implies active protection or pursuit"
        }}
    ],
    "cultural_concepts": [
        {{
            "concept_name": "greed",
            "kikuyu_expressions": ["kuona kwingi", "gutaka kwingi"],
            "cultural_explanation": "Insatiable desire for more, culturally viewed negatively",
            "moral_dimension": "negative"
        }}
    ],
    "metaphor": {{
        "vehicle": "storks pursuing locusts",
        "tenor": "relentless pursuit of wealth",
        "mapping_explanation": "Storks relentlessly chase locusts for food, mapped to endless pursuit of money",
        "cultural_resonance": "Kikuyu agricultural society understands bird behavior metaphors"
    }},
    "extraction_confidence": 0.9,
    "extraction_notes": "Clear metaphorical structure with explicit cultural teaching"
}}

Focus on extracting concepts that are EXPLICITLY stated or strongly implied in the expert annotations. Do not invent cultural meanings."""
    
    def _parse_extraction_response(
        self,
        proverb_row: Dict[str, Any],
        extracted_data: Dict[str, Any]
    ) -> ExtractedConcepts:
        """Parse GPT-4 response into structured dataclasses."""
        
        # Parse entities
        entities = [
            KikuyuEntity(**entity_data)
            for entity_data in extracted_data.get('entities', [])
        ]
        
        # Parse actions
        actions = [
            KikuyuAction(**action_data)
            for action_data in extracted_data.get('actions', [])
        ]
        
        # Parse cultural concepts
        cultural_concepts = [
            CulturalConcept(**concept_data)
            for concept_data in extracted_data.get('cultural_concepts', [])
        ]
        
        # Parse metaphor (optional)
        metaphor = None
        if 'metaphor' in extracted_data and extracted_data['metaphor']:
            metaphor = ProverbMetaphor(**extracted_data['metaphor'])
        
        return ExtractedConcepts(
            proverb_id=proverb_row['proverb_id'],
            kikuyu_text=proverb_row['kikuyu_text'],
            expert_translation=proverb_row.get('expert_translation', ''),
            expert_cultural_meaning=proverb_row.get('expert_cultural_meaning', ''),
            expert_teaching=proverb_row.get('expert_teaching', ''),
            thematic_category=proverb_row.get('thematic_category', ''),
            entities=entities,
            actions=actions,
            cultural_concepts=cultural_concepts,
            metaphor=metaphor,
            extraction_confidence=extracted_data.get('extraction_confidence', 0.8),
            extraction_notes=extracted_data.get('extraction_notes', '')
        )
    
    def extract_batch(
        self,
        proverbs: List[Dict[str, Any]],
        max_proverbs: Optional[int] = None
    ) -> List[ExtractedConcepts]:
        """Extract concepts from a batch of proverbs.
        
        Args:
            proverbs: List of proverb dictionaries
            max_proverbs: Optional limit on number to process
        
        Returns:
            List of ExtractedConcepts objects
        """
        if max_proverbs:
            proverbs = proverbs[:max_proverbs]
        
        logger.info(f"Starting extraction for {len(proverbs)} proverbs...")
        
        for i, proverb in enumerate(proverbs, 1):
            logger.info(f"Processing {i}/{len(proverbs)}: {proverb['proverb_id']}")
            
            concepts = self.extract_concepts_from_proverb(proverb)
            self.extracted_concepts.append(concepts)
        
        logger.info(f"✓ Completed extraction for {len(self.extracted_concepts)} proverbs")
        return self.extracted_concepts
    
    def save_to_json(self, output_path: Path) -> None:
        """Save extracted concepts to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert dataclasses to dictionaries for JSON serialization
        data = [
            self._concept_to_dict(concept) 
            for concept in self.extracted_concepts
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Saved extracted concepts to {output_path}")
    
    def _concept_to_dict(self, concept: ExtractedConcepts) -> Dict[str, Any]:
        """Convert ExtractedConcepts to dictionary for JSON."""
        data = asdict(concept)
        return data
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """Generate summary statistics of extracted concepts."""
        total_entities = sum(
            len(c.entities) for c in self.extracted_concepts
        )
        total_actions = sum(
            len(c.actions) for c in self.extracted_concepts
        )
        total_concepts = sum(
            len(c.cultural_concepts) for c in self.extracted_concepts
        )
        total_metaphors = sum(
            1 for c in self.extracted_concepts if c.metaphor
        )
        
        # Collect unique entities
        unique_entities = set()
        for concept in self.extracted_concepts:
            for entity in concept.entities:
                unique_entities.add(entity.kikuyu_term)
        
        # Collect unique cultural concepts
        unique_concepts = set()
        for concept in self.extracted_concepts:
            for cultural_concept in concept.cultural_concepts:
                unique_concepts.add(cultural_concept.concept_name)
        
        avg_confidence = (
            sum(c.extraction_confidence for c in self.extracted_concepts) / 
            len(self.extracted_concepts)
            if self.extracted_concepts else 0
        )
        
        summary = {
            'total_proverbs_processed': len(self.extracted_concepts),
            'total_entities_extracted': total_entities,
            'total_actions_extracted': total_actions,
            'total_cultural_concepts_extracted': total_concepts,
            'total_metaphors_identified': total_metaphors,
            'unique_kikuyu_entities': len(unique_entities),
            'unique_cultural_concepts': len(unique_concepts),
            'average_extraction_confidence': round(avg_confidence, 3),
            'top_kikuyu_entities': list(unique_entities)[:20],
            'top_cultural_concepts': list(unique_concepts)[:20],
            'generated_at': datetime.now().isoformat()
        }
        
        return summary


def load_gold_standard_proverbs(
    csv_path: Path,
    max_proverbs: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Load proverbs from gold standard CSV.
    
    Args:
        csv_path: Path to gold_standard_ireri_deduplicated.csv
        max_proverbs: Optional limit on number to load
    
    Returns:
        List of proverb dictionaries
    """
    logger.info(f"Loading proverbs from {csv_path}")
    
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    if max_proverbs:
        df = df.head(max_proverbs)
    
    logger.info(f"Loaded {len(df)} proverbs")
    
    return df.to_dict('records')


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Extract ontology concepts from Kikuyu proverbs using GPT-4'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='data/evaluation/gold_standard_ireri_deduplicated.csv',
        help='Path to gold standard CSV file'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/ontology/extracted_concepts_100proverbs.json',
        help='Path to output JSON file'
    )
    parser.add_argument(
        '--max-proverbs',
        type=int,
        default=None,
        help='Maximum number of proverbs to process (for testing)'
    )
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Run in test mode with first 5 proverbs only'
    )
    
    args = parser.parse_args()
    
    # Test mode override
    if args.test_mode:
        args.max_proverbs = 5
        args.output = 'data/ontology/extracted_concepts_test.json'
        logger.info("🧪 Running in TEST MODE (5 proverbs)")
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)
    
    # Load proverbs
    proverbs = load_gold_standard_proverbs(input_path, args.max_proverbs)
    
    # Initialize extractor
    extractor = OntologyConceptExtractor()
    
    # Extract concepts
    logger.info("\n" + "="*60)
    logger.info("STARTING ONTOLOGY CONCEPT EXTRACTION")
    logger.info("="*60 + "\n")
    
    extracted = extractor.extract_batch(proverbs, args.max_proverbs)
    
    # Save results
    extractor.save_to_json(output_path)
    
    # Generate and save summary
    summary = extractor.generate_summary_report()
    summary_path = output_path.parent / f"{output_path.stem}_summary.json"
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✓ Saved summary report to {summary_path}")
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("EXTRACTION SUMMARY")
    logger.info("="*60)
    logger.info(f"Proverbs processed: {summary['total_proverbs_processed']}")
    logger.info(f"Entities extracted: {summary['total_entities_extracted']}")
    logger.info(f"Actions extracted: {summary['total_actions_extracted']}")
    logger.info(f"Cultural concepts: {summary['total_cultural_concepts_extracted']}")
    logger.info(f"Metaphors identified: {summary['total_metaphors_identified']}")
    logger.info(f"Unique Kikuyu terms: {summary['unique_kikuyu_entities']}")
    logger.info(f"Avg confidence: {summary['average_extraction_confidence']}")
    logger.info("="*60 + "\n")
    
    logger.info(f"✓ Extraction complete! Check {output_path} for full results.")


if __name__ == "__main__":
    main()
