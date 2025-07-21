#!/bin/bash

# CRISP-DM Overview Issues Creator for OPIT RAI9001 Research Project
# Creates GitHub issues for CRISP-DM methodology milestone tracking

set -e

# Disable GitHub CLI pager
export GH_PAGER=""
export PAGER=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}🎯 Creating CRISP-DM Overview Issues for OPIT RAI9001${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v gh >/dev/null 2>&1; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
    echo "Please install: brew install gh"
    exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
    echo -e "${RED}❌ Not authenticated with GitHub${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites satisfied${NC}"
echo ""

# Function to create issue with retry logic
create_issue_with_retry() {
    local title="$1"
    local body="$2"
    local labels="$3"
    local assignee="$4"
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if gh issue create \
            --title "$title" \
            --body "$body" \
            --label "$labels" \
            --assignee "$assignee" 2>/dev/null; then
            return 0
        else
            retry_count=$((retry_count + 1))
            echo -e "${YELLOW}⚠️  Retry $retry_count/$max_retries for: $title${NC}"
            sleep 2
        fi
    done
    
    echo -e "${RED}❌ Failed to create issue after $max_retries attempts: $title${NC}"
    return 1
}

# Issue 1: Business Understanding Phase
echo -e "${CYAN}📝 Creating Business Understanding Phase Overview...${NC}"

ISSUE_1_TITLE="[CRISP-DM OVERVIEW] 🎯 Business Understanding Phase Progress"
ISSUE_1_LABELS="crisp-dm,overview,business-understanding,milestone,week-1"
ISSUE_1_ASSIGNEE="@me"
ISSUE_1_BODY="# 🎯 Business Understanding Phase Overview

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

## PROJECT_FIELDS
- Sprint_Week: Week 1 (Jun 20-26)
- Criticality: 🚨 CRITICAL
- OPIT_Deadline: Examining Committee (Jul 13)
- Thesis_Section: Methodology
- CRISP_DM_Phase: 🎯 Business Understanding
- Effort_Hours: 27

## Notes
This overview issue tracks the overall progress of the Business Understanding phase across all related detailed implementation issues. Updates reflect completion of CRISP-DM methodology requirements."

create_issue_with_retry "$ISSUE_1_TITLE" "$ISSUE_1_BODY" "$ISSUE_1_LABELS" "$ISSUE_1_ASSIGNEE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Created Business Understanding Phase Overview${NC}"
else
    echo -e "${RED}❌ Failed to create Business Understanding Phase Overview${NC}"
fi
sleep 2

# Issue 2: Data Understanding Phase
echo -e "${CYAN}📝 Creating Data Understanding Phase Overview...${NC}"

ISSUE_2_TITLE="[CRISP-DM OVERVIEW] 📊 Data Understanding Phase Progress"
ISSUE_2_LABELS="crisp-dm,overview,data-understanding,milestone,week-1,week-2"
ISSUE_2_ASSIGNEE="@me"
ISSUE_2_BODY="# 📊 Data Understanding Phase Overview

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
- \"1000 Kikuyu Proverbs\" collection
- Cultural expert interviews and knowledge
- Academic literature and research papers
- Community documentation and oral traditions

## Related Issues
Links to proverb collection, cultural expert interviews, literature analysis, ethics approval, and data quality assessment issues.

## PROJECT_FIELDS
- Sprint_Week: Week 1-2 (Jun 20-Jul 3)
- Criticality: 🚨 CRITICAL
- OPIT_Deadline: Examining Committee (Jul 13)
- Thesis_Section: Methodology
- CRISP_DM_Phase: 📊 Data Understanding
- Effort_Hours: 43

## Notes
This phase establishes the foundation for ontology construction by ensuring comprehensive understanding of the cultural and linguistic data landscape."

create_issue_with_retry "$ISSUE_2_TITLE" "$ISSUE_2_BODY" "$ISSUE_2_LABELS" "$ISSUE_2_ASSIGNEE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Created Data Understanding Phase Overview${NC}"
else
    echo -e "${RED}❌ Failed to create Data Understanding Phase Overview${NC}"
fi
sleep 2

# Issue 3: Data Preparation Phase
echo -e "${CYAN}📝 Creating Data Preparation Phase Overview...${NC}"

ISSUE_3_TITLE="[CRISP-DM OVERVIEW] 🏗️ Data Preparation Phase Progress"
ISSUE_3_LABELS="crisp-dm,overview,data-preparation,milestone,week-2,week-3,week-4"
ISSUE_3_ASSIGNEE="@me"
ISSUE_3_BODY="# 🏗️ Data Preparation Phase Overview

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

## PROJECT_FIELDS
- Sprint_Week: Week 2-4 (Jun 27-Jul 17)
- Criticality: 🛑 BLOCKER
- OPIT_Deadline: Thesis to Committee (Jul 27)
- Thesis_Section: Implementation
- CRISP_DM_Phase: 🏗️ Data Preparation
- Effort_Hours: 62

## Notes
This is the most intensive CRISP-DM phase, requiring careful balance of technical accuracy and cultural authenticity in knowledge representation."

create_issue_with_retry "$ISSUE_3_TITLE" "$ISSUE_3_BODY" "$ISSUE_3_LABELS" "$ISSUE_3_ASSIGNEE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Created Data Preparation Phase Overview${NC}"
else
    echo -e "${RED}❌ Failed to create Data Preparation Phase Overview${NC}"
fi
sleep 2

# Issue 4: Modeling Phase
echo -e "${CYAN}📝 Creating Modeling Phase Overview...${NC}"

ISSUE_4_TITLE="[CRISP-DM OVERVIEW] 🤖 Modeling Phase Progress"
ISSUE_4_LABELS="crisp-dm,overview,modeling,milestone,week-4,week-5"
ISSUE_4_ASSIGNEE="@me"
ISSUE_4_BODY="# 🤖 Modeling Phase Overview

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

## PROJECT_FIELDS
- Sprint_Week: Week 4-5 (Jul 11-24)
- Criticality: 🚨 CRITICAL
- OPIT_Deadline: Thesis to Committee (Jul 27)
- Thesis_Section: Implementation
- CRISP_DM_Phase: 🤖 Modeling
- Effort_Hours: 50

## Notes
This phase transforms the prepared knowledge representation into a functional translation system, balancing technical performance with cultural authenticity."

create_issue_with_retry "$ISSUE_4_TITLE" "$ISSUE_4_BODY" "$ISSUE_4_LABELS" "$ISSUE_4_ASSIGNEE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Created Modeling Phase Overview${NC}"
else
    echo -e "${RED}❌ Failed to create Modeling Phase Overview${NC}"
fi
sleep 2

# Issue 5: Evaluation Phase
echo -e "${CYAN}📝 Creating Evaluation Phase Overview...${NC}"

ISSUE_5_TITLE="[CRISP-DM OVERVIEW] ⚖️ Evaluation Phase Progress"
ISSUE_5_LABELS="crisp-dm,overview,evaluation,milestone,week-5,week-6,week-7"
ISSUE_5_ASSIGNEE="@me"
ISSUE_5_BODY="# ⚖️ Evaluation Phase Overview

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

## PROJECT_FIELDS
- Sprint_Week: Week 5-7 (Jul 18-Aug 7)
- Criticality: 🛑 BLOCKER
- OPIT_Deadline: Defense Form (Aug 3)
- Thesis_Section: Evaluation
- CRISP_DM_Phase: ⚖️ Evaluation
- Effort_Hours: 90

## Notes
This phase provides the evidence base for thesis conclusions, requiring rigorous methodology to ensure academic validity and cultural authenticity."

create_issue_with_retry "$ISSUE_5_TITLE" "$ISSUE_5_BODY" "$ISSUE_5_LABELS" "$ISSUE_5_ASSIGNEE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Created Evaluation Phase Overview${NC}"
else
    echo -e "${RED}❌ Failed to create Evaluation Phase Overview${NC}"
fi
sleep 2

# Issue 6: Deployment Phase
echo -e "${CYAN}📝 Creating Deployment Phase Overview...${NC}"

ISSUE_6_TITLE="[CRISP-DM OVERVIEW] 🚀 Deployment Phase Progress"
ISSUE_6_LABELS="crisp-dm,overview,deployment,milestone,week-7,week-8,week-9,week-10"
ISSUE_6_ASSIGNEE="@me"
ISSUE_6_BODY="# 🚀 Deployment Phase Overview

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

## PROJECT_FIELDS
- Sprint_Week: Week 7-10 (Jul 25-Aug 30)
- Criticality: 🛑 BLOCKER
- OPIT_Deadline: Post-Defense (Aug 30)
- Thesis_Section: All Sections
- CRISP_DM_Phase: 🚀 Deployment
- Effort_Hours: 95

## Notes
This final phase ensures the research contributes meaningfully to academic knowledge while providing practical guidance for future work in culturally-grounded NLP."

create_issue_with_retry "$ISSUE_6_TITLE" "$ISSUE_6_BODY" "$ISSUE_6_LABELS" "$ISSUE_6_ASSIGNEE"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Created Deployment Phase Overview${NC}"
else
    echo -e "${RED}❌ Failed to create Deployment Phase Overview${NC}"
fi

echo ""
echo -e "${GREEN}🎉 CRISP-DM Overview Issues Creation Complete!${NC}"
echo ""
echo -e "${BLUE}📋 Summary of Created Issues:${NC}"
echo "1. 🎯 Business Understanding Phase Progress"
echo "2. 📊 Data Understanding Phase Progress"
echo "3. 🏗️ Data Preparation Phase Progress"
echo "4. 🤖 Modeling Phase Progress"
echo "5. ⚖️ Evaluation Phase Progress"
echo "6. 🚀 Deployment Phase Progress"
echo ""
echo -e "${YELLOW}📌 Next Steps:${NC}"
echo "1. Review the created issues in your GitHub repository"
echo "2. Add them to your project board if using GitHub Projects"
echo "3. Link related implementation issues to these overview issues"
echo "4. Update project field values using the project-fields.js script if needed"
echo ""
echo -e "${CYAN}📊 Current Issues in Repository:${NC}"
gh issue list --limit 15 --json number,title,labels --jq '.[] | "\(.number): \(.title) [\(.labels | map(.name) | join(","))]"' | head -15

echo ""
echo -e "${GREEN}✨ All CRISP-DM milestone issues have been successfully created!${NC}"
