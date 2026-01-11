#!/usr/bin/env python3
"""
Restore Neo4j Knowledge Graph from Repository Data

This script rebuilds the Neo4j database (local or AuraDB) from the data stored
in the repository. It can restore:
1. Schema (constraints, indexes, node/relationship types)
2. Ontology data (cultural concepts, semantic fields)
3. Proverbs and their relationships

Usage:
    python scripts/restore_neo4j_from_repo.py --env development
    python scripts/restore_neo4j_from_repo.py --env production --auradb
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import argparse
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / '.env')

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError

class Neo4jRestorer:
    """Restore Neo4j knowledge graph from repository data."""
    
    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        """Initialize connection to Neo4j."""
        self.uri = uri
        self.user = user
        self.database = database
        
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection
            self.driver.verify_connectivity()
            print(f"✅ Connected to Neo4j at {uri}")
        except AuthError:
            raise Exception(f"❌ Authentication failed for user {user}")
        except ServiceUnavailable:
            raise Exception(f"❌ Cannot connect to Neo4j at {uri}")
    
    def close(self):
        """Close database connection."""
        if hasattr(self, 'driver'):
            self.driver.close()
            print("✅ Database connection closed")
    
    def clear_database(self, confirm: bool = False):
        """Delete all nodes and relationships (use with caution!)."""
        if not confirm:
            response = input("\n⚠️  This will DELETE ALL DATA in the database. Continue? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Aborted")
                return False
        
        print("\n🗑️  Clearing database...")
        with self.driver.session(database=self.database) as session:
            # Delete all nodes and relationships
            session.run("MATCH (n) DETACH DELETE n")
            
            # Drop all constraints
            constraints = session.run("SHOW CONSTRAINTS").data()
            for constraint in constraints:
                name = constraint.get('name')
                if name:
                    session.run(f"DROP CONSTRAINT {name} IF EXISTS")
            
            # Drop all indexes
            indexes = session.run("SHOW INDEXES").data()
            for index in indexes:
                name = index.get('name')
                if name and not name.startswith('constraint_'):  # Don't drop constraint indexes
                    session.run(f"DROP INDEX {name} IF EXISTS")
        
        print("✅ Database cleared")
        return True
    
    def deploy_schema(self):
        """Deploy schema from Cypher file."""
        print("\n📝 Deploying schema...")
        
        schema_file = project_root / "src/neo4j/schemas/enhanced_kikuyu_schema.cypher"
        
        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            return False
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            cypher_content = f.read()
        
        # Split into individual statements (simple split on semicolon)
        statements = [stmt.strip() for stmt in cypher_content.split(';') if stmt.strip()]
        
        with self.driver.session(database=self.database) as session:
            for i, statement in enumerate(statements, 1):
                # Skip comments
                if statement.startswith('//') or not statement:
                    continue
                
                try:
                    session.run(statement)
                    print(f"  ✓ Statement {i}/{len(statements)}")
                except Exception as e:
                    # Continue even if some statements fail (e.g., constraint already exists)
                    print(f"  ⚠️  Statement {i} warning: {str(e)[:100]}")
        
        print("✅ Schema deployed")
        return True
    
    def import_ontology_concepts(self):
        """Import cultural concepts from JSON data."""
        print("\n🧠 Importing ontology concepts...")
        
        concepts_file = project_root / "data/ontology/extracted_concepts_100proverbs.json"
        
        if not concepts_file.exists():
            print(f"❌ Concepts file not found: {concepts_file}")
            return False
        
        with open(concepts_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract unique concepts
        all_concepts = set()
        for proverb_data in data.values():
            for theme in proverb_data.get('themes', []):
                all_concepts.add(theme)
            for concept in proverb_data.get('concepts', []):
                all_concepts.add(concept)
        
        print(f"  Found {len(all_concepts)} unique concepts")
        
        with self.driver.session(database=self.database) as session:
            for concept in all_concepts:
                session.run("""
                    MERGE (c:CulturalConcept {name: $name})
                    SET c.id = toLower(replace($name, ' ', '_')),
                        c.description = $name,
                        c.created_at = datetime()
                """, name=concept)
        
        print(f"✅ Imported {len(all_concepts)} concepts")
        return True
    
    def import_proverbs(self):
        """Import proverbs from JSON data."""
        print("\n📚 Importing proverbs...")
        
        # Try multiple possible proverb data locations
        proverb_files = [
            project_root / "data/proverbs/tier1_50_gold_standard.json",
            project_root / "data/proverbs/tier2_50_diverse_sample.json",
            project_root / "data/evaluation/gold_standard_100.json"
        ]
        
        proverbs_imported = 0
        
        for proverb_file in proverb_files:
            if not proverb_file.exists():
                continue
            
            print(f"  Loading {proverb_file.name}...")
            
            with open(proverb_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with self.driver.session(database=self.database) as session:
                for proverb_id, proverb_data in data.items():
                    kikuyu_text = proverb_data.get('kikuyu_text', '')
                    english_translation = proverb_data.get('expert_translation', 
                                                          proverb_data.get('english_translation', ''))
                    
                    if not kikuyu_text:
                        continue
                    
                    # Create proverb node
                    result = session.run("""
                        MERGE (p:Proverb {kikuyu_text: $kikuyu})
                        SET p.id = $id,
                            p.english_translation = $english,
                            p.literal_translation = $literal,
                            p.cultural_meaning = $cultural,
                            p.source = $source,
                            p.created_at = datetime()
                        RETURN p
                    """, 
                        id=proverb_id,
                        kikuyu=kikuyu_text,
                        english=english_translation,
                        literal=proverb_data.get('literal_translation', ''),
                        cultural=proverb_data.get('cultural_meaning', ''),
                        source=proverb_file.name
                    )
                    
                    # Link to concepts/themes
                    themes = proverb_data.get('themes', [])
                    for theme in themes:
                        session.run("""
                            MATCH (p:Proverb {id: $proverb_id})
                            MERGE (c:CulturalConcept {name: $theme})
                            MERGE (p)-[:EXPRESSES]->(c)
                        """, proverb_id=proverb_id, theme=theme)
                    
                    proverbs_imported += 1
        
        print(f"✅ Imported {proverbs_imported} proverbs")
        return True
    
    def create_backup_script(self):
        """Generate a Cypher export for future restoration."""
        print("\n💾 Creating backup script...")
        
        backup_file = project_root / f"src/neo4j/backups/full_backup_{self._get_timestamp()}.cypher"
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        
        with self.driver.session(database=self.database) as session:
            # Export all nodes and relationships as Cypher
            result = session.run("""
                CALL apoc.export.cypher.all(null, {
                    format: 'cypher-shell',
                    useOptimizations: {type: 'UNWIND_BATCH', unwindBatchSize: 20}
                })
                YIELD file, nodes, relationships, properties
                RETURN file, nodes, relationships, properties
            """)
            
            data = result.single()
            if data:
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(data['file'])
                
                print(f"✅ Backup created: {backup_file}")
                print(f"   Nodes: {data['nodes']}, Relationships: {data['relationships']}")
                return True
        
        print("⚠️  APOC plugin not available, creating manual backup...")
        return self._create_manual_backup(backup_file)
    
    def _create_manual_backup(self, backup_file: Path):
        """Create a manual Cypher backup without APOC."""
        with self.driver.session(database=self.database) as session:
            with open(backup_file, 'w', encoding='utf-8') as f:
                # Export all nodes
                f.write("// Nodes\n")
                result = session.run("MATCH (n) RETURN n LIMIT 1000")
                for record in result:
                    node = record['n']
                    labels = ':'.join(node.labels)
                    props = dict(node.items())
                    f.write(f"CREATE (n:{labels} {self._format_props(props)});\n")
                
                # Export all relationships
                f.write("\n// Relationships\n")
                result = session.run("""
                    MATCH (a)-[r]->(b) 
                    RETURN id(a) as src_id, id(b) as tgt_id, type(r) as rel_type, properties(r) as props
                    LIMIT 1000
                """)
                for record in result:
                    f.write(f"// MATCH (a), (b) WHERE id(a)={record['src_id']} AND id(b)={record['tgt_id']} "
                           f"CREATE (a)-[:{record['rel_type']} {self._format_props(record['props'])}]->(b);\n")
        
        print(f"✅ Manual backup created: {backup_file}")
        return True
    
    def _format_props(self, props: dict) -> str:
        """Format properties for Cypher."""
        if not props:
            return "{}"
        
        items = []
        for k, v in props.items():
            if isinstance(v, str):
                v_escaped = v.replace("'", "\\'").replace('"', '\\"')
                items.append(f"{k}: '{v_escaped}'")
            elif isinstance(v, (int, float, bool)):
                items.append(f"{k}: {v}")
            elif isinstance(v, list):
                items.append(f"{k}: {v}")
        
        return "{" + ", ".join(items) + "}"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for backup naming."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_database_stats(self):
        """Print database statistics."""
        print("\n📊 Database Statistics:")
        
        with self.driver.session(database=self.database) as session:
            # Count nodes by label
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
                ORDER BY count DESC
            """)
            
            print("\n  Nodes:")
            for record in result:
                print(f"    {record['label']}: {record['count']}")
            
            # Count relationships by type
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(r) as count
                ORDER BY count DESC
            """)
            
            print("\n  Relationships:")
            for record in result:
                print(f"    {record['type']}: {record['count']}")


def main():
    """Main restoration workflow."""
    parser = argparse.ArgumentParser(description='Restore Neo4j from repository data')
    parser.add_argument('--env', choices=['development', 'production'], default='development',
                       help='Environment to restore (default: development)')
    parser.add_argument('--auradb', action='store_true',
                       help='Restoring to AuraDB (use production credentials)')
    parser.add_argument('--clear', action='store_true',
                       help='Clear database before restoration')
    parser.add_argument('--skip-backup', action='store_true',
                       help='Skip creating backup after restoration')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("NEO4J DATABASE RESTORATION FROM REPOSITORY")
    print("=" * 70)
    
    # Get credentials based on environment
    if args.auradb or args.env == 'production':
        uri = os.getenv('NEO4J_URI', os.getenv('AURA_URI'))
        user = os.getenv('NEO4J_USER', os.getenv('AURA_USER', 'neo4j'))
        password = os.getenv('NEO4J_PASSWORD', os.getenv('AURA_PASSWORD'))
        env_name = "AuraDB Production"
    else:
        uri = os.getenv('NEO4J_DEV_URI', 'bolt://localhost:7687')
        user = os.getenv('NEO4J_DEV_USER', 'neo4j')
        password = os.getenv('NEO4J_DEV_PASSWORD', 'kikuyu_proverbs_2024')
        env_name = "Local Development"
    
    if not password:
        print(f"❌ Error: Password not found in .env file")
        print(f"   Required: NEO4J_PASSWORD or AURA_PASSWORD")
        sys.exit(1)
    
    print(f"\n🎯 Target: {env_name}")
    print(f"🔗 URI: {uri}")
    print(f"👤 User: {user}")
    
    try:
        restorer = Neo4jRestorer(uri, user, password)
        
        # Clear database if requested
        if args.clear:
            if not restorer.clear_database():
                sys.exit(1)
        
        # Deploy schema
        restorer.deploy_schema()
        
        # Import data
        restorer.import_ontology_concepts()
        restorer.import_proverbs()
        
        # Show stats
        restorer.get_database_stats()
        
        # Create backup
        if not args.skip_backup:
            restorer.create_backup_script()
        
        restorer.close()
        
        print("\n" + "=" * 70)
        print("✅ RESTORATION COMPLETE!")
        print("=" * 70)
        print("\n📝 Next steps:")
        print("   1. Verify data in Neo4j Browser")
        print("   2. Run validation queries")
        print("   3. Test OG-RAG retrieval")
        
    except Exception as e:
        print(f"\n❌ Restoration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
