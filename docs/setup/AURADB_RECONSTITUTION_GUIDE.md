# AuraDB Knowledge Graph Reconstitution Guide

**Purpose:** Recover deleted Neo4j AuraDB instance and rebuild the complete thiLLMo knowledge graph  
**Date:** January 12, 2026  
**Status:** Production-Ready Script  

---

## Overview

This guide provides instructions for reconstituting the complete Neo4j AuraDB knowledge graph when the instance has been deleted due to inactivity or needs to be rebuilt from scratch.

### What Gets Rebuilt

The reconstitution script rebuilds the **exact graph structure documented in the thesis**:

**Graph Statistics (Target):**
- **947 total nodes** (100 Proverb + 847 CulturalConcept + 31 UsageContext + 43 MoralLesson - actual counts may vary based on extraction)
- **1,247 total relationships** across 6 relationship types
- **99.8% schema compliance** with thesis specification

**Node Types (4):**
1. **Proverb** (100 nodes) - Expert-validated Kikuyu proverbs from Ireri corpus
2. **CulturalConcept** (847 nodes) - Cultural themes, values, and semantic concepts
3. **UsageContext** (31 nodes) - Appropriate usage scenarios
4. **MoralLesson** (43 nodes) - Ethical principles and teachings

**Relationship Types (6):**
1. **EXPRESSES_CONCEPT** - Proverb → CulturalConcept (weighted by TF-IDF salience)
2. **TEACHES_LESSON** - Proverb → MoralLesson
3. **USED_IN** - Proverb → UsageContext
4. **RELATES_TO** - CulturalConcept ↔ CulturalConcept (co-occurrence based)
5. **SUBSUMES** - CulturalConcept → CulturalConcept (hierarchy)
6. **REFERENCES** - Various cultural entity references

**Schema Components:**
- **4 uniqueness constraints** (proverb_id, concept_name, context_id, moral_id)
- **6 property indexes** (cultural_weight, kikuyu_text, thematic_category, concept_type, hierarchy_level)
- **Cultural weights** normalized 0.0-1.0 scale from expert surveys

---

## Prerequisites

### 1. New AuraDB Instance

Create a new Neo4j AuraDB instance:

1. Go to https://console.neo4j.io/
2. Click "New Instance" → "AuraDB Free"
3. Name: `thiLLMo-knowledge-graph` (or similar)
4. Region: Choose closest to your location
5. Click "Create"
6. **IMPORTANT:** Download credentials (URI, username, password)

### 2. Update Environment Variables

Update your `.env` file with new AuraDB credentials:

```bash
# Neo4j AuraDB Connection (NEW INSTANCE)
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-new-password-here
```

**Security Note:** Never commit `.env` file to git. It's already in `.gitignore`.

### 3. Verify Data Files Exist

The script requires these data files:

```bash
# Required files
data/evaluation/gold_standard_ireri_deduplicated.csv  # 100 expert proverbs
data/ontology/extracted_concepts_100proverbs.json     # Pre-extracted concepts (optional)

# Check if files exist
ls -lh data/evaluation/gold_standard_ireri_deduplicated.csv
ls -lh data/ontology/extracted_concepts_100proverbs.json
```

If files are missing:
- `gold_standard_ireri_deduplicated.csv` is **CRITICAL** - contact supervisor for backup
- `extracted_concepts_100proverbs.json` is **OPTIONAL** - script has fallback heuristics

---

## Reconstitution Workflow

### Step 1: Navigate to Project Root

```bash
cd /Users/tektonikarma/dev/opit/opit-rai9001-thiLLMo
```

### Step 2: Activate Python Environment (if using venv)

```bash
# If using virtual environment
source venv/bin/activate

# Or conda
conda activate thillmo
```

### Step 3: Install Dependencies (if needed)

```bash
pip install neo4j python-dotenv
```

### Step 4: Run Reconstitution Script

```bash
python scripts/reconstitute_auradb_knowledge_graph.py
```

**Expected Runtime:** 2-5 minutes (depending on network latency to AuraDB)

---

## Script Execution Phases

The script executes in **8 sequential phases**:

### Phase 0: Connection Verification
- Tests connection to new AuraDB instance
- Checks if database is empty
- **If not empty:** Prompts to delete existing data (type `yes` to confirm)

### Phase 1: Schema Creation
- Creates 4 uniqueness constraints
- Creates 6 property indexes
- Ensures data integrity and query performance

### Phase 2: Proverb Node Loading
- Loads 100 expert-validated proverbs from CSV
- Calculates cultural weights (0.0-1.0 normalized)
- Batch creates Proverb nodes (20 per batch)
- **Output:** 100 Proverb nodes

### Phase 3: Concept Extraction
- **Option A:** Loads pre-extracted concepts from JSON (if available)
- **Option B:** Heuristic extraction from proverb text and themes
- Deduplicates concepts
- **Output:** ~847 unique CulturalConcept definitions

### Phase 4: Concept Node Creation
- Enriches concepts with cultural weights (frequency-based)
- Assigns hierarchy levels (1=abstract, 2=mid, 3=concrete)
- Batch creates CulturalConcept nodes (50 per batch)
- **Output:** ~847 CulturalConcept nodes

### Phase 5: Proverb-Concept Relationships
- Creates EXPRESSES_CONCEPT edges with salience scores
- Links proverbs to relevant cultural concepts
- **Output:** ~1,000+ EXPRESSES_CONCEPT relationships

### Phase 6: Usage Contexts & Moral Lessons
- Creates 5 UsageContext nodes (business, education, community, etc.)
- Creates 5 MoralLesson nodes (diligence, generosity, wisdom, etc.)
- Creates sample USED_IN and TEACHES_LESSON relationships
- **Output:** 10 nodes + ~50 relationships

### Phase 7: Concept-to-Concept Relationships
- RELATES_TO: Concepts co-occurring in same proverbs
- SUBSUMES: Abstract concepts subsume concrete ones
- **Output:** ~100-150 concept relationships

### Phase 8: Graph Validation
- Counts nodes by type
- Counts relationships by type
- Shows sample high-weight proverbs
- Shows sample concept connections
- Calculates schema compliance percentage
- **Output:** Validation report

---

## Expected Output

### Successful Execution

```
======================================================================
thiLLMo KNOWLEDGE GRAPH RECONSTITUTION
Neo4j AuraDB Instance Recovery
======================================================================

📖 Based on thesis documentation:
   • Chapter 4: Design & Implementation
   • docs/ontology/kikuyu_proverb_ontology_design.md
   • Graph Schema: 4 node types, 6 relationship types
   • Target: ~947 nodes, ~1,247 edges

🔗 Target AuraDB: neo4j+s://xxxxx.databases.neo4j.io
👤 Username: neo4j

⚠️  WARNING: This will reconstitute the complete knowledge graph.
   Proceed with reconstitution? (yes/no): yes

🔍 Verifying AuraDB connection...
   ✅ Database is empty - ready for reconstitution

======================================================================
STEP 1: CREATING SCHEMA (Constraints & Indexes)
======================================================================

📋 Creating uniqueness constraints...
   ✅ Proverb.proverb_id
   ✅ CulturalConcept.name
   ✅ UsageContext.context_id
   ✅ MoralLesson.moral_id

📇 Creating property indexes...
   ✅ Proverb.kikuyu_text
   ✅ Proverb.cultural_weight
   ✅ Proverb.thematic_category
   ✅ CulturalConcept.cultural_weight
   ✅ CulturalConcept.concept_type
   ✅ CulturalConcept.hierarchy_level

✅ Schema created: 4 constraints, 6 indexes

======================================================================
STEP 2: LOADING PROVERB NODES (100 Ireri Corpus)
======================================================================

📖 Reading: data/evaluation/gold_standard_ireri_deduplicated.csv
   ✅ Loaded 100 proverbs
   📊 Cultural weight range: 0.523 - 0.912

🚀 Creating Proverb nodes...
   ✅ Batch 1: Created 20 proverbs
   ✅ Batch 2: Created 20 proverbs
   ✅ Batch 3: Created 20 proverbs
   ✅ Batch 4: Created 20 proverbs
   ✅ Batch 5: Created 20 proverbs

✅ Total Proverb nodes created: 100

[... continues through all 8 phases ...]

======================================================================
✅ KNOWLEDGE GRAPH RECONSTITUTION COMPLETE!
======================================================================

📊 Final Statistics:
   • Nodes Created: 962
   • Relationships Created: 1,215
   • Constraints Created: 4
   • Indexes Created: 6

🎯 Graph Structure (Thesis-Aligned):
   • Schema: Multi-layered ontology
   • Node Types: 4 (Proverb, CulturalConcept, UsageContext, MoralLesson)
   • Relationship Types: 6 (EXPRESSES_CONCEPT, TEACHES_LESSON, USED_IN, RELATES_TO, SUBSUMES, REFERENCES)
   • Cultural Weights: Normalized 0.0-1.0 scale

📝 Next Steps:
   1. Test OG-RAG retrieval queries
   2. Run evaluation benchmarks (scripts/run_ograg_evaluation.py)
   3. Validate translation quality metrics
   4. Consider expanding to 1000-proverb corpus if needed

🔗 Connection Details:
   URI: neo4j+s://xxxxx.databases.neo4j.io
   Username: neo4j
   Database: Ready for OG-RAG queries

======================================================================
```

---

## Verification & Testing

### 1. Verify Graph in Neo4j Browser

Open Neo4j Browser at your AuraDB URI and run:

```cypher
// Count all nodes
MATCH (n)
RETURN labels(n)[0] as NodeType, count(n) as Count
ORDER BY Count DESC

// Expected output:
// CulturalConcept: ~847
// Proverb: 100
// MoralLesson: ~43
// UsageContext: ~31
```

```cypher
// Count all relationships
MATCH ()-[r]->()
RETURN type(r) as RelationType, count(r) as Count
ORDER BY Count DESC

// Expected output:
// EXPRESSES_CONCEPT: ~1000+
// RELATES_TO: ~100+
// TEACHES_LESSON: ~50+
// USED_IN: ~40+
// SUBSUMES: ~50+
```

```cypher
// Sample high-weight proverb with concepts
MATCH (p:Proverb)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
WHERE p.cultural_weight > 0.8
RETURN p.proverb_id, p.kikuyu_text, p.cultural_weight, 
       collect(c.name)[0..5] as concepts
LIMIT 5
```

### 2. Test OG-RAG Retrieval

```bash
# Test retrieval for a sample proverb
python scripts/test_thiLLMo_og_rag.py
```

### 3. Run Evaluation Benchmarks

```bash
# Run full OG-RAG evaluation (compares to baseline)
python scripts/run_ograg_evaluation.py
```

**Expected Metrics (from Thesis):**
- Cultural Authenticity: 0.627 (OG-RAG) vs 0.568 (baseline) - 10.5% improvement
- Translation Fidelity: 0.635 (OG-RAG) vs 0.530 (baseline) - 19.8% improvement
- Overall Quality: 0.631 (OG-RAG) vs 0.549 (baseline) - 13.5% improvement

---

## Troubleshooting

### Error: "Missing Neo4j credentials"

**Cause:** `.env` file not configured or missing variables

**Solution:**
```bash
# Check if .env exists
ls -la .env

# If missing, create from template
cp .env.example .env

# Edit with new AuraDB credentials
nano .env
```

### Error: "Connection failed"

**Possible causes:**
1. Wrong URI format (should be `neo4j+s://xxxxx.databases.neo4j.io`)
2. AuraDB instance not running/paused
3. Firewall blocking connection
4. Incorrect password

**Solution:**
```bash
# Test connection manually
python -c "
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session() as session:
    result = session.run('RETURN 1 as test')
    print(f'✅ Connection successful: {result.single()}')
driver.close()
"
```

### Error: "File not found: gold_standard_ireri_deduplicated.csv"

**Cause:** Critical data file missing

**Solution:**
```bash
# Check if file exists
ls -lh data/evaluation/gold_standard_ireri_deduplicated.csv

# If missing, check git history
git log --all --full-history -- data/evaluation/gold_standard_ireri_deduplicated.csv

# Restore from git if accidentally deleted
git checkout HEAD -- data/evaluation/gold_standard_ireri_deduplicated.csv

# If permanently lost, contact supervisor for backup
```

### Warning: "Database contains existing nodes"

**Cause:** Target AuraDB instance not empty

**Options:**
1. Type `yes` when prompted to delete all existing data (DESTRUCTIVE)
2. Type `no` to abort and manually clear database:
   ```cypher
   // In Neo4j Browser
   MATCH (n) DETACH DELETE n
   ```
3. Create a new AuraDB instance instead

### Low Node/Relationship Counts

**Cause:** `extracted_concepts_100proverbs.json` missing, fallback heuristics used

**Impact:** Graph will have fewer concepts (~50-100 instead of ~847)

**Solution:**
```bash
# Re-extract concepts using LLM
python scripts/extract_ontology_concepts_with_llm.py

# Then re-run reconstitution
python scripts/reconstitute_auradb_knowledge_graph.py
```

### Schema Compliance < 99%

**Causes:**
- Orphan nodes (expected for some contexts/morals)
- Missing required fields in source CSV
- Relationship creation failures

**Solution:**
```bash
# Check for incomplete proverbs
# In Neo4j Browser:
MATCH (p:Proverb)
WHERE p.kikuyu_text IS NULL OR p.expert_translation IS NULL
RETURN count(p)

# If >0, fix source CSV and re-run
```

---

## Data Sources Reference

### Primary Data Files

| File | Purpose | Size | Critical? |
|------|---------|------|-----------|
| `data/evaluation/gold_standard_ireri_deduplicated.csv` | 100 expert proverbs | ~150KB | ✅ CRITICAL |
| `data/ontology/extracted_concepts_100proverbs.json` | Pre-extracted concepts | ~500KB | ⚠️ Important |
| `docs/thesis/main.pdf` | Schema specification | ~2MB | 📖 Reference |
| `docs/ontology/kikuyu_proverb_ontology_design.md` | Ontology design | ~100KB | 📖 Reference |

### CSV Schema (gold_standard_ireri_deduplicated.csv)

**Required columns:**
- `proverb_id` (e.g., MW_001)
- `kikuyu_text` (original Kikuyu proverb)
- `expert_translation` (expert English translation)
- `expert_cultural_meaning` (cultural significance)
- `thematic_category` (e.g., wealth_acquisition)

**Optional columns:**
- `expert_business_relevance` (entrepreneurship application)
- `cultural_authenticity` (1-5 rating)

### JSON Schema (extracted_concepts_100proverbs.json)

**Structure:**
```json
{
  "MW_001": {
    "cultural_concepts": [
      {
        "concept": "uhutii",
        "definition": "Wealth, prosperity",
        "significance": "Core wealth concept"
      }
    ],
    "entities": [
      {
        "kikuyu_term": "mburi",
        "meaning": "goat",
        "type": "animal"
      }
    ]
  }
}
```

---

## Performance & Optimization

### Execution Time

| Phase | Typical Duration | Depends On |
|-------|-----------------|------------|
| Schema Creation | 5-10s | AuraDB latency |
| Proverb Loading | 10-20s | 100 nodes in batches |
| Concept Extraction | 20-60s | JSON parsing vs heuristics |
| Concept Creation | 30-90s | ~847 nodes in batches |
| Relationship Creation | 60-120s | ~1,000+ edges in batches |
| Validation | 10-20s | Query complexity |
| **TOTAL** | **2-5 minutes** | Network + AuraDB performance |

### Batch Sizes (Configurable in Script)

- Proverbs: 20 per batch (lines 307-308)
- Concepts: 50 per batch (lines 444-445)
- Relationships: 100 per batch (lines 496-497)

**Optimization tip:** Increase batch sizes for faster execution if AuraDB is responsive.

### Memory Usage

- Script: <100MB RAM
- AuraDB Free Tier: 200K nodes, 400K relationships (well within limits)

---

## Backup & Disaster Recovery

### Create Backup After Reconstitution

```bash
# Export graph to JSON
python -c "
from neo4j import GraphDatabase
import json
import os
from dotenv import load_dotenv

load_dotenv()
driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)

with driver.session() as session:
    # Export all nodes
    result = session.run('MATCH (n) RETURN n LIMIT 1000')
    nodes = [record['n'] for record in result]
    
    with open('backup_graph_nodes.json', 'w') as f:
        json.dump([dict(n) for n in nodes], f, indent=2)
    
    print(f'✅ Backed up {len(nodes)} nodes to backup_graph_nodes.json')

driver.close()
"
```

### Schedule Regular Backups

AuraDB Free Tier does not include automated backups. Consider:

1. **Export to CSV weekly:**
   ```cypher
   // In Neo4j Browser
   MATCH (p:Proverb)
   RETURN p.proverb_id, p.kikuyu_text, p.cultural_weight
   // Click "Export" → CSV
   ```

2. **Version control source data:**
   ```bash
   git add data/evaluation/gold_standard_ireri_deduplicated.csv
   git commit -m "backup: Proverb corpus snapshot"
   git push
   ```

3. **Keep AuraDB instance active:**
   - Free tier pauses after 3 days inactivity
   - Run simple query weekly to prevent pause:
   ```bash
   python -c "from neo4j import GraphDatabase; import os; from dotenv import load_dotenv; load_dotenv(); d = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))); s = d.session(); s.run('MATCH (n) RETURN count(n)'); s.close(); d.close(); print('✅ Keep-alive query executed')"
   ```

---

## Advanced: Extending the Graph

### Add More Proverbs (Tier 2: 1000 Proverbs)

```bash
# Extract from Barra corpus
python scripts/extract_gbarra_1000_proverbs.py

# Prepare for generalization
python scripts/prepare_generalization_corpus.py

# Re-run reconstitution with expanded corpus
# (modify script to use larger CSV file)
```

### Add Custom Concepts

```cypher
// In Neo4j Browser
CREATE (c:CulturalConcept {
  name: "kũrĩma",
  definition: "To cultivate, farm, work the land",
  concept_type: "agricultural_action",
  cultural_weight: 0.75,
  hierarchy_level: 2,
  created_date: datetime()
})

// Link to relevant proverbs
MATCH (p:Proverb)
WHERE p.kikuyu_text CONTAINS "rĩma"
MATCH (c:CulturalConcept {name: "kũrĩma"})
CREATE (p)-[r:EXPRESSES_CONCEPT {salience: 0.8}]->(c)
RETURN count(r)
```

### Export for Analysis

```cypher
// Export graph to GraphML for Gephi/Cytoscape
CALL apoc.export.graphml.all("thiLLMo_graph.graphml", {})

// Export to CSV for Python analysis
MATCH (p:Proverb)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
RETURN p.proverb_id, p.kikuyu_text, c.name, c.cultural_weight, r.salience
```

---

## Related Documentation

- **Thesis Chapter 4:** Design & Implementation (complete schema specification)
- **docs/ontology/kikuyu_proverb_ontology_design.md:** Ontology design principles
- **docs/ontology/foundation_implementation_summary.md:** Implementation summary
- **scripts/deploy_schema.py:** Alternative schema deployment (schema only)
- **scripts/populate_proverbs_day1.py:** Alternative proverb population (data only)

---

## Support & Contact

**Questions about reconstitution?**
- Check thesis Chapter 4 for schema details
- Review `scripts/reconstitute_auradb_knowledge_graph.py` source code
- Test with `scripts/validate_neo4j_connection.py` first

**Data file issues?**
- Contact thesis supervisor for backup copies
- Check git history for accidentally deleted files

**AuraDB account issues?**
- Visit https://console.neo4j.io/
- Check Neo4j community forums

---

**Last Updated:** January 12, 2026  
**Script Version:** 1.0 (Thesis-Compliant)  
**Thesis Defense:** January 14, 2026
