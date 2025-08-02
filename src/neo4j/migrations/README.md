# Database Migrations

This directory contains database migration scripts for evolving the Neo4j knowledge graph schema over time.

## Migration Strategy

Migrations enable:
- **Schema Evolution** - Add new node types and relationships
- **Data Transformation** - Modify existing data structures  
- **Constraint Updates** - Add/modify database constraints
- **Index Management** - Create/drop performance indexes
- **Backward Compatibility** - Maintain compatibility with existing code

## Migration Files

### Naming Convention
- `YYYYMMDD_HHmm_description.cypher`
- Example: `20250802_1400_add_proverb_sentiment.cypher`

### Migration Types
- **Schema** - Add/modify node labels and relationship types
- **Data** - Transform existing data
- **Constraint** - Add/remove constraints and indexes
- **Cleanup** - Remove deprecated elements

## Current Migrations

- `20250802_1200_initial_schema.cypher` - Initial knowledge graph schema
- `20250802_1300_add_cultural_constraints.cypher` - Cultural data constraints
- `20250802_1400_add_semantic_indexes.cypher` - Performance optimization indexes

## Migration Execution

### Using cypher-shell
```bash
# Execute migration file
cypher-shell -u neo4j -p ograg2025 -f 20250802_1200_initial_schema.cypher
```

### Using Python
```python
from scripts.migration_runner import MigrationRunner
runner = MigrationRunner()
runner.run_migration('20250802_1200_initial_schema.cypher')
```

## Migration Tracking

Each migration creates a tracking record:
```cypher
CREATE (:Migration {
    filename: '20250802_1200_initial_schema.cypher',
    executed_at: datetime(),
    success: true,
    version: '1.0.0'
});
```

## Best Practices

1. **Test Migrations** - Test on development database first
2. **Backup Before Migration** - Always backup before schema changes
3. **Incremental Changes** - Make small, focused changes
4. **Document Changes** - Include clear descriptions
5. **Rollback Plans** - Prepare rollback procedures when possible

## Migration Template

```cypher
// Migration: YYYYMMDD_HHmm_description
// Description: What this migration does
// Author: Your Name
// Date: YYYY-MM-DD

// Pre-migration validation
MATCH (n:Migration {filename: 'YYYYMMDD_HHmm_description.cypher'})
RETURN CASE WHEN count(n) > 0 THEN 
  error('Migration already executed') 
  ELSE 'OK' END as status;

// Migration operations
// ... your migration code here ...

// Post-migration tracking
CREATE (:Migration {
    filename: 'YYYYMMDD_HHmm_description.cypher',
    executed_at: datetime(),
    success: true,
    description: 'Your migration description'
});
```
