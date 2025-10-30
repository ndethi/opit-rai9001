"""
Context Builder for OG-RAG System

Formats retrieved proverbs from Neo4j graph into structured prompts for GPT-4.
Provides cultural context through:
1. Similar proverbs with expert translations
2. Cultural meanings and explanations
3. Concept definitions and relationships
4. Metaphorical patterns and themes

Author: Research Team
Date: October 30, 2025
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

# Use try/except for imports to support both direct execution and module import
try:
    from .graph_retriever import RetrievedProverb
except ImportError:
    from graph_retriever import RetrievedProverb


@dataclass
class CulturalContext:
    """Structured cultural context package for LLM prompting."""
    similar_proverbs: List[RetrievedProverb]
    concepts: List[str]
    concept_definitions: Dict[str, str]
    cultural_themes: List[str]
    prompt_text: str


class ContextBuilder:
    """
    Builds culturally-grounded context for GPT-4 translation.
    
    Formats retrieved proverbs into structured prompts that:
    - Provide example translations from experts
    - Explain cultural meanings and metaphors
    - Define relevant cultural concepts
    - Guide LLM towards faithful translations
    """
    
    # Concept definitions from Kikuyu cultural framework
    CONCEPT_DEFINITIONS = {
        'wealth': 'Utonga in Kikuyu - Material prosperity measured not just in possessions but in social capital (family, livestock, land). Wealth enables generosity and community standing.',
        'poverty': 'Ũthĩĩni in Kikuyu - Lack of resources, but also social isolation. Poverty is both material and relational, affecting one\'s ability to participate in community life.',
        'wisdom': 'Ũũgĩ in Kikuyu - Practical knowledge gained through experience, age, and cultural learning. Wisdom is demonstrated through proper behavior, speech, and decision-making.',
        'foolishness': 'Ũrimũ in Kikuyu - Lack of judgment, often manifest in impulsive actions, disrespect for elders, or ignoring cultural norms. Foolishness brings shame and social consequences.',
        'kinship': 'Ũrĩa wa mũhĩrĩga - Blood relationships and clan connections. Kinship defines obligations, support networks, and social identity. Extended family is central to Kikuyu society.',
        'greed': 'Ũkoroku - Insatiable desire for possessions beyond one\'s needs. Greed violates the cultural value of sharing and community reciprocity.',
        'perseverance': 'Kũũmĩrĩria - Endurance through hardship, patience in long-term efforts. Perseverance is valued in agriculture, relationships, and personal development.',
        'patience': 'Kĩhonia - Ability to wait, to endure discomfort, to delay gratification. Patience is essential for farming cycles, conflict resolution, and achieving goals.',
        'cooperation': 'Ũrũmwe - Unity and collective action. Cooperation through work parties (ngwatio), mutual aid, and communal decision-making is fundamental to community survival.',
        'respect': 'Gĩtĩĩo - Deference shown to elders, authority figures, and cultural norms. Respect is demonstrated through language, posture, and behavior.',
        'hospitality': 'Ũhote wa mũgeni - Welcoming strangers and visitors with food and shelter. Hospitality is a sacred duty that brings blessings and strengthens social bonds.',
        'honesty': 'Ũhoro wa ma - Truth-telling and integrity in dealings. Honesty builds trust and reputation, while dishonesty destroys social standing.',
        'hard_work': 'Kũruta wĩra - Diligent labor, especially in agriculture. Hard work is morally valued and distinguishes the responsible from the lazy.',
        'laziness': 'Ũgũta - Avoidance of work, dependence on others. Laziness is morally condemned as it burdens the community and leads to poverty.',
        'marriage': 'Ũhiki - Sacred union between families, not just individuals. Marriage involves bride wealth (rũraacio), creates kinship alliances, and ensures continuity.'
    }
    
    def __init__(self):
        """Initialize the context builder."""
        pass
    
    def build_cultural_context(
        self, 
        retrieved_proverbs: List[RetrievedProverb],
        max_examples: int = 5
    ) -> CulturalContext:
        """
        Build complete cultural context from retrieved proverbs.
        
        Args:
            retrieved_proverbs: List of proverbs from graph retrieval
            max_examples: Maximum number of example proverbs to include
            
        Returns:
            CulturalContext object with formatted prompt
        """
        # Limit to max examples
        proverbs = retrieved_proverbs[:max_examples]
        
        # Extract unique concepts
        concepts = self._extract_unique_concepts(proverbs)
        
        # Get concept definitions
        concept_defs = self._get_concept_definitions(concepts)
        
        # Extract cultural themes
        themes = self._extract_themes(proverbs)
        
        # Build the prompt
        prompt = self._build_prompt(proverbs, concepts, concept_defs, themes)
        
        return CulturalContext(
            similar_proverbs=proverbs,
            concepts=concepts,
            concept_definitions=concept_defs,
            cultural_themes=themes,
            prompt_text=prompt
        )
    
    def _extract_unique_concepts(self, proverbs: List[RetrievedProverb]) -> List[str]:
        """Extract unique cultural concepts from retrieved proverbs."""
        concepts = set()
        for proverb in proverbs:
            if proverb.matched_concepts:
                concepts.update(proverb.matched_concepts)
        return sorted(list(concepts))
    
    def _get_concept_definitions(self, concepts: List[str]) -> Dict[str, str]:
        """Get definitions for cultural concepts."""
        return {
            concept: self.CONCEPT_DEFINITIONS.get(concept, f"Cultural concept: {concept}")
            for concept in concepts
        }
    
    def _extract_themes(self, proverbs: List[RetrievedProverb]) -> List[str]:
        """Extract common cultural themes from proverbs."""
        themes = []
        
        # Analyze cultural meanings for themes
        meanings = [p.expert_cultural_meaning for p in proverbs if p.expert_cultural_meaning]
        
        # Common theme keywords
        theme_keywords = {
            'community': ['community', 'together', 'collective', 'cooperation'],
            'wisdom': ['wisdom', 'knowledge', 'learning', 'understanding'],
            'caution': ['caution', 'careful', 'warning', 'danger'],
            'reciprocity': ['reciprocity', 'return', 'exchange', 'mutual'],
            'consequences': ['consequences', 'result', 'outcome', 'effect'],
            'values': ['values', 'virtue', 'moral', 'character']
        }
        
        # Identify themes
        meanings_text = ' '.join(meanings).lower()
        for theme, keywords in theme_keywords.items():
            if any(keyword in meanings_text for keyword in keywords):
                themes.append(theme)
        
        return themes if themes else ['cultural wisdom']
    
    def _build_prompt(
        self,
        proverbs: List[RetrievedProverb],
        concepts: List[str],
        concept_defs: Dict[str, str],
        themes: List[str]
    ) -> str:
        """
        Build structured prompt for GPT-4.
        
        Creates a comprehensive context package including:
        - Role definition (cultural expert)
        - Similar proverb examples
        - Cultural meanings and metaphors
        - Concept definitions
        - Translation guidelines
        """
        prompt_parts = []
        
        # 1. Role Definition
        prompt_parts.append(
            "You are a cultural translation expert specializing in Kikuyu proverbs. "
            "Your task is to translate Kikuyu proverbs into English while preserving "
            "cultural meanings, metaphorical structures, and figurative language."
        )
        
        # 2. Cultural Context Section
        if concepts:
            prompt_parts.append("\n## CULTURAL CONCEPTS\n")
            prompt_parts.append("The following proverb involves these Kikuyu cultural concepts:\n")
            for concept in concepts:
                definition = concept_defs.get(concept, "")
                prompt_parts.append(f"- **{concept.title()}**: {definition}\n")
        
        # 3. Example Proverbs Section
        prompt_parts.append("\n## SIMILAR KIKUYU PROVERBS (Expert Translations)\n")
        prompt_parts.append(
            "These are similar proverbs from the Kikuyu tradition, "
            "translated by cultural experts:\n"
        )
        
        for i, proverb in enumerate(proverbs, 1):
            prompt_parts.append(f"\n### Example {i}:")
            prompt_parts.append(f"\n**Kikuyu:** {proverb.kikuyu_text}")
            prompt_parts.append(f"\n**Expert Translation:** {proverb.expert_translation}")
            
            if proverb.expert_cultural_meaning:
                prompt_parts.append(f"\n**Cultural Meaning:** {proverb.expert_cultural_meaning}")
            
            if proverb.expert_business_relevance:
                prompt_parts.append(f"\n**Practical Application:** {proverb.expert_business_relevance}")
            
            if proverb.matched_concepts:
                concepts_str = ", ".join(proverb.matched_concepts)
                prompt_parts.append(f"\n**Related Concepts:** {concepts_str}")
        
        # 4. Cultural Themes
        if themes:
            prompt_parts.append("\n\n## CULTURAL THEMES\n")
            prompt_parts.append(f"Common themes in these proverbs: {', '.join(themes)}")
        
        # 5. Translation Guidelines
        prompt_parts.append("\n\n## TRANSLATION GUIDELINES\n")
        guidelines = [
            "1. **Preserve Metaphors**: Keep the figurative language and imagery intact",
            "2. **Cultural Fidelity**: Maintain the cultural meaning and values expressed",
            "3. **Natural English**: Use fluent English that sounds like a proverb",
            "4. **Avoid Literalism**: Don't translate word-for-word; capture the essence",
            "5. **Contextual Meaning**: Consider the cultural context shown in examples above"
        ]
        prompt_parts.append("\n".join(guidelines))
        
        # 6. Output Format
        prompt_parts.append("\n\n## OUTPUT FORMAT\n")
        prompt_parts.append(
            "Provide your translation in the following format:\n"
            "**Translation:** [Your English translation]\n"
            "**Explanation:** [Brief explanation of the cultural meaning and metaphor]"
        )
        
        return "".join(prompt_parts)
    
    def build_ograg_prompt(
        self,
        kikuyu_proverb: str,
        retrieved_proverbs: List[RetrievedProverb],
        max_examples: int = 5
    ) -> str:
        """
        Build complete OG-RAG prompt for translation.
        
        Args:
            kikuyu_proverb: The proverb to translate
            retrieved_proverbs: Retrieved similar proverbs from graph
            max_examples: Maximum number of examples to include
            
        Returns:
            Complete prompt string ready for GPT-4 API
        """
        # Build cultural context
        context = self.build_cultural_context(retrieved_proverbs, max_examples)
        
        # Combine context with translation request
        full_prompt = f"{context.prompt_text}\n\n"
        full_prompt += "=" * 80 + "\n\n"
        full_prompt += "## PROVERB TO TRANSLATE\n\n"
        full_prompt += f"**Kikuyu Text:** {kikuyu_proverb}\n\n"
        full_prompt += "Using the cultural context and examples above, provide a culturally faithful translation:\n"
        
        return full_prompt
    
    def build_traditional_rag_prompt(
        self,
        kikuyu_proverb: str,
        retrieved_proverbs: List[RetrievedProverb],
        max_examples: int = 5
    ) -> str:
        """
        Build traditional RAG prompt (without ontology grounding).
        
        This is for comparison purposes - uses retrieved examples but
        without the rich cultural context, concept definitions, or
        structured formatting that OG-RAG provides.
        
        Args:
            kikuyu_proverb: The proverb to translate
            retrieved_proverbs: Retrieved similar proverbs
            max_examples: Maximum number of examples
            
        Returns:
            Traditional RAG prompt string
        """
        proverbs = retrieved_proverbs[:max_examples]
        
        prompt_parts = []
        
        # Simple instruction
        prompt_parts.append(
            "Translate the following Kikuyu proverb into English. "
            "Here are some similar proverbs for reference:\n\n"
        )
        
        # Just list examples without cultural context
        for i, proverb in enumerate(proverbs, 1):
            prompt_parts.append(f"{i}. {proverb.kikuyu_text} → {proverb.expert_translation}\n")
        
        # Translation request
        prompt_parts.append(f"\nNow translate: {kikuyu_proverb}\n")
        prompt_parts.append("Translation:")
        
        return "".join(prompt_parts)
    
    def build_raw_prompt(self, kikuyu_proverb: str) -> str:
        """
        Build raw prompt (no RAG, no context).
        
        This is the baseline - just asking GPT-4 to translate
        without any examples or cultural context.
        
        Args:
            kikuyu_proverb: The proverb to translate
            
        Returns:
            Raw prompt string
        """
        return (
            f"Translate this Kikuyu proverb into English: {kikuyu_proverb}\n"
            "Translation:"
        )
    
    def format_example_context(
        self,
        proverbs: List[RetrievedProverb],
        include_meanings: bool = True,
        include_concepts: bool = True
    ) -> str:
        """
        Format proverbs as example context (flexible formatting).
        
        Args:
            proverbs: List of retrieved proverbs
            include_meanings: Whether to include cultural meanings
            include_concepts: Whether to include concept tags
            
        Returns:
            Formatted example text
        """
        examples = []
        
        for i, proverb in enumerate(proverbs, 1):
            example = f"{i}. **Kikuyu:** {proverb.kikuyu_text}\n"
            example += f"   **English:** {proverb.expert_translation}\n"
            
            if include_meanings and proverb.expert_cultural_meaning:
                example += f"   **Meaning:** {proverb.expert_cultural_meaning}\n"
            
            if include_concepts and proverb.matched_concepts:
                concepts_str = ", ".join(proverb.matched_concepts)
                example += f"   **Concepts:** {concepts_str}\n"
            
            examples.append(example)
        
        return "\n".join(examples)


# Testing harness
if __name__ == "__main__":
    print("=" * 80)
    print("CONTEXT BUILDER TEST")
    print("=" * 80)
    
    # Create mock retrieved proverbs for testing
    mock_proverbs = [
        RetrievedProverb(
            proverb_id="MW_001",
            kikuyu_text="Aikaragia mbia ta njuu ngigi",
            expert_translation="He looks after his money the way storks pursue locusts",
            expert_cultural_meaning="Describes someone who is extremely careful with their money, watching it vigilantly like storks chase locusts. Emphasizes both carefulness and perhaps greed.",
            expert_business_relevance="Applies to financial management and resource stewardship in organizations.",
            cultural_weight=10.0,
            thematic_category="wealth",
            matched_concepts=["wealth", "greed"],
            similarity_score=0.960,
            retrieval_method="hybrid"
        ),
        RetrievedProverb(
            proverb_id="MW_002",
            kikuyu_text="Andu ni indo",
            expert_translation="People are wealth",
            expert_cultural_meaning="True wealth is measured in relationships and community, not just material possessions. People provide labor, support, and social capital.",
            expert_business_relevance="Emphasizes human capital and relationship building as core business assets.",
            cultural_weight=10.0,
            thematic_category="wealth",
            matched_concepts=["wealth", "kinship"],
            similarity_score=0.800,
            retrieval_method="hybrid"
        ),
        RetrievedProverb(
            proverb_id="MW_003",
            kikuyu_text="Bururi uri ngui nduraagagwo ni indo",
            expert_translation="In an unstable country, wealth is not accumulated",
            expert_cultural_meaning="Political instability and insecurity prevent economic prosperity. Without peace and order, wealth cannot be built or maintained.",
            expert_business_relevance="Highlights importance of stable governance and security for economic development.",
            cultural_weight=10.0,
            thematic_category="wealth",
            matched_concepts=["wealth", "cooperation"],
            similarity_score=0.800,
            retrieval_method="hybrid"
        )
    ]
    
    # Initialize context builder
    builder = ContextBuilder()
    
    # Test 1: Build OG-RAG prompt
    print("\n" + "=" * 80)
    print("TEST 1: OG-RAG PROMPT (Full Cultural Context)")
    print("=" * 80)
    
    input_proverb = "Aikaragia mbia ta njuu ngigi"
    ograg_prompt = builder.build_ograg_prompt(input_proverb, mock_proverbs, max_examples=3)
    
    print("\n" + ograg_prompt[:1000] + "...\n")  # Show first 1000 chars
    print(f"✅ OG-RAG prompt length: {len(ograg_prompt)} characters")
    
    # Test 2: Build Traditional RAG prompt
    print("\n" + "=" * 80)
    print("TEST 2: TRADITIONAL RAG PROMPT (Examples Only)")
    print("=" * 80)
    
    trad_prompt = builder.build_traditional_rag_prompt(input_proverb, mock_proverbs, max_examples=3)
    print("\n" + trad_prompt)
    print(f"\n✅ Traditional RAG prompt length: {len(trad_prompt)} characters")
    
    # Test 3: Build Raw prompt
    print("\n" + "=" * 80)
    print("TEST 3: RAW PROMPT (No Context)")
    print("=" * 80)
    
    raw_prompt = builder.build_raw_prompt(input_proverb)
    print("\n" + raw_prompt)
    print(f"\n✅ Raw prompt length: {len(raw_prompt)} characters")
    
    # Test 4: Cultural Context Object
    print("\n" + "=" * 80)
    print("TEST 4: CULTURAL CONTEXT OBJECT")
    print("=" * 80)
    
    context = builder.build_cultural_context(mock_proverbs, max_examples=3)
    print(f"\n✅ Similar Proverbs: {len(context.similar_proverbs)}")
    print(f"✅ Concepts Identified: {context.concepts}")
    print(f"✅ Cultural Themes: {context.cultural_themes}")
    print(f"✅ Concept Definitions: {len(context.concept_definitions)} defined")
    
    # Show concept definitions
    print("\nConcept Definitions:")
    for concept, definition in context.concept_definitions.items():
        print(f"  - {concept}: {definition[:100]}...")
    
    # Test 5: Compare prompt lengths
    print("\n" + "=" * 80)
    print("TEST 5: PROMPT COMPARISON")
    print("=" * 80)
    
    print(f"\nRaw prompt:           {len(raw_prompt):>6} chars (baseline)")
    print(f"Traditional RAG:      {len(trad_prompt):>6} chars ({len(trad_prompt)/len(raw_prompt):.1f}x raw)")
    print(f"OG-RAG (ontology):    {len(ograg_prompt):>6} chars ({len(ograg_prompt)/len(raw_prompt):.1f}x raw)")
    
    ratio = len(ograg_prompt) / len(trad_prompt)
    print(f"\nOG-RAG provides {ratio:.1f}x more context than traditional RAG")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print("\nContext Builder successfully:")
    print("  ✓ Formats proverbs with cultural meanings")
    print("  ✓ Includes concept definitions from ontology")
    print("  ✓ Extracts cultural themes automatically")
    print("  ✓ Provides translation guidelines")
    print("  ✓ Supports three prompt types (raw, traditional RAG, OG-RAG)")
    print("  ✓ Builds structured, comprehensive prompts for GPT-4")
