#!/usr/bin/env python3
"""
Create Local Backup of Neo4j Knowledge Graph

This script creates comprehensive backups of the Neo4j database that can be
easily restored later. Supports multiple backup formats:
- Cypher script (portable, human-readable)
- JSON export (easy to version control)
- Neo4j dump file (fastest restore)

Usage:
    python scripts/backup_neo4j.py --format cypher
    python scripts/backup_neo4j.py --format json --include-vectors
    python scripts/backup_neo4j.py --format dump --output /path/to/backup
"""

import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv(project_root / '.env')

from neo4j import GraphDatabase


class Neo4jBackup:
    """Create backups of Neo4j knowledge graph."""
    
    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        """Initialize connection to Neo4j."""
        self.uri = uri
        self.user = user
        self.database = database
        
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()
        print(f"✅ Connected to Neo4j at {uri}")
    
    def close(self):
        """Close database connection."""
        if hasattr(self, 'driver'):
            self.driver.close()
    
    def get_database_info(self) -> Dict:
        """Get database statistics."""
        with self.driver.session(database=self.database) as session:
            # Count nodes
            node_counts = {}
            result = session.run("MATCH (n) RETURN labels(n)[0] as label, count(n) as count")
            for record in result:
                node_counts[record['label']] = record['count']
            
            # Count relationships
            rel_counts = {}
            result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
            for record in result:
                rel_counts[record['type']] = record['count']
            
            # Get constraints
            constraints = session.run("SHOW CONSTRAINTS").data()
            
            # Get indexes
            indexes = session.run("SHOW INDEXES").data()
            
            return {
                'nodes': node_counts,
                'relationships': rel_counts,
                'constraints': len(constraints),
                'indexes': len(indexes),
                'total_nodes': sum(node_counts.values()),
                'total_relationships': sum(rel_counts.values())
            }
    
    def backup_to_cypher(self, output_file: Path) -> bool:
        """Export database as Cypher script."""
        print(f"\n💾 Creating Cypher backup: {output_file.name}")
        
        with self.driver.session(database=self.database) as session:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"// Neo4j Knowledge Graph Backup\n")
                f.write(f"// Created: {datetime.now().isoformat()}\n")
                f.write(f"// Database: {self.database}\n")
                f.write(f"// URI: {self.uri}\n\n")
                
                # Export constraints
                f.write("// ========================================\n")
                f.write("// CONSTRAINTS\n")
                f.write("// ========================================\n\n")
                
                constraints = session.run("SHOW CONSTRAINTS").data()
                for constraint in constraints:
                    # This is a simplified approach - real constraint recreation is complex
                    f.write(f"// {constraint.get('name', 'unnamed')}\n")
                
                f.write("\n")
                
                # Export indexes
                f.write("// ========================================\n")
                f.write("// INDEXES\n")
                f.write("// ========================================\n\n")
                
                indexes = session.run("SHOW INDEXES").data()
                for index in indexes:
                    f.write(f"// {index.get('name', 'unnamed')}\n")
                
                f.write("\n")
                
                # Export nodes
                f.write("// ========================================\n")
                f.write("// NODES\n")
                f.write("// ========================================\n\n")
                
                node_count = 0
                result = session.run("MATCH (n) RETURN n")
                for record in result:
                    node = record['n']
                    labels = ':'.join(node.labels)
                    props = self._format_props_cypher(dict(node.items()))
                    
                    # Use MERGE for nodes with unique identifiers
                    if 'id' in node:
                        f.write(f"MERGE (n:{labels} {{id: '{node['id']}'}}) SET n = {props};\n")
                    else:
                        f.write(f"CREATE (n:{labels} {props});\n")
                    
                    node_count += 1
                    if node_count % 100 == 0:
                        print(f"  Exported {node_count} nodes...")
                
                print(f"  ✓ Exported {node_count} nodes")
                
                # Export relationships
                f.write("\n// ========================================\n")
                f.write("// RELATIONSHIPS\n")
                f.write("// ========================================\n\n")
                
                rel_count = 0
                result = session.run("""
                    MATCH (a)-[r]->(b)
                    RETURN a, b, r, type(r) as rel_type
                """)
                
                for record in result:
                    a = record['a']
                    b = record['b']
                    r = record['r']
                    rel_type = record['rel_type']
                    
                    # Try to match nodes by ID if available
                    if 'id' in a and 'id' in b:
                        a_match = f"{{id: '{a['id']}'}}"
                        b_match = f"{{id: '{b['id']}'}}"
                    else:
                        # Fall back to matching all properties
                        a_match = self._format_props_cypher(dict(a.items()))
                        b_match = self._format_props_cypher(dict(b.items()))
                    
                    rel_props = self._format_props_cypher(dict(r.items()))
                    
                    f.write(f"MATCH (a:{':'.join(a.labels)} {a_match}), ")
                    f.write(f"(b:{':'.join(b.labels)} {b_match}) ")
                    f.write(f"MERGE (a)-[r:{rel_type} {rel_props}]->(b);\n")
                    
                    rel_count += 1
                    if rel_count % 100 == 0:
                        print(f"  Exported {rel_count} relationships...")
                
                print(f"  ✓ Exported {rel_count} relationships")
        
        print(f"✅ Cypher backup complete: {output_file}")
        return True
    
    def backup_to_json(self, output_file: Path, include_vectors: bool = False) -> bool:
        """Export database as JSON."""
        print(f"\n💾 Creating JSON backup: {output_file.name}")
        
        backup_data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'database': self.database,
                'uri': self.uri,
            },
            'nodes': [],
            'relationships': []
        }
        
        with self.driver.session(database=self.database) as session:
            # Export nodes
            print("  Exporting nodes...")
            result = session.run("MATCH (n) RETURN n")
            for record in result:
                node = record['n']
                node_data = {
                    'labels': list(node.labels),
                    'properties': {}
                }
                
                for key, value in node.items():
                    # Skip large vector embeddings unless explicitly requested
                    if not include_vectors and key.endswith('_vector'):
                        continue
                    
                    # Convert non-JSON-serializable types
                    if hasattr(value, 'isoformat'):  # datetime
                        value = value.isoformat()
                    elif isinstance(value, bytes):
                        value = value.hex()
                    
                    node_data['properties'][key] = value
                
                backup_data['nodes'].append(node_data)
            
            print(f"    ✓ {len(backup_data['nodes'])} nodes")
            
            # Export relationships
            print("  Exporting relationships...")
            result = session.run("""
                MATCH (a)-[r]->(b)
                RETURN a, b, r, type(r) as rel_type
            """)
            
            for record in result:
                a = record['a']
                b = record['b']
                r = record['r']
                
                rel_data = {
                    'type': record['rel_type'],
                    'start_node': {
                        'labels': list(a.labels),
                        'id': a.get('id', str(a.id))
                    },
                    'end_node': {
                        'labels': list(b.labels),
                        'id': b.get('id', str(b.id))
                    },
                    'properties': {}
                }
                
                for key, value in r.items():
                    if hasattr(value, 'isoformat'):
                        value = value.isoformat()
                    elif isinstance(value, bytes):
                        value = value.hex()
                    
                    rel_data['properties'][key] = value
                
                backup_data['relationships'].append(rel_data)
            
            print(f"    ✓ {len(backup_data['relationships'])} relationships")
        
        # Write JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON backup complete: {output_file}")
        return True
    
    def _format_props_cypher(self, props: dict) -> str:
        """Format properties for Cypher."""
        if not props:
            return "{}"
        
        items = []
        for k, v in props.items():
            if v is None:
                continue
            elif isinstance(v, str):
                v_escaped = v.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
                items.append(f"{k}: '{v_escaped}'")
            elif isinstance(v, bool):
                items.append(f"{k}: {str(v).lower()}")
            elif isinstance(v, (int, float)):
                items.append(f"{k}: {v}")
            elif isinstance(v, list):
                # Format lists
                list_items = []
                for item in v:
                    if isinstance(item, str):
                        item_escaped = item.replace("'", "\\'")
                        list_items.append(f"'{item_escaped}'")
                    else:
                        list_items.append(str(item))
                items.append(f"{k}: [{', '.join(list_items)}]")
            elif hasattr(v, 'isoformat'):  # datetime
                items.append(f"{k}: datetime('{v.isoformat()}')")
        
        return "{" + ", ".join(items) + "}"


def main():
    """Main backup workflow."""
    parser = argparse.ArgumentParser(description='Backup Neo4j knowledge graph')
    parser.add_argument('--format', choices=['cypher', 'json', 'both'], default='both',
                       help='Backup format (default: both)')
    parser.add_argument('--output', type=Path,
                       help='Output directory (default: src/neo4j/backups)')
    parser.add_argument('--include-vectors', action='store_true',
                       help='Include vector embeddings in JSON backup')
    parser.add_argument('--auradb', action='store_true',
                       help='Backup from AuraDB (use production credentials)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("NEO4J KNOWLEDGE GRAPH BACKUP")
    print("=" * 70)
    
    # Get credentials
    if args.auradb:
        uri = os.getenv('NEO4J_URI', os.getenv('AURA_URI'))
        user = os.getenv('NEO4J_USER', os.getenv('AURA_USER', 'neo4j'))
        password = os.getenv('NEO4J_PASSWORD', os.getenv('AURA_PASSWORD'))
        env_name = "AuraDB"
    else:
        uri = os.getenv('NEO4J_DEV_URI', 'bolt://localhost:7687')
        user = os.getenv('NEO4J_DEV_USER', 'neo4j')
        password = os.getenv('NEO4J_DEV_PASSWORD', 'kikuyu_proverbs_2024')
        env_name = "Local"
    
    if not password:
        print(f"❌ Error: Password not found in .env file")
        sys.exit(1)
    
    # Setup output directory
    output_dir = args.output or (project_root / "src/neo4j/backups")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n🎯 Source: {env_name}")
    print(f"🔗 URI: {uri}")
    print(f"📁 Output: {output_dir}")
    
    try:
        backup = Neo4jBackup(uri, user, password)
        
        # Get database info
        info = backup.get_database_info()
        print(f"\n📊 Database Statistics:")
        print(f"   Nodes: {info['total_nodes']}")
        print(f"   Relationships: {info['total_relationships']}")
        print(f"   Constraints: {info['constraints']}")
        print(f"   Indexes: {info['indexes']}")
        
        # Create backups
        if args.format in ['cypher', 'both']:
            cypher_file = output_dir / f"backup_{timestamp}.cypher"
            backup.backup_to_cypher(cypher_file)
        
        if args.format in ['json', 'both']:
            json_file = output_dir / f"backup_{timestamp}.json"
            backup.backup_to_json(json_file, args.include_vectors)
        
        backup.close()
        
        print("\n" + "=" * 70)
        print("✅ BACKUP COMPLETE!")
        print("=" * 70)
        print(f"\n📝 Backup files created in: {output_dir}")
        print("\n💡 Restore using:")
        print(f"   python scripts/restore_neo4j_from_backup.py {output_dir}/backup_{timestamp}.cypher")
        
    except Exception as e:
        print(f"\n❌ Backup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
