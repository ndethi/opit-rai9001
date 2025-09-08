#!/usr/bin/env python3
"""Dynamic Proverb Loader for thiLLMo Kikuyu Cultural Translation System.

This module loads and processes Kikuyu proverbs from external data files
with configurable domain themes and validation rules for the thiLLMo 
Ontology-Grounded RAG system.

The loader supports the thiLLMo mission of preserving cultural heritage
through AI by providing robust data ingestion, validation, and enrichment
capabilities for Kikuyu proverbs (thimo) with cultural context preservation.

Features:
    - Environment-driven configuration from .env files
    - Minimal hard-coded test data for development
    - PEP 8 compliant code structure with type hints
    - Type-safe implementation using dataclasses
    - Comprehensive error handling and logging
    - Cultural validation and linguistic enrichment
    - Neo4j ontology integration compatibility

Examples:
    Basic usage with default configuration:
    
    >>> loader = WealthEntrepreneurshipProverbLoader()
    >>> csv_file, json_file = loader.create_minimal_test_data()
    >>> proverbs = loader.load_and_process_proverbs(csv_file)
    >>> len(proverbs)
    2
    
    Environment-driven configuration:
    
    >>> loader = WealthEntrepreneurshipProverbLoader(config_file=".env")
    >>> proverbs = loader.load_and_process_proverbs("data/proverbs/full_dataset.csv")
    >>> neo4j_data = loader.get_proverbs_for_neo4j()

Author: ndethi <ndethi@example.com>
Project: thiLLMo - OPIT RAI9001 Research Project
Institution: Oxford Postgraduate Institute of Technology
Created: September 2025
License: MIT (see project root for full license)
Version: 1.0.0

Note:
    This module is part of the thiLLMo research project focusing on 
    culturally faithful Kikuyu proverb translation using Ontology-Grounded
    Retrieval Augmented Generation (OG-RAG).
"""

import csv
import json
import logging
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from decouple import Config, RepositoryEnv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ProverbData:
    """Data structure for a single Kikuyu proverb entry.
    
    This dataclass represents a complete proverb record with all
    necessary fields for cultural preservation and linguistic analysis
    in the thiLLMo system.
    
    Attributes:
        kikuyu_text: Original Kikuyu proverb text
        literal_translation: Direct word-for-word English translation
        cultural_meaning: Deep cultural interpretation and significance
        themes: List of thematic categories (e.g., ["business", "wisdom"])
        domain_relevance: Explanation of relevance to target domain
        usage_context: When/how the proverb is traditionally used
        complexity_level: Linguistic complexity ("simple", "moderate", "complex")
        frequency_rating: Usage frequency in community ("rare" to "very_common")
        source_type: Origin type ("oral_tradition", "written_collection", etc.)
        region_variants: List of regional variations or dialects
        id: Unique identifier (auto-generated if not provided)
        phonetic_transcription: IPA or simplified phonetic notation
        morphological_analysis: Word-level linguistic breakdown
        metaphorical_structure: JSON string of metaphor mapping
        usage_notes: Additional contextual usage information
        validation_status: Data quality status ("pending_review", "validated", etc.)
    """
    
    kikuyu_text: str
    literal_translation: str
    cultural_meaning: str
    themes: List[str]
    domain_relevance: str
    usage_context: str
    complexity_level: str
    frequency_rating: str
    source_type: str
    region_variants: List[str] = field(default_factory=list)
    id: str = ""
    phonetic_transcription: Optional[str] = None
    morphological_analysis: Optional[str] = None
    metaphorical_structure: Optional[str] = None
    usage_notes: Optional[str] = None
    validation_status: str = "pending_review"
    
    def __post_init__(self) -> None:
        """Validate and clean data after initialization."""
        self._ensure_list_fields()
        self._generate_id_if_missing()
    
    def _ensure_list_fields(self) -> None:
        """Ensure themes and region_variants are lists."""
        if isinstance(self.themes, str):
            self.themes = [t.strip() for t in self.themes.split(',')]
        
        if isinstance(self.region_variants, str):
            self.region_variants = [
                r.strip() for r in self.region_variants.split(',')
            ]
    
    def _generate_id_if_missing(self) -> None:
        """Generate ID if not provided."""
        if not self.id:
            self.id = f"prov_{hash(self.kikuyu_text) % 10000:04d}"


class ProverbLoaderConfig:
    """Configuration manager for proverb loader.
    
    Loads configuration from environment variables or .env files
    to support flexible domain targeting and validation rules.
    Compatible with thiLLMo project .env structure.
    """
    
    def __init__(self, env_file: Optional[str] = None) -> None:
        """Initialize configuration from environment file.
        
        Args:
            env_file: Path to .env file. If None or file doesn't exist,
                     falls back to system environment variables.
        """
        if env_file and Path(env_file).exists():
            self.config = Config(RepositoryEnv(env_file))
        else:
            # Fallback to project root .env if it exists
            project_root_env = Path(__file__).parent.parent.parent / ".env"
            if project_root_env.exists():
                self.config = Config(RepositoryEnv(str(project_root_env)))
            else:
                self.config = Config()
        
        self._load_domain_config()
        self._load_validation_config()
    
    def _load_domain_config(self) -> None:
        """Load domain-specific configuration from environment."""
        # Load from environment or use defaults
        themes_json = self.config(
            'DOMAIN_THEMES',
            default='{"business_wisdom": ["trade", "business", "commerce"]}'
        )
        self.domain_themes = json.loads(themes_json)
        
        terms_json = self.config(
            'KIKUYU_DOMAIN_TERMS',
            default='{"wonjoria": "business, trade", "mbeca": "money"}'
        )
        self.kikuyu_domain_terms = json.loads(terms_json)
        
        self.target_domain = self.config('TARGET_DOMAIN', default='business')
    
    def _load_validation_config(self) -> None:
        """Load validation configuration from environment."""
        self.min_kikuyu_length = self.config(
            'MIN_KIKUYU_LENGTH', default=5, cast=int
        )
        self.min_translation_length = self.config(
            'MIN_TRANSLATION_LENGTH', default=5, cast=int
        )
        self.min_cultural_meaning_length = self.config(
            'MIN_CULTURAL_MEANING_LENGTH', default=10, cast=int
        )


class WealthEntrepreneurshipProverbLoader:
    """Loads and processes Kikuyu proverbs with configurable domain focus.
    
    This loader is designed for the thiLLMo project to handle proverb data
    ingestion, validation, cultural enrichment, and Neo4j compatibility.
    It supports the wealth/entrepreneurship domain by default but can be
    configured for other domains through environment variables.
    
    The loader integrates with the thiLLMo project structure:
    - Uses data/proverbs/ for input files (as per PROVERB_DATA_DIR)
    - Exports to data/processed/ for processed output
    - Provides Neo4j-compatible output for ontology integration
    
    Attributes:
        data_dir: Path to proverb data directory
        config: Configuration manager instance
        loaded_proverbs: List of processed ProverbData instances
    """
    
    def __init__(
        self, 
        data_directory: Optional[str] = None,
        config_file: Optional[str] = None
    ) -> None:
        """Initialize the loader with data directory and configuration.
        
        Args:
            data_directory: Path to data directory. If None, uses
                           PROVERB_DATA_DIR from environment or default.
            config_file: Path to configuration file. If None, uses
                        project root .env or environment variables.
        """
        if data_directory is None:
            # Use environment variable or default from thiLLMo project structure
            env_config = Config()
            data_directory = env_config('PROVERB_DATA_DIR', default='data/proverbs/')
        
        self.data_dir = Path(data_directory)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = ProverbLoaderConfig(config_file)
        self.loaded_proverbs: List[ProverbData] = []
    
    def create_minimal_test_data(self) -> tuple[Path, Path]:
        """Create minimal test data files with domain-relevant examples.
        
        Creates two sample proverbs focused on wealth and entrepreneurship
        themes to support development and testing of the thiLLMo system.
        
        Returns:
            tuple: (csv_file_path, json_file_path) of created test files
        """
        test_data = [
            {
                'kikuyu_text': 'Mũndũ wa wĩra ndaagaga thiĩni',
                'literal_translation': 
                    'A person of work does not remain in poverty',
                'cultural_meaning': 
                    'Those who work hard consistently will eventually '
                    'achieve prosperity and escape poverty. This proverb '
                    'emphasizes the Kikuyu cultural value of diligence '
                    'and perseverance as the foundation of success.',
                'themes': 'hard_work,wealth_accumulation,success',
                'domain_relevance': 
                    'Emphasizes work ethic as foundation for wealth building '
                    'and entrepreneurial success in Kikuyu culture',
                'usage_context': 
                    'Encouraging someone to persist in their efforts, '
                    'especially young people starting businesses',
                'complexity_level': 'simple',
                'frequency_rating': 'very_common',
                'source_type': 'oral_tradition',
                'region_variants': 'central_kenya,muranga,kiambu',
                'usage_notes': 
                    'Often used by elders to motivate youth in business ventures'
            },
            {
                'kikuyu_text': 'Mbeca ĩrĩa ĩhithĩtwo nĩyo ĩcokagĩra mũciĩ',
                'literal_translation': 
                    'Money that is saved is what returns home',
                'cultural_meaning': 
                    'Only through saving and careful financial planning '
                    'can one build lasting wealth that benefits the family '
                    'and community. This reflects the Kikuyu emphasis on '
                    'financial prudence and long-term thinking.',
                'themes': 'saving,financial_wisdom,resource_management',
                'domain_relevance': 
                    'Teaches importance of saving over spending for '
                    'long-term wealth accumulation and business sustainability',
                'usage_context': 'Financial advice for entrepreneurs and young families',
                'complexity_level': 'simple',
                'frequency_rating': 'common',
                'source_type': 'traditional_teachings',
                'region_variants': 'central_kenya,muranga,nyeri',
                'usage_notes': 
                    'Common advice for new business owners about '
                    'financial discipline and reinvestment'
            }
        ]
        
        # Save as CSV
        csv_file = self.data_dir / "test_proverbs.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=test_data[0].keys())
            writer.writeheader()
            writer.writerows(test_data)
        
        # Save as JSON with linguistic enrichment
        enriched_data = []
        for item in test_data:
            enriched_item = item.copy()
            enriched_item['morphological_analysis'] = (
                self._generate_morphological_analysis(item['kikuyu_text'])
            )
            enriched_item['metaphorical_structure'] = (
                self._generate_metaphorical_structure(
                    item['kikuyu_text'], 
                    item['cultural_meaning']
                )
            )
            enriched_data.append(enriched_item)
        
        json_file = self.data_dir / "test_proverbs_extended.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(enriched_data, f, indent=2, ensure_ascii=False)
        
        logger.info(
            f"Created minimal test data: {csv_file.name} and {json_file.name}"
        )
        return csv_file, json_file
    
    def _generate_morphological_analysis(self, kikuyu_text: str) -> str:
        """Generate basic morphological analysis for Kikuyu text.
        
        Provides simplified morphological breakdown following Kikuyu
        linguistic patterns. This supports the thiLLMo linguistic
        analysis component.
        
        Args:
            kikuyu_text: Original Kikuyu proverb text
            
        Returns:
            String with morphological analysis
        """
        words = kikuyu_text.split()
        analysis_parts = []
        
        # Morphological patterns for Kikuyu
        patterns = {
            r'^mũ': lambda w: f"mũ-{w[2:]}",  # Noun class 1 (person)
            r'^kĩ': lambda w: f"kĩ-{w[2:]}",  # Noun class 7 (thing)
            r'^nda': lambda w: f"NEG-{w[3:]}",  # Negation
            r'^ndu': lambda w: f"NEG-{w[3:]}",  # Negation
            r'ĩtwo$': lambda w: f"{w[:-4]}-PAST.PASS",  # Past passive
        }
        
        for word in words:
            analyzed = False
            for pattern, transform in patterns.items():
                if re.match(pattern, word) and len(word) > 2:
                    analysis_parts.append(transform(word))
                    analyzed = True
                    break
            
            if not analyzed:
                analysis_parts.append(word)
        
        return ' '.join(analysis_parts)
    
    def _generate_metaphorical_structure(
        self, 
        kikuyu_text: str, 
        cultural_meaning: str
    ) -> str:
        """Generate metaphorical structure analysis.
        
        Analyzes the metaphorical mapping in Kikuyu proverbs following
        conceptual metaphor theory. This supports the thiLLMo cultural
        preservation mission by documenting metaphorical patterns.
        
        Args:
            kikuyu_text: Original Kikuyu text
            cultural_meaning: Cultural interpretation
            
        Returns:
            JSON string with metaphor structure analysis
        """
        # Metaphorical mappings based on common vehicles in Kikuyu proverbs
        vehicle_mappings = {
            'mũgũnda|gĩthaka': {
                "vehicle": "agricultural_field",
                "tenor": "business_venture",
                "mapping": "cultivation_growth_harvest",
                "cultural_domain": "farming_business"
            },
            'mũtĩ': {
                "vehicle": "tree_plant", 
                "tenor": "person_business",
                "mapping": "growth_strength_roots",
                "cultural_domain": "nature_human"
            },
            'njĩra': {
                "vehicle": "path_road",
                "tenor": "business_journey", 
                "mapping": "direction_progress_destination",
                "cultural_domain": "journey_life"
            },
            'mbeca|mbeca': {
                "vehicle": "money_currency",
                "tenor": "value_worth",
                "mapping": "saving_accumulation_return",
                "cultural_domain": "economics_values"
            }
        }
        
        kikuyu_lower = kikuyu_text.lower()
        
        for pattern, structure in vehicle_mappings.items():
            if re.search(pattern, kikuyu_lower):
                return json.dumps(structure)
        
        # Default structure for non-metaphorical proverbs
        return json.dumps({
            "vehicle": "concrete_concept",
            "tenor": "abstract_principle",
            "mapping": "direct_application",
            "cultural_domain": "wisdom_teaching"
        })
    
    def load_from_csv(self, csv_file: Union[str, Path]) -> List[ProverbData]:
        """Load proverbs from CSV file.
        
        Args:
            csv_file: Path to CSV file with proverb data
            
        Returns:
            List of ProverbData instances
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            Exception: For CSV parsing errors
        """
        csv_path = Path(csv_file)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            proverbs = []
            
            for _, row in df.iterrows():
                proverb = ProverbData(
                    id=row.get('id', ''),
                    kikuyu_text=row['kikuyu_text'],
                    literal_translation=row['literal_translation'],
                    cultural_meaning=row['cultural_meaning'],
                    themes=row['themes'],
                    domain_relevance=row['domain_relevance'],
                    usage_context=row['usage_context'],
                    complexity_level=row['complexity_level'],
                    frequency_rating=row['frequency_rating'],
                    source_type=row['source_type'],
                    region_variants=row['region_variants'],
                    phonetic_transcription=row.get('phonetic_transcription'),
                    morphological_analysis=row.get('morphological_analysis'),
                    usage_notes=row.get('usage_notes'),
                    validation_status=row.get(
                        'validation_status', 
                        'pending_review'
                    )
                )
                proverbs.append(proverb)
            
            logger.info(f"Loaded {len(proverbs)} proverbs from {csv_path}")
            return proverbs
            
        except Exception as e:
            logger.error(f"Error loading CSV {csv_path}: {e}")
            raise
    
    def load_from_json(self, json_file: Union[str, Path]) -> List[ProverbData]:
        """Load proverbs from JSON file.
        
        Args:
            json_file: Path to JSON file with proverb data
            
        Returns:
            List of ProverbData instances
            
        Raises:
            FileNotFoundError: If JSON file doesn't exist
            Exception: For JSON parsing errors
        """
        json_path = Path(json_file)
        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            proverbs = [ProverbData(**item) for item in data]
            
            logger.info(f"Loaded {len(proverbs)} proverbs from {json_path}")
            return proverbs
            
        except Exception as e:
            logger.error(f"Error loading JSON {json_path}: {e}")
            raise
    
    def filter_by_domain(self, proverbs: List[ProverbData]) -> List[ProverbData]:
        """Filter proverbs to match configured domain themes.
        
        Args:
            proverbs: List of ProverbData instances to filter
            
        Returns:
            List of domain-relevant ProverbData instances
        """
        domain_proverbs = []
        
        for proverb in proverbs:
            proverb_themes = [theme.lower().strip() for theme in proverb.themes]
            
            is_domain_relevant = self._check_theme_relevance(proverb_themes)
            
            if not is_domain_relevant:
                is_domain_relevant = self._check_kikuyu_terms(proverb.kikuyu_text)
            
            if not is_domain_relevant and proverb.domain_relevance:
                is_domain_relevant = len(proverb.domain_relevance.strip()) > 10
            
            if is_domain_relevant:
                domain_proverbs.append(proverb)
        
        logger.info(
            f"Filtered to {len(domain_proverbs)} domain-relevant proverbs "
            f"from {len(proverbs)} total"
        )
        return domain_proverbs
    
    def _check_theme_relevance(self, proverb_themes: List[str]) -> bool:
        """Check if proverb themes match domain configuration."""
        for domain_category, keywords in self.config.domain_themes.items():
            if any(
                keyword in theme 
                for theme in proverb_themes 
                for keyword in keywords
            ):
                return True
        return False
    
    def _check_kikuyu_terms(self, kikuyu_text: str) -> bool:
        """Check if Kikuyu text contains domain-specific terms."""
        kikuyu_lower = kikuyu_text.lower()
        return any(
            term in kikuyu_lower 
            for term in self.config.kikuyu_domain_terms.keys()
        )
    
    def validate_proverb_data(
        self, 
        proverbs: List[ProverbData]
    ) -> List[ProverbData]:
        """Validate and clean proverb data.
        
        Performs comprehensive validation of proverb data quality
        to ensure cultural accuracy and completeness for the thiLLMo system.
        
        Args:
            proverbs: List of ProverbData instances to validate
            
        Returns:
            List of validated ProverbData instances with status updates
        """
        valid_proverbs = []
        
        for proverb in proverbs:
            issues = self._identify_validation_issues(proverb)
            
            if issues:
                logger.warning(
                    f"Validation issues for '{proverb.kikuyu_text[:30]}...': "
                    f"{'; '.join(issues)}"
                )
                proverb.validation_status = (
                    f"has_issues: {'; '.join(issues[:2])}"
                )
            else:
                proverb.validation_status = "validated"
            
            valid_proverbs.append(proverb)
        
        issues_count = len([
            p for p in valid_proverbs 
            if 'has_issues' in p.validation_status
        ])
        
        logger.info(
            f"Validated {len(valid_proverbs)} proverbs, "
            f"{issues_count} have issues"
        )
        return valid_proverbs
    
    def _identify_validation_issues(self, proverb: ProverbData) -> List[str]:
        """Identify validation issues for a proverb."""
        issues = []
        
        # Required field validations
        validations = [
            (
                len(proverb.kikuyu_text.strip()) < 
                self.config.min_kikuyu_length,
                "Missing or too short Kikuyu text"
            ),
            (
                len(proverb.literal_translation.strip()) < 
                self.config.min_translation_length,
                "Missing or too short literal translation"
            ),
            (
                len(proverb.cultural_meaning.strip()) < 
                self.config.min_cultural_meaning_length,
                "Missing or too short cultural meaning"
            ),
            (
                not proverb.themes or len(proverb.themes) == 0,
                "No themes specified"
            ),
            (
                proverb.kikuyu_text == proverb.literal_translation,
                "Kikuyu text identical to translation"
            ),
            (
                len(proverb.cultural_meaning) < 
                len(proverb.literal_translation) * 0.5,
                "Cultural meaning suspiciously short"
            )
        ]
        
        for condition, message in validations:
            if condition:
                issues.append(message)
        
        return issues
    
    def enrich_with_linguistics(
        self, 
        proverbs: List[ProverbData]
    ) -> List[ProverbData]:
        """Add linguistic analysis to proverbs that lack it.
        
        Enriches proverbs with morphological analysis, metaphorical
        structure, and phonetic transcription to support the thiLLMo
        linguistic processing pipeline.
        
        Args:
            proverbs: List of ProverbData instances to enrich
            
        Returns:
            List of linguistically enriched ProverbData instances
        """
        for proverb in proverbs:
            if not proverb.morphological_analysis:
                proverb.morphological_analysis = (
                    self._generate_morphological_analysis(proverb.kikuyu_text)
                )
            
            if not proverb.metaphorical_structure:
                proverb.metaphorical_structure = (
                    self._generate_metaphorical_structure(
                        proverb.kikuyu_text, 
                        proverb.cultural_meaning
                    )
                )
            
            if not proverb.phonetic_transcription:
                proverb.phonetic_transcription = (
                    f"[{proverb.kikuyu_text.lower()}]"
                )
        
        logger.info(f"Enriched {len(proverbs)} proverbs with linguistic data")
        return proverbs
    
    def load_and_process_proverbs(
        self, 
        file_path: Union[str, Path]
    ) -> List[ProverbData]:
        """Main method to load and process proverbs from file.
        
        This is the primary interface for loading proverb data into
        the thiLLMo system with complete processing pipeline.
        
        Args:
            file_path: Path to proverb data file (CSV or JSON)
            
        Returns:
            List of fully processed ProverbData instances
            
        Raises:
            ValueError: For unsupported file types
        """
        file_path = Path(file_path)
        
        # Load based on file type
        if file_path.suffix.lower() == '.csv':
            proverbs = self.load_from_csv(file_path)
        elif file_path.suffix.lower() == '.json':
            proverbs = self.load_from_json(file_path)
        else:
            raise ValueError(
                f"Unsupported file type: {file_path.suffix}. "
                f"Use .csv or .json"
            )
        
        # Process the data through thiLLMo pipeline
        proverbs = self.filter_by_domain(proverbs)
        proverbs = self.validate_proverb_data(proverbs)
        proverbs = self.enrich_with_linguistics(proverbs)
        
        self.loaded_proverbs = proverbs
        return proverbs
    
    def get_proverbs_for_neo4j(self) -> List[Dict[str, Any]]:
        """Convert loaded proverbs to Neo4j-compatible format.
        
        Prepares proverb data for integration with the thiLLMo
        Neo4j ontology system.
        
        Returns:
            List of dictionaries formatted for Neo4j ingestion
        """
        neo4j_proverbs = []
        
        for proverb in self.loaded_proverbs:
            neo4j_data = {
                'id': proverb.id,
                'kikuyu_text': proverb.kikuyu_text,
                'phonetic_transcription': (
                    proverb.phonetic_transcription or 
                    f"[{proverb.kikuyu_text.lower()}]"
                ),
                'morphological_analysis': proverb.morphological_analysis or '',
                'literal_translation': proverb.literal_translation,
                'cultural_meaning': proverb.cultural_meaning,
                'usage_notes': proverb.usage_notes or '',
                'metaphorical_structure': proverb.metaphorical_structure or '{}',
                'themes': proverb.themes,
                'domain_relevance': proverb.domain_relevance,
                'complexity_level': proverb.complexity_level,
                'frequency_rating': proverb.frequency_rating,
                'validation_status': proverb.validation_status,
                'source_type': proverb.source_type,
                'region_variants': proverb.region_variants,
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat()
            }
            neo4j_proverbs.append(neo4j_data)
        
        return neo4j_proverbs
    
    def export_processed_data(self, output_path: Union[str, Path]) -> None:
        """Export processed proverbs to file.
        
        Exports processed proverb data to the thiLLMo data/processed/
        directory for use by other system components.
        
        Args:
            output_path: Path for output file (JSON or CSV)
            
        Raises:
            ValueError: For unsupported export formats
        """
        output_path = Path(output_path)
        
        if output_path.suffix.lower() == '.json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(
                    [asdict(proverb) for proverb in self.loaded_proverbs],
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=str
                )
        elif output_path.suffix.lower() == '.csv':
            df = pd.DataFrame([
                asdict(proverb) for proverb in self.loaded_proverbs
            ])
            df.to_csv(output_path, index=False, encoding='utf-8')
        else:
            raise ValueError(
                f"Unsupported export format: {output_path.suffix}"
            )
        
        logger.info(
            f"Exported {len(self.loaded_proverbs)} processed proverbs "
            f"to {output_path}"
        )


def create_domain_proverbs(
    ontology_instance, 
    proverb_loader: WealthEntrepreneurshipProverbLoader
) -> None:
    """Create proverbs from loaded data in Neo4j ontology.
    
    Integrates with the thiLLMo ontology system to create proverb nodes
    in the Neo4j knowledge graph.
    
    Args:
        ontology_instance: thiLLMo ontology manager instance
        proverb_loader: Configured proverb loader with data
    """
    if not proverb_loader.loaded_proverbs:
        logger.warning("No proverbs loaded. Creating minimal test data...")
        csv_file, _ = proverb_loader.create_minimal_test_data()
        proverb_loader.load_and_process_proverbs(csv_file)
    
    neo4j_proverbs = proverb_loader.get_proverbs_for_neo4j()
    
    with ontology_instance.driver.session() as session:
        for proverb_data in neo4j_proverbs:
            proverb_query = """
            CREATE (p:Proverb {
                id: $id,
                kikuyu_text: $kikuyu_text,
                phonetic_transcription: $phonetic_transcription,
                morphological_analysis: $morphological_analysis,
                literal_translation: $literal_translation,
                cultural_meaning: $cultural_meaning,
                usage_notes: $usage_notes,
                metaphorical_structure: $metaphorical_structure,
                themes: $themes,
                domain_relevance: $domain_relevance,
                complexity_level: $complexity_level,
                frequency_rating: $frequency_rating,
                validation_status: $validation_status,
                source_type: $source_type,
                region_variants: $region_variants,
                created_at: $created_at,
                last_updated: $last_updated
            })
            """
            
            session.run(proverb_query, proverb_data)
            logger.info(f"Created proverb node: {proverb_data['id']}")
    
    logger.info(f"Created {len(neo4j_proverbs)} proverbs in Neo4j")


if __name__ == "__main__":
    """Development and testing script for thiLLMo proverb loader."""
    
    # Initialize loader with thiLLMo project configuration
    loader = WealthEntrepreneurshipProverbLoader()
    
    # Create minimal test data for development
    print("thiLLMo Proverb Loader - Creating minimal test data...")
    csv_file, json_file = loader.create_minimal_test_data()
    
    # Load and process the data
    print("Loading and processing proverbs...")
    proverbs = loader.load_and_process_proverbs(csv_file)
    
    # Display results
    print(f"\nLoaded {len(proverbs)} proverbs for thiLLMo system:")
    for i, proverb in enumerate(proverbs, 1):
        print(f"\n{i}. {proverb.kikuyu_text}")
        print(f"   Translation: {proverb.literal_translation}")
        print(f"   Themes: {', '.join(proverb.themes)}")
        print(f"   Cultural relevance: {proverb.domain_relevance}")
        print(f"   Status: {proverb.validation_status}")
    
    # Export processed data to thiLLMo data/processed/ directory
    processed_dir = Path("data/processed")
    processed_dir.mkdir(exist_ok=True)
    output_file = processed_dir / "processed_test_proverbs.json"
    loader.export_processed_data(output_file)
    
    print(f"\nthiLLMo proverb loader ready!")
    print(f"Test data exported to: {output_file}")
    print("Configure .env file to customize domain themes and validation rules.")
