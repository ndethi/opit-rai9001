# Ontology Construction Guide - Gap Analysis & Recommendations
**Date:** October 17, 2025  
**Status:** Strategic Review  
**Purpose:** Compare current ontology design against comprehensive implementation guide

---

## Executive Summary

After deep analysis of the comprehensive **Kikuyu Proverb Ontology Creation Guide** and comparison with our current **Phase 2b design specification**, I've identified significant gaps and opportunities for enhancement. This document provides strategic recommendations before proceeding to Phase 2c implementation.

### Current State
✅ **Strengths:**
- Excellent design specification (Phase 2b completed)
- 100 proverbs with gold standard translations
- 186 entities, 88 actions, 150 concepts, 80 metaphors extracted (Phase 2a)
- Gap analysis completed identifying critical failure points
- Clear priority-based implementation roadmap
- Existing Neo4j infrastructure (`ontology_builder.py`)

⚠️ **Critical Gaps Identified:**
- **Missing community engagement framework** (ethical foundation)
- **No formal cultural weight calculation algorithms**
- **Lack of OWL 2 formal specification** (only Neo4j schema)
- **Insufficient expert validation protocols**
- **Missing semantic distance calculators**
- **No OOPS! validation pipeline**
- **Incomplete relationship property specifications**
- **Missing knowledge elicitation methodology**

---

## DETAILED GAP ANALYSIS

### 1. ETHICAL & COMMUNITY ENGAGEMENT (Critical Gap)

#### What the Guide Requires:
- Formal community engagement protocol
- Free, Prior, and Informed Consent (FPIC) process
- Benefit-sharing agreements
- Cultural authority identification
- Compensation framework ($50-100 per session)
- Intellectual property rights protection
- Sacred knowledge exclusion protocols

#### Our Current State:
- ❌ No documented community engagement process
- ❌ No consent framework
- ❌ No compensation agreements
- ✅ Implicit respect for cultural knowledge (Ireri expert translations)
- ⚠️ Risk: Using expert data without formal ethical framework

#### **RECOMMENDATION 1: Establish Ethical Foundation**

**Action Items:**
1. **Retroactive Documentation** (if Ireri data already collected):
   - Document existing relationship with Ireri expert
   - Create retrospective consent documentation
   - Establish benefit-sharing for thesis/publications
   - Clarify usage rights and attribution

2. **Future-Ready Framework** (for expansion beyond 100 proverbs):
   ```python
   # Create: src/ontology/community_engagement.py
   class CommunityEngagementProtocol:
       """Ethical framework for cultural knowledge collaboration"""
       - FPIC consent management
       - Contribution tracking with attribution
       - Compensation calculation
       - Usage restriction enforcement
       - Community review cycles
   ```

3. **Immediate Actions:**
   - Create `docs/ethics/community_engagement_protocol.md`
   - Draft consent form templates (Kikuyu + English)
   - Document Ireri collaboration details
   - Establish thesis acknowledgment section

**Priority:** HIGH (ethical requirement)  
**Timeline:** Complete before any additional data collection  
**Effort:** 2-3 days documentation + template creation

---

### 2. CULTURAL WEIGHT ALGORITHMS (Major Technical Gap)

#### What the Guide Requires:
Sophisticated multi-factor cultural weight calculation:

```python
class CulturalWeightCalculator:
    WEIGHTS = {
        'expert_consensus': 0.30,
        'usage_frequency': 0.15,
        'cultural_depth': 0.25,
        'translation_difficulty': 0.15,
        'historical_continuity': 0.10,
        'centrality': 0.05
    }
    
    def calculate_concept_weight(self, metrics: ConceptMetrics) -> float:
        # Multi-dimensional calculation
        # Returns 0.0-1.0 cultural significance score
```

#### Our Current State:
- ❌ No formal cultural weight calculation
- ✅ Implicit prioritization in gap analysis (Tier 1/2/3)
- ⚠️ Manual "cultural_weight" properties in design spec without algorithm

#### **RECOMMENDATION 2: Implement Cultural Weight System**

**Action Items:**
1. **Create Weight Calculator Module:**
   ```bash
   # Create: src/ontology/cultural_weights.py
   - CulturalWeightCalculator class
   - ConceptMetrics dataclass
   - SemanticDistanceCalculator class
   - Batch calculation for all concepts
   ```

2. **Data Requirements:**
   For each concept, collect/estimate:
   - `expert_agreement_score` (0-1): Ireri + 2nd validator?
   - `usage_count`: Frequency in 100-proverb corpus
   - `semantic_dimensions_count`: Number of meanings
   - `translation_complexity_score` (0-1): Gap analysis scores
   - `historical_persistence_score` (0-1): Traditional vs modern
   - `centrality_in_worldview` (0-1): Cultural importance

3. **Integration with Gap Analysis:**
   ```python
   # Use existing gap analysis data as input
   - Wealth concept failures (20) → high cultural_weight
   - Poverty concept failures (10) → high cultural_weight
   - Metaphor preservation 4.5% → metaphor centrality boost
   ```

4. **Implementation Strategy:**
   - Start with **Tier 1 concepts** (wealth, poverty, metaphors)
   - Use gap analysis failure counts as proxy for cultural weight
   - Gradually refine with expert input

**Priority:** HIGH (affects RAG retrieval quality)  
**Timeline:** Week 1 Days 3-4 (during data loading)  
**Effort:** 3-4 days implementation + validation

---

### 3. OWL 2 FORMAL SPECIFICATION (Moderate Gap)

#### What the Guide Requires:
- Complete OWL 2 DL ontology file
- RDF/XML serialization
- RDFS class hierarchies
- OWL object properties with domain/range
- Data properties with datatypes
- Cardinality constraints
- Disjointness axioms
- OOPS! validation compliance

#### Our Current State:
- ✅ Neo4j property graph schema (well-designed)
- ✅ Clear class hierarchies in design doc
- ✅ Relationship specifications
- ❌ No OWL file
- ❌ No RDF serialization
- ❌ No formal reasoner compatibility

#### **RECOMMENDATION 3: Dual Representation Strategy**

**Rationale:** 
- Neo4j is optimal for **RAG retrieval** (speed, flexibility)
- OWL 2 is essential for **formal validation** and **semantic web compliance**
- Both serve different purposes - maintain both!

**Action Items:**
1. **Create OWL Export Module:**
   ```bash
   # Create: scripts/export_to_owl.py
   - Read Neo4j graph
   - Generate OWL 2 ontology
   - Export as .owl (RDF/XML)
   - Export as .ttl (Turtle)
   - Export as .jsonld (JSON-LD for web)
   ```

2. **OWL File Structure:**
   ```
   kikuyu_proverb_ontology.owl
   ├── Metadata (DC terms, versioning)
   ├── Class Definitions (Proverb, CulturalConcept, etc.)
   ├── Object Properties (expressesTheme, containsConcept)
   ├── Data Properties (kikuyuText, culturalWeight)
   ├── Axioms (cardinality, disjointness)
   └── Instances (optional - can be separate)
   ```

3. **Validation Pipeline:**
   ```bash
   # Add to implementation roadmap
   - Week 4 Day 22: Export to OWL
   - Week 4 Day 23: Run OOPS! validation
   - Week 4 Day 23: Fix critical errors
   ```

**Priority:** MEDIUM (Week 4 deliverable, not blocking Phase 2c)  
**Timeline:** Week 4 Days 22-23  
**Effort:** 2-3 days + OOPS! iteration

---

### 4. EXPERT VALIDATION PROTOCOLS (Critical Gap)

#### What the Guide Requires:
- Multi-expert validation panels (3-5 experts)
- Structured validation sessions
- Inter-rater reliability (Fleiss' Kappa ≥0.80)
- Quantitative rating scales (1-5 Likert)
- Qualitative feedback collection
- Discrepancy resolution process
- Validation status tracking

#### Our Current State:
- ✅ Ireri expert translations (gold standard)
- ✅ Gap analysis validation (baseline comparison)
- ⚠️ Single expert (Ireri) - no inter-rater reliability
- ❌ No formal validation protocol
- ❌ No quantitative validation scores

#### **RECOMMENDATION 4: Pragmatic Validation Strategy**

**Given Constraints:**
- Master's thesis timeline
- Limited access to multiple Kikuyu experts
- Ireri data already collected

**Action Items:**
1. **Document Current Validation:**
   ```python
   # Add to Proverb nodes in Neo4j:
   validation_status: "expert_verified_ireri"
   validator_ids: ["ireri_expert_001"]
   validation_date: "2024-[actual_date]"
   validation_method: "expert_translation_gold_standard"
   validation_confidence: 0.95  # High (sole expert)
   inter_rater_agreement: null  # Single rater
   ```

2. **Enhanced Validation for Critical Concepts:**
   - Identify **Tier 1 concepts** (wealth, poverty)
   - Seek 2nd validator for these critical items
   - Use semantic similarity as proxy validation
   - Cross-reference with published Kikuyu literature

3. **Validation Tracking System:**
   ```bash
   # Create: scripts/validation_tracker.py
   - Track validation coverage
   - Identify unvalidated items
   - Calculate validation statistics
   - Generate validation reports
   ```

4. **Thesis Limitation Documentation:**
   ```markdown
   # In thesis limitations section:
   "Cultural validation conducted with single expert (Ireri).
   Future work should include multi-expert panels for
   inter-rater reliability validation."
   ```

**Priority:** HIGH (thesis methodology requirement)  
**Timeline:** Week 2 Days 13-14  
**Effort:** 2 days + potential 2nd expert recruitment

---

### 5. NEO4J SCHEMA ENHANCEMENTS (Moderate Gap)

#### What the Guide Requires vs. Our Current Design:

| Aspect | Guide Specification | Our Current Design | Gap Assessment |
|--------|-------------------|-------------------|----------------|
| **Proverb Node Properties** | 20+ properties including validation metadata | 15 properties | ⚠️ Missing: `inter_rater_agreement`, `validator_ids`, `regional_variations` |
| **CulturalConcept Properties** | Multi-dimensional with presuppositions | Basic properties | ⚠️ Missing: `presupposed_concepts[]`, `worldview_implications`, `historical_context` |
| **Relationship Properties** | Scored relationships (strength 0-1) | Basic relationships | ⚠️ Missing: `strength`, `confidence`, `annotator_agreement` |
| **Metaphor Representation** | Explicit MetaphoricalDomain nodes | Embedded in Proverb | ⚠️ Need: Separate metaphor domain taxonomy |
| **Historical Context** | HistoricalPeriod nodes | Not included | ⚠️ Missing: Temporal context modeling |
| **Social Context** | SocialContext nodes with appropriateness | Not included | ⚠️ Missing: Usage context modeling |

#### **RECOMMENDATION 5: Incremental Schema Enhancement**

**Phase 2c (Week 1) - Core Schema:**
```cypher
// Enhanced Proverb Node
CREATE (p:Proverb {
    // Existing properties...
    
    // ADD validation metadata:
    validator_ids: ["ireri_expert_001"],
    inter_rater_agreement: null,
    validation_confidence: 0.95,
    
    // ADD usage metadata:
    regional_variations: [],
    formality_level: "medium",
    usage_frequency: 7.5  // 1-10 scale
})
```

**Phase 2c (Week 2) - Extended Classes:**
```cypher
// NEW: MetaphoricalDomain nodes
CREATE (md:MetaphoricalDomain {
    domain_id: "MD_001",
    domain_type: "agricultural",
    domain_name: "Agricultural Domain",
    source_elements: ["planting", "harvest", "weeding"],
    target_concepts: ["investment", "reward", "maintenance"],
    cultural_grounding: "Kikuyu farming heritage",
    proverb_usage_count: 34
})

// NEW: SocialContext nodes
CREATE (sc:SocialContext {
    context_id: "SC_001",
    context_type: "family_dispute_resolution",
    appropriate_speakers: ["elders"],
    formality_level: "high",
    usage_frequency: "common"
})
```

**Priority:** MEDIUM-HIGH (improves ontology richness)  
**Timeline:** Week 1-2 of Phase 2c  
**Effort:** 3-4 days additional implementation

---

### 6. RELATIONSHIP PROPERTY SPECIFICATIONS (Major Gap)

#### What the Guide Requires:

**Every relationship should have:**
- `strength` (0-1): How strong the relationship
- `confidence` (0-1): How certain we are
- `annotator_agreement` (0-1): Expert consensus
- `evidence_type`: Source of relationship knowledge
- Type-specific properties (e.g., `salience` for CONTAINS_CONCEPT)

#### Our Current Design:
```cypher
// Current: Basic relationship
(p:Proverb)-[:CONTAINS_CONCEPT]->(c:CulturalConcept)

// Missing: Rich metadata
```

#### **RECOMMENDATION 6: Enhanced Relationships**

**Implementation:**
```cypher
// Enhanced CONTAINS_CONCEPT relationship
CREATE (p:Proverb)-[:CONTAINS_CONCEPT {
    // Core metadata
    strength: 0.92,
    confidence: 0.88,
    evidence_type: "expert_annotation",
    
    // Concept-specific
    salience: 0.92,           // How central to proverb
    concept_role: "central",   // central | supporting | background
    invocation_type: "explicit", // explicit | implicit | presupposed
    
    // Translation impact
    cultural_necessity: 0.89,      // Need to understand proverb
    translation_criticality: 0.94  // Need to preserve in translation
}]->(c:CulturalConcept)

// Enhanced EXPRESSES relationship
CREATE (p:Proverb)-[:EXPRESSES {
    strength: 0.88,
    confidence: 0.92,
    directionality: "primary",    // primary | secondary | tertiary
    explicitness: "implicit",     // explicit | implicit
    cultural_validation: "expert_confirmed"
}]->(wt:WealthTheme)
```

**Priority:** HIGH (critical for RAG quality)  
**Timeline:** Week 1 Days 5-7  
**Effort:** 2-3 days

---

### 7. VALIDATION & QUALITY ASSURANCE PIPELINE (Critical Gap)

#### What the Guide Requires:
- Automated validation pipeline (`ontology_validation.sh`)
- OOPS! structural validation
- HermiT reasoner consistency checking
- Competency question testing
- Cultural validation metrics
- Comprehensive validation reports

#### Our Current State:
- ❌ No automated validation
- ❌ No OOPS! integration
- ❌ No reasoner validation
- ✅ Manual gap analysis (good foundation)

#### **RECOMMENDATION 7: Validation Pipeline**

**Create Multi-Stage Validation:**

```bash
# Create: scripts/validate_ontology.sh
#!/bin/bash
echo "=== Kikuyu Proverb Ontology Validation ==="

# Stage 1: Data Completeness
python3 scripts/validation/check_data_completeness.py

# Stage 2: Neo4j Integrity
python3 scripts/validation/check_neo4j_integrity.py

# Stage 3: Cultural Metrics
python3 scripts/validation/compute_cultural_metrics.py

# Stage 4: OWL Validation (Week 4 only)
# curl -X POST http://oops.linkeddata.es/rest \
#   -F ontology=@kikuyu_proverbs.owl

# Stage 5: Competency Questions
python3 scripts/validation/test_competency_questions.py

echo "=== Validation Complete ==="
```

**Competency Questions to Test:**
```python
# scripts/validation/test_competency_questions.py

COMPETENCY_QUESTIONS = [
    {
        'question': 'What cultural concepts does proverb KP_001 presuppose?',
        'cypher': '''
            MATCH (p:Proverb {id: 'KP_001'})-[:CONTAINS_CONCEPT]->(c:CulturalConcept)
            RETURN c.name, c.cultural_significance
        ''',
        'expected_result_type': 'list_of_concepts'
    },
    {
        'question': 'Which proverbs express wealth themes with high cultural weight?',
        'cypher': '''
            MATCH (p:Proverb)-[:EXPRESSES]->(wt:WealthTheme)
            WHERE p.cultural_weight > 0.85
            RETURN p.kikuyu_text, p.cultural_weight
            ORDER BY p.cultural_weight DESC
        ''',
        'expected_min_results': 10
    },
    {
        'question': 'What metaphorical mappings are used in agricultural proverbs?',
        'cypher': '''
            MATCH (p:Proverb)-[:EMPLOYS_METAPHOR]->(md:MetaphoricalDomain)
            WHERE md.domain_type = 'agricultural'
            RETURN p.kikuyu_text, md.mapping_principles
        ''',
        'expected_result_type': 'metaphor_mappings'
    }
]
```

**Priority:** HIGH (Week 2, 3, 4 deliverables)  
**Timeline:** Implement Week 2 Days 13-14, run throughout  
**Effort:** 4-5 days development + ongoing usage

---

## PRIORITIZED IMPLEMENTATION RECOMMENDATIONS

### IMMEDIATE ACTIONS (Before Phase 2c Begins)

#### 1. Ethical Foundation (2-3 days)
```
Priority: CRITICAL - Cannot proceed ethically without this
Action: Document Ireri collaboration, create consent framework
Deliverable: docs/ethics/community_engagement_protocol.md
```

#### 2. Cultural Weight Algorithm Design (1-2 days)
```
Priority: HIGH - Needed for Week 1 Days 3-4
Action: Design ConceptMetrics dataclass, plan calculation
Deliverable: src/ontology/cultural_weights.py (skeleton)
```

#### 3. Enhanced Schema Specification (1 day)
```
Priority: HIGH - Needed for Week 1 Days 1-2
Action: Update Neo4j schema creation script with enhanced properties
Deliverable: Updated Cypher schema with relationship properties
```

### PHASE 2C INTEGRATION

#### Week 1: Core Foundation + Enhancements
```
Days 1-2: Schema Design & Neo4j Setup
  - Implement enhanced Proverb node properties
  - Add validation metadata fields
  - Create relationship property templates
  
Days 3-4: Core Data Loading + Cultural Weights
  - Load 100 proverbs with enhanced properties
  - Calculate cultural weights using new algorithm
  - Apply weights to concepts and proverbs
  
Days 5-7: Priority Relationships + Metadata
  - Create relationships with strength/confidence scores
  - Implement CONTAINS_CONCEPT with salience
  - Add validation status tracking
```

#### Week 2: Depth Enhancement + Validation
```
Days 8-10: Secondary Classes
  - Implement MetaphoricalDomain nodes
  - Add SocialContext nodes (if time permits)
  - Create historical period markers
  
Days 11-12: Inter-Proverb Relationships
  - Implement semantic similarity relationships
  - Use SemanticDistanceCalculator
  
Days 13-14: Testing & Validation
  - Run validation pipeline
  - Test competency questions
  - Calculate cultural metrics
  - Generate validation report
```

#### Week 3: RAG Optimization + Documentation
```
Days 15-17: Indexing & Performance
  - Full-text search optimization
  - Composite indexes for retrieval patterns
  
Days 18-19: RAG Integration
  - Subgraph retrieval testing
  - Context assembly validation
  
Days 20-21: Documentation
  - Cypher query library
  - API documentation
  - Cultural weight calculation docs
```

#### Week 4: Formal Validation + OWL Export
```
Days 22-23: OWL Export & OOPS! Validation
  - Export to OWL 2 format
  - Run OOPS! pitfall scanner
  - Fix critical issues
  
Days 24-25: Expert Review (if possible)
  - Seek 2nd validator for Tier 1 concepts
  - Document validation limitations
  
Days 26-28: FAIR Compliance & Finalization
  - Add provenance metadata
  - Create JSON-LD export
  - Final validation report
  - Update thesis documentation
```

---

## GUIDE SECTIONS WE CAN ADAPT DIRECTLY

### ✅ Ready to Use (Copy-Paste with Minimal Changes)

1. **Neo4j Schema Creation Script** (Section 3.3)
   - Constraints and indexes
   - Node structure templates
   - Verification queries
   - **Action:** Use as template for Week 1 Days 1-2

2. **Cultural Weight Calculator** (Section 5.1)
   - Python implementation ready
   - ConceptMetrics dataclass defined
   - Multi-factor calculation logic
   - **Action:** Adapt for Week 1 Days 3-4

3. **Semantic Distance Calculator** (Section 5.2)
   - Embedding-based similarity
   - Knowledge graph relationship strength
   - Expert proximity scoring
   - **Action:** Use for Week 2 Days 11-12

4. **Validation Metrics** (Section 8.2)
   - Concept coverage calculation
   - Relationship density analysis
   - Weight distribution statistics
   - Validation rate tracking
   - **Action:** Implement Week 2 Days 13-14

### ⚠️ Adapt with Caution (Context-Specific)

1. **Community Engagement Framework** (Section 6.1)
   - Designed for multi-expert, multi-year projects
   - Our context: Master's thesis, single expert (Ireri)
   - **Adaptation:** Simplified version + retroactive documentation

2. **Knowledge Elicitation Sessions** (Section 6.2)
   - Assumes ongoing expert access
   - Our context: Data already collected
   - **Adaptation:** Use for validation/refinement only

3. **OWL Formal Specification** (Section 4)
   - Very comprehensive (200+ lines XML)
   - Our context: Need lightweight version
   - **Adaptation:** Core classes only, instances separate

---

## THESIS IMPLICATIONS

### What to Document in Thesis Methodology

#### Chapter 4: Ontology Construction Methodology

**4.1 Ethical Framework**
```
- Community engagement protocol (citing guide)
- Informed consent process with Ireri
- Benefit-sharing agreement
- Data sovereignty considerations
- Limitations: single expert validation
```

**4.2 Ontology Design**
```
- Design principles (cultural primacy)
- Schema specification (Neo4j + OWL)
- Cultural weight calculation algorithm
- Validation methodology
- Citing: Comprehensive Guide sections 2, 3, 5
```

**4.3 Implementation**
```
- 4-week implementation roadmap
- Data loading and transformation
- Relationship creation with confidence scores
- Quality assurance pipeline
- Citing: Guide sections 7, 8
```

**4.4 Validation**
```
- Multi-stage validation process
- Cultural metrics computation
- Competency question testing
- Inter-rater reliability (limitations)
- Citing: Guide section 8
```

### Limitations Section

**Acknowledge:**
1. Single expert validation (Ireri) vs. multi-expert panels
2. 100-proverb scope vs. comprehensive corpus
3. Retrospective consent vs. prospective FPIC
4. Limited metaphorical domain taxonomy
5. No historical period modeling (future work)

**Mitigate:**
1. Gap analysis provides quantitative validation
2. Gold standard quality compensates for quantity
3. Clear ethical documentation post-hoc
4. Core metaphors captured in proverb metadata
5. Design supports future extension

---

## DELIVERABLES CHECKLIST

### Before Phase 2c Begins
- [ ] `docs/ethics/community_engagement_protocol.md`
- [ ] `docs/ethics/ireri_collaboration_documentation.md`
- [ ] `src/ontology/cultural_weights.py` (skeleton)
- [ ] Enhanced Cypher schema specification
- [ ] Updated todo list with ethical + algorithm tasks

### Week 1 Deliverables
- [ ] Neo4j database with enhanced schema
- [ ] 100 proverbs loaded with validation metadata
- [ ] 186 entities, 88 actions, 150 concepts as nodes
- [ ] Cultural weights calculated for all concepts
- [ ] Priority relationships with confidence scores
- [ ] Initial validation report

### Week 2 Deliverables
- [ ] MetaphoricalDomain nodes (80 metaphors)
- [ ] Secondary class nodes (if time)
- [ ] Inter-proverb semantic relationships
- [ ] Validation pipeline running
- [ ] Cultural metrics dashboard
- [ ] Competency questions tested

### Week 3 Deliverables
- [ ] Optimized indexes for RAG retrieval
- [ ] Subgraph retrieval functions
- [ ] Cypher query library
- [ ] API documentation
- [ ] Performance benchmarks

### Week 4 Deliverables
- [ ] OWL 2 ontology export
- [ ] OOPS! validation report (with fixes)
- [ ] JSON-LD export for web
- [ ] Provenance metadata
- [ ] Final validation report
- [ ] Thesis methodology documentation

---

## CONCLUSION & NEXT STEPS

### Key Insights from Guide Analysis

1. **We have a strong foundation** - Phase 2b design is solid
2. **Ethical framework is urgent** - Document Ireri collaboration now
3. **Cultural weights are critical** - Implement algorithm Week 1
4. **Validation pipeline is essential** - Build incrementally Week 2+
5. **OWL export is valuable** - But not blocking (Week 4)
6. **Guide provides excellent code** - Adapt Python implementations directly

### Recommended Immediate Actions

**TODAY (Before starting Phase 2c):**
1. Create ethical documentation
2. Design cultural weight calculator
3. Enhance Neo4j schema with relationship properties
4. Update Phase 2c todo list with new tasks

**WEEK 1 (Days 1-2):**
1. Implement enhanced schema in Neo4j
2. Create validation tracking infrastructure
3. Set up cultural weight calculation pipeline

**ONGOING:**
1. Build validation pipeline incrementally
2. Test competency questions as you populate
3. Document everything for thesis methodology

### Success Criteria

✅ **Minimum Viable Ontology (for thesis):**
- 100 proverbs with cultural weights
- Core relationships with confidence scores
- Validation pipeline with metrics
- Ethical documentation
- Thesis-ready methodology chapter

🎯 **Optimal Ontology (if time permits):**
- All of above PLUS:
- MetaphoricalDomain taxonomy
- OWL 2 export with OOPS! validation
- 2nd expert validation for Tier 1 concepts
- SocialContext modeling
- JSON-LD export for semantic web

---

**Status:** Ready to proceed with enhanced Phase 2c implementation  
**Next Action:** Review recommendations, update todo list, begin ethical documentation  
**Timeline:** 4 weeks (as planned) with incremental enhancements
