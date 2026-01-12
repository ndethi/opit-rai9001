# AuraDB Backup & Restore System

**Quick reference for backing up and restoring your knowledge graph**

---

## 🎯 Purpose

Prevent permanent data loss when AuraDB Free Tier instances are deleted due to inactivity (>3 days). Your complete knowledge graph (1,069 nodes, 6,445 relationships) is now backed up in version control.

---

## 📦 Current Backup

**Location:** `data/backups/graph_backup_20260112_193921/`

**Contents:**
- ✅ 100 Proverb nodes (87 KB)
- ✅ 959 CulturalConcept nodes (361 KB) - **exceeds thesis target of 847!**
- ✅ 5 UsageContext nodes
- ✅ 5 MoralLesson nodes
- ✅ 1,895 EXPRESSES_CONCEPT relationships
- ✅ 4,394 RELATES_TO relationships
- ✅ 67 TEACHES_LESSON relationships
- ✅ 39 USED_IN relationships
- ✅ 50 SUBSUMES relationships

**Total Size:** 2.1 MB (10 JSON files)  
**Backup Date:** January 12, 2026, 7:39 PM  
**Status:** ✅ Committed to git and pushed to GitHub

---

## 🚀 Quick Commands

### Create New Backup

```bash
# Export current AuraDB to JSON files
python scripts/backup_auradb_to_json.py

# Creates: data/backups/graph_backup_YYYYMMDD_HHMMSS/
```

**Runtime:** ~30 seconds  
**Output:** Timestamped directory with 10 JSON files

### Restore from Backup

```bash
# Restore from latest backup
python scripts/restore_auradb_from_json.py data/backups/graph_backup_20260112_193921

# Or from any backup directory
python scripts/restore_auradb_from_json.py data/backups/graph_backup_YYYYMMDD_HHMMSS
```

**Runtime:** 2-5 minutes  
**Note:** Will prompt before clearing existing database

---

## 📋 Workflow Examples

### Scenario 1: AuraDB Instance Deleted

```bash
# 1. Create new AuraDB instance at https://console.neo4j.io/
# 2. Update .env with new credentials
nano .env  # Update NEO4J_URI, NEO4J_PASSWORD

# 3. Restore from latest backup
python scripts/restore_auradb_from_json.py data/backups/graph_backup_20260112_193921

# 4. Verify restoration
python scripts/validate_auradb_graph.py
```

**Total time:** ~10 minutes from deletion to fully operational

### Scenario 2: Regular Backup Schedule

```bash
# Run weekly backup (before defense and after)
python scripts/backup_auradb_to_json.py

# Commit to git for version control
git add data/backups/graph_backup_*
git commit -m "backup: Weekly knowledge graph snapshot"
git push
```

### Scenario 3: Test Restore (Verification)

```bash
# 1. Backup current state first
python scripts/backup_auradb_to_json.py

# 2. Test restore on a different AuraDB instance
# Update .env to point to test instance
python scripts/restore_auradb_from_json.py data/backups/graph_backup_20260112_193921

# 3. Validate
python scripts/validate_auradb_graph.py
```

---

## 📂 Backup File Structure

```
data/backups/graph_backup_20260112_193921/
├── README.md                              # Restore instructions
├── metadata.json                          # Backup statistics
├── nodes_proverb.json                     # 100 Proverb nodes
├── nodes_culturalconcept.json             # 959 CulturalConcept nodes
├── nodes_usagecontext.json                # 5 UsageContext nodes
├── nodes_morallesson.json                 # 5 MoralLesson nodes
├── relationships_expresses_concept.json   # 1,895 edges
├── relationships_relates_to.json          # 4,394 edges
├── relationships_teaches_lesson.json      # 67 edges
├── relationships_used_in.json             # 39 edges
└── relationships_subsumes.json            # 50 edges
```

---

## 🔍 Verifying Backups

### Check Backup Integrity

```bash
# List all backups
ls -lh data/backups/

# Check specific backup metadata
cat data/backups/graph_backup_20260112_193921/metadata.json | python -m json.tool

# Verify file sizes
du -sh data/backups/graph_backup_20260112_193921/
```

### Compare Backup to Current Graph

```bash
# Run backup
python scripts/backup_auradb_to_json.py

# Compare node counts
cat data/backups/graph_backup_*/metadata.json | grep -A 10 "nodes"
```

---

## 📊 Backup Format

### Node File Format (nodes_proverb.json)

```json
[
  {
    "proverb_id": "MW_001",
    "kikuyu_text": "Aikaragia mbia ta njuu ngigi.",
    "expert_translation": "He looks after his money...",
    "expert_cultural_meaning": "Whoever has much always wants more.",
    "cultural_weight": 1.0,
    "thematic_category": "wealth_acquisition",
    "source": "ireri_expert_2014",
    "validation_status": "expert_validated",
    "created_date": "2026-01-12T..."
  }
]
```

### Relationship File Format (relationships_expresses_concept.json)

```json
[
  {
    "type": "EXPRESSES_CONCEPT",
    "start_label": "Proverb",
    "start_id": "MW_001",
    "end_label": "CulturalConcept",
    "end_id": "wealth_acquisition",
    "properties": {
      "salience": 0.8,
      "created_date": "2026-01-12T..."
    }
  }
]
```

---

## ⚙️ Advanced Options

### Backup to Custom Location

```python
# Modify backup script temporarily
backup_dir = Path('/path/to/custom/backup')
```

### Selective Restore

```python
# Restore only specific node types
# Edit restore script to skip certain files
# Example: Only restore Proverb nodes
```

### Export to Other Formats

```bash
# Convert JSON to CSV for analysis
python -c "
import json
import csv
with open('data/backups/graph_backup_20260112_193921/nodes_proverb.json') as f:
    data = json.load(f)
with open('proverbs.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
"
```

---

## 🛡️ Backup Strategy

### Recommended Schedule

**Before Defense (Critical):**
- ✅ Backup created: January 12, 2026, 7:39 PM
- ✅ Committed to git
- ✅ Pushed to GitHub

**After Defense:**
- Create backup if graph is modified
- Schedule weekly backups for ongoing research

**Before Major Changes:**
- Backup before running any destructive scripts
- Backup before schema modifications
- Backup before bulk data imports

### Version Control

```bash
# Backups are in .gitignore by default for large repos
# But for thesis, we've committed the backup for safety

# Check backup is in git
git log --oneline --all -- data/backups/

# Should show: "feat: Add complete AuraDB backup and restore system"
```

---

## 🔧 Troubleshooting

### Backup Fails

**Error:** "Connection failed"
```bash
# Check .env credentials
grep "NEO4J_" .env

# Test connection
python -c "from neo4j import GraphDatabase; import os; from dotenv import load_dotenv; load_dotenv(); d = GraphDatabase.driver(os.getenv('NEO4J_URI'), auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))); print('✅ Connected'); d.close()"
```

**Error:** "Permission denied"
```bash
# Check directory permissions
ls -ld data/backups/
mkdir -p data/backups/
```

### Restore Fails

**Error:** "Backup directory not found"
```bash
# List available backups
ls data/backups/

# Use full path
python scripts/restore_auradb_from_json.py $(pwd)/data/backups/graph_backup_20260112_193921
```

**Error:** "Node count mismatch"
```bash
# Check metadata
cat data/backups/graph_backup_20260112_193921/metadata.json

# Verify current graph
python scripts/validate_auradb_graph.py
```

---

## 📈 Backup Statistics

**Current Backup (graph_backup_20260112_193921):**

| Metric | Count | Size |
|--------|-------|------|
| Total Nodes | 1,069 | 450 KB |
| Total Relationships | 6,445 | 1.6 MB |
| Proverb Nodes | 100 | 87 KB |
| CulturalConcept Nodes | 959 | 361 KB |
| EXPRESSES_CONCEPT Edges | 1,895 | 483 KB |
| RELATES_TO Edges | 4,394 | 1.1 MB |
| **Total Backup Size** | - | **2.1 MB** |

**Thesis Compliance:**
- ✅ 959 concepts (exceeds 847 target by 13%)
- ✅ 100 proverbs (exact match)
- ✅ 6,445 relationships (exceeds 1,247 target by 416%)

---

## 🎓 Defense Notes

**For Jan 14, 2026 Defense:**

✅ **Current state backed up** - No risk of data loss  
✅ **Backup in git** - Available even if local files lost  
✅ **Restore tested** - Can demonstrate recovery if needed  
✅ **Exceeds thesis claims** - 959 concepts vs. 847 claimed  

**Talking Points:**
- "We've implemented a robust backup system to preserve cultural knowledge"
- "Complete graph can be restored in 5 minutes from JSON backups"
- "Backup is version-controlled alongside thesis documentation"
- "959 cultural concepts exceeds our thesis target of 847"

---

## 📞 Support

**Backup Script:** `scripts/backup_auradb_to_json.py` (400+ lines)  
**Restore Script:** `scripts/restore_auradb_from_json.py` (350+ lines)  
**Documentation:** This file + `data/backups/graph_backup_*/README.md`

**Related Scripts:**
- `scripts/reconstitute_auradb_knowledge_graph.py` - Rebuild from source CSVs
- `scripts/validate_auradb_graph.py` - Validate graph integrity

---

**Last Backup:** January 12, 2026, 7:39 PM  
**Next Backup:** After thesis defense (Jan 14, 2026)  
**Status:** ✅ Production Ready
