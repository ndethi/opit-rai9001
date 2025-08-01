#!/bin/bash

# CRISP-DM Overview Issues Creation Script
# This script creates the 6 CRISP-DM overview milestone issues

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Creating CRISP-DM Overview Issues...${NC}"

# Issue 1: Business Understanding Phase
echo "Creating Business Understanding Phase overview..."
./add-issue.sh create <<EOF
[CRISP-DM OVERVIEW] 🎯 Business Understanding Phase Progress
crisp-dm,overview,business-understanding,milestone,week-1
@me
2025-06-26
# 🎯 Business Understanding Phase Overview

## Phase Objective
Establish research problem definition, stakeholder alignment, and project foundation for the Kikuyu proverb Ontology-Grounded RAG thesis.

## Key Deliverables
- [ ] Research proposal with clear cultural fidelity objectives
- [ ] Stakeholder requirements documented (supervisor + cultural experts)
- [ ] Success criteria and evaluation metrics defined
- [ ] Risk assessment and mitigation strategies
- [ ] Project charter and timeline alignment with OPIT deadlines

## CRISP-DM Activities Completed
- [ ] Research problem definition and scope
- [ ] Stakeholder requirements gathering
- [ ] Success criteria establishment
- [ ] Risk assessment and timeline planning
- [ ] Technical infrastructure setup

## Phase Success Criteria
- ✅ Supervisor approval of research direction
- ✅ Clear cultural fidelity criteria established
- ✅ Technical infrastructure operational
- ✅ OPIT deadline compliance strategy defined

## Related Issues
Links to specific implementation issues in Business Understanding phase (Week 1 sprint issues, partnership agreement, architecture diagrams, etc.)

## Notes
This overview issue tracks the overall progress of the Business Understanding phase across all related detailed implementation issues. Updates reflect completion of CRISP-DM methodology requirements.
END
Week 1 (Jun 20-26)
🚨 CRITICAL
Examining Committee (Jul 13)
Methodology
27
EOF

# Issue 2: Data Understanding Phase
echo "Creating Data Understanding Phase overview..."
./add-issue.sh create <<EOF
[CRISP-DM OVERVIEW] 📊 Data Understanding Phase Progress
crisp-dm,overview,data-understanding,milestone,week-1,week-2
@me
2025-07-03
# 📊 Data Understanding Phase Overview

## Phase Objective
Comprehensive exploration and analysis of Kikuyu proverb landscape, cultural context, and data quality assessment for ontology construction.

## Key Deliverables
- [ ] 300+ Kikuyu proverbs catalogued with metadata
- [ ] Cultural expert network established (3+ experts)
- [ ] Data quality assessment completed
- [ ] Cultural themes taxonomy created
- [ ] Translation challenge documentation
- [ ] Ethics approval for cultural collaboration

## CRISP-DM Activities Completed
- [ ] Initial data collection from multiple sources
- [ ] Data exploration and familiarization
- [ ] Data quality assessment and gap analysis
- [ ] Cultural context understanding and documentation
- [ ] Expert domain knowledge gathering

## Phase Success Criteria
- ✅ 300+ unique proverbs with cultural context
- ✅ Cultural expert validation and collaboration agreements
- ✅ Data quality sufficient for ontology construction
- ✅ Translation challenges identified and documented

## Data Sources Utilized
- "1000 Kikuyu Proverbs" collection
- Cultural expert interviews and knowledge
- Academic literature and research papers
- Community documentation and oral traditions

## Related Issues
Links to proverb collection, cultural expert interviews, literature analysis, ethics approval, and data quality assessment issues.

## Notes
This phase establishes the foundation for ontology construction by ensuring comprehensive understanding of the cultural and linguistic data landscape.
END
Week 1-2 (Jun 20-Jul 3)
🚨 CRITICAL
Examining Committee (Jul 13)
Methodology
43
EOF

# Issue 3: Data Preparation Phase
echo "Creating Data Preparation Phase overview..."
./add-issue.sh create <<EOF
[CRISP-DM OVERVIEW] 🏗️ Data Preparation Phase Progress
crisp-dm,overview,data-preparation,milestone,week-2,week-3,week-4
@me
2025-07-17
# 🏗️ Data Preparation Phase Overview

## Phase Objective
Systematic construction of Kikuyu proverb ontology and knowledge graph infrastructure for OG-RAG system integration.

## Key Deliverables
- [ ] Complete Kikuyu proverb ontology (OWL format)
- [ ] OOPS! validation passed with expert review
- [ ] Neo4j knowledge graph populated with 300+ instances
- [ ] Hypergraph representations created
- [ ] Data preparation documentation completed

## CRISP-DM Activities Completed
- [ ] Data cleaning and preparation
- [ ] Feature engineering (ontology terms and concepts)
- [ ] Data transformation to graph structure
- [ ] Data integration and consistency validation
- [ ] Knowledge graph instantiation and population

## Ontology Construction Progress
- [ ] Scope and boundaries defined (100+ terms)
- [ ] Class hierarchy and taxonomies designed
- [ ] Object and data properties specified
- [ ] Cultural context annotations integrated
- [ ] Expert validation and approval obtained

## Technical Implementation
- [ ] Neo4j database setup and configuration
- [ ] Graph population scripts and automation
- [ ] Data consistency checks and quality assurance
- [ ] Hypergraph structure preparation for retrieval

## Phase Success Criteria
- ✅ Ontology passes OOPS! validation
- ✅ Cultural expert approval of knowledge representation
- ✅ Knowledge graph successfully populated
- ✅ Data quality suitable for OG-RAG integration

## Related Issues
Links to ontology construction, OOPS! validation, Neo4j setup, knowledge graph population, and expert review issues.

## Notes
This is the most intensive CRISP-DM phase, requiring careful balance of technical accuracy and cultural authenticity in knowledge representation.
END
Week 2-4 (Jun 27-Jul 17)
🛑 BLOCKER
Thesis to Committee (Jul 27)
Implementation
62
EOF

# Issue 4: Modeling Phase
echo "Creating Modeling Phase overview..."
./add-issue.sh create <<EOF
[CRISP-DM OVERVIEW] 🤖 Modeling Phase Progress
crisp-dm,overview,modeling,milestone,week-4,week-5
@me
2025-07-24
# 🤖 Modeling Phase Overview

## Phase Objective
Implementation of Ontology-Grounded RAG system integrating knowledge graph with LLM for culturally-faithful proverb translation.

## Key Deliverables
- [ ] Functional OG-RAG system prototype
- [ ] LLM-knowledge graph integration working
- [ ] Cultural context injection pipeline
- [ ] System performance benchmarks established
- [ ] Technical documentation completed

## CRISP-DM Activities Completed
- [ ] Modeling technique selection and justification
- [ ] Model building (OG-RAG architecture implementation)
- [ ] Parameter tuning and optimization
- [ ] Model assessment and validation
- [ ] Integration testing and performance evaluation

## System Architecture Components
- [ ] Hypergraph retrieval mechanism
- [ ] LLM API integration (Gemini/GPT-4)
- [ ] Cultural context injection pipeline
- [ ] Translation quality assessment module
- [ ] Error handling and fallback mechanisms

## Technical Implementation Progress
- [ ] OG-RAG architecture design and implementation
- [ ] Knowledge graph retrieval optimization
- [ ] Prompt engineering for cultural fidelity
- [ ] System integration and debugging
- [ ] Performance benchmarking and tuning

## Phase Success Criteria
- ✅ System produces culturally-faithful translations
- ✅ Performance meets baseline quality requirements
- ✅ Integration stable and reliable
- ✅ Architecture suitable for evaluation phase

## Related Issues
Links to OG-RAG implementation, hypergraph retrieval, LLM integration, system testing, and performance optimization issues.

## Notes
This phase transforms the prepared knowledge representation into a functional translation system, balancing technical performance with cultural authenticity.
END
Week 4-5 (Jul 11-24)
🚨 CRITICAL
Thesis to Committee (Jul 27)
Implementation
50
EOF

# Issue 5: Evaluation Phase
echo "Creating Evaluation Phase overview..."
./add-issue.sh create <<EOF
[CRISP-DM OVERVIEW] ⚖️ Evaluation Phase Progress
crisp-dm,overview,evaluation,milestone,week-5,week-6,week-7
@me
2025-08-07
# ⚖️ Evaluation Phase Overview

## Phase Objective
Comprehensive evaluation of OG-RAG system performance with focus on cultural fidelity validation through human expert assessment.

## Key Deliverables
- [ ] Comprehensive evaluation framework implemented
- [ ] Statistical analysis of 100+ translations completed
- [ ] Cultural expert validation results documented
- [ ] Performance comparison with baseline methods
- [ ] Error analysis and improvement recommendations

## CRISP-DM Activities Completed
- [ ] Evaluation method design and implementation
- [ ] Model testing and validation execution
- [ ] Results interpretation and analysis
- [ ] Cultural fidelity assessment completion
- [ ] Statistical significance validation

## Evaluation Framework Components
- [ ] Human evaluation protocol and rubrics
- [ ] Cultural evaluator recruitment and onboarding
- [ ] LLM-as-judge evaluation pipeline
- [ ] Statistical analysis methodology
- [ ] Inter-rater reliability assessment

## Assessment Metrics
- [ ] Translation accuracy (linguistic correctness)
- [ ] Cultural fidelity preservation
- [ ] Contextual appropriateness
- [ ] Usage scenario applicability
- [ ] Expert satisfaction ratings

## Phase Success Criteria
- ✅ Statistical significance in key metrics
- ✅ Cultural expert validation achieved
- ✅ Performance exceeds baseline methods
- ✅ Results support thesis hypothesis

## Related Issues
Links to evaluation protocol design, cultural evaluator recruitment, statistical analysis, results visualization, and expert feedback integration issues.

## Notes
This phase provides the evidence base for thesis conclusions, requiring rigorous methodology to ensure academic validity and cultural authenticity.
END
Week 5-7 (Jul 18-Aug 7)
🛑 BLOCKER
Defense Form (Aug 3)
Evaluation
90
EOF

# Issue 6: Deployment Phase
echo "Creating Deployment Phase overview..."
./add-issue.sh create <<EOF
[CRISP-DM OVERVIEW] 🚀 Deployment Phase Progress
crisp-dm,overview,deployment,milestone,week-7,week-8,week-9,week-10
@me
2025-08-30
# 🚀 Deployment Phase Overview

## Phase Objective
Documentation, knowledge transfer, thesis defense preparation, and academic contribution finalization for the Kikuyu proverb OG-RAG research.

## Key Deliverables
- [ ] Complete thesis document (18,000+ words)
- [ ] Professional defense presentation prepared
- [ ] Technical system demonstration ready
- [ ] Comprehensive documentation package
- [ ] Knowledge transfer materials created

## CRISP-DM Activities Completed
- [ ] Deployment planning and execution
- [ ] Documentation creation and review
- [ ] Knowledge transfer to academic community
- [ ] Project review and lessons learned
- [ ] Academic contribution finalization

## Thesis Documentation Progress
- [ ] Results chapter (2500 words)
- [ ] Discussion and analysis chapter (2000 words)
- [ ] Executive summary and abstract
- [ ] Limitations and future work section
- [ ] Complete bibliography and citations

## Defense Preparation
- [ ] 45-minute presentation created
- [ ] Technical demonstration prepared
- [ ] Committee Q&A preparation
- [ ] Practice sessions completed
- [ ] Backup materials and contingencies

## Knowledge Transfer Components
- [ ] System documentation for replication
- [ ] Implementation guide for future researchers
- [ ] Academic publication draft
- [ ] Community presentation materials
- [ ] Best practices documentation

## Phase Success Criteria
- ✅ Successful thesis defense completion
- ✅ Committee approval and recommendations
- ✅ Final submission accepted
- ✅ Knowledge effectively transferred

## Related Issues
Links to thesis writing, defense preparation, documentation creation, final submission, and project archival issues.

## Notes
This final phase ensures the research contributes meaningfully to academic knowledge while providing practical guidance for future work in culturally-grounded NLP.
END
Week 7-10 (Jul 25-Aug 30)
🛑 BLOCKER
Post-Defense (Aug 30)
All Sections
95
EOF

echo -e "${GREEN}All 6 CRISP-DM overview issues created successfully!${NC}"
echo -e "${BLUE}Issues created:${NC}"
echo "  1. Business Understanding Phase Progress"
echo "  2. Data Understanding Phase Progress"
echo "  3. Data Preparation Phase Progress"
echo "  4. Modeling Phase Progress"
echo "  5. Evaluation Phase Progress"
echo "  6. Deployment Phase Progress"
