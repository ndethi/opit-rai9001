# Kikuyu Proverb Ontology Design Specification
**Version:** 2.0  
**Date:** October 14, 2025  
**Status:** Design Phase (Phase 2b)  
**Project:** thiLLMo - Ontology-Grounded RAG for Kikuyu Proverb Translation

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Design Principles](#design-principles)
3. [Gap Analysis Integration](#gap-analysis-integration)
4. [Core Ontology Classes](#core-ontology-classes)
5. [Object Properties (Relationships)](#object-properties-relationships)
6. [Data Properties](#data-properties)
7. [Constraints and Cardinality](#constraints-and-cardinality)
8. [Priority-Based Implementation](#priority-based-implementation)
9. [Integration with Existing Infrastructure](#integration-with-existing-infrastructure)
10. [OG-RAG Optimization Strategy](#og-rag-optimization-strategy)
11. [Implementation Roadmap](#implementation-roadmap)

---

## 1. Executive Summary

This document specifies the manual ontology design for the Kikuyu Proverb Knowledge Graph, integrating:

### Data Foundation
- **Phase 2a Extraction:** 186 entities, 88 actions, 150 cultural concepts, 80 metaphors from 100 proverbs
- **Gap Analysis (Phase 2.5):** 97% baseline MT failure rate, identifying critical concepts requiring deep representation
- **Existing Infrastructure:** ontology_builder.py and kikuyu_proverb_ontology.py frameworks

### Critical Design Drivers (from Gap Analysis)
1. **Wealth/Poverty concepts** - CRITICAL priority (30 combined failures)
2. **Metaphorical structures** - 4.5% baseline preservation (near zero)
3. **Cultural meanings** - 6.7% baseline fidelity (catastrophic loss)
4. **Semantic similarity** - 11.5% baseline (extremely poor)

### Design Goals
- **Primary:** Enable OG-RAG system to achieve >50% cultural fidelity (7.5x improvement over baseline)
- **Secondary:** Preserve 100+ metaphorical structures identified in extraction
- **Tertiary:** Support wealth-domain generalization to 1000-proverb corpus

---

## 2. Design Principles

### 2.1 Ontology Philosophy

**Cultural Primacy**
- Cultural authenticity > translation accuracy
- Expert knowledge authority > MT outputs
- Metaphorical preservation > literal translation

**RAG Optimization**
- Graph structures optimized for subgraph retrieval
- Full-text search indexes on Kikuyu terms
- Semantic relationship density for context richness

**Scalability**
- Core ontology: 100 proverbs (Ireri wealth-domain)
- Extension capability: 1000+ proverbs (mixed domains)
- Modular class design for domain expansion

### 2.2 Semantic Web Standards

**W3C Compliance**
- RDF-compatible property definitions
- OWL-style class hierarchies
- SKOS concept taxonomies

**FAIR Principles**
- **Findable:** Unique URIs for all entities
- **Accessible:** Neo4j Cypher query interface
- **Interoperable:** JSON-LD export capability
- **Reusable:** CC-BY-4.0 license, provenance tracking

---

## 3. Gap Analysis Integration

### 3.1 Baseline Failure Analysis Summary

From `docs/baseline_gap_analysis.md`:

| Metric | Baseline Score | Target OG-RAG | Improvement Factor |
|--------|---------------|---------------|-------------------|
| Semantic Similarity | 0.115 (11.5%) | 0.50+ (50%+) | 4.3x |
| Cultural Fidelity | 0.067 (6.7%) | 0.50+ (50%+) | 7.5x |
| Metaphor Preservation | 0.045 (4.5%) | 0.50+ (50%+) | 11x |
| Complete Failures | 97/100 (97%) | <30/100 (<30%) | 3.2x reduction |

### 3.2 Critical Concepts Requiring Deep Representation

**Tier 1 - CRITICAL (5+ failures)**
1. **Wealth** (`uhutii`, `ũtonga`) - 20 failures
   - Ontology Requirement: Rich semantic definition, multiple Kikuyu expressions, cultural significance, usage contexts, biblical parallels
   
2. **Poverty** (`gukiaga`, `ũthĩĩni`) - 10 failures
   - Ontology Requirement: Same depth as wealth, interconnection with wealth concepts

**Tier 2 - HIGH (3-4 failures)**
3. **Ownership** - 4 failures
4. **Wealth Acquisition** - 4 failures
5. **Debt** - 4 failures

**Tier 3 - MEDIUM (2 failures)**
6. Greed, Investment, Impermanence, Wisdom, Hospitality, Self-reliance, Collaboration, Resource Management, Stewardship, Pride, Patience

### 3.3 Failed Metaphor Patterns

100+ unique metaphors identified, including:
- Animal metaphors: storks→locusts (pursuit), goats→brideswealth (value)
- Agricultural metaphors: granary→wealth, land→toil
- Social metaphors: people→wealth, community→prosperity
- Temporal metaphors: youth→opportunity, seasons→timing

**Ontology Design Implication:** Explicit Metaphor class with vehicle-tenor-mapping-resonance structure.

---

## 4. Core Ontology Classes

### 4.1 Class Hierarchy Overview

```
Thing
├── Proverb (root cultural artifact)
│   ├── WealthProverb (domain subclass)
│   ├── FamilyProverb (future extension)
│   └── WisdomProverb (future extension)
├── LinguisticEntity
│   ├── KikuyuEntity (concrete/abstract terms)
│   │   ├── Person (mũndũ, gitonga, mũthĩĩni)
│   │   ├── Animal (njũũ, ngigi, mbũri)
│   │   ├── Object (mbia, ikumbi, mugunda)
│   │   ├── Place (bururi, gĩthaka)
│   │   └── AbstractConcept (uhutii, gukiaga, ũũgĩ)
│   └── KikuyuAction (verbs with cultural context)
│       ├── PhysicalAction (gikaarima, kiriaga)
│       ├── MentalAction (kũmenya, meciiria)
│       ├── SocialAction (gũtaarana, ũnyiitania)
│       └── EconomicAction (kũgaacĩra, gũtonga)
├── CulturalConcept (abstract values/morals)
│   ├── PositiveConcept (prudence, generosity, justice)
│   ├── NegativeConcept (greed, squandering, pride)
│   └── ContextualConcept (impermanence, destiny, balance)
├── Metaphor (vehicle-tenor mappings)
│   ├── AnimalMetaphor
│   ├── AgriculturalMetaphor
│   ├── SocialMetaphor
│   └── TemporalMetaphor
├── Moral (explicit teachings)
│   ├── EthicalMoral (right/wrong behavior)
│   ├── PracticalMoral (life advice)
│   └── SpiritualMoral (biblical parallels)
├── CulturalTheme (thematic categories)
│   ├── WealthAcquisition (primary domain)
│   ├── WealthManagement
│   ├── PovertyWarnings
│   └── Generosity
├── UsageContext (application scenarios)
│   ├── TraditionalContext (historical usage)
│   ├── ModernContext (contemporary application)
│   └── BusinessContext (entrepreneurship)
└── BiblicalParallel (scriptural connections)
```

### 4.2 Core Class Definitions

#### 4.2.1 Proverb (Root Class)

**Definition:** A traditional Kikuyu saying with cultural wisdom, typically metaphorical.

**Properties:**
- `proverb_id`: Unique identifier (e.g., MW_001)
- `kikuyu_text`: Original Kikuyu proverb text
- `phonetic_transcription`: IPA phonetic representation
- `literal_translation`: Word-for-word English translation
- `interpretive_translation`: Contextual English translation
- `expert_translation`: Gold standard expert translation
- `expert_cultural_meaning`: Deep cultural significance
- `expert_teaching`: Explicit moral/lesson
- `expert_business_relevance`: Entrepreneurship application
- `thematic_category`: Primary theme classification
- `biblical_context`: Related biblical verses
- `cultural_authenticity_score`: Expert validation score (0-1)
- `translation_difficulty`: Complexity level (low/medium/high/very_high)
- `usage_frequency`: Traditional usage frequency (common/occasional/rare)
- `regional_variants`: List of regional text variations
- `source`: Source authority (Ireri, Barra, Kabira, etc.)
- `source_reference`: Page/section reference
- `extraction_date`: Data collection timestamp
- `validation_status`: Quality control status

**Subclasses:**
- `WealthProverb`: Proverbs focused on wealth/prosperity/finance (current scope)
- `FamilyProverb`: Proverbs about kinship/relationships (future extension)
- `WisdomProverb`: Proverbs about knowledge/decision-making (future extension)

**Rationale:** Central node connecting all ontology elements. Rich metadata supports both cultural preservation and RAG retrieval.

---

#### 4.2.2 KikuyuEntity (Linguistic Entities)

**Definition:** Concrete or abstract entities referenced in proverbs with cultural significance.

**Properties:**
- `kikuyu_term`: Kikuyu word/phrase
- `english_translation`: English meaning
- `category`: Entity type (person/animal/object/place/abstract_concept)
- `cultural_significance`: Why this entity matters in Kikuyu culture
- `usage_examples`: Example sentences using this term
- `morphological_analysis`: Grammatical structure (prefix, root, suffix)
- `semantic_field`: Related concept cluster
- `frequency_in_corpus`: How often term appears

**Subclasses:**

**Person** (e.g., gitonga, mũndũ, mũthĩĩni)
- `social_status`: Elite/common/marginalized
- `gender_marking`: Masculine/feminine/neutral
- `age_category`: Elder/adult/youth

**Animal** (e.g., njũũ [storks], ngigi [locusts], mbũri [goats])
- `habitat`: Natural environment
- `cultural_symbolism`: What animal represents
- `agricultural_relevance`: Role in Kikuyu farming

**Object** (e.g., mbia [money], ikumbi [granary], mugunda [farm])
- `material_type`: Physical/immaterial
- `ownership_implications`: Property concepts
- `wealth_association`: Connection to prosperity

**Place** (e.g., bururi [country], gĩthaka [land])
- `geographic_scale`: Village/region/nation
- `political_significance`: Governance implications
- `economic_importance`: Resource value

**AbstractConcept** ⭐ **CRITICAL - Priority 1**
- **Wealth concepts** (`uhutii`, `ũtonga`, `indo`)
  - `kikuyu_expressions`: [List of wealth-related phrases]
  - `cultural_explanation`: Holistic wealth definition (not just money)
  - `moral_dimension`: Positive (with responsibility)
  - `biblical_parallel`: Proverbs 10:22 ("blessing of Lord brings wealth")
  - `opposite_concept`: → Poverty
  
- **Poverty concepts** (`gukiaga`, `ũthĩĩni`)
  - `kikuyu_expressions`: [List of poverty-related phrases]
  - `cultural_explanation`: Lacking material and social capital
  - `moral_dimension`: Contextual (not moral failing, but warning)
  - `opposite_concept`: → Wealth

**Rationale:** Entities are foundational vocabulary. Deep representation of wealth/poverty addresses 30 combined baseline failures (Tier 1 priority).

---

#### 4.2.3 KikuyuAction (Verbs with Cultural Context)

**Definition:** Actions/verbs appearing in proverbs, with cultural implications.

**Properties:**
- `kikuyu_verb`: Kikuyu verb form
- `english_translation`: English action
- `action_type`: Physical/mental/social/economic
- `cultural_context`: What this action means culturally
- `subject_constraints`: Who typically performs action
- `object_constraints`: What action typically affects
- `temporal_aspects`: Duration/frequency implications

**Subclasses:**

**PhysicalAction** (e.g., gikaarima [cultivates], kiriaga [eats])
- Agricultural/bodily actions

**MentalAction** (e.g., kũmenya [to know], meciiria [thoughts])
- Cognitive processes

**SocialAction** (e.g., gũtaarana [to collaborate], ũnyiitania [mutual support])
- Community interactions

**EconomicAction** ⭐ **HIGH Priority**
(e.g., kũgaacĩra [to prosper], aikaragia [guards/pursues])
- Wealth-related activities
- Critical for understanding wealth acquisition proverbs

**Rationale:** Actions provide dynamic context to static entities. Economic actions critical for wealth-domain proverbs.

---

#### 4.2.4 CulturalConcept (Abstract Values/Morals)

**Definition:** Abstract cultural values, morals, or societal principles expressed in proverbs.

**Properties:**
- `concept_name`: English name (e.g., "greed", "prudence")
- `kikuyu_expressions`: List of Kikuyu terms expressing concept
- `cultural_explanation`: How Kikuyu culture views this concept
- `moral_dimension`: Positive/negative/neutral/contextual
- `teaching_applications`: How elders use this concept
- `modern_relevance`: Contemporary business application
- `related_concepts`: Semantic neighbors

**Subclasses:**

**PositiveConcept** (e.g., prudence, generosity, justice, patience)
- Virtues encouraged in Kikuyu society

**NegativeConcept** ⭐ **HIGH Priority**
(e.g., greed, squandering, meanness, pretence)
- Vices warned against
- Critical for understanding wealth warnings (6 baseline failures)

**ContextualConcept** (e.g., impermanence, destiny, balance)
- Situational values
- Example: wealth impermanence (2 baseline failures)

**Rationale:** Cultural concepts are the "soul" of proverbs. Gap analysis shows 6.7% cultural fidelity in baseline → must be explicit in ontology.

---

#### 4.2.5 Metaphor ⭐ **CRITICAL - Priority 1**

**Definition:** Metaphorical structure mapping concrete vehicle to abstract tenor.

**Properties:**
- `vehicle`: Concrete thing/scenario (e.g., "storks pursuing locusts")
- `tenor`: Abstract concept being illustrated (e.g., "relentless greed")
- `mapping_explanation`: How vehicle maps to tenor
- `cultural_resonance`: Why this metaphor works in Kikuyu culture
- `linguistic_markers`: Kikuyu words signaling metaphor (e.g., "ta" [like])
- `interpretation_difficulty`: Easy/moderate/complex
- `preservation_priority`: Critical/high/medium (from gap analysis)

**Subclasses:**

**AnimalMetaphor** (e.g., storks→greed, goats→value)
- Agricultural society familiarity with animal behavior

**AgriculturalMetaphor** (e.g., granary→accumulation, land→toil)
- Farming as central cultural experience

**SocialMetaphor** (e.g., people→wealth, community→prosperity)
- Ubuntu philosophy

**TemporalMetaphor** (e.g., youth→opportunity, seasons→timing)
- Patience and long-term thinking

**Rationale:** Baseline metaphor preservation: 4.5% (essentially zero). 100+ metaphors identified in extraction. Explicit representation CRITICAL for OG-RAG success.

---

#### 4.2.6 Moral (Explicit Teachings)

**Definition:** Explicit lesson or teaching conveyed by proverb.

**Properties:**
- `teaching_text`: Explicit moral statement
- `lesson_type`: Ethical/practical/spiritual
- `application_context`: When/how to apply lesson
- `target_audience`: Who should learn this (youth/entrepreneurs/everyone)
- `severity_level`: Advisory/warning/prohibition
- `positive_framing`: Encouragement vs warning
- `modern_translation`: Contemporary business application

**Subclasses:**

**EthicalMoral** (e.g., "Greed destroys relationships")
- Right vs wrong behavior

**PracticalMoral** (e.g., "Save during prosperity for times of need")
- Pragmatic life advice
- High relevance for wealth-domain proverbs

**SpiritualMoral** (e.g., biblical parallels)
- Faith-based teachings

**Rationale:** Explicit moral extraction enables OG-RAG to surface "teaching" in translation, addressing cultural meaning loss.

---

#### 4.2.7 CulturalTheme (Thematic Categories)

**Definition:** High-level thematic categorization of proverbs for retrieval.

**Properties:**
- `theme_name`: Theme identifier
- `description`: Theme explanation
- `subcategories`: Finer-grained theme breakdown
- `proverb_count`: Number of proverbs in theme
- `cultural_importance`: Centrality to Kikuyu worldview
- `business_relevance`: Entrepreneurship application score

**Subclasses:**

**WealthAcquisition** ⭐ **PRIMARY DOMAIN**
- How to gain wealth
- Subcategories: trade, farming, investment, opportunity

**WealthManagement**
- How to preserve/grow wealth
- Subcategories: prudence, stewardship, resource_allocation

**PovertyWarnings**
- How to avoid poverty
- Subcategories: debt_warning, squandering, poor_planning

**Generosity**
- Sharing wealth with community
- Subcategories: hospitality, Ubuntu, social_responsibility

**Rationale:** Themes enable domain filtering and hierarchical retrieval for OG-RAG. Aligns with Ireri's thematic_category field.

---

#### 4.2.8 UsageContext (Application Scenarios)

**Definition:** Contexts in which proverb is traditionally or contemporarily used.

**Properties:**
- `context_type`: Traditional/modern/business
- `situation_description`: When proverb is appropriate
- `speaker_role`: Who typically uses proverb (elder/peer/mentor)
- `audience`: Who typically hears proverb
- `formality_level`: Formal_ceremony/informal_advice/everyday_conversation
- `effectiveness_rating`: How impactful in this context

**Subclasses:**

**TraditionalContext**
- Historical usage in village settings

**ModernContext**
- Contemporary urban/rural application

**BusinessContext** ⭐ **HIGH Priority**
- Entrepreneurship/workplace application
- Critical for thesis business relevance argument

**Rationale:** Usage contexts guide OG-RAG in generating appropriate translations for target audience.

---

#### 4.2.9 BiblicalParallel (Scriptural Connections)

**Definition:** Biblical verses with similar teachings to proverb.

**Properties:**
- `verse_reference`: Book Chapter:Verse (e.g., "Proverbs 10:22")
- `verse_text`: Actual biblical text
- `thematic_connection`: How biblical verse relates to proverb
- `cultural_integration`: How Christianity merged with Kikuyu wisdom
- `teaching_alignment`: Degree of theological similarity

**Rationale:** Ireri's gold standard includes biblical parallels. Enhances cultural depth and appeals to Christian Kikuyu audience.

---

## 5. Object Properties (Relationships)

### 5.1 Core Relationships

#### 5.1.1 Proverb-Centric Relationships

**expresses** (Proverb → CulturalConcept)
- **Domain:** Proverb
- **Range:** CulturalConcept
- **Cardinality:** 1:many (proverb expresses 1-5 concepts typically)
- **Inverse:** isExpressedBy
- **Description:** Links proverb to abstract concepts it teaches
- **Example:** MW_001 expresses "greed", "insatiability"

**hasMoral** (Proverb → Moral)
- **Domain:** Proverb
- **Range:** Moral
- **Cardinality:** 1:1 or 1:few (most proverbs have 1 primary moral)
- **Inverse:** isMoralOf
- **Description:** Links proverb to explicit teaching
- **Example:** MW_013 hasMoral "wealth is impermanent, practice prudence"

**usesMetaphor** (Proverb → Metaphor) ⭐ **CRITICAL**
- **Domain:** Proverb
- **Range:** Metaphor
- **Cardinality:** 1:0..1 (80% of proverbs have metaphor)
- **Inverse:** isMetaphorIn
- **Description:** Links proverb to metaphorical structure
- **Example:** MW_001 usesMetaphor "storks pursuing locusts"
- **RAG Priority:** HIGH - retrieve metaphor context for cultural translation

**involvesEntity** (Proverb → KikuyuEntity)
- **Domain:** Proverb
- **Range:** KikuyuEntity
- **Cardinality:** 1:many (avg 1.86 entities per proverb)
- **Inverse:** appearsIn
- **Description:** Links proverb to concrete/abstract entities
- **Example:** MW_001 involvesEntity "mbia" (money), "njũũ" (storks), "ngigi" (locusts)

**performsAction** (Proverb → KikuyuAction)
- **Domain:** Proverb
- **Range:** KikuyuAction
- **Cardinality:** 1:0..many (88% have actions)
- **Inverse:** isActionIn
- **Description:** Links proverb to verbs/actions
- **Example:** MW_001 performsAction "aikaragia" (guards/pursues)

**hasTheme** (Proverb → CulturalTheme)
- **Domain:** Proverb
- **Range:** CulturalTheme
- **Cardinality:** 1:1..3 (primary + secondary themes)
- **Inverse:** includesProverb
- **Description:** Thematic categorization
- **Example:** MW_001 hasTheme "wealth_acquisition", "greed_warning"

**isUsedIn** (Proverb → UsageContext)
- **Domain:** Proverb
- **Range:** UsageContext
- **Cardinality:** 1:many (multiple usage scenarios)
- **Inverse:** contextualizesProverb
- **Description:** Application contexts
- **Example:** MW_001 isUsedIn "business_mentorship", "wealth_counseling"

**hasBiblicalParallel** (Proverb → BiblicalParallel)
- **Domain:** Proverb
- **Range:** BiblicalParallel
- **Cardinality:** 1:0..many (not all proverbs have parallels)
- **Inverse:** parallelOf
- **Description:** Scriptural connections
- **Example:** MW_002 hasBiblicalParallel "Proverbs 27:17"

**relatesTo** (Proverb ↔ Proverb) [symmetric]
- **Domain:** Proverb
- **Range:** Proverb
- **Cardinality:** many:many
- **Type:** Symmetric
- **Description:** Semantic similarity between proverbs
- **Subtypes:**
  - `contradicts`: Opposite teachings
  - `reinforces`: Similar teachings
  - `elaborates`: Deeper exploration of same theme
- **Example:** MW_012 relatesTo MW_013 (both about wealth impermanence)

#### 5.1.2 Metaphor Relationships ⭐ **CRITICAL**

**mapsVehicle** (Metaphor → KikuyuEntity)
- **Domain:** Metaphor
- **Range:** KikuyuEntity
- **Cardinality:** 1:1..few (concrete entities in metaphor)
- **Description:** Links metaphor to concrete vehicle entities
- **Example:** "storks pursuing locusts" metaphor mapsVehicle "njũũ", "ngigi"

**mapsToTenor** (Metaphor → CulturalConcept)
- **Domain:** Metaphor
- **Range:** CulturalConcept
- **Cardinality:** 1:1 (one abstract concept per metaphor)
- **Description:** Links metaphor to abstract tenor concept
- **Example:** "storks pursuing locusts" mapsToTenor "greed"

**requiresContext** (Metaphor → CulturalContext)
- **Domain:** Metaphor
- **Range:** CulturalContext (new class to add)
- **Cardinality:** 1:1
- **Description:** Cultural knowledge needed to understand metaphor
- **Example:** "storks→locusts" requiresContext "Kikuyu agricultural society"

#### 5.1.3 Entity Relationships

**synonymOf** (KikuyuEntity ↔ KikuyuEntity) [symmetric]
- **Description:** Synonymous Kikuyu terms
- **Example:** "mbia" synonymOf "mbeeca" (both mean money)

**antonymOf** (KikuyuEntity ↔ KikuyuEntity) [symmetric]
- **Description:** Opposite concepts
- **Example:** "uhutii" (wealth) antonymOf "gukiaga" (poverty)

**partOf** (KikuyuEntity → KikuyuEntity) [transitive]
- **Description:** Meronymy relationships
- **Example:** "ikumbi" (granary) partOf "mugunda" (farm)

**subcategoryOf** (CulturalConcept → CulturalConcept) [transitive]
- **Description:** Concept hierarchy
- **Example:** "greed" subcategoryOf "negative_wealth_attitudes"

### 5.2 Relationship Priority for OG-RAG

**Tier 1 - Retrieve Always:**
1. `usesMetaphor` (4.5% baseline → must fix)
2. `expresses` (cultural concepts lost)
3. `involvesEntity` (Kikuyu terms)

**Tier 2 - Retrieve for Deep Context:**
4. `hasMoral` (teaching extraction)
5. `performsAction` (action context)
6. `hasTheme` (domain filtering)

**Tier 3 - Retrieve Conditionally:**
7. `relatesTo` (similar proverbs for reinforcement)
8. `hasBiblicalParallel` (if Christian audience)
9. `isUsedIn` (if usage scenario specified)

---

## 6. Data Properties

### 6.1 String Properties
- `kikuyu_text`: Original Kikuyu
- `english_translation`: English meaning
- `phonetic_transcription`: IPA
- `cultural_significance`: Why important
- `teaching_text`: Moral lesson
- `verse_reference`: Biblical citation

### 6.2 Numeric Properties
- `cultural_authenticity_score`: 0.0-1.0
- `business_relevance_score`: 0.0-1.0
- `frequency_in_corpus`: Integer count
- `extraction_confidence`: 0.0-1.0 (from GPT-4o)

### 6.3 Enum Properties
- `category`: {person, animal, object, place, abstract_concept}
- `action_type`: {physical, mental, social, economic}
- `moral_dimension`: {positive, negative, neutral, contextual}
- `translation_difficulty`: {low, medium, high, very_high}
- `validation_status`: {validated, pending, disputed}

### 6.4 Array Properties
- `kikuyu_expressions`: List[String]
- `themes`: List[String]
- `related_concepts`: List[String]
- `regional_variants`: List[String]

### 6.5 Temporal Properties
- `extraction_date`: DateTime
- `created_at`: DateTime
- `updated_at`: DateTime

---

## 7. Constraints and Cardinality

### 7.1 Required Properties (NOT NULL)

**Proverb:**
- `proverb_id` (unique, indexed)
- `kikuyu_text` (unique, full-text indexed)
- `expert_translation`
- `thematic_category`

**KikuyuEntity:**
- `kikuyu_term` (unique within category)
- `english_translation`
- `category`

**Metaphor:**
- `vehicle` (non-empty)
- `tenor` (non-empty)
- `mapping_explanation` (non-empty)

**CulturalConcept:**
- `concept_name` (unique)
- `moral_dimension`

### 7.2 Cardinality Constraints

**Proverb Relationships:**
- `expresses`: 1..* (every proverb must express at least one concept)
- `hasMoral`: 1..3 (at least one moral)
- `usesMetaphor`: 0..1 (optional metaphor)
- `involvesEntity`: 1..* (at least one entity)
- `hasTheme`: 1..3 (primary theme required)

**Metaphor Relationships:**
- `mapsVehicle`: 1..5 (at least one vehicle entity)
- `mapsToTenor`: 1 (exactly one tenor concept)

### 7.3 Uniqueness Constraints

- `proverb_id` unique across Proverb
- `kikuyu_text` unique across Proverb (no duplicates)
- (`kikuyu_term`, `category`) unique across KikuyuEntity
- `concept_name` unique across CulturalConcept

### 7.4 Domain/Range Constraints

All object properties have explicit domain/range (see Section 5).

---

## 8. Priority-Based Implementation

### 8.1 Phase 1: Critical Foundation (Week 1)

**Goal:** Address top baseline failures (wealth/poverty/metaphors)

**Classes to Implement:**
1. Proverb (core)
2. KikuyuEntity (with AbstractConcept subclass for wealth/poverty)
3. Metaphor (explicit vehicle-tenor structure)
4. CulturalConcept (positive/negative/contextual)

**Relationships to Implement:**
1. `involvesEntity` (link proverbs to wealth/poverty terms)
2. `usesMetaphor` (4.5% baseline → priority)
3. `expresses` (6.7% cultural fidelity → priority)
4. `mapsVehicle`, `mapsToTenor` (metaphor structure)

**Data Population:**
- Load 100 proverbs from gold_standard_ireri_deduplicated.csv
- Extract wealth/poverty entities from extracted_concepts_100proverbs.json
- Extract 80 metaphors from extraction JSON
- Map 150 cultural concepts

**Success Criteria:**
- All 100 proverbs loaded
- Wealth (20 instances) and poverty (10 instances) fully represented
- 80 metaphors with explicit structure
- Full-text search on kikuyu_text operational

### 8.2 Phase 2: Depth Enhancement (Week 2)

**Goal:** Add remaining classes for complete cultural representation

**Classes to Implement:**
5. KikuyuAction (all subclasses)
6. Moral (ethical/practical/spiritual)
7. CulturalTheme (wealth_acquisition, wealth_management, poverty_warnings)
8. BiblicalParallel

**Relationships to Implement:**
5. `performsAction`
6. `hasMoral`
7. `hasTheme`
8. `hasBiblicalParallel`
9. `relatesTo` (inter-proverb semantic similarity)

**Data Population:**
- Extract 88 actions from extraction JSON
- Parse expert_teaching field for morals
- Use thematic_category for themes
- Parse biblical_context for parallels

**Success Criteria:**
- All 186 entities loaded
- All 88 actions loaded
- All 100 morals extracted
- Thematic hierarchy operational

### 8.3 Phase 3: RAG Optimization (Week 3)

**Goal:** Optimize for OG-RAG retrieval

**Implementation:**
1. Create composite indexes for common queries
2. Implement semantic similarity scoring (embeddings)
3. Add subgraph retrieval functions
4. Create view materialization for frequent patterns

**Indexes to Create:**
- Full-text: `kikuyu_text`, `english_translation`, `cultural_significance`
- Composite: (`hasTheme`, `involvesEntity`) for domain filtering
- Vector: Proverb embeddings for semantic search

**Success Criteria:**
- Subgraph retrieval <100ms for any proverb
- Full-text search recall >95%
- Semantic similarity top-10 precision >80%

### 8.4 Phase 4: Validation & Extension (Week 4)

**Goal:** Validate ontology and prepare for scale

**Tasks:**
1. Run OOPS! ontology validation
2. Expert review of cultural concepts (if possible)
3. FAIR compliance check
4. Documentation completion

**Extension Planning:**
- UsageContext class (deferred to post-evaluation)
- Multi-domain expansion strategy (1000-proverb corpus)
- Ontology versioning strategy

**Success Criteria:**
- Zero critical OOPS! errors
- FAIR principles checklist 100%
- Documentation complete

---

## 9. Integration with Existing Infrastructure

### 9.1 Existing ontology_builder.py Integration

**Current Structure (from scripts/ontology_builder.py):**
- `KikuyuProverbsOntologyBuilder` class (line 26)
- Cultural concepts dictionary (lines 55-91)
- Neo4j connection management
- Proverb node creation (line 200)
- Concept extraction (line 290)

**Integration Strategy:**

**Preserve:**
- Neo4j driver infrastructure
- Cultural concepts dictionary (merge with extracted concepts)
- Statistics tracking

**Extend:**
- Add new class creation methods for Metaphor, Moral, BiblicalParallel
- Enhance concept extraction to use extracted_concepts_100proverbs.json
- Add relationship creation methods for all object properties

**Modify:**
- `create_proverb_node()` to include new properties
- Concept extraction to prioritize wealth/poverty (Tier 1)

### 9.2 Existing kikuyu_proverb_ontology.py Integration

**Current Structure (from src/ontology/kikuyu_proverb_ontology.py):**
- `IntegratedKikuyuOntology` class
- `ProverbData` dataclass (line 83)
- `ProverbLoaderConfig` (line 121)
- Dynamic proverb loading (line 634)

**Integration Strategy:**

**Preserve:**
- Configuration management (.env integration)
- ProverbData dataclass structure
- Dynamic loading capability

**Extend:**
- Add dataclasses for Metaphor, Moral, Entity, Action
- Extend ProverbData with new fields (metaphor_id, moral_id, entity_ids)
- Add loaders for extracted_concepts_100proverbs.json

**Modify:**
- Update `create_domain_proverbs()` to create relationships
- Add methods for metaphor/entity/concept population

### 9.3 Data Source Integration

**Primary Data Sources:**
1. `data/evaluation/gold_standard_ireri_deduplicated.csv` (100 proverbs + expert annotations)
2. `data/ontology/extracted_concepts_100proverbs.json` (186 entities, 88 actions, 150 concepts, 80 metaphors)
3. `docs/baseline_gap_analysis.md` (priority rankings)

**Loading Strategy:**
```python
# Pseudo-code
def load_integrated_ontology():
    # 1. Load proverbs from gold standard
    proverbs = load_gold_standard_csv()
    
    # 2. Load extracted concepts
    concepts = load_extracted_concepts_json()
    
    # 3. Create Proverb nodes
    for proverb in proverbs:
        create_proverb_node(proverb)
    
    # 4. Create Entity nodes (prioritize wealth/poverty)
    for entity in concepts['entities']:
        priority = get_priority_from_gap_analysis(entity)
        create_entity_node(entity, priority)
    
    # 5. Create Metaphor nodes
    for metaphor in concepts['metaphors']:
        create_metaphor_node(metaphor)
    
    # 6. Create relationships
    for proverb in proverbs:
        link_proverb_to_entities(proverb, concepts)
        link_proverb_to_metaphor(proverb, concepts)
        link_proverb_to_concepts(proverb, concepts)
```

---

## 10. OG-RAG Optimization Strategy

### 10.1 Retrieval Patterns

**Pattern 1: Entity-Centric Retrieval**
```cypher
// Given input Kikuyu proverb, retrieve relevant entities
MATCH (p:Proverb {kikuyu_text: $input_proverb})
MATCH (p)-[:involvesEntity]->(e:KikuyuEntity)
MATCH (e)-[:appearsIn]->(related:Proverb)
RETURN p, e, related
LIMIT 5
```

**Pattern 2: Metaphor-Centric Retrieval** ⭐ **CRITICAL**
```cypher
// Retrieve metaphorical structure for context
MATCH (p:Proverb {kikuyu_text: $input_proverb})
MATCH (p)-[:usesMetaphor]->(m:Metaphor)
MATCH (m)-[:mapsVehicle]->(vehicle:KikuyuEntity)
MATCH (m)-[:mapsToTenor]->(tenor:CulturalConcept)
RETURN m.vehicle, m.tenor, m.mapping_explanation, m.cultural_resonance
```

**Pattern 3: Theme-Based Retrieval**
```cypher
// Retrieve similar proverbs in same theme
MATCH (p:Proverb {kikuyu_text: $input_proverb})
MATCH (p)-[:hasTheme]->(t:CulturalTheme)
MATCH (t)<-[:hasTheme]-(similar:Proverb)
WHERE similar.proverb_id <> p.proverb_id
RETURN similar.kikuyu_text, similar.expert_translation
LIMIT 3
```

**Pattern 4: Concept-Rich Context**
```cypher
// Retrieve full cultural context
MATCH (p:Proverb {kikuyu_text: $input_proverb})
MATCH (p)-[:expresses]->(c:CulturalConcept)
MATCH (p)-[:hasMoral]->(mo:Moral)
OPTIONAL MATCH (p)-[:hasBiblicalParallel]->(b:BiblicalParallel)
RETURN c.concept_name, c.cultural_explanation, 
       mo.teaching_text, b.verse_text
```

### 10.2 Subgraph Retrieval for RAG

**Optimized Subgraph Query:**
```cypher
// Single query to get comprehensive proverb context
MATCH (p:Proverb {kikuyu_text: $input_proverb})
OPTIONAL MATCH (p)-[:usesMetaphor]->(m:Metaphor)
OPTIONAL MATCH (m)-[:mapsVehicle]->(v:KikuyuEntity)
OPTIONAL MATCH (m)-[:mapsToTenor]->(t:CulturalConcept)
OPTIONAL MATCH (p)-[:involvesEntity]->(e:KikuyuEntity)
OPTIONAL MATCH (p)-[:expresses]->(c:CulturalConcept)
OPTIONAL MATCH (p)-[:hasMoral]->(mo:Moral)
OPTIONAL MATCH (p)-[:hasBiblicalParallel]->(b:BiblicalParallel)
RETURN p, m, v, t, collect(DISTINCT e) as entities, 
       collect(DISTINCT c) as concepts, 
       collect(DISTINCT mo) as morals,
       collect(DISTINCT b) as biblical_parallels
```

**Response Time Target:** <100ms

### 10.3 RAG Prompt Construction

**Context Assembly:**
```python
def construct_rag_context(proverb_subgraph):
    context = f"""
    Kikuyu Proverb: {proverb_subgraph['p'].kikuyu_text}
    Expert Translation: {proverb_subgraph['p'].expert_translation}
    Cultural Meaning: {proverb_subgraph['p'].expert_cultural_meaning}
    
    Metaphorical Structure:
    - Vehicle: {proverb_subgraph['m'].vehicle}
    - Tenor: {proverb_subgraph['m'].tenor}
    - Mapping: {proverb_subgraph['m'].mapping_explanation}
    - Cultural Resonance: {proverb_subgraph['m'].cultural_resonance}
    
    Key Kikuyu Terms:
    {format_entities(proverb_subgraph['entities'])}
    
    Cultural Concepts:
    {format_concepts(proverb_subgraph['concepts'])}
    
    Moral Teaching:
    {proverb_subgraph['morals'][0].teaching_text}
    
    Biblical Parallel (if applicable):
    {proverb_subgraph['biblical_parallels'][0].verse_text if proverb_subgraph['biblical_parallels'] else "N/A"}
    """
    return context
```

**Gemini 2.0 Prompt:**
```
You are translating a Kikuyu proverb to English. Use the following cultural context:

{rag_context}

Translate the proverb faithfully, preserving:
1. Metaphorical structure (map {vehicle} → {tenor})
2. Cultural meaning ({cultural_concepts})
3. Moral teaching ({moral_text})

English Translation:
```

### 10.4 Evaluation Metrics (vs Baseline)

| Metric | Baseline | OG-RAG Target | Improvement |
|--------|----------|---------------|-------------|
| Semantic Similarity | 0.115 | 0.50+ | 4.3x |
| Cultural Fidelity | 0.067 | 0.50+ | 7.5x |
| Metaphor Preservation | 0.045 | 0.50+ | 11x |
| Complete Failures | 97/100 | <30/100 | 3.2x |

**Success Criteria:** ANY metric >0.40 is publishable improvement.

---

## 11. Implementation Roadmap

### Week 1: Core Foundation
**Days 1-2:** Schema design + Neo4j setup
- Create node labels, property definitions
- Implement uniqueness constraints
- Create indexes

**Days 3-4:** Data loading (Proverb, Entity, Metaphor, Concept)
- Adapt ontology_builder.py
- Load gold_standard CSV
- Load extracted_concepts JSON
- Create ~400 nodes (100 proverbs + 186 entities + 80 metaphors + 150 concepts)

**Days 5-7:** Relationship creation
- Implement priority relationships (involvesEntity, usesMetaphor, expresses)
- Validate cardinality constraints
- Test subgraph queries

**Deliverable:** Core ontology operational, basic RAG queries working

### Week 2: Depth Enhancement
**Days 8-10:** Secondary classes (Action, Moral, Theme, Biblical)
- Load 88 actions
- Parse morals from expert_teaching
- Create thematic hierarchy
- Extract biblical parallels

**Days 11-12:** Inter-proverb relationships
- Implement relatesTo (semantic similarity)
- Calculate relatedness scores
- Create synonym/antonym relationships

**Days 13-14:** Testing & validation
- Query performance benchmarking
- Data completeness check
- Relationship integrity validation

**Deliverable:** Complete ontology with all classes and relationships

### Week 3: RAG Optimization
**Days 15-17:** Indexing & performance
- Full-text search optimization
- Composite indexes for common patterns
- Query plan analysis and optimization

**Days 18-19:** RAG integration
- Implement subgraph retrieval functions
- Test with sample proverbs
- Refine context assembly

**Days 20-21:** Documentation
- Cypher query library
- API documentation
- Usage examples

**Deliverable:** OG-RAG-ready knowledge graph

### Week 4: Validation & Extension
**Days 22-23:** OOPS! validation
- Run ontology pitfall scanner
- Fix critical/major issues
- Document known limitations

**Days 24-25:** Expert review (if available)
- Present ontology to Kikuyu speaker
- Validate cultural concepts
- Incorporate feedback

**Days 26-28:** FAIR compliance & finalization
- Add provenance metadata
- Implement versioning
- Create export formats (JSON-LD, RDF)
- Final documentation

**Deliverable:** Validated, FAIR-compliant ontology ready for Phase 2c (Neo4j population)

---

## Appendix A: Cypher Schema Definition

```cypher
// Node Labels
CREATE CONSTRAINT proverb_id_unique IF NOT EXISTS
FOR (p:Proverb) REQUIRE p.proverb_id IS UNIQUE;

CREATE CONSTRAINT kikuyu_text_unique IF NOT EXISTS
FOR (p:Proverb) REQUIRE p.kikuyu_text IS UNIQUE;

CREATE CONSTRAINT entity_term_unique IF NOT EXISTS
FOR (e:KikuyuEntity) REQUIRE (e.kikuyu_term, e.category) IS NODE KEY;

CREATE CONSTRAINT concept_name_unique IF NOT EXISTS
FOR (c:CulturalConcept) REQUIRE c.concept_name IS UNIQUE;

// Full-text indexes
CREATE FULLTEXT INDEX proverb_fulltext IF NOT EXISTS
FOR (p:Proverb) ON EACH [p.kikuyu_text, p.expert_translation, p.expert_cultural_meaning];

CREATE FULLTEXT INDEX entity_fulltext IF NOT EXISTS
FOR (e:KikuyuEntity) ON EACH [e.kikuyu_term, e.english_translation, e.cultural_significance];

// Property indexes
CREATE INDEX proverb_theme IF NOT EXISTS
FOR (p:Proverb) ON (p.thematic_category);

CREATE INDEX entity_category IF NOT EXISTS
FOR (e:KikuyuEntity) ON (e.category);

CREATE INDEX concept_dimension IF NOT EXISTS
FOR (c:CulturalConcept) ON (c.moral_dimension);
```

---

## Appendix B: Priority Matrix (from Gap Analysis)

| Concept | Baseline Failures | Ontology Priority | Representation Depth |
|---------|------------------|-------------------|---------------------|
| Wealth | 20 | 🔴 CRITICAL | Rich: 5+ properties, biblical parallels, usage contexts |
| Poverty | 10 | 🔴 CRITICAL | Rich: 5+ properties, antonym to wealth |
| Ownership | 4 | 🟠 HIGH | Medium: 3-4 properties |
| Wealth Acquisition | 4 | 🟠 HIGH | Medium: 3-4 properties |
| Debt | 4 | 🟠 HIGH | Medium: 3-4 properties |
| Greed | 2 | 🟡 MEDIUM | Standard: 2-3 properties |
| Investment | 2 | 🟡 MEDIUM | Standard: 2-3 properties |
| Metaphors (all) | 100+ | 🔴 CRITICAL | Explicit vehicle-tenor-mapping structure |

---

## Appendix C: Design Decisions Log

**Decision 1: Explicit Metaphor Class**
- **Rationale:** Baseline metaphor preservation 4.5% (catastrophic). Implicit metaphor handling in proverb text insufficient.
- **Alternative Considered:** Store metaphor as Proverb property (rejected - not granular enough)
- **Impact:** +80 Metaphor nodes, +240 relationships (mapsVehicle, mapsToTenor, usesMetaphor)

**Decision 2: Wealth/Poverty as AbstractConcept Subclass**
- **Rationale:** Gap analysis shows 30 combined failures (highest priority). Need deepest representation.
- **Alternative Considered:** General CulturalConcept (rejected - insufficient depth)
- **Impact:** Specialized properties for wealth domain (kikuyu_expressions, biblical_parallel, opposite_concept)

**Decision 3: Prioritized Implementation (4 phases)**
- **Rationale:** PhD timeline constraints, iterative validation
- **Alternative Considered:** Complete ontology in one build (rejected - high risk)
- **Impact:** Core functionality Week 1, full depth Week 4

**Decision 4: Neo4j vs Triple Store**
- **Rationale:** Existing infrastructure uses Neo4j, better subgraph retrieval performance for RAG
- **Alternative Considered:** RDF triple store (rejected - overhead of SPARQL for RAG use case)
- **Impact:** Cypher queries, graph algorithms, native Neo4j integration

**Decision 5: 100-Proverb Core Ontology**
- **Rationale:** Methodological integrity (Phase 2.5 decision), proposal alignment (wealth domain)
- **Alternative Considered:** Immediate 1000-proverb expansion (rejected - scope creep, timeline risk)
- **Impact:** Deep quality on 100, extensibility to 1000 in Phase 5

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-14 | ndethi | Initial design based on Phase 2a extraction + Phase 2.5 gap analysis |

---

**Next Step:** Implement ontology population script (Phase 2c) based on this design specification.

**Approval Status:** ✅ Ready for implementation  
**Review Date:** 2025-10-14  
**Reviewer:** ndethi
