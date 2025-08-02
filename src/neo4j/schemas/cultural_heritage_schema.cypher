// Cultural Heritage Knowledge Graph Schema
// Core schema for OG-RAG cultural heritage research

// =====================================
// NODE CONSTRAINTS AND INDEXES
// =====================================

// Proverb nodes
CREATE CONSTRAINT proverb_id IF NOT EXISTS FOR (p:Proverb) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT proverb_text IF NOT EXISTS FOR (p:Proverb) REQUIRE p.text IS NOT NULL;
CREATE INDEX proverb_text_index IF NOT EXISTS FOR (p:Proverb) ON (p.text);
CREATE INDEX proverb_language_index IF NOT EXISTS FOR (p:Proverb) ON (p.language);

// Culture nodes
CREATE CONSTRAINT culture_id IF NOT EXISTS FOR (c:Culture) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT culture_name IF NOT EXISTS FOR (c:Culture) REQUIRE c.name IS NOT NULL;
CREATE INDEX culture_name_index IF NOT EXISTS FOR (c:Culture) ON (c.name);

// Language nodes  
CREATE CONSTRAINT language_code IF NOT EXISTS FOR (l:Language) REQUIRE l.code IS UNIQUE;
CREATE CONSTRAINT language_name IF NOT EXISTS FOR (l:Language) REQUIRE l.name IS NOT NULL;
CREATE INDEX language_family_index IF NOT EXISTS FOR (l:Language) ON (l.family);

// Concept nodes
CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT concept_name IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS NOT NULL;
CREATE INDEX concept_semantic_index IF NOT EXISTS FOR (c:Concept) ON (c.semantic_field);

// Category nodes
CREATE CONSTRAINT category_id IF NOT EXISTS FOR (c:Category) REQUIRE c.id IS UNIQUE;
CREATE INDEX category_type_index IF NOT EXISTS FOR (c:Category) ON (c.type);

// =====================================
// SAMPLE SCHEMA CREATION
// =====================================

// Create sample cultures
CREATE (:Culture {
    id: 'kikuyu',
    name: 'Kikuyu',
    region: 'East Africa',
    country: 'Kenya',
    population: 6600000,
    created_at: datetime()
});

CREATE (:Culture {
    id: 'luo',
    name: 'Luo',
    region: 'East Africa', 
    country: 'Kenya',
    population: 4000000,
    created_at: datetime()
});

// Create sample languages
CREATE (:Language {
    code: 'kik',
    name: 'Kikuyu',
    family: 'Niger-Congo',
    subfamily: 'Bantu',
    iso_639_3: 'kik',
    speakers: 6600000,
    status: 'active',
    created_at: datetime()
});

CREATE (:Language {
    code: 'luo',
    name: 'Dholuo',
    family: 'Nilo-Saharan',
    subfamily: 'Nilotic',
    iso_639_3: 'luo',
    speakers: 4000000,
    status: 'active',
    created_at: datetime()
});

// Create semantic categories for wealth/prosperity theme
CREATE (:Category {
    id: 'wealth',
    name: 'Wealth',
    type: 'semantic',
    description: 'Concepts related to material prosperity and abundance',
    created_at: datetime()
});

CREATE (:Category {
    id: 'wisdom',
    name: 'Wisdom',
    type: 'semantic',
    description: 'Concepts related to knowledge and understanding',
    created_at: datetime()
});

CREATE (:Category {
    id: 'community',
    name: 'Community',
    type: 'semantic',
    description: 'Concepts related to social relationships and cooperation',
    created_at: datetime()
});

// Create core concepts
CREATE (:Concept {
    id: 'hard_work',
    name: 'Hard Work',
    semantic_field: 'effort',
    definition: 'Dedicated effort and diligence in pursuing goals',
    created_at: datetime()
});

CREATE (:Concept {
    id: 'patience',
    name: 'Patience',
    semantic_field: 'virtue',
    definition: 'The ability to wait and endure difficulties',
    created_at: datetime()
});

CREATE (:Concept {
    id: 'unity',
    name: 'Unity',
    semantic_field: 'cooperation',
    definition: 'Working together in harmony',
    created_at: datetime()
});

// =====================================
// RELATIONSHIP EXAMPLES
// =====================================

// Link cultures to languages
MATCH (c:Culture {id: 'kikuyu'}), (l:Language {code: 'kik'})
CREATE (c)-[:SPEAKS {primary: true}]->(l);

MATCH (c:Culture {id: 'luo'}), (l:Language {code: 'luo'})  
CREATE (c)-[:SPEAKS {primary: true}]->(l);

// Link concepts to categories
MATCH (concept:Concept {id: 'hard_work'}), (cat:Category {id: 'wealth'})
CREATE (concept)-[:BELONGS_TO {strength: 0.8}]->(cat);

MATCH (concept:Concept {id: 'patience'}), (cat:Category {id: 'wisdom'})
CREATE (concept)-[:BELONGS_TO {strength: 0.9}]->(cat);

MATCH (concept:Concept {id: 'unity'}), (cat:Category {id: 'community'})
CREATE (concept)-[:BELONGS_TO {strength: 0.95}]->(cat);
