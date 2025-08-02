# Database Storage

This directory contains the actual Neo4j database files and storage.

## Contents

When Neo4j is running, this directory will contain:

### Database Files
- `databases/` - Database storage files
- `transactions/` - Transaction logs
- `graph.db/` - Graph database files (legacy format)

### System Files  
- `system/` - System database
- `logs/` - Database log files
- `conf/` - Configuration files
- `certificates/` - SSL certificates

### Runtime Data
- `run/` - Runtime files (PIDs, locks)
- `import/` - Import staging area
- `plugins/` - Neo4j plugins (APOC, GDS, etc.)

## Storage Structure

```
database/
├── databases/
│   ├── neo4j/           # Main application database
│   └── system/          # System database
├── transactions/
│   ├── neo4j/
│   └── system/
└── dbms/
    ├── logs/
    ├── conf/
    └── certificates/
```

## Important Notes

### Data Persistence
- This directory contains your actual graph data
- **Always backup before major operations**
- Data files are binary format (not human readable)
- Requires proper shutdown to maintain consistency

### Volume Mounting
For Docker deployments:
```bash
docker run -v $PWD/database:/data neo4j:latest
```

### Permissions
- Ensure proper file permissions (neo4j user access)
- Read/write access required for database operations
- Backup files should be readable by admin users

### Storage Requirements
- Plan for data growth over time
- Monitor disk space usage
- Consider SSD storage for better performance
- Allocate space for transaction logs

## Monitoring

### Disk Usage
```bash
# Check database size
du -sh database/databases/neo4j

# Monitor growth over time
watch -n 60 'du -sh database/databases/neo4j'
```

### Database Health
```cypher
// Check database status
CALL dbms.info();

// Check storage usage
CALL db.stats.retrieve('GRAPH COUNTS');
```

## Maintenance

### Log Rotation
- Configure log rotation to prevent disk filling
- Archive old transaction logs
- Monitor log file sizes

### Cleanup
- Remove old transaction logs (after backup)
- Clean temporary files
- Compress archived data

### Performance
- Monitor I/O patterns
- Consider database tuning parameters
- Optimize storage layout for workload

## Backup Integration

This directory is the primary target for:
- Full database backups
- Incremental backups  
- Point-in-time recovery
- Data migration operations

## Security

### Access Control
- Restrict file system access
- Encrypt sensitive data at rest
- Secure backup files
- Monitor access logs

### Data Protection
- Regular integrity checks
- Corruption detection
- Disaster recovery planning
- Geographic backup distribution
