// Basic Queries for Cultural Heritage Knowledge Graph
// Core queries for exploring the OG-RAG knowledge base

// =====================================
// NODE EXPLORATION QUERIES
// =====================================

// Get all node types and counts
MATCH (n)
RETURN labels(n) as NodeType, count(n) as Count
ORDER BY Count DESC;

// Get all cultures in the database
MATCH (c:Culture)
RETURN c.name, c.region, c.population
ORDER BY c.name;

// Get all languages and their families
MATCH (l:Language)
RETURN l.name, l.family, l.speakers, l.status
ORDER BY l.speakers DESC;

// Get all semantic concepts
MATCH (c:Concept)
RETURN c.name, c.semantic_field, c.definition
ORDER BY c.name;

// =====================================
// RELATIONSHIP EXPLORATION QUERIES
// =====================================

// Get all relationship types and counts
MATCH ()-[r]->()
RETURN type(r) as RelationshipType, count(r) as Count
ORDER BY Count DESC;

// Find cultures and their primary languages
MATCH (c:Culture)-[s:SPEAKS]->(l:Language)
WHERE s.primary = true
RETURN c.name as Culture, l.name as Language, c.region as Region;

// Find concepts and their categories
MATCH (concept:Concept)-[b:BELONGS_TO]->(cat:Category)
RETURN concept.name as Concept, cat.name as Category, b.strength as Strength
ORDER BY Strength DESC;

// =====================================
// PROVERB EXPLORATION QUERIES
// =====================================

// Get sample proverbs by culture
MATCH (p:Proverb)-[:BELONGS_TO]->(c:Culture)
RETURN c.name as Culture, p.text as Proverb, p.meaning as Meaning
LIMIT 10;

// Find proverbs by language
MATCH (p:Proverb)
WHERE p.language = 'kikuyu'
RETURN p.text, p.meaning, p.themes
LIMIT 5;

// Find proverbs expressing specific concepts
MATCH (p:Proverb)-[:EXPRESSES]->(c:Concept)
WHERE c.name = 'hard work'
RETURN p.text, p.meaning, c.definition;

// =====================================
// SEMANTIC RELATIONSHIP QUERIES
// =====================================

// Find similar concepts
MATCH (c1:Concept)-[:SIMILAR_TO]->(c2:Concept)
RETURN c1.name as Concept1, c2.name as Concept2
ORDER BY c1.name;

// Find concept hierarchies
MATCH (child:Concept)-[:SUBCLASS_OF]->(parent:Concept)
RETURN parent.name as Parent, child.name as Child;

// Find contrasting concepts
MATCH (c1:Concept)-[:CONTRASTS_WITH]->(c2:Concept)
RETURN c1.name as Concept1, c2.name as Concept2;

// =====================================
// CROSS-CULTURAL ANALYSIS QUERIES
// =====================================

// Find concepts shared across cultures
MATCH (c1:Culture)<-[:BELONGS_TO]-(p1:Proverb)-[:EXPRESSES]->(concept:Concept)<-[:EXPRESSES]-(p2:Proverb)-[:BELONGS_TO]->(c2:Culture)
WHERE c1 <> c2
RETURN c1.name as Culture1, c2.name as Culture2, concept.name as SharedConcept, 
       p1.text as Proverb1, p2.text as Proverb2
LIMIT 10;

// Find unique concepts per culture
MATCH (c:Culture)<-[:BELONGS_TO]-(p:Proverb)-[:EXPRESSES]->(concept:Concept)
WITH concept, collect(DISTINCT c.name) as cultures
WHERE size(cultures) = 1
RETURN concept.name as UniqueConcept, cultures[0] as Culture;

// =====================================
// GRAPH STRUCTURE QUERIES
// =====================================

// Find nodes with highest degree (most connections)
MATCH (n)
WITH n, size((n)--()) as degree
WHERE degree > 0
RETURN labels(n) as NodeType, n.name as Name, degree
ORDER BY degree DESC
LIMIT 10;

// Find shortest path between two concepts
MATCH path = shortestPath((c1:Concept {name: 'wealth'})-[*]-(c2:Concept {name: 'wisdom'}))
RETURN path;

// Find nodes with no relationships (orphaned nodes)
MATCH (n)
WHERE NOT (n)--()
RETURN labels(n) as NodeType, count(n) as Count;

// =====================================
// DATA QUALITY QUERIES
// =====================================

// Find nodes missing required properties
MATCH (p:Proverb)
WHERE p.text IS NULL OR p.text = ''
RETURN count(p) as ProverbsWithoutText;

MATCH (c:Culture)
WHERE c.name IS NULL OR c.name = ''
RETURN count(c) as CulturesWithoutName;

// Find duplicate proverbs
MATCH (p1:Proverb), (p2:Proverb)
WHERE p1.text = p2.text AND id(p1) < id(p2)
RETURN p1.text as DuplicateText, count(*) as Count;

// =====================================
// PERFORMANCE TESTING QUERIES
// =====================================

// Test index usage for proverb text search
EXPLAIN MATCH (p:Proverb)
WHERE p.text CONTAINS 'wisdom'
RETURN p.text;

// Test relationship traversal performance
EXPLAIN MATCH (c:Culture)-[:SPEAKS]->(l:Language)
RETURN c.name, l.name;
