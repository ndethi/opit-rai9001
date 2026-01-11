# Neo4j Database Recovery Guide

## Overview

This guide explains how to recover your Neo4j AuraDB instance and create local backups for easy restoration.

## Quick Start

### 1. Restore from Repository Data

If your AuraDB instance was deleted, you can rebuild it from the data in this repository:

```bash
# Restore to local Neo4j (development)
python scripts/restore_neo4j_from_repo.py --env development --clear

# Restore to AuraDB (production)
python scripts/restore_neo4j_from_repo.py --env production --auradb --clear
```

### 2. Create Regular Backups

To prevent data loss, create regular backups:

```bash
# Backup local database (both Cypher and JSON formats)
python scripts/backup_neo4j.py --format both

# Backup AuraDB to local files
python scripts/backup_neo4j.py --auradb --format both
```

### 3. Restore from Backup

To restore from a previous backup:

```bash
# Restore from Cypher backup
cypher-shell -u neo4j -p your_password < src/neo4j/backups/backup_20250111_120000.cypher

# Or use the restore script (if created)
python scripts/restore_neo4j_from_backup.py src/neo4j/backups/backup_20250111_120000.cypher
```

## Repository Data Structure

Your repository contains the following Neo4j-related data:

```
src/neo4j/
├── schemas/
│   └── enhanced_kikuyu_schema.cypher  # Complete schema definition
├── backups/                            # Local backup storage
│   └── README.md
├── cypher/                             # Reusable Cypher queries
│   └── basic_queries.cypher
└── scripts/                            # Database utilities
    └── connection.py

data/
├── ontology/
│   └── extracted_concepts_100proverbs.json  # Cultural concepts
└── proverbs/
    ├── tier1_50_gold_standard.json          # Core proverbs
    └── tier2_50_diverse_sample.json

scripts/
├── restore_neo4j_from_repo.py   # Main restoration script
├── backup_neo4j.py               # Backup creation script
└── deploy_schema.py              # Schema deployment
```

## Environment Configuration

Ensure your `.env` file contains the necessary credentials:

```bash
# Local Development
NEO4J_DEV_URI=bolt://localhost:7687
NEO4J_DEV_USER=neo4j
NEO4J_DEV_PASSWORD=kikuyu_proverbs_2024

# AuraDB Production
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
AURA_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
AURA_USER=neo4j
NEO4J_PASSWORD=your_auradb_password
AURA_PASSWORD=your_auradb_password
```

## Detailed Recovery Steps

### Step 1: Verify Repository Data

Check what data is available in the repository:

```bash
# List available ontology data
ls -lh data/ontology/

# List available proverb data
ls -lh data/proverbs/

# Check schema files
ls -lh src/neo4j/schemas/
```

### Step 2: Choose Target Environment

Decide whether to restore to:
- **Local Neo4j** (development, testing) - faster, free, full control
- **AuraDB** (production) - managed, cloud-based, requires subscription

### Step 3: Run Restoration

```bash
# For LOCAL development database
python scripts/restore_neo4j_from_repo.py \
    --env development \
    --clear

# For AURADB production database
python scripts/restore_neo4j_from_repo.py \
    --env production \
    --auradb \
    --clear
```

The script will:
1. ✅ Connect to the database
2. 🗑️  Clear existing data (if `--clear` flag used)
3. 📝 Deploy schema (constraints, indexes)
4. 🧠 Import ontology concepts
5. 📚 Import proverbs
6. 🔗 Create relationships
7. 📊 Display statistics
8. 💾 Create a backup

### Step 4: Verify Restoration

Check the restoration was successful:

```bash
# Using Neo4j Browser
# Navigate to http://localhost:7474 (local) or AuraDB console
# Run query:
MATCH (n) RETURN labels(n) as label, count(n) as count

# Using Python validation script
python scripts/validate_neo4j_connection.py
```

Expected results:
- **Proverb** nodes: ~100
- **CulturalConcept** nodes: ~50-150 (depending on data)
- **EXPRESSES** relationships: ~200-500

## Backup Strategy

### Automated Backups

Set up automated backups to prevent future data loss:

#### Daily Backups (Recommended)

Create a cron job (macOS/Linux) or Task Scheduler (Windows):

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /Users/ndethi/dev/opit/opit-rai9001 && python scripts/backup_neo4j.py --format both
```

#### Pre-Migration Backups

Before any major changes:

```bash
# Create backup with descriptive name
python scripts/backup_neo4j.py --format both --output src/neo4j/backups/pre_migration_$(date +%Y%m%d)
```

### Backup Formats

#### 1. Cypher Script (Recommended for version control)

**Pros:**
- Human-readable
- Easy to review in Git
- Portable across Neo4j versions
- Can selectively restore

**Cons:**
- Slower to restore
- Larger file size

```bash
python scripts/backup_neo4j.py --format cypher
```

#### 2. JSON Export (Good for data analysis)

**Pros:**
- Easy to parse programmatically
- Can import into other systems
- Compact without vectors

**Cons:**
- Not native Neo4j format
- Requires custom restore script

```bash
python scripts/backup_neo4j.py --format json
```

#### 3. Both Formats (Best practice)

```bash
python scripts/backup_neo4j.py --format both
```

### Backup Storage

#### Local Backups

```
src/neo4j/backups/
├── backup_20250111_140000.cypher
├── backup_20250111_140000.json
├── backup_20250110_140000.cypher
└── backup_20250110_140000.json
```

#### Cloud Backups (Recommended)

Store backups in cloud storage for disaster recovery:

```bash
# Upload to cloud (example with AWS S3)
aws s3 sync src/neo4j/backups/ s3://your-bucket/neo4j-backups/

# Or use GitHub (for small databases)
git add src/neo4j/backups/backup_$(date +%Y%m%d)*.cypher
git commit -m "chore: daily Neo4j backup $(date +%Y-%m-%d)"
git push
```

⚠️ **Security Note:** Ensure backups containing sensitive data are encrypted and access-controlled.

## Restoration Options

### From Repository Data (Full Rebuild)

Use when:
- Database was completely deleted
- Starting fresh environment
- Major schema changes

```bash
python scripts/restore_neo4j_from_repo.py --env development --clear
```

### From Backup File (Quick Restore)

Use when:
- Need to revert to previous state
- Recovering from corruption
- Testing rollback scenarios

```bash
# Using Cypher shell
cypher-shell -u neo4j -p password < src/neo4j/backups/backup_20250111.cypher

# Or programmatically
python scripts/restore_from_backup.py src/neo4j/backups/backup_20250111.cypher
```

### Incremental Updates

Use when:
- Adding new proverbs
- Updating specific concepts
- Minimal changes needed

```bash
# Import only new data
python scripts/import_new_proverbs.py data/proverbs/new_batch.json
```

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to Neo4j

**Solutions:**
1. Check database is running: `docker ps` or check AuraDB console
2. Verify credentials in `.env` file
3. Test connection: `python scripts/validate_neo4j_connection.py`
4. Check firewall/network settings

### Schema Conflicts

**Problem:** "Constraint already exists" errors

**Solutions:**
1. Use `--clear` flag to start fresh
2. Manually drop conflicting constraints:
   ```cypher
   SHOW CONSTRAINTS;
   DROP CONSTRAINT constraint_name IF EXISTS;
   ```

### Missing Data Files

**Problem:** "File not found" errors

**Solutions:**
1. Check file paths in restoration script
2. Verify data files exist: `ls data/proverbs/`
3. Pull latest from Git: `git pull origin main`

### Performance Issues

**Problem:** Restoration is very slow

**Solutions:**
1. Use batch operations (already implemented in scripts)
2. Temporarily disable constraints: remove `IF NOT EXISTS` checks
3. For large datasets, use `LOAD CSV` or `APOC` procedures

## Docker Setup (Alternative)

If you don't have local Neo4j installed, use Docker:

```bash
# Start Neo4j container
docker-compose up -d neo4j

# Wait for startup (check logs)
docker-compose logs -f neo4j

# Restore data
python scripts/restore_neo4j_from_repo.py --env development
```

Your `docker-compose.yml` should include:

```yaml
services:
  neo4j:
    image: neo4j:5.15
    ports:
      - "7474:7474"  # Browser
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/kikuyu_proverbs_2024
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
    volumes:
      - ./src/neo4j/data:/data
      - ./src/neo4j/logs:/logs
      - ./src/neo4j/plugins:/plugins
      - ./src/neo4j/backups:/backups
```

## Best Practices

### 1. Regular Backups

- **Daily:** Automated backups to local storage
- **Weekly:** Upload to cloud storage
- **Pre-deployment:** Manual backup before major changes

### 2. Version Control

- Commit schema changes to Git
- Version control small backup files (<10MB)
- Use `.gitignore` for large backup files

### 3. Testing

- Test restoration on local environment first
- Verify data integrity after restoration
- Keep production and development separate

### 4. Documentation

- Document any custom schema modifications
- Keep track of manual data edits
- Maintain changelog of database changes

### 5. Monitoring

- Set up alerts for failed backups
- Monitor database size and growth
- Track query performance

## Recovery Checklist

When recovering from AuraDB deletion:

- [ ] Check `.env` file has correct credentials
- [ ] Verify repository data is up-to-date (`git pull`)
- [ ] Choose target environment (local or new AuraDB)
- [ ] Run restoration script with `--clear` flag
- [ ] Verify node and relationship counts
- [ ] Test sample queries in Neo4j Browser
- [ ] Create immediate backup of restored database
- [ ] Update application connection strings
- [ ] Test OG-RAG retrieval functionality
- [ ] Document any issues or deviations

## Additional Resources

- **Neo4j Documentation:** https://neo4j.com/docs/
- **Cypher Manual:** https://neo4j.com/docs/cypher-manual/
- **APOC Procedures:** https://neo4j.com/labs/apoc/
- **AuraDB Documentation:** https://neo4j.com/docs/aura/

## Support

For issues or questions:
1. Check this README
2. Review script help: `python scripts/restore_neo4j_from_repo.py --help`
3. Check Neo4j logs: `src/neo4j/logs/`
4. Consult Neo4j community forum

---

**Last Updated:** January 11, 2026  
**Tested With:** Neo4j 5.15, Python 3.11, AuraDB Professional
