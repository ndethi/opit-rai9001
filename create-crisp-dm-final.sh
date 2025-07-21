#!/bin/bash

echo "Creating CRISP-DM Overview Issues..."

# Issue 1: Business Understanding
gh issue create \
  --title "[CRISP-DM OVERVIEW] 🎯 Business Understanding Phase Progress" \
  --body "CRISP-DM Business Understanding Phase milestone tracking.

## Phase Objective
Establish research problem definition and stakeholder alignment for the Kikuyu proverb Ontology-Grounded RAG thesis.

## Key Deliverables
- [ ] Research proposal with cultural fidelity objectives
- [ ] Stakeholder requirements documented
- [ ] Success criteria and evaluation metrics defined
- [ ] Project charter and timeline alignment

## PROJECT_FIELDS
- Sprint_Week: Week 1 (Jun 20-26)
- Criticality: 🚨 CRITICAL
- CRISP_DM_Phase: 🎯 Business Understanding
- Effort_Hours: 27" \
  --label "crisp-dm,overview,business-understanding,milestone,week-1" \
  --assignee "@me"

echo "Created Business Understanding issue"
sleep 3

# Issue 2: Data Understanding
gh issue create \
  --title "[CRISP-DM OVERVIEW] 📊 Data Understanding Phase Progress" \
  --body "CRISP-DM Data Understanding Phase milestone tracking.

## Phase Objective
Comprehensive exploration and analysis of Kikuyu proverb landscape for ontology construction.

## Key Deliverables
- [ ] 300+ Kikuyu proverbs catalogued with metadata
- [ ] Cultural expert network established (3+ experts)
- [ ] Data quality assessment completed
- [ ] Cultural themes taxonomy created

## PROJECT_FIELDS
- Sprint_Week: Week 1-2 (Jun 20-Jul 3)
- Criticality: 🚨 CRITICAL
- CRISP_DM_Phase: 📊 Data Understanding
- Effort_Hours: 43" \
  --label "crisp-dm,overview,data-understanding,milestone,week-1,week-2" \
  --assignee "@me"

echo "Created Data Understanding issue"
sleep 3

# Issue 3: Data Preparation
gh issue create \
  --title "[CRISP-DM OVERVIEW] 🏗️ Data Preparation Phase Progress" \
  --body "CRISP-DM Data Preparation Phase milestone tracking.

## Phase Objective
Systematic construction of Kikuyu proverb ontology and knowledge graph infrastructure.

## Key Deliverables
- [ ] Complete Kikuyu proverb ontology (OWL format)
- [ ] OOPS! validation passed with expert review
- [ ] Neo4j knowledge graph populated with 300+ instances
- [ ] Hypergraph representations created

## PROJECT_FIELDS
- Sprint_Week: Week 2-4 (Jun 27-Jul 17)
- Criticality: 🛑 BLOCKER
- CRISP_DM_Phase: 🏗️ Data Preparation
- Effort_Hours: 62" \
  --label "crisp-dm,overview,data-preparation,milestone,week-2,week-3,week-4" \
  --assignee "@me"

echo "Created Data Preparation issue"
sleep 3

# Issue 4: Modeling
gh issue create \
  --title "[CRISP-DM OVERVIEW] 🤖 Modeling Phase Progress" \
  --body "CRISP-DM Modeling Phase milestone tracking.

## Phase Objective
Implementation of Ontology-Grounded RAG system integrating knowledge graph with LLM.

## Key Deliverables
- [ ] Functional OG-RAG system prototype
- [ ] LLM-knowledge graph integration working
- [ ] Cultural context injection pipeline
- [ ] System performance benchmarks established

## PROJECT_FIELDS
- Sprint_Week: Week 4-5 (Jul 11-24)
- Criticality: 🚨 CRITICAL
- CRISP_DM_Phase: 🤖 Modeling
- Effort_Hours: 50" \
  --label "crisp-dm,overview,modeling,milestone,week-4,week-5" \
  --assignee "@me"

echo "Created Modeling issue"
sleep 3

# Issue 5: Evaluation
gh issue create \
  --title "[CRISP-DM OVERVIEW] ⚖️ Evaluation Phase Progress" \
  --body "CRISP-DM Evaluation Phase milestone tracking.

## Phase Objective
Comprehensive evaluation of OG-RAG system performance with cultural fidelity validation.

## Key Deliverables
- [ ] Comprehensive evaluation framework implemented
- [ ] Statistical analysis of 100+ translations completed
- [ ] Cultural expert validation results documented
- [ ] Performance comparison with baseline methods

## PROJECT_FIELDS
- Sprint_Week: Week 5-7 (Jul 18-Aug 7)
- Criticality: 🛑 BLOCKER
- CRISP_DM_Phase: ⚖️ Evaluation
- Effort_Hours: 90" \
  --label "crisp-dm,overview,evaluation,milestone,week-5,week-6,week-7" \
  --assignee "@me"

echo "Created Evaluation issue"
sleep 3

# Issue 6: Deployment
gh issue create \
  --title "[CRISP-DM OVERVIEW] 🚀 Deployment Phase Progress" \
  --body "CRISP-DM Deployment Phase milestone tracking.

## Phase Objective
Documentation, knowledge transfer, thesis defense preparation and academic contribution finalization.

## Key Deliverables
- [ ] Complete thesis document (18,000+ words)
- [ ] Professional defense presentation prepared
- [ ] Technical system demonstration ready
- [ ] Comprehensive documentation package

## PROJECT_FIELDS
- Sprint_Week: Week 7-10 (Jul 25-Aug 30)
- Criticality: 🛑 BLOCKER
- CRISP_DM_Phase: 🚀 Deployment
- Effort_Hours: 95" \
  --label "crisp-dm,overview,deployment,milestone,week-7,week-8,week-9,week-10" \
  --assignee "@me"

echo "Created Deployment issue"

echo ""
echo "✅ All CRISP-DM Overview Issues Created Successfully!"
echo ""
echo "Created issues:"
echo "1. 🎯 Business Understanding Phase Progress"
echo "2. 📊 Data Understanding Phase Progress"
echo "3. 🏗️ Data Preparation Phase Progress"
echo "4. 🤖 Modeling Phase Progress"
echo "5. ⚖️ Evaluation Phase Progress"
echo "6. 🚀 Deployment Phase Progress"
