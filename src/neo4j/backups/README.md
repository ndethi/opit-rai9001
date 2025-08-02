# Database Backups

This directory contains backup files and backup management scripts for the Neo4j knowledge graph database.

## Backup Strategy

### Automated Backups
- **Daily** - Full database backup at 2 AM
- **Hourly** - Incremental backups during active development
- **Pre-Migration** - Automatic backup before schema changes
- **Pre-Import** - Backup before large data imports

### Backup Types
- **Full Backup** - Complete database dump
- **Incremental** - Changes since last backup
- **Schema Only** - Database structure without data
- **Data Only** - Node and relationship data without schema

## Backup Files

### Naming Convention
- `backup_YYYYMMDD_HHmm_TYPE.dump`
- `backup_20250802_1400_full.dump`
- `backup_20250802_1500_incremental.dump`

### Storage
- **Local** - This directory for development
- **Cloud** - S3/Azure for production backups
- **Archive** - Compressed long-term storage

## Backup Commands

### Using neo4j-admin
```bash
# Full backup
neo4j-admin database backup --database=neo4j --to-path=./backups neo4j

# Restore from backup
neo4j-admin database restore --from-path=./backups/backup_20250802_1400_full.dump --database=neo4j --overwrite-destination
```

### Using APOC Procedures
```cypher
// Export full database
CALL apoc.export.cypher.all("backup_full.cypher", {
    format: "cypher-shell",
    useOptimizations: {type: "UNWIND_BATCH", unwindBatchSize: 20}
});

// Export specific nodes
CALL apoc.export.cypher.query(
    "MATCH (p:Proverb) RETURN p",
    "backup_proverbs.cypher",
    {}
);
```

## Backup Scripts

### Automated Backup Script
```bash
#!/bin/bash
# backup_database.sh

BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M)
DATABASE="neo4j"

# Create backup
neo4j-admin database backup \
    --database=$DATABASE \
    --to-path=$BACKUP_DIR \
    backup_${DATE}_full

# Compress backup
tar -czf $BACKUP_DIR/backup_${DATE}_full.tar.gz \
    $BACKUP_DIR/backup_${DATE}_full.dump

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
```

## Backup Verification

### Test Restore Process
```bash
# 1. Stop Neo4j
sudo systemctl stop neo4j

# 2. Restore backup to test database
neo4j-admin database restore \
    --from-path=./backups/backup_20250802_1400_full.dump \
    --database=test \
    --overwrite-destination

# 3. Start Neo4j and verify
sudo systemctl start neo4j
cypher-shell -d test "MATCH (n) RETURN count(n)"
```

### Backup Integrity Checks
```cypher
// Verify node counts
MATCH (n) RETURN labels(n) as NodeType, count(n) as Count;

// Verify relationship counts  
MATCH ()-[r]->() RETURN type(r) as RelType, count(r) as Count;

// Check constraints
CALL db.constraints() YIELD name, type, properties;

// Check indexes
CALL db.indexes() YIELD name, type, properties;
```

## Recovery Procedures

### Full Database Recovery
1. Stop Neo4j service
2. Remove existing database files
3. Restore from backup
4. Start Neo4j service
5. Verify data integrity

### Partial Data Recovery
1. Export specific data from backup
2. Import into running database
3. Resolve conflicts and duplicates
4. Update relationships

## Backup Monitoring

### Health Checks
- Backup file size consistency
- Backup completion verification
- Storage space monitoring
- Automated backup notifications

### Metrics
- Backup duration
- File sizes
- Success/failure rates
- Recovery time objectives (RTO)

## Configuration

### Backup Configuration File
```properties
# backup.properties
backup.schedule=0 2 * * *  # Daily at 2 AM
backup.retention.days=30
backup.compression=true
backup.notification.email=admin@example.com
backup.storage.path=/var/backups/neo4j
```
