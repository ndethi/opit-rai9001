# Neo4j Recovery - Quick Reference

## 🚨 Emergency Recovery (AuraDB Deleted)

### Option 1: Interactive Script (Easiest)
```bash
./scripts/neo4j_quick_restore.sh
# Then select: 2) Restore to AURADB (production)
```

### Option 2: Direct Command
```bash
python scripts/restore_neo4j_from_repo.py --env production --auradb --clear
```

## 📋 What Gets Restored

From the repository data:
- ✅ **Schema**: All constraints and indexes from `src/neo4j/schemas/enhanced_kikuyu_schema.cypher`
- ✅ **Concepts**: Cultural concepts from `data/ontology/extracted_concepts_100proverbs.json`
- ✅ **Proverbs**: ~100 proverbs from `data/proverbs/` and `data/evaluation/`
- ✅ **Relationships**: EXPRESSES relationships between proverbs and concepts

Expected database size after restoration:
- **Nodes**: ~150-250 (100 Proverbs + 50-150 CulturalConcepts)
- **Relationships**: ~200-500 (EXPRESSES relationships)

## 🔐 Required Configuration

Ensure your `.env` file has:

```bash
# For AuraDB restoration
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_actual_auradb_password
```

Get these from your AuraDB console:
1. Go to https://console.neo4j.io/
2. Select your database instance
3. Click "Connect"
4. Copy the connection URI and password

## 💾 Create Regular Backups

### After Restoration
```bash
# Immediately backup the restored database
python scripts/backup_neo4j.py --auradb --format both
```

### Daily Backups (Recommended)
Set up a cron job:
```bash
# Edit crontab
crontab -e

# Add this line (backs up at 2 AM daily)
0 2 * * * cd /Users/ndethi/dev/opit/opit-rai9001 && python scripts/backup_neo4j.py --auradb --format both
```

## 📊 Verify Restoration

After restoration, verify the data:

```bash
# Check connection and stats
python scripts/validate_neo4j_connection.py
```

Or in Neo4j Browser:
```cypher
// Count nodes by type
MATCH (n) RETURN labels(n)[0] as type, count(n) as count

// Count relationships
MATCH ()-[r]->() RETURN type(r) as type, count(r) as count

// Sample proverb with concepts
MATCH (p:Proverb)-[:EXPRESSES]->(c:CulturalConcept)
RETURN p.kikuyu_text, collect(c.name) as concepts
LIMIT 5
```

Expected results:
```
Proverb: ~100
CulturalConcept: ~50-150
EXPRESSES: ~200-500
```

## 🛠️ Troubleshooting

### "Authentication failed"
- Check your password in `.env` file
- Verify credentials in AuraDB console
- Ensure using `NEO4J_PASSWORD` not `NEO4J_DEV_PASSWORD`

### "Cannot connect to database"
- Check AuraDB instance is running (not paused)
- Verify URI is correct: `neo4j+s://` for AuraDB
- Check firewall/network settings

### "No data imported"
- Verify data files exist: `ls data/proverbs/`
- Pull latest from git: `git pull origin supervisor-revisions`
- Check script output for specific errors

### "Script not found"
- Ensure you're in project root: `cd /Users/ndethi/dev/opit/opit-rai9001`
- Verify Python 3 is installed: `python3 --version`
- Install dependencies: `pip install -r requirements.txt`

## 📚 Full Documentation

For detailed information:
- **Recovery Guide**: [docs/setup/NEO4J_RECOVERY_GUIDE.md](docs/setup/NEO4J_RECOVERY_GUIDE.md)
- **Backup Strategy**: [src/neo4j/backups/README.md](src/neo4j/backups/README.md)
- **Schema Details**: [src/neo4j/schemas/enhanced_kikuyu_schema.cypher](src/neo4j/schemas/enhanced_kikuyu_schema.cypher)

## ⏱️ Time Estimates

- **Restoration**: 2-5 minutes (depends on network speed to AuraDB)
- **Backup creation**: 1-3 minutes
- **Verification**: 30 seconds

## 🎯 Next Steps After Recovery

1. ✅ Verify data restored correctly
2. ✅ Create immediate backup
3. ✅ Set up automated daily backups
4. ✅ Test OG-RAG retrieval functionality
5. ✅ Update application connection strings (if needed)
6. ✅ Document any custom modifications

---

**Created**: January 11, 2026  
**Last Tested**: With Neo4j 5.15 and AuraDB Professional  
**Contact**: Check README.md for support information
