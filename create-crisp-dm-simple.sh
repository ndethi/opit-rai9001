#!/bin/bash

# CRISP-DM Overview Issues Creator - Simplified Version
# Creates GitHub issues for CRISP-DM methodology milestone tracking

set -e

# Disable GitHub CLI pager
export GH_PAGER=""
export PAGER=""

echo "🎯 Creating CRISP-DM Overview Issues for OPIT RAI9001"
echo "================================================="
echo ""

# Function to create issue with simplified approach
create_simple_issue() {
    local title="$1"
    local labels="$2"
    local body_file="$3"
    
    echo "📝 Creating: $title"
    
    if [ -f "$body_file" ]; then
        gh issue create \
            --title "$title" \
            --body-file "$body_file" \
            --label "$labels" \
            --assignee "@me"
    else
        echo "❌ Body file not found: $body_file"
        return 1
    fi
}

# Create temporary directory for issue bodies
mkdir -p .tmp/crisp-dm-bodies

# Create Issue 1 body
cat > .tmp/crisp-dm-bodies/business-understanding.md << 'EOF'
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

## PROJECT_FIELDS
- Sprint_Week: Week 1 (Jun 20-26)
- Criticality: 🚨 CRITICAL
- OPIT_Deadline: Examining Committee (Jul 13)
- Thesis_Section: Methodology
- CRISP_DM_Phase: 🎯 Business Understanding
- Effort_Hours: 27
EOF

# Create Issue 2 body
cat > .tmp/crisp-dm-bodies/data-understanding.md << 'EOF'
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

## PROJECT_FIELDS
- Sprint_Week: Week 1-2 (Jun 20-Jul 3)
- Criticality: 🚨 CRITICAL
- OPIT_Deadline: Examining Committee (Jul 13)
- Thesis_Section: Methodology
- CRISP_DM_Phase: 📊 Data Understanding
- Effort_Hours: 43
EOF

# Create Issue 3 body
cat > .tmp/crisp-dm-bodies/data-preparation.md << 'EOF'
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

## Phase Success Criteria
- ✅ Ontology passes OOPS! validation
- ✅ Cultural expert approval of knowledge representation
- ✅ Knowledge graph successfully populated
- ✅ Data quality suitable for OG-RAG integration

## PROJECT_FIELDS
- Sprint_Week: Week 2-4 (Jun 27-Jul 17)
- Criticality: 🛑 BLOCKER
- OPIT_Deadline: Thesis to Committee (Jul 27)
- Thesis_Section: Implementation
- CRISP_DM_Phase: 🏗️ Data Preparation
- Effort_Hours: 62
EOF

# Create Issue 4 body
cat > .tmp/crisp-dm-bodies/modeling.md << 'EOF'
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

## Phase Success Criteria
- ✅ System produces culturally-faithful translations
- ✅ Performance meets baseline quality requirements
- ✅ Integration stable and reliable
- ✅ Architecture suitable for evaluation phase

## PROJECT_FIELDS
- Sprint_Week: Week 4-5 (Jul 11-24)
- Criticality: 🚨 CRITICAL
- OPIT_Deadline: Thesis to Committee (Jul 27)
- Thesis_Section: Implementation
- CRISP_DM_Phase: 🤖 Modeling
- Effort_Hours: 50
EOF

# Create Issue 5 body
cat > .tmp/crisp-dm-bodies/evaluation.md << 'EOF'
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

## Phase Success Criteria
- ✅ Statistical significance in key metrics
- ✅ Cultural expert validation achieved
- ✅ Performance exceeds baseline methods
- ✅ Results support thesis hypothesis

## PROJECT_FIELDS
- Sprint_Week: Week 5-7 (Jul 18-Aug 7)
- Criticality: 🛑 BLOCKER
- OPIT_Deadline: Defense Form (Aug 3)
- Thesis_Section: Evaluation
- CRISP_DM_Phase: ⚖️ Evaluation
- Effort_Hours: 90
EOF

# Create Issue 6 body
cat > .tmp/crisp-dm-bodies/deployment.md << 'EOF'
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

## Phase Success Criteria
- ✅ Successful thesis defense completion
- ✅ Committee approval and recommendations
- ✅ Final submission accepted
- ✅ Knowledge effectively transferred

## PROJECT_FIELDS
- Sprint_Week: Week 7-10 (Jul 25-Aug 30)
- Criticality: 🛑 BLOCKER
- OPIT_Deadline: Post-Defense (Aug 30)
- Thesis_Section: All Sections
- CRISP_DM_Phase: 🚀 Deployment
- Effort_Hours: 95
EOF

# Create the issues
echo "Creating CRISP-DM Overview Issues..."

create_simple_issue \
    "[CRISP-DM OVERVIEW] 🎯 Business Understanding Phase Progress" \
    "crisp-dm,overview,business-understanding,milestone,week-1" \
    ".tmp/crisp-dm-bodies/business-understanding.md"

sleep 2

create_simple_issue \
    "[CRISP-DM OVERVIEW] 📊 Data Understanding Phase Progress" \
    "crisp-dm,overview,data-understanding,milestone,week-1,week-2" \
    ".tmp/crisp-dm-bodies/data-understanding.md"

sleep 2

create_simple_issue \
    "[CRISP-DM OVERVIEW] 🏗️ Data Preparation Phase Progress" \
    "crisp-dm,overview,data-preparation,milestone,week-2,week-3,week-4" \
    ".tmp/crisp-dm-bodies/data-preparation.md"

sleep 2

create_simple_issue \
    "[CRISP-DM OVERVIEW] 🤖 Modeling Phase Progress" \
    "crisp-dm,overview,modeling,milestone,week-4,week-5" \
    ".tmp/crisp-dm-bodies/modeling.md"

sleep 2

create_simple_issue \
    "[CRISP-DM OVERVIEW] ⚖️ Evaluation Phase Progress" \
    "crisp-dm,overview,evaluation,milestone,week-5,week-6,week-7" \
    ".tmp/crisp-dm-bodies/evaluation.md"

sleep 2

create_simple_issue \
    "[CRISP-DM OVERVIEW] 🚀 Deployment Phase Progress" \
    "crisp-dm,overview,deployment,milestone,week-7,week-8,week-9,week-10" \
    ".tmp/crisp-dm-bodies/deployment.md"

echo ""
echo "🎉 CRISP-DM Overview Issues Creation Complete!"
echo ""
echo "📋 Current Issues in Repository:"
gh issue list --limit 10 --json number,title,labels --jq '.[] | "\(.number): \(.title)"'

# Clean up temporary files
rm -rf .tmp/crisp-dm-bodies

echo ""
echo "✨ All CRISP-DM milestone issues have been successfully created!"
