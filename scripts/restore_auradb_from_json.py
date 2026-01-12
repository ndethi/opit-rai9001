#!/usr/bin/env python3
"""
Restore AuraDB Knowledge Graph from JSON Backup
================================================

This script restores a complete Neo4j knowledge graph from JSON backup files.

Usage:
    python scripts/restore_auradb_from_json.py data/backups/graph_backup_20260112_150000

Requirements:
- Backup directory with node and relationship JSON files
- Empty or clearable AuraDB instance
- Valid .env credentials

Process:
1. Verify backup integrity
2. Clear existing database (with confirmation)
3. Recreate schema (constraints and indexes)
4. Load all nodes
5. Load all relationships
6. Validate restoration

Runtime: 2-5 minutes depending on backup size
"""

import json
import sys
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / '.env')


class GraphRestore:
    """Restore Neo4j knowledge graph from JSON backup."""
    
    def __init__(self, backup_dir: Path, uri: str, username: str, password: str):
        """Initialize connection and backup directory."""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.backup_dir = backup_dir
        self.uri = uri
        self.stats = {
            'nodes_created': 0,
            'relationships_created': 0
        }
    
    def close(self):
        """Close database connection."""
        self.driver.close()
    
    def verify_backup(self) -> bool:
        """Verify backup directory and files exist."""
        print("\n🔍 Verifying backup files...")
        
        if not self.backup_dir.exists():
            print(f"   ❌ Backup directory not found: {self.backup_dir}")
            return False
        
        # Check for metadata
        metadata_file = self.backup_dir / 'metadata.json'
        if not metadata_file.exists():
            print(f"   ❌ metadata.json not found")
            return False
        
        # Load metadata
        with open(metadata_file, 'r') as f:
            self.metadata = json.load(f)
        
        print(f"   ✅ Backup verified")
        print(f"      Date: {self.metadata.get('backup_date', 'Unknown')}")
        print(f"      Nodes: {self.metadata.get('total_nodes', 0)}")
        print(f"      Relationships: {self.metadata.get('total_relationships', 0)}")
        
        return True
    
    def clear_database(self):
        """Clear existing database."""
        print("\n🗑️  Clearing existing database...")
        
        with self.driver.session() as session:
            # Check existing nodes
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()['count']
            
            if count > 0:
                print(f"   ⚠️  Database contains {count} nodes")
                response = input("   Delete all existing data? (yes/no): ")
                if response.lower() != 'yes':
                    print("   ❌ Restore cancelled")
                    return False
                
                session.run("MATCH (n) DETACH DELETE n")
                print(f"   ✅ Deleted {count} nodes")
            else:
                print(f"   ✅ Database is empty")
        
        return True
    
    def create_schema(self):
        """Recreate schema constraints and indexes."""
        print("\n📋 Creating schema...")
        
        with self.driver.session() as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT proverb_id_unique IF NOT EXISTS FOR (p:Proverb) REQUIRE p.proverb_id IS UNIQUE",
                "CREATE CONSTRAINT concept_name_unique IF NOT EXISTS FOR (c:CulturalConcept) REQUIRE c.name IS UNIQUE",
                "CREATE CONSTRAINT context_id_unique IF NOT EXISTS FOR (u:UsageContext) REQUIRE u.context_id IS UNIQUE",
                "CREATE CONSTRAINT moral_id_unique IF NOT EXISTS FOR (m:MoralLesson) REQUIRE m.moral_id IS UNIQUE"
            ]
            
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    pass  # Constraint might already exist
            
            print(f"   ✅ Created constraints")
            
            # Indexes
            indexes = [
                "CREATE INDEX proverb_kikuyu_text IF NOT EXISTS FOR (p:Proverb) ON (p.kikuyu_text)",
                "CREATE INDEX proverb_cultural_weight IF NOT EXISTS FOR (p:Proverb) ON (p.cultural_weight)",
                "CREATE INDEX concept_cultural_weight IF NOT EXISTS FOR (c:CulturalConcept) ON (c.cultural_weight)",
                "CREATE INDEX concept_type IF NOT EXISTS FOR (c:CulturalConcept) ON (c.concept_type)"
            ]
            
            for index in indexes:
                try:
                    session.run(index)
                except Exception as e:
                    pass
            
            print(f"   ✅ Created indexes")
    
    def restore_nodes(self):
        """Restore all node files."""
        print("\n" + "="*70)
        print("RESTORING NODES")
        print("="*70)
        
        node_files = sorted(self.backup_dir.glob('nodes_*.json'))
        
        for node_file in node_files:
            label = node_file.stem.replace('nodes_', '').replace('_', ' ').title().replace(' ', '')
            
            print(f"\n📦 Restoring {label} nodes from {node_file.name}...")
            
            with open(node_file, 'r', encoding='utf-8') as f:
                nodes = json.load(f)
            
            if not nodes:
                print(f"   ⚠️  No nodes in file")
                continue
            
            # Remove internal fields
            for node in nodes:
                node.pop('_labels', None)
                node.pop('_id', None)
            
            # Batch create nodes
            with self.driver.session() as session:
                batch_size = 50
                created = 0
                
                for i in range(0, len(nodes), batch_size):
                    batch = nodes[i:i+batch_size]
                    
                    # Dynamic property mapping
                    result = session.run(f"""
                        UNWIND $nodes AS node
                        CREATE (n:{label})
                        SET n = node
                        RETURN count(n) as created
                    """, nodes=batch)
                    
                    batch_created = result.single()['created']
                    created += batch_created
                    self.stats['nodes_created'] += batch_created
                
                print(f"   ✅ Created {created} {label} nodes")
    
    def restore_relationships(self):
        """Restore all relationship files."""
        print("\n" + "="*70)
        print("RESTORING RELATIONSHIPS")
        print("="*70)
        
        rel_files = sorted(self.backup_dir.glob('relationships_*.json'))
        
        for rel_file in rel_files:
            rel_type = rel_file.stem.replace('relationships_', '').upper()
            
            print(f"\n🔗 Restoring {rel_type} relationships from {rel_file.name}...")
            
            with open(rel_file, 'r', encoding='utf-8') as f:
                relationships = json.load(f)
            
            if not relationships:
                print(f"   ⚠️  No relationships in file")
                continue
            
            # Batch create relationships
            with self.driver.session() as session:
                batch_size = 100
                created = 0
                
                for i in range(0, len(relationships), batch_size):
                    batch = relationships[i:i+batch_size]
                    
                    # Dynamic relationship creation based on node identifiers
                    for rel in batch:
                        start_label = rel['start_label']
                        end_label = rel['end_label']
                        start_id = rel['start_id']
                        end_id = rel['end_id']
                        props = rel.get('properties', {})
                        
                        # Determine identifier field
                        if start_label == 'Proverb':
                            start_match = f"(start:Proverb {{proverb_id: $start_id}})"
                        elif start_label == 'CulturalConcept':
                            start_match = f"(start:CulturalConcept {{name: $start_id}})"
                        elif start_label == 'UsageContext':
                            start_match = f"(start:UsageContext {{context_id: $start_id}})"
                        elif start_label == 'MoralLesson':
                            start_match = f"(start:MoralLesson {{moral_id: $start_id}})"
                        else:
                            continue
                        
                        if end_label == 'Proverb':
                            end_match = f"(end:Proverb {{proverb_id: $end_id}})"
                        elif end_label == 'CulturalConcept':
                            end_match = f"(end:CulturalConcept {{name: $end_id}})"
                        elif end_label == 'UsageContext':
                            end_match = f"(end:UsageContext {{context_id: $end_id}})"
                        elif end_label == 'MoralLesson':
                            end_match = f"(end:MoralLesson {{moral_id: $end_id}})"
                        else:
                            continue
                        
                        query = f"""
                            MATCH {start_match}
                            MATCH {end_match}
                            CREATE (start)-[r:{rel_type}]->(end)
                            SET r = $props
                            RETURN count(r) as created
                        """
                        
                        result = session.run(query, start_id=start_id, end_id=end_id, props=props)
                        created += result.single()['created']
                    
                    self.stats['relationships_created'] += created
                
                print(f"   ✅ Created {created} {rel_type} relationships")
    
    def validate_restoration(self):
        """Validate restored graph."""
        print("\n" + "="*70)
        print("VALIDATING RESTORATION")
        print("="*70)
        
        with self.driver.session() as session:
            # Count nodes
            result = session.run("MATCH (n) RETURN labels(n)[0] as label, count(n) as count")
            print(f"\n📊 Restored Nodes:")
            total_nodes = 0
            for record in result:
                count = record['count']
                total_nodes += count
                print(f"   • {record['label']}: {count}")
            
            # Count relationships
            result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
            print(f"\n🔗 Restored Relationships:")
            total_rels = 0
            for record in result:
                count = record['count']
                total_rels += count
                print(f"   • {record['type']}: {count}")
            
            # Compare with backup
            expected_nodes = self.metadata.get('total_nodes', 0)
            expected_rels = self.metadata.get('total_relationships', 0)
            
            print(f"\n✅ Validation Results:")
            node_match = total_nodes == expected_nodes
            rel_match = total_rels == expected_rels
            
            print(f"   Nodes: {total_nodes}/{expected_nodes} {'✅' if node_match else '❌'}")
            print(f"   Relationships: {total_rels}/{expected_rels} {'✅' if rel_match else '❌'}")
            
            return node_match and rel_match


def main():
    """Main restore workflow."""
    
    if len(sys.argv) < 2:
        print("Usage: python scripts/restore_auradb_from_json.py <backup_directory>")
        print("\nExample:")
        print("  python scripts/restore_auradb_from_json.py data/backups/graph_backup_20260112_150000")
        return False
    
    backup_dir = Path(sys.argv[1])
    
    print("="*70)
    print("AURADB KNOWLEDGE GRAPH RESTORE")
    print("From JSON Backup Files")
    print("="*70)
    print(f"\n📁 Backup directory: {backup_dir}")
    
    # Get credentials
    uri = os.getenv('NEO4J_URI')
    username = os.getenv('NEO4J_USER', os.getenv('NEO4J_USERNAME', 'neo4j'))
    password = os.getenv('NEO4J_PASSWORD')
    
    if not all([uri, password]):
        print("\n❌ ERROR: Missing Neo4j credentials in .env file")
        return False
    
    print(f"\n🔗 Target AuraDB: {uri}")
    print(f"👤 Username: {username}")
    
    # Initialize restore
    restore = GraphRestore(backup_dir, uri, username, password)
    
    try:
        # Verify backup
        if not restore.verify_backup():
            return False
        
        # Clear database
        if not restore.clear_database():
            return False
        
        # Create schema
        restore.create_schema()
        
        # Restore nodes
        restore.restore_nodes()
        
        # Restore relationships
        restore.restore_relationships()
        
        # Validate
        success = restore.validate_restoration()
        
        print("\n" + "="*70)
        if success:
            print("✅ RESTORATION COMPLETE!")
        else:
            print("⚠️  RESTORATION COMPLETE WITH WARNINGS")
        print("="*70)
        
        print(f"\n📊 Restoration Summary:")
        print(f"   • {restore.stats['nodes_created']} nodes created")
        print(f"   • {restore.stats['relationships_created']} relationships created")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Restore failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        restore.close()


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
