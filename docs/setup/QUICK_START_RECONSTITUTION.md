# AuraDB Reconstitution - Quick Start

**One-command reconstitution for experienced users**

---

## Prerequisites Check

```bash
# 1. Verify you have the required data files
ls -lh data/evaluation/gold_standard_ireri_deduplicated.csv
ls -lh data/ontology/extracted_concepts_100proverbs.json

# 2. Check .env file has new AuraDB credentials
grep "NEO4J_URI\|NEO4J_USER\|NEO4J_PASSWORD" .env
```

---

## Quick Start (3 Steps)

### 1. Update .env with New AuraDB Credentials

```bash
# Edit .env file
nano .env

# Add your new AuraDB connection details:
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password-here
```

### 2. Run Reconstitution Script

```bash
python scripts/reconstitute_auradb_knowledge_graph.py
```

When prompted: **Type `yes` and press Enter**

### 3. Verify Success

```bash
# Should show ~962 nodes, ~1,215 relationships
# Open Neo4j Browser at your AuraDB URI and run:
```

```cypher
MATCH (n) RETURN labels(n)[0] as Type, count(n) as Count
```

**Expected:**
- Proverb: 100
- CulturalConcept: ~847
- UsageContext: ~31
- MoralLesson: ~43

---

## Runtime

⏱️ **2-5 minutes** total

---

## What Gets Created

✅ **Schema:** 4 constraints + 6 indexes  
✅ **Nodes:** ~962 nodes (4 types)  
✅ **Relationships:** ~1,215 edges (6 types)  
✅ **Cultural Weights:** 0.0-1.0 normalized  
✅ **Thesis-Compliant:** Matches Chapter 4 specification  

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing .env | `cp .env.example .env` then edit |
| Connection failed | Check NEO4J_URI format: `neo4j+s://xxxxx.databases.neo4j.io` |
| Missing CSV | Contact supervisor or restore from git |
| Low concept count | Missing JSON - script uses fallback heuristics |

---

## Next Steps After Reconstitution

```bash
# Test OG-RAG system
python scripts/test_thiLLMo_og_rag.py

# Run evaluation benchmarks
python scripts/run_ograg_evaluation.py

# Validate metrics match thesis (t=7.468, p<0.000001)
python scripts/run_integrated_statistical_analysis.py
```

---

**Full Documentation:** `docs/setup/AURADB_RECONSTITUTION_GUIDE.md`  
**Script Location:** `scripts/reconstitute_auradb_knowledge_graph.py`  
**Defense Date:** January 14, 2026 (2 days away!)
