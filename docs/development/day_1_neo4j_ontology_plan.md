# Day 1: Neo4j & Ontology Population Plan

**Date:** October 28, 2025  
**Status:** PLANNING  
**Timeline:** 8 hours (1 day)  
**Dependencies:** Day 0 COMPLETE ✅

---

## 🔍 Configuration Health Check

### Existing Neo4j Configuration Status

#### ✅ Configuration Files Present
1. **`config/neo4j_config.py`** - Comprehensive configuration management
   - Environment-based configs (dev, prod, test)
   - Docker Compose integration
   - Connection validation
   - `.env` file template generation

2. **`src/ontology/enhanced_neo4j_schema.py`** - Schema deployment script
   - 760 lines of comprehensive schema
   - Constraints, indexes, full-text search
   - Multiple node types (Proverb, CulturalConcept, Metaphor, etc.)
   - Relationship properties with cultural weights

3. **`scripts/ontology_builder.py`** - Ontology population script
   - 1103 lines of domain knowledge
   - Cultural concept patterns
   - Business domain mappings
   - Comprehensive proverb loading

#### ✅ Environment Configuration (.env)
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=ograg2025
NEO4J_DATABASE=kikuyu-kg
```

#### ✅ Docker Compose Configuration
```yaml
neo4j:
  image: neo4j:5.15-community
  container_name: kikuyu-og-rag-neo4j
  ports: ["7474:7474", "7687:7687"]
  environment:
    - NEO4J_AUTH=neo4j/ograg2025
    - NEO4J_PLUGINS=["apoc", "graph-data-science"]
    - NEO4J_dbms_default__database=kikuyu-kg
```

#### ⚠️ Configuration Inconsistency Detected

**ISSUE:** Password mismatch between config files
- **config/neo4j_config.py default:** `kikuyu_proverbs_2024`
- **.env file actual:** `ograg2025`
- **docker-compose.yml:** `ograg2025`

**RESOLUTION:** Use `.env` values (already configured) - config file defaults are just fallbacks

#### ❌ Docker Not Available
```bash
docker ps -a | grep neo4j
# Result: zsh: command not found: docker
```

**IMPLICATION:** Need to use local Neo4j installation or install Docker

---

## 🎯 Day 1 Objectives

### Primary Goals
1. ✅ Verify/establish Neo4j connection
2. ✅ Deploy enhanced schema (if not already deployed)
3. ✅ Load 100 Ireri proverbs with full metadata
4. ✅ Extract and load 20 priority concepts from gap analysis
5. ✅ Create initial concept-proverb relationships
6. ✅ Validate graph structure and data quality

### Success Criteria
- Neo4j accessible and responsive
- 100 proverb nodes created with cultural weights
- 20 concept nodes created
- Basic relationships established
- Query performance verified
- Ready for Day 2 (OG-RAG implementation)

---

## 📊 Data Inventory

### Available Corpora
1. **Tier 1 (Ireri - In-Domain):** ✅ 100 proverbs
   - Source: `data/evaluation/gold_standard_ireri_deduplicated.csv`
   - Domain: Wealth/prosperity
   - Quality: Expert-validated
   - Columns: kikuyu_text, expert_translation, expert_cultural_meaning, expert_business_relevance, thematic_category, cultural_authenticity, etc.

2. **Tier 2 (Gbarra - Generalization):** ✅ 75 proverbs
   - Source: `data/evaluation/tier2_diverse_sample.csv`
   - Themes: 9 diverse (wisdom, family, social, nature, conflict, work, morality, life, general)
   - Quality: Validated extraction
   - Purpose: Out-of-domain generalization testing

3. **Baseline Gap Analysis:** ✅ Available
   - Source: `data/analysis/baseline_gap_analysis.json`
   - Size: 173KB
   - Contains: Missing concepts, failed metaphors, cultural gaps

### Priority Data for Day 1
**Focus:** Load only Tier 1 (100 Ireri proverbs) initially
- Tier 2 can be loaded later if needed for evaluation
- Priority concepts from gap analysis (top 20)
- Core metaphors (top 30-40)

---

## 🔧 Technical Approach

### Phase 1: Neo4j Setup & Validation (2 hours)

#### Option A: Local Neo4j Installation
```bash
# Check if Neo4j is installed locally
which neo4j
neo4j --version

# If installed, start service
neo4j start
# OR (if using Homebrew)
brew services start neo4j

# Access web interface
open http://localhost:7474
```

#### Option B: Install Neo4j (if not present)
```bash
# macOS with Homebrew
brew install neo4j

# Configure
neo4j-admin dbms set-initial-password ograg2025

# Start
neo4j start
```

#### Option C: Docker Setup (if Docker available)
```bash
# Check Docker status
docker --version

# If available, use docker-compose
cd /Users/ndethi/dev/opit/opit-rai9001
docker-compose up -d neo4j

# Verify
docker ps | grep neo4j
```

#### Validation Script
```python
# scripts/validate_neo4j_connection.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.neo4j_config import Neo4jConfig
from neo4j import GraphDatabase

def validate_connection():
    """Validate Neo4j connection using .env configuration"""
    
    config = Neo4jConfig.get_config('development')
    
    print("🔍 Neo4j Configuration:")
    print(f"   URI: {config['uri']}")
    print(f"   Username: {config['username']}")
    print(f"   Database: {config['database']}")
    
    try:
        driver = GraphDatabase.driver(
            config['uri'],
            auth=(config['username'], config['password'])
        )
        
        with driver.session(database=config['database']) as session:
            result = session.run("RETURN 1 as test")
            value = result.single()['test']
            
            if value == 1:
                print("✅ Neo4j connection successful!")
                
                # Get graph stats
                stats = session.run("""
                MATCH (n)
                RETURN count(n) as node_count,
                       count(distinct labels(n)) as label_count
                """).single()
                
                print(f"   Nodes: {stats['node_count']}")
                print(f"   Labels: {stats['label_count']}")
                
                return True
        
        driver.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    validate_connection()
```

### Phase 2: Schema Deployment (1 hour)

#### Deploy Enhanced Schema
```python
# Use existing script with validation
import sys
sys.path.append('/Users/ndethi/dev/opit/opit-rai9001')

from src.ontology.enhanced_neo4j_schema import EnhancedOntologySchema
from config.neo4j_config import get_development_config

def deploy_schema():
    """Deploy enhanced Neo4j schema"""
    
    config = get_development_config()
    
    schema = EnhancedOntologySchema(
        uri=config['uri'],
        user=config['username'],
        password=config['password']
    )
    
    print("🚀 Deploying enhanced schema...")
    schema.create_complete_schema()
    schema.close()
    
    print("✅ Schema deployment complete!")

if __name__ == "__main__":
    deploy_schema()
```

#### Verify Schema
```cypher
// Check constraints
SHOW CONSTRAINTS;

// Check indexes
SHOW INDEXES;

// Should see:
// - proverb_id UNIQUE constraint
// - concept_name UNIQUE constraint
// - entity_id UNIQUE constraint
// - Multiple property indexes
// - Full-text search indexes
```

### Phase 3: Extract Priority Concepts (1 hour)

#### Script: Extract Top Concepts from Gap Analysis
```python
# scripts/extract_priority_concepts.py
import json
import pandas as pd
from pathlib import Path

def extract_priority_concepts(
    gap_analysis_path='data/analysis/baseline_gap_analysis.json',
    output_path='data/processed/priority_concepts.csv',
    top_n=20
):
    """Extract priority concepts from baseline gap analysis"""
    
    print(f"📖 Loading gap analysis from: {gap_analysis_path}")
    
    with open(gap_analysis_path, 'r') as f:
        gap_data = json.load(f)
    
    # Extract concepts with frequency/importance
    concepts_list = []
    
    # Check different possible structures in the JSON
    if 'missing_concepts' in gap_data:
        concepts = gap_data['missing_concepts']
        for concept in concepts[:top_n]:
            if isinstance(concept, dict):
                concepts_list.append(concept)
            else:
                concepts_list.append({
                    'concept_name': concept,
                    'domain': 'wealth_prosperity',
                    'priority': 'high',
                    'source': 'gap_analysis'
                })
    
    if 'cultural_gaps' in gap_data:
        cultural_gaps = gap_data['cultural_gaps']
        # Process cultural gaps
    
    # Create DataFrame
    df = pd.DataFrame(concepts_list)
    
    # Add importance scores if not present
    if 'importance_score' not in df.columns:
        df['importance_score'] = range(10, 10 - len(df), -1)
    
    # Save
    df.to_csv(output_path, index=False)
    
    print(f"✅ Extracted {len(df)} priority concepts")
    print(f"💾 Saved to: {output_path}")
    print(f"\nTop 5 concepts:")
    print(df.head()[['concept_name', 'importance_score']].to_string(index=False))
    
    return df

if __name__ == "__main__":
    extract_priority_concepts()
```

### Phase 4: Load Proverbs with Cultural Weights (2 hours)

#### Script: Populate Proverb Nodes
```python
# scripts/populate_proverbs_day1.py
import sys
import pandas as pd
from pathlib import Path
sys.path.append('/Users/ndethi/dev/opit/opit-rai9001')

from neo4j import GraphDatabase
from config.neo4j_config import get_development_config
from datetime import datetime

def calculate_cultural_weight(row):
    """Calculate cultural weight based on available metadata"""
    
    weight = 5.0  # Base weight
    
    # Boost for expert validation
    if row.get('validation_status') == 'expert_validated':
        weight += 2.0
    
    # Boost for cultural meaning
    if pd.notna(row.get('expert_cultural_meaning')) and len(str(row['expert_cultural_meaning'])) > 50:
        weight += 1.5
    
    # Boost for business relevance
    if pd.notna(row.get('expert_business_relevance')) and len(str(row['expert_business_relevance'])) > 50:
        weight += 1.0
    
    # Boost for cultural authenticity
    auth = row.get('cultural_authenticity')
    if auth == 'high':
        weight += 1.5
    elif auth == 'very_high':
        weight += 2.0
    
    return min(weight, 10.0)  # Cap at 10.0

def populate_proverbs(
    corpus_path='data/evaluation/gold_standard_ireri_deduplicated.csv',
    batch_size=10
):
    """Populate Neo4j with Tier 1 proverbs"""
    
    config = get_development_config()
    driver = GraphDatabase.driver(
        config['uri'],
        auth=(config['username'], config['password'])
    )
    
    # Load corpus
    print(f"📖 Loading Tier 1 corpus from: {corpus_path}")
    df = pd.read_csv(corpus_path)
    print(f"   Loaded: {len(df)} proverbs")
    
    # Create proverbs
    created_count = 0
    
    with driver.session(database=config['database']) as session:
        for idx, row in df.iterrows():
            
            # Calculate cultural weight
            cultural_weight = calculate_cultural_weight(row)
            
            # Create proverb node
            query = """
            CREATE (p:Proverb {
                proverb_id: $proverb_id,
                kikuyu_text: $kikuyu_text,
                expert_translation: $expert_translation,
                expert_cultural_meaning: $cultural_meaning,
                expert_business_relevance: $business_relevance,
                thematic_category: $thematic_category,
                cultural_authenticity: $cultural_authenticity,
                cultural_weight: $cultural_weight,
                domain: 'wealth_prosperity',
                source: $source,
                source_reference: $source_reference,
                validation_status: $validation_status,
                extraction_date: $extraction_date,
                load_timestamp: datetime()
            })
            RETURN p.proverb_id as id
            """
            
            result = session.run(query,
                proverb_id=row['proverb_id'],
                kikuyu_text=row['kikuyu_text'],
                expert_translation=row['expert_translation'],
                cultural_meaning=str(row.get('expert_cultural_meaning', '')),
                business_relevance=str(row.get('expert_business_relevance', '')),
                thematic_category=row.get('thematic_category', 'general'),
                cultural_authenticity=row.get('cultural_authenticity', 'medium'),
                cultural_weight=cultural_weight,
                source=row.get('source', 'ireri_2014'),
                source_reference=row.get('source_reference', ''),
                validation_status=row.get('validation_status', 'expert_validated'),
                extraction_date=row.get('extraction_date', str(datetime.now().date()))
            )
            
            created_count += 1
            
            if created_count % batch_size == 0:
                print(f"   Created {created_count}/{len(df)} proverbs...")
    
    driver.close()
    
    print(f"✅ Successfully created {created_count} proverb nodes!")
    print(f"   Average cultural weight: {df.apply(calculate_cultural_weight, axis=1).mean():.2f}")
    
    return created_count

if __name__ == "__main__":
    populate_proverbs()
```

### Phase 5: Create Concept Nodes (1 hour)

```python
# scripts/create_concept_nodes.py
import pandas as pd
import sys
sys.path.append('/Users/ndethi/dev/opit/opit-rai9001')

from neo4j import GraphDatabase
from config.neo4j_config import get_development_config

def create_concept_nodes(
    concepts_path='data/processed/priority_concepts.csv'
):
    """Create cultural concept nodes"""
    
    config = get_development_config()
    driver = GraphDatabase.driver(
        config['uri'],
        auth=(config['username'], config['password'])
    )
    
    # Load concepts
    print(f"📖 Loading priority concepts from: {concepts_path}")
    df = pd.read_csv(concepts_path)
    print(f"   Loaded: {len(df)} concepts")
    
    created_count = 0
    
    with driver.session(database=config['database']) as session:
        for idx, row in df.iterrows():
            query = """
            MERGE (c:CulturalConcept {name: $concept_name})
            SET c.domain = $domain,
                c.importance_score = $importance_score,
                c.priority = $priority,
                c.source = $source,
                c.created_timestamp = datetime()
            RETURN c.name as name
            """
            
            session.run(query,
                concept_name=row['concept_name'],
                domain=row.get('domain', 'wealth_prosperity'),
                importance_score=float(row.get('importance_score', 5.0)),
                priority=row.get('priority', 'high'),
                source=row.get('source', 'gap_analysis')
            )
            
            created_count += 1
    
    driver.close()
    
    print(f"✅ Successfully created {created_count} concept nodes!")
    
    return created_count

if __name__ == "__main__":
    create_concept_nodes()
```

### Phase 6: Link Proverbs to Concepts (1 hour)

```python
# scripts/link_proverbs_to_concepts.py
import sys
sys.path.append('/Users/ndethi/dev/opit/opit-rai9001')

from neo4j import GraphDatabase
from config.neo4j_config import get_development_config
import re

def create_concept_relationships():
    """Create relationships between proverbs and concepts"""
    
    config = get_development_config()
    driver = GraphDatabase.driver(
        config['uri'],
        auth=(config['username'], config['password'])
    )
    
    # Concept keyword mappings
    concept_keywords = {
        'wealth': ['utonga', 'money', 'riches', 'property', 'mbeca', 'indo'],
        'poverty': ['thiini', 'poor', 'poverty', 'lack', 'need'],
        'work': ['wira', 'work', 'labor', 'effort', 'kũruta'],
        'wisdom': ['ũũgĩ', 'wisdom', 'knowledge', 'wise', 'kũmenya'],
        'patience': ['kirĩrĩria', 'patience', 'wait', 'eterera'],
        'planning': ['thugunda', 'plan', 'prepare', 'mũbango'],
        'cooperation': ['ũrũmwe', 'together', 'unity', 'cooperation', 'taarana'],
        'leadership': ['tongoria', 'leader', 'chief', 'mũnene'],
        'perseverance': ['kirĩrĩria', 'persist', 'endure', 'ũũrĩria'],
        'community': ['andũ', 'people', 'community', 'mũndũ', 'ũrata'],
        # Add more mappings...
    }
    
    relationship_count = 0
    
    with driver.session(database=config['database']) as session:
        
        for concept, keywords in concept_keywords.items():
            
            # Create relationships based on text matching
            query = """
            MATCH (p:Proverb)
            MATCH (c:CulturalConcept {name: $concept})
            WHERE any(keyword IN $keywords WHERE 
                toLower(p.kikuyu_text) CONTAINS toLower(keyword) OR
                toLower(p.expert_translation) CONTAINS toLower(keyword) OR
                toLower(p.expert_cultural_meaning) CONTAINS toLower(keyword)
            )
            MERGE (p)-[r:EXPRESSES_CONCEPT]->(c)
            SET r.strength = 0.8,
                r.extraction_method = 'keyword_matching',
                r.created_timestamp = datetime()
            RETURN count(r) as created
            """
            
            result = session.run(query,
                concept=concept,
                keywords=keywords
            ).single()
            
            if result:
                count = result['created']
                relationship_count += count
                print(f"   Created {count} links for concept: {concept}")
    
    driver.close()
    
    print(f"\n✅ Successfully created {relationship_count} proverb-concept relationships!")
    
    return relationship_count

if __name__ == "__main__":
    create_concept_relationships()
```

---

## 📋 Execution Sequence

### Step 1: Neo4j Connection Validation
```bash
cd /Users/ndethi/dev/opit/opit-rai9001

# Create validation script
python3 scripts/validate_neo4j_connection.py
```

**Expected Output:**
```
🔍 Neo4j Configuration:
   URI: bolt://localhost:7687
   Username: neo4j
   Database: kikuyu-kg
✅ Neo4j connection successful!
   Nodes: 0 (or existing count)
   Labels: 0 (or existing count)
```

### Step 2: Schema Deployment
```bash
# Run schema deployment
python3 -c "
import sys
sys.path.append('/Users/ndethi/dev/opit/opit-rai9001')
from src.ontology.enhanced_neo4j_schema import EnhancedOntologySchema
from config.neo4j_config import get_development_config

config = get_development_config()
schema = EnhancedOntologySchema(
    uri=config['uri'],
    user=config['username'],
    password=config['password']
)
schema.create_complete_schema()
schema.close()
"
```

### Step 3: Extract Priority Concepts
```bash
python3 scripts/extract_priority_concepts.py
```

### Step 4: Populate Proverbs
```bash
python3 scripts/populate_proverbs_day1.py
```

### Step 5: Create Concepts
```bash
python3 scripts/create_concept_nodes.py
```

### Step 6: Link Proverbs to Concepts
```bash
python3 scripts/link_proverbs_to_concepts.py
```

### Step 7: Validation & Statistics
```bash
python3 -c "
import sys
sys.path.append('/Users/ndethi/dev/opit/opit-rai9001')
from neo4j import GraphDatabase
from config.neo4j_config import get_development_config

config = get_development_config()
driver = GraphDatabase.driver(config['uri'], auth=(config['username'], config['password']))

with driver.session(database=config['database']) as session:
    stats = session.run('''
    MATCH (p:Proverb)
    OPTIONAL MATCH (p)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
    RETURN 
        count(DISTINCT p) as proverbs,
        count(DISTINCT c) as concepts,
        count(r) as relationships,
        avg(p.cultural_weight) as avg_weight
    ''').single()
    
    print('📊 Graph Statistics:')
    print(f'   Proverbs: {stats[\"proverbs\"]}')
    print(f'   Concepts: {stats[\"concepts\"]}')
    print(f'   Relationships: {stats[\"relationships\"]}')
    print(f'   Avg Cultural Weight: {stats[\"avg_weight\"]:.2f}')

driver.close()
"
```

---

## ✅ Success Criteria

### Minimum Viable Ontology (MVo) for Day 1
- [ ] Neo4j accessible and responsive
- [ ] Enhanced schema deployed (constraints + indexes)
- [ ] 100 proverb nodes created (Tier 1)
- [ ] 20 concept nodes created (priority concepts)
- [ ] 50-100 proverb-concept relationships
- [ ] Average cultural weight: 6.0-8.0
- [ ] Query response time < 100ms
- [ ] Zero errors in data loading

### Quality Checks
```cypher
// Check proverb completeness
MATCH (p:Proverb)
WHERE p.kikuyu_text IS NULL OR p.expert_translation IS NULL
RETURN count(p) as incomplete_proverbs;
// Expected: 0

// Check concept coverage
MATCH (c:CulturalConcept)<-[:EXPRESSES_CONCEPT]-(p:Proverb)
RETURN c.name, count(p) as proverb_count
ORDER BY proverb_count DESC
LIMIT 10;
// Expected: Multiple proverbs per concept

// Check cultural weights distribution
MATCH (p:Proverb)
RETURN min(p.cultural_weight) as min_weight,
       max(p.cultural_weight) as max_weight,
       avg(p.cultural_weight) as avg_weight,
       stdev(p.cultural_weight) as std_weight;
// Expected: Reasonable distribution (5-10 range)
```

---

## 🚧 Known Challenges & Mitigations

### Challenge 1: Docker Not Available
**Impact:** Cannot use docker-compose setup  
**Mitigation:** Use local Neo4j installation  
**Action:** Install via Homebrew if needed  

### Challenge 2: Password Configuration Mismatch
**Impact:** Confusion about correct credentials  
**Mitigation:** Use .env values (`ograg2025`)  
**Action:** Update scripts to read from .env consistently  

### Challenge 3: Gap Analysis Structure Unknown
**Impact:** May not extract concepts correctly  
**Mitigation:** Inspect JSON structure first  
**Action:** Create flexible extraction that handles various formats  

### Challenge 4: Concept-Proverb Matching Accuracy
**Impact:** May miss relevant relationships  
**Mitigation:** Start with keyword matching, can enhance later  
**Action:** Use comprehensive keyword lists, plan for semantic matching in future  

---

## 📝 Deliverables Summary

### Code Files to Create
1. `scripts/validate_neo4j_connection.py` - Connection validation
2. `scripts/extract_priority_concepts.py` - Concept extraction from gap analysis
3. `scripts/populate_proverbs_day1.py` - Proverb node creation
4. `scripts/create_concept_nodes.py` - Concept node creation
5. `scripts/link_proverbs_to_concepts.py` - Relationship creation

### Data Files Created
1. `data/processed/priority_concepts.csv` - Top 20 concepts
2. Neo4j database with:
   - 100 Proverb nodes
   - 20 CulturalConcept nodes
   - 50-100 EXPRESSES_CONCEPT relationships

### Documentation
1. This plan document
2. Validation report (generated at end of day)
3. Updated todo list with Day 1 COMPLETE

---

## 🔄 Next Steps (Day 2 Preview)

### Day 2: OG-RAG System Implementation
**Prerequisites from Day 1:**
- ✅ Neo4j ontology with proverbs and concepts
- ✅ Queryable graph structure
- ✅ Cultural weights assigned

**Day 2 Activities:**
1. Build concept extraction pipeline
2. Implement graph traversal for context retrieval
3. Create cultural context injection mechanism
4. Integrate with translation generation
5. Test with 10-proverb pilot

**Connection to Day 1:**
Day 1 ontology becomes the knowledge base that Day 2 RAG system queries to enhance translations with cultural context.

---

*Document created: October 28, 2025*  
*Status: READY FOR EXECUTION*  
*Timeline: ON SCHEDULE*
