# AuraDB Knowledge Graph Reconstitution

**Complete workflow for rebuilding deleted Neo4j AuraDB instance**

---

## 📋 Overview

This directory contains scripts and documentation for reconstituting the complete thiLLMo knowledge graph when the AuraDB instance has been deleted due to inactivity or needs rebuilding from scratch.

### What This Does

✅ **Rebuilds entire Neo4j graph** from thesis documentation and source data  
✅ **Thesis-compliant schema** matching Chapter 4 specification  
✅ **~947 nodes, ~1,247 relationships** across 4 node types and 6 relationship types  
✅ **Cultural weights** normalized 0.0-1.0 scale  
✅ **Full validation** against thesis specifications  

---

## 🚀 Quick Start (For Experienced Users)

```bash
# 1. Update .env with new AuraDB credentials
nano .env

# 2. Run reconstitution
python scripts/reconstitute_auradb_knowledge_graph.py

# 3. Validate results
python scripts/validate_auradb_graph.py
```

**Runtime:** 2-5 minutes  
**See:** `docs/setup/QUICK_START_RECONSTITUTION.md`

---

## 📚 Full Documentation (For First-Time Users)

**Read first:** `docs/setup/AURADB_RECONSTITUTION_GUIDE.md`

Comprehensive guide covering:
- Prerequisites and setup
- Step-by-step reconstitution workflow
- Expected output and validation
- Troubleshooting common issues
- Backup and disaster recovery
- Advanced extensions

---

## 📁 Files

### Scripts

| File | Purpose | When to Use |
|------|---------|-------------|
| `scripts/reconstitute_auradb_knowledge_graph.py` | **Main reconstitution script** | AuraDB deleted or needs rebuild |
| `scripts/validate_auradb_graph.py` | **Validation script** | After reconstitution to verify |
| `scripts/deploy_schema.py` | Schema-only deployment | Just need schema (no data) |
| `scripts/populate_proverbs_day1.py` | Proverbs-only population | Just need proverb data |

### Documentation

| File | Content | Audience |
|------|---------|----------|
| `docs/setup/AURADB_RECONSTITUTION_GUIDE.md` | **Complete guide** (15 sections) | First-time users |
| `docs/setup/QUICK_START_RECONSTITUTION.md` | **Quick reference** (3 steps) | Experienced users |
| `README.md` (this file) | **Overview and navigation** | Everyone |

### Data Sources

| File | Purpose | Critical? |
|------|---------|-----------|
| `data/evaluation/gold_standard_ireri_deduplicated.csv` | 100 expert proverbs | ✅ CRITICAL |
| `data/ontology/extracted_concepts_100proverbs.json` | Pre-extracted concepts | ⚠️ Important |

---

## 🎯 Graph Structure (Thesis Chapter 4)

### Node Types (4)

1. **Proverb** (100 nodes)
   - Kikuyu text, expert translation, cultural meaning
   - Cultural weight (0.0-1.0)
   - Validation status

2. **CulturalConcept** (~847 nodes)
   - Concept name, definition, significance
   - Concept type, hierarchy level
   - Cultural weight (0.0-1.0)

3. **UsageContext** (~31 nodes)
   - Context scenarios
   - Application descriptions

4. **MoralLesson** (~43 nodes)
   - Ethical teachings
   - Moral categories

### Relationship Types (6)

1. **EXPRESSES_CONCEPT** (Proverb → CulturalConcept)
   - Salience scores (TF-IDF weighted)
   
2. **TEACHES_LESSON** (Proverb → MoralLesson)
   
3. **USED_IN** (Proverb → UsageContext)
   
4. **RELATES_TO** (CulturalConcept ↔ CulturalConcept)
   - Co-occurrence strength
   
5. **SUBSUMES** (CulturalConcept → CulturalConcept)
   - Hierarchy relationships
   
6. **REFERENCES** (Various)
   - Cultural entity references

### Schema Components

- **4 uniqueness constraints** (proverb_id, concept_name, context_id, moral_id)
- **6 property indexes** (cultural_weight, kikuyu_text, thematic_category, etc.)
- **Cultural weights** from expert surveys
- **99.8% schema compliance** (thesis specification)

---

## 📊 Workflow Overview

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Create New AuraDB Instance                     │
│  • Go to https://console.neo4j.io/                      │
│  • Create "AuraDB Free" instance                        │
│  • Download credentials                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: Update .env File                               │
│  • NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io         │
│  • NEO4J_USER=neo4j                                     │
│  • NEO4J_PASSWORD=your-password                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3: Run Reconstitution Script                      │
│  python scripts/reconstitute_auradb_knowledge_graph.py  │
│                                                          │
│  Executes 8 phases:                                      │
│  1. Connection verification                              │
│  2. Schema creation (constraints + indexes)             │
│  3. Load 100 proverb nodes                              │
│  4. Extract ~847 cultural concepts                      │
│  5. Create concept nodes                                │
│  6. Create proverb-concept relationships                │
│  7. Create usage contexts & moral lessons               │
│  8. Create concept-to-concept relationships             │
│  9. Validate graph structure                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4: Validate Results                               │
│  python scripts/validate_auradb_graph.py                │
│                                                          │
│  Checks:                                                 │
│  ✅ Node counts (100 Proverb, ~847 Concept, etc.)       │
│  ✅ Relationship counts (~1,247 total)                  │
│  ✅ Schema constraints (4 constraints)                  │
│  ✅ Schema indexes (6+ indexes)                         │
│  ✅ Proverb completeness (all required fields)          │
│  ✅ Cultural weights (0.0-1.0 normalized)               │
│  ✅ Graph connectivity (no orphans)                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 5: Test OG-RAG System                             │
│  python scripts/test_thiLLMo_og_rag.py                  │
│  python scripts/run_ograg_evaluation.py                 │
└─────────────────────────────────────────────────────────┘
```

---

## ⏱️ Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| AuraDB Setup | 5 min | Create instance, get credentials |
| .env Update | 2 min | Update configuration |
| Reconstitution | 2-5 min | Run main script |
| Validation | 1 min | Verify results |
| **TOTAL** | **10-15 min** | Complete reconstitution |

---

## ✅ Prerequisites

### 1. New AuraDB Instance

- [ ] Created at https://console.neo4j.io/
- [ ] Type: AuraDB Free (200K nodes, 400K relationships)
- [ ] Credentials downloaded (URI, username, password)

### 2. Environment Configuration

- [ ] `.env` file exists in project root
- [ ] `NEO4J_URI` set to new AuraDB URI
- [ ] `NEO4J_USER` set (default: neo4j)
- [ ] `NEO4J_PASSWORD` set

### 3. Source Data Files

- [ ] `data/evaluation/gold_standard_ireri_deduplicated.csv` exists (CRITICAL)
- [ ] `data/ontology/extracted_concepts_100proverbs.json` exists (important)

### 4. Python Dependencies

```bash
pip install neo4j python-dotenv
```

---

## 🧪 Testing After Reconstitution

### Quick Test

```bash
# Should show ~962 nodes, ~1,215 relationships
python scripts/validate_auradb_graph.py
```

### Full OG-RAG Test

```bash
# Test retrieval system
python scripts/test_thiLLMo_og_rag.py

# Run evaluation benchmarks
python scripts/run_ograg_evaluation.py
```

**Expected Metrics (from Thesis):**
- Cultural Authenticity: 0.627 (OG-RAG) vs 0.568 (baseline) - **10.5% improvement**
- Translation Fidelity: 0.635 (OG-RAG) vs 0.530 (baseline) - **19.8% improvement**
- Overall Quality: 0.631 (OG-RAG) vs 0.549 (baseline) - **13.5% improvement**

### Neo4j Browser Queries

```cypher
// 1. Count all nodes
MATCH (n) RETURN labels(n)[0] as Type, count(n) as Count

// 2. Sample high-weight proverb with concepts
MATCH (p:Proverb)-[r:EXPRESSES_CONCEPT]->(c:CulturalConcept)
WHERE p.cultural_weight > 0.8
RETURN p.kikuyu_text, collect(c.name)[0..5] as concepts
LIMIT 5

// 3. Concept relationship network
MATCH (c1:CulturalConcept)-[r:RELATES_TO]->(c2:CulturalConcept)
RETURN c1.name, type(r), c2.name, r.strength
ORDER BY r.strength DESC
LIMIT 10
```

---

## 🔧 Troubleshooting

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| "Missing Neo4j credentials" | .env not configured | Create/edit `.env` with AuraDB credentials |
| "Connection failed" | Wrong URI format | Use `neo4j+s://xxxxx.databases.neo4j.io` |
| "File not found: gold_standard..." | Missing data file | Contact supervisor or restore from git |
| Low concept count (<100) | Missing JSON file | Script uses fallback heuristics (acceptable) |
| Schema compliance <99% | Incomplete data | Check CSV for missing fields |

**Full troubleshooting guide:** `docs/setup/AURADB_RECONSTITUTION_GUIDE.md` (section 9)

---

## 💾 Backup & Recovery

### Prevent Future Data Loss

```bash
# 1. Keep source data in version control
git add data/evaluation/gold_standard_ireri_deduplicated.csv
git commit -m "backup: Proverb corpus snapshot"

# 2. Keep AuraDB instance active (query weekly)
python -c "from neo4j import GraphDatabase; import os; from dotenv import load_dotenv; load_dotenv(); d = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))); s = d.session(); s.run('MATCH (n) RETURN count(n)'); s.close(); d.close(); print('✅ Keep-alive')"

# 3. Export graph to JSON (backup)
# See full guide for export scripts
```

**Note:** AuraDB Free Tier pauses after 3 days of inactivity. Run a query weekly to prevent.

---

## 📖 Related Documentation

### Thesis References

- **Chapter 4:** Design & Implementation (complete schema specification)
- **Section 4.2.1:** Neo4j Schema Design
- **Figure 4.1:** System Architecture (5-layer ontology)
- **Table 4.2:** Node Properties Specification

### Project Documentation

- `docs/ontology/kikuyu_proverb_ontology_design.md` - Ontology design principles
- `docs/ontology/foundation_implementation_summary.md` - Implementation details
- `README.md` (project root) - Project overview

### Alternative Scripts

- `scripts/deploy_schema.py` - Deploy schema only (no data)
- `scripts/populate_proverbs_day1.py` - Populate proverbs only
- `scripts/create_concept_nodes.py` - Create concepts only
- `scripts/link_proverbs_to_concepts.py` - Link proverbs to concepts

---

## 🎓 Thesis Context

**Thesis Title:** "thiLLMo: Culturally Faithful Kikuyu Proverb Translation Using Ontology-Grounded RAG"

**Defense Date:** January 14, 2026 (2 days from now!)

**Graph Purpose:**
- Enable Ontology-Grounded Retrieval Augmented Generation (OG-RAG)
- Preserve cultural knowledge in Kikuyu proverbs
- Improve translation fidelity by 19.8% over baseline
- Support cultural heritage preservation

**Research Impact:**
- First application of OG-RAG to low-resource language translation
- Demonstrates 7.5x improvement in cultural fidelity metrics
- Scalable to 1000+ proverb corpus

---

## 📞 Support

**Script Issues:**
- Review source code: `scripts/reconstitute_auradb_knowledge_graph.py`
- Check validation: `scripts/validate_auradb_graph.py`

**Data Issues:**
- Contact thesis supervisor for backup files
- Check git history: `git log --all -- data/evaluation/`

**AuraDB Issues:**
- Visit https://console.neo4j.io/
- Check Neo4j community forums

---

## 🔄 Version History

| Date | Version | Changes |
|------|---------|---------|
| Jan 12, 2026 | 1.0 | Initial reconstitution script and documentation |

---

**Last Updated:** January 12, 2026  
**Script Author:** thiLLMo Project Team  
**Thesis Defense:** January 14, 2026  
**License:** CC-BY-4.0 (per thesis documentation)
