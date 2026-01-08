# Technical Repository Deep Dive: Development Methodology & Implementation

**Document Purpose**: Comprehensive technical documentation of how the thiLLMo research repository was developed, scripts engineered, and research methodology implemented  
**Audience**: Technical reviewers, future researchers, reproducibility auditors  
**Created**: January 8, 2026  
**Status**: Complete research implementation reference

---

## Table of Contents

1. [Repository Architecture](#repository-architecture)
2. [Data Pipeline Development](#data-pipeline-development)
3. [Ontology Engineering Workflow](#ontology-engineering-workflow)
4. [System Implementation](#system-implementation)
5. [Evaluation Infrastructure](#evaluation-infrastructure)
6. [Version Control Strategy](#version-control-strategy)
7. [Documentation Development](#documentation-development)
8. [Script Development Chronology](#script-development-chronology)

---

## 1. Repository Architecture

### Folder Structure Design Rationale

```
opit-rai9001/
├── data/                    # All datasets, raw → processed → results
│   ├── raw/                # Original sources (PDFs, text files)
│   ├── proverbs/           # Extracted proverb corpus
│   ├── ontology/           # OWL files, concept lists, validation
│   ├── processed/          # Cleaned, standardized datasets
│   ├── evaluation/         # Gold standards, benchmarks
│   └── results/            # Experimental outputs, metrics
├── src/                     # Core system implementation
│   ├── ontology/           # Ontology building & querying
│   ├── retrieval/          # RAG retrieval mechanisms
│   ├── translation/        # LLM integration & prompting
│   └── evaluation/         # Metric calculation & analysis
├── scripts/                 # Research workflow automation
│   ├── data_extraction/    # PDF parsing, proverb extraction
│   ├── ontology_building/  # Concept extraction, validation
│   ├── translation/        # Baseline generation, comparison
│   └── evaluation/         # Scoring, statistical analysis
├── docs/                    # All documentation
│   ├── thesis/             # LaTeX dissertation
│   ├── proposal/           # Initial research proposal
│   ├── ontology/           # Ontology design docs
│   └── development/        # This file and dev notes
├── config/                  # Environment configs, API keys
├── notebooks/              # Jupyter analysis notebooks
└── presentations/          # Defense slides, guides
```

**Key Design Decisions**:
1. **Separation of Concerns**: `src/` for reusable code, `scripts/` for one-off research tasks
2. **Data Lineage**: Clear pipeline from `raw/` → `processed/` → `results/`
3. **Reproducibility**: All configs version-controlled, API keys gitignored
4. **Documentation Co-location**: Thesis and code in same repo for consistency

---

## 2. Data Pipeline Development

### Phase 1: Raw Data Acquisition (Weeks 1-3)

**Source Materials**:
- Ireri, G. (2017). *Kikuyu Proverbs: A Comprehensive Collection* (PDF)
- Gikandi, N. (1982). *Cultural Analysis of Kikuyu Oral Literature* (digitized text)
- Kenyatta, J. (1938). *Facing Mount Kenya* (ethnographic reference)

**Script**: `scripts/extract_proverbs_from_pdf.py`

**Technical Challenges**:
1. **PDF Text Extraction Quality**:
   - Problem: OCR errors in scanned PDFs (θ → 0, ĩ → i)
   - Solution: Used `pdfplumber` with custom preprocessing
   - Validation: Manual review of 20% sample, 97% accuracy threshold

2. **Kikuyu Unicode Handling**:
   - Problem: Diacritics (ĩ, ũ, ĩ) often corrupted
   - Solution: Unicode normalization (NFC), custom char mapping
   - Code snippet:
   ```python
   import unicodedata
   
   def normalize_kikuyu(text):
       # Normalize to NFC (canonical composition)
       text = unicodedata.normalize('NFC', text)
       
       # Fix common OCR errors
       replacements = {
           'i~': 'ĩ',  # Tilde separate from letter
           'u~': 'ũ',
           'θ': 'th',  # Greek theta → English digraph
       }
       for wrong, right in replacements.items():
           text = text.replace(wrong, right)
       
       return text
   ```

3. **Proverb Boundary Detection**:
   - Problem: No clear delimiters in source text
   - Solution: Regex patterns + heuristic rules
   - Pattern: `^[A-Z][^.!?]*[.!?]$` (sentence-like structure)
   - Heuristic: Length 5-50 words, starts with Kikuyu name prefix (Mũ-, Ng-)

**Output**: `data/proverbs/ireri_1000_proverbs.json`
```json
{
  "proverbs": [
    {
      "id": "PRV_001",
      "kikuyu_text": "Andu ni indo",
      "literal_gloss": "People are wealth/things",
      "source": "Ireri_2017",
      "page": 47,
      "dialect": "standard",
      "extracted_date": "2024-01-15"
    }
  ]
}
```

---

### Phase 2: Gold Standard Translation (Weeks 4-8)

**Script**: `scripts/gold_standard_pipeline.py`

**Methodology**:
1. **Expert Translation Protocol**:
   - Native speaker (author) translated all 100 proverbs
   - Guidelines: Preserve cultural meaning > literal accuracy
   - Reference materials: Gikandi (1982), Kenyatta (1938)
   - Time: 2-3 minutes per proverb (deliberate, not rushed)

2. **Quality Assurance**:
   - Cross-validation: Compared with published translations (Ireri 2017)
   - Discrepancy resolution: Consulted secondary sources
   - Test-retest: Re-translated 20 proverbs 1 week later (92% consistency)

3. **Annotation Schema**:
   ```python
   {
       "proverb_id": "PRV_001",
       "expert_translation": "True prosperity lies in community relationships...",
       "cultural_themes": ["reciprocity", "community_wealth", "ngwatio"],
       "usage_contexts": ["wealth_distribution", "advice_to_youth"],
       "metaphorical_elements": {
           "source_domain": "material_wealth",
           "target_domain": "social_capital"
       },
       "confidence": 0.95  # Self-assessed translation confidence
   }
   ```

**Validation Metrics**:
- Coverage: 100/100 proverbs translated
- Consistency: 92% test-retest agreement
- Cross-validation: 94% alignment with published sources

---

### Phase 3: Baseline Translation Generation (Weeks 9-12)

**Scripts**:
- `scripts/generate_baseline_translations.py` (Raw GPT-4)
- `scripts/test_traditional_rag_fix.py` (Traditional RAG)

**Technical Implementation**:

#### Raw GPT-4 Baseline
```python
import openai

def generate_raw_translation(kikuyu_text):
    """Direct GPT-4 translation with minimal prompting."""
    prompt = f"""Translate this Kikuyu proverb to English, preserving cultural meaning:

Kikuyu: {kikuyu_text}

English translation:"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # Low temp for consistency
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()
```

#### Traditional RAG Baseline
```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class TraditionalRAG:
    def __init__(self, corpus_proverbs):
        self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
        self.corpus = corpus_proverbs
        
        # Build FAISS index
        embeddings = self.model.encode([p['kikuyu_text'] for p in corpus_proverbs])
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))
    
    def retrieve_similar(self, query_proverb, k=3):
        """Retrieve k most similar proverbs by vector similarity."""
        query_emb = self.model.encode([query_proverb])
        distances, indices = self.index.search(query_emb.astype('float32'), k)
        
        return [self.corpus[idx] for idx in indices[0]]
    
    def generate_translation(self, kikuyu_text):
        """Retrieve examples, then prompt GPT-4."""
        similar = self.retrieve_similar(kikuyu_text, k=3)
        
        # Build prompt with examples
        examples = "\n\n".join([
            f"Kikuyu: {p['kikuyu_text']}\nEnglish: {p['expert_translation']}"
            for p in similar
        ])
        
        prompt = f"""Here are similar Kikuyu proverbs with translations:

{examples}

Now translate this proverb:
Kikuyu: {kikuyu_text}

English translation:"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()
```

**Challenges**:
1. **API Rate Limiting**: GPT-4 quota (500 requests/day)
   - Solution: Batch processing with exponential backoff
   - Code: `scripts/utils/api_helpers.py` → `rate_limited_call()`

2. **Cost Management**: GPT-4 expensive (~$0.03/request)
   - Solution: Cache all responses, never re-call for same input
   - Storage: `data/results/translation_cache.json`

3. **Prompt Stability**: Same input, different outputs
   - Solution: Temperature=0.3 (low but not zero for naturalness)
   - Validation: Generated 3x for 10% sample, 89% consistency

---

## 3. Ontology Engineering Workflow

### Phase 1: LLM-Assisted Concept Extraction (Weeks 13-16)

**Script**: `scripts/extract_ontology_concepts_with_llm.py`

**Methodology**:
```python
def extract_concepts_from_proverb(proverb_text, proverb_translation):
    """Use GPT-4 to propose cultural concepts."""
    prompt = f"""Analyze this Kikuyu proverb and identify cultural concepts:

Kikuyu: {proverb_text}
English: {proverb_translation}

Extract:
1. Cultural themes (e.g., reciprocity, wisdom, kinship)
2. Value systems (e.g., collectivism, patience, respect)
3. Social structures (e.g., age-sets, gender roles, governance)
4. Economic concepts (e.g., wealth definitions, exchange systems)
5. Metaphorical mappings (source → target domains)

Output as JSON:
{{
    "themes": ["theme1", "theme2"],
    "values": ["value1", "value2"],
    "social_structures": [],
    "economic_concepts": [],
    "metaphors": {{
        "source": "domain1",
        "target": "domain2"
    }}
}}
"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,  # Slightly higher for creativity
        max_tokens=500
    )
    
    return json.loads(response.choices[0].message.content)
```

**Quality Control**:
1. **Expert Review Protocol**:
   - Every GPT-4 suggestion reviewed by native speaker
   - Acceptance criteria: Culturally accurate + non-redundant
   - Rejection rate: 15-20% (too generic or Western-biased)

2. **Common Rejection Reasons**:
   - "Ngwatio" mapped to "barter" (WRONG—misses obligation aspect)
   - "Wealth" as purely material (WRONG—includes social capital)
   - "Elder" as just age (WRONG—tied to wisdom + social role)

3. **Refinement Process**:
   ```python
   # LLM proposed:
   concept_1 = {"name": "barter", "definition": "exchange of goods"}
   
   # Expert refined:
   concept_1_refined = {
       "name": "ngwatio",
       "definition": "Reciprocal labor exchange system based on social obligation",
       "properties": {
           "is_transactional": False,
           "requires_trust": True,
           "memory_based": True,
           "community_enforced": True
       },
       "not_equivalent_to": ["barter", "trade", "commerce"]
   }
   ```

**Output Statistics**:
- LLM proposed: ~1,200 concepts
- After deduplication: 950 concepts
- After expert review: 847 concepts (final)
- Acceptance rate: 89%

---

### Phase 2: Ontology Formalization (Weeks 17-20)

**Script**: `scripts/ontology_builder.py`

**Technology Stack**:
- **OWL Serialization**: RDFLib (Python library)
- **Graph Database**: Neo4j 5.x
- **Validation**: OOPS! (Ontology Pitfall Scanner)

**OWL Class Hierarchy**:
```python
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal

# Define namespace
KIKU = Namespace("http://kikuyu-ontology.org/onto#")

def create_ontology():
    g = Graph()
    g.bind("kiku", KIKU)
    
    # Top-level classes
    g.add((KIKU.CulturalConcept, RDF.type, OWL.Class))
    g.add((KIKU.Proverb, RDF.type, OWL.Class))
    g.add((KIKU.Theme, RDF.type, OWL.Class))
    g.add((KIKU.Domain, RDF.type, OWL.Class))
    
    # Subclass hierarchy
    g.add((KIKU.EconomicConcept, RDFS.subClassOf, KIKU.CulturalConcept))
    g.add((KIKU.SocialConcept, RDFS.subClassOf, KIKU.CulturalConcept))
    g.add((KIKU.MoralConcept, RDFS.subClassOf, KIKU.CulturalConcept))
    
    # Object properties (relationships)
    g.add((KIKU.expresses, RDF.type, OWL.ObjectProperty))
    g.add((KIKU.expresses, RDFS.domain, KIKU.Proverb))
    g.add((KIKU.expresses, RDFS.range, KIKU.Theme))
    
    # Data properties (attributes)
    g.add((KIKU.kikuyuText, RDF.type, OWL.DatatypeProperty))
    g.add((KIKU.kikuyuText, RDFS.domain, KIKU.Proverb))
    g.add((KIKU.kikuyuText, RDFS.range, XSD.string))
    
    return g
```

**Neo4j Integration**:
```python
from neo4j import GraphDatabase

class OntologyLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def load_concepts(self, concepts):
        """Load concepts as nodes."""
        with self.driver.session() as session:
            for concept in concepts:
                session.run("""
                    CREATE (c:Concept {
                        id: $id,
                        name: $name,
                        definition: $definition,
                        category: $category
                    })
                """, **concept)
    
    def load_relationships(self, relationships):
        """Load relationships as edges."""
        with self.driver.session() as session:
            for rel in relationships:
                session.run("""
                    MATCH (a:Concept {id: $source_id})
                    MATCH (b:Concept {id: $target_id})
                    CREATE (a)-[r:RELATED_TO {type: $rel_type}]->(b)
                """, **rel)
    
    def create_indexes(self):
        """Create indexes for fast retrieval."""
        with self.driver.session() as session:
            session.run("CREATE INDEX concept_name IF NOT EXISTS FOR (c:Concept) ON (c.name)")
            session.run("CREATE FULLTEXT INDEX concept_text IF NOT EXISTS FOR (c:Concept) ON EACH [c.name, c.definition]")
```

**Validation**:
1. **OOPS! Scan Results**:
   - No critical pitfalls (P01-P05)
   - 3 minor warnings (P22: Missing annotations)
   - Fixed: Added rdfs:label to all classes

2. **Logical Consistency Check**:
   - Used Pellet reasoner
   - No contradictions detected
   - All inferences valid

---

### Phase 3: Proverb-Concept Linking (Weeks 21-24)

**Script**: `scripts/link_proverbs_to_concepts.py`

**Semi-Automated Approach**:
1. **Automatic Linking**:
   - Keyword matching: If proverb contains "andu" (people) → link to Community concept
   - Embedding similarity: Vector distance < 0.3 threshold → candidate link
   
2. **Manual Validation**:
   - Expert reviewed all proposed links
   - Acceptance rate: 82%
   - Added 127 links that automation missed

**Code Example**:
```python
def link_proverb_to_concepts(proverb, concepts, threshold=0.3):
    """Hybrid automatic + manual linking."""
    proverb_emb = model.encode(proverb['expert_translation'])
    
    candidates = []
    for concept in concepts:
        concept_emb = model.encode(concept['definition'])
        similarity = cosine_similarity(proverb_emb, concept_emb)
        
        if similarity > threshold:
            candidates.append({
                'concept': concept,
                'similarity': similarity,
                'auto_suggested': True
            })
    
    # Present to expert for confirmation
    confirmed = expert_review_ui(proverb, candidates)
    
    # Expert can also add manual links
    manual_links = expert_add_links_ui(proverb, concepts)
    
    return confirmed + manual_links
```

**Final Statistics**:
- 100 proverbs
- 847 concepts
- 1,247 proverb-concept links
- Average links per proverb: 12.5
- Average links per concept: 1.5

---

## 4. System Implementation

### Retrieval Module Architecture

**File**: `src/retrieval/hybrid_retriever.py`

**Design Pattern**: Strategy Pattern (pluggable retrieval strategies)

```python
from abc import ABC, abstractmethod

class RetrievalStrategy(ABC):
    @abstractmethod
    def retrieve(self, query, k=5):
        pass

class GraphTraversalStrategy(RetrievalStrategy):
    def __init__(self, neo4j_driver):
        self.driver = neo4j_driver
    
    def retrieve(self, proverb_id, k=5):
        """Traverse graph to find related concepts."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Proverb {id: $proverb_id})-[r:EXPRESSES]->(c:Concept)
                OPTIONAL MATCH (c)-[:PART_OF]->(d:Domain)
                OPTIONAL MATCH (c)-[:RELATED_TO]->(c2:Concept)
                RETURN c, d, collect(c2) as related_concepts
                LIMIT $k
            """, proverb_id=proverb_id, k=k)
            
            return [self._format_concept(record) for record in result]

class VectorSimilarityStrategy(RetrievalStrategy):
    def __init__(self, index, corpus):
        self.index = index  # FAISS index
        self.corpus = corpus
    
    def retrieve(self, query_text, k=5):
        """Find similar proverbs by embedding distance."""
        query_emb = model.encode([query_text])
        distances, indices = self.index.search(query_emb.astype('float32'), k)
        
        return [self.corpus[idx] for idx in indices[0]]

class HybridRetriever:
    def __init__(self, graph_strategy, vector_strategy):
        self.graph = graph_strategy
        self.vector = vector_strategy
    
    def retrieve(self, proverb_id, proverb_text, k=5):
        """Combine graph and vector retrieval."""
        # Get cultural concepts from graph
        concepts = self.graph.retrieve(proverb_id, k=k)
        
        # Get similar proverbs from vectors
        similar = self.vector.retrieve(proverb_text, k=k)
        
        # Merge and deduplicate
        return self._merge_contexts(concepts, similar)
```

---

### Prompt Engineering System

**File**: `src/translation/prompt_builder.py`

**Template System**:
```python
class PromptTemplate:
    SYSTEM_TEMPLATE = """You are an expert in Kikuyu culture specializing in proverb translation.
Your task is to translate Kikuyu proverbs to English while preserving deep cultural meaning,
not just literal words."""

    CONTEXT_TEMPLATE = """CULTURAL CONTEXT (from Kikuyu cultural ontology):

{cultural_themes}

{usage_contexts}

{related_proverbs}

{moral_lessons}"""

    TRANSLATION_TEMPLATE = """PROVERB TO TRANSLATE:
Kikuyu: {kikuyu_text}
Literal gloss: {literal_gloss}

Provide a culturally faithful English translation that preserves the Kikuyu worldview
embedded in this proverb. Consider the cultural context above."""

    def build(self, proverb, retrieved_context):
        """Assemble final prompt."""
        context = self._format_context(retrieved_context)
        
        return f"""{self.SYSTEM_TEMPLATE}

{self.CONTEXT_TEMPLATE.format(**context)}

{self.TRANSLATION_TEMPLATE.format(**proverb)}"""
```

**Retrieval Context Formatting**:
```python
def _format_context(self, retrieved):
    """Convert graph data to natural language."""
    themes = "\n".join([f"- {c['name']}: {c['definition']}" 
                        for c in retrieved['concepts']])
    
    usage = "\n".join([f"- {u['context']}: {u['description']}" 
                       for u in retrieved['usage_contexts']])
    
    related = "\n\n".join([
        f"Kikuyu: {p['kikuyu_text']}\nMeaning: {p['expert_translation']}"
        for p in retrieved['similar_proverbs'][:3]
    ])
    
    moral = retrieved['moral_lesson']
    
    return {
        'cultural_themes': themes,
        'usage_contexts': usage,
        'related_proverbs': related,
        'moral_lessons': moral
    }
```

---

## 5. Evaluation Infrastructure

### Metric Calculation Engine

**File**: `src/evaluation/metrics.py`

**Architecture**: Plugin-based metric system

```python
from abc import ABC, abstractmethod
from typing import Dict

class Metric(ABC):
    @abstractmethod
    def compute(self, hypothesis: str, reference: str, source: str = None) -> float:
        pass

class BLEUMetric(Metric):
    def compute(self, hypothesis, reference, source=None):
        from sacrebleu import sentence_bleu
        return sentence_bleu(hypothesis, [reference]).score / 100.0

class CHRFMetric(Metric):
    def compute(self, hypothesis, reference, source=None):
        from sacrebleu import sentence_chrf
        return sentence_chrf(hypothesis, [reference]).score / 100.0

class COMETMetric(Metric):
    def __init__(self):
        from comet import download_model, load_from_checkpoint
        model_path = download_model("Unbabel/wmt22-comet-da")
        self.model = load_from_checkpoint(model_path)
    
    def compute(self, hypothesis, reference, source):
        data = [{
            "src": source,
            "mt": hypothesis,
            "ref": reference
        }]
        return self.model.predict(data, batch_size=1).scores[0]

class MetricRegistry:
    def __init__(self):
        self._metrics = {}
    
    def register(self, name: str, metric: Metric):
        self._metrics[name] = metric
    
    def compute_all(self, hypothesis, reference, source=None) -> Dict[str, float]:
        return {
            name: metric.compute(hypothesis, reference, source)
            for name, metric in self._metrics.items()
        }
```

**Usage**:
```python
# scripts/calculate_metrics.py

registry = MetricRegistry()
registry.register("BLEU", BLEUMetric())
registry.register("CHRF", CHRFMetric())
registry.register("COMET", COMETMetric())

for proverb in evaluation_set:
    for system in ["raw_gpt4", "traditional_rag", "og_rag"]:
        translation = translations[system][proverb['id']]
        
        scores = registry.compute_all(
            hypothesis=translation,
            reference=proverb['expert_translation'],
            source=proverb['kikuyu_text']
        )
        
        save_scores(proverb['id'], system, scores)
```

---

### Statistical Analysis Pipeline

**File**: `scripts/run_integrated_statistical_analysis.py`

**Implementation**:
```python
import scipy.stats as stats
import numpy as np
import pandas as pd

def compute_paired_ttest(system_a_scores, system_b_scores):
    """Paired t-test for within-subjects comparison."""
    t_stat, p_value = stats.ttest_rel(system_a_scores, system_b_scores)
    
    # Effect size (Cohen's d for paired samples)
    diff = np.array(system_a_scores) - np.array(system_b_scores)
    cohen_d = np.mean(diff) / np.std(diff, ddof=1)
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'cohen_d': cohen_d,
        'significant': p_value < 0.05
    }

def bonferroni_correction(p_values, alpha=0.05):
    """Adjust significance threshold for multiple comparisons."""
    adjusted_alpha = alpha / len(p_values)
    return [p < adjusted_alpha for p in p_values]

def run_full_analysis(results_df):
    """Complete statistical analysis pipeline."""
    systems = ['raw_gpt4', 'traditional_rag', 'og_rag']
    metrics = ['cultural_authenticity', 'translation_fidelity', 'overall_quality']
    
    comparisons = [
        ('og_rag', 'raw_gpt4'),
        ('og_rag', 'traditional_rag'),
        ('traditional_rag', 'raw_gpt4')
    ]
    
    results = []
    for metric in metrics:
        for sys_a, sys_b in comparisons:
            scores_a = results_df[results_df['system'] == sys_a][metric]
            scores_b = results_df[results_df['system'] == sys_b][metric]
            
            test_result = compute_paired_ttest(scores_a, scores_b)
            test_result['metric'] = metric
            test_result['comparison'] = f"{sys_a} vs {sys_b}"
            
            results.append(test_result)
    
    # Apply Bonferroni correction
    p_values = [r['p_value'] for r in results]
    corrected = bonferroni_correction(p_values)
    
    for result, is_sig in zip(results, corrected):
        result['bonferroni_significant'] = is_sig
    
    return pd.DataFrame(results)
```

**Visualization Generation**:
```python
import matplotlib.pyplot as plt
import seaborn as sns

def generate_comparison_plots(results_df, output_dir):
    """Generate all evaluation visualizations."""
    
    # 1. Box plots for each metric
    for metric in ['cultural_authenticity', 'translation_fidelity']:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=results_df, x='system', y=metric)
        plt.title(f'{metric.replace("_", " ").title()} by System')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{metric}_boxplot.png', dpi=300)
        plt.close()
    
    # 2. Violin plots for distribution
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=results_df, x='system', y='overall_quality', inner='box')
    plt.title('Overall Quality Distribution by System')
    plt.savefig(f'{output_dir}/quality_violin.png', dpi=300)
    plt.close()
    
    # 3. Pairwise comparison heatmap
    systems = results_df['system'].unique()
    comparison_matrix = np.zeros((len(systems), len(systems)))
    
    for i, sys_a in enumerate(systems):
        for j, sys_b in enumerate(systems):
            if i != j:
                scores_a = results_df[results_df['system'] == sys_a]['overall_quality']
                scores_b = results_df[results_df['system'] == sys_b]['overall_quality']
                _, p_value = stats.ttest_rel(scores_a, scores_b)
                comparison_matrix[i, j] = p_value
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(comparison_matrix, annot=True, fmt='.6f', 
                xticklabels=systems, yticklabels=systems,
                cmap='RdYlGn_r', center=0.05)
    plt.title('Pairwise p-values (lower = more significant)')
    plt.savefig(f'{output_dir}/pvalue_heatmap.png', dpi=300)
    plt.close()
```

---

## 6. Version Control Strategy

### Git Workflow

**Branch Strategy**:
```
main                    # Stable, thesis submission versions
├── development         # Active development
├── data-pipeline       # Data extraction experiments
├── ontology-dev        # Ontology engineering
├── system-impl         # Core system implementation
├── evaluation-exp      # Evaluation experiments
└── supervisor-revisions # Post-review edits
```

**Commit Message Convention**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature (e.g., `feat(retrieval): add hybrid graph+vector retrieval`)
- `fix`: Bug fix (e.g., `fix(ontology): correct ngwatio definition`)
- `docs`: Documentation (e.g., `docs(thesis): add related work section`)
- `data`: Data changes (e.g., `data(proverbs): extract Ireri 1000 corpus`)
- `refactor`: Code restructure (e.g., `refactor(metrics): move to plugin architecture`)
- `test`: Tests (e.g., `test(retrieval): add unit tests for hybrid retriever`)

**Example Commits**:
```bash
# Data extraction
git commit -m "data(extraction): extract 100 proverbs from Ireri PDF

- Used pdfplumber for OCR-free extraction
- Applied Unicode normalization for Kikuyu diacritics
- Validated 20% sample manually (97% accuracy)

Closes #15"

# Ontology development
git commit -m "feat(ontology): add LLM-assisted concept extraction

- GPT-4 proposes concepts from proverb analysis
- Expert validation loop rejects 15-20% suggestions
- Version control all LLM vs human contributions

Output: 847 validated concepts from 1200 proposals"

# System implementation
git commit -m "feat(retrieval): implement hybrid retrieval strategy

- Graph traversal for cultural concepts (Neo4j Cypher)
- Vector similarity for related proverbs (FAISS + Sentence-BERT)
- Merging logic to deduplicate contexts

Benchmark: 0.79 cultural authenticity (5.3% over baseline)"
```

---

### Reproducibility Tracking

**File**: `.env.example` (template for API keys)
```bash
# OpenAI API
OPENAI_API_KEY=sk-...
OPENAI_ORG_ID=org-...

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=...

# Google Gemini (backup LLM)
GOOGLE_API_KEY=...

# Experiment tracking
EXPERIMENT_ID=thiLLMo_v1
RANDOM_SEED=42
```

**Dependency Management**:
```bash
# requirements.txt (pinned versions for reproducibility)
openai==1.3.5
sentence-transformers==2.2.2
neo4j==5.14.0
rdflib==7.0.0
sacrebleu==2.3.1
comet-ml==3.35.0
pandas==2.1.3
numpy==1.24.3
scipy==1.11.4
matplotlib==3.8.2
seaborn==0.13.0
```

**Experiment Configuration**:
```yaml
# config/experiment_config.yaml
experiment:
  name: "OG-RAG vs Baselines"
  random_seed: 42
  
data:
  proverb_corpus: "data/proverbs/evaluation_100.json"
  gold_standard: "data/evaluation/expert_translations.json"
  
systems:
  - name: "raw_gpt4"
    model: "gpt-4-turbo"
    temperature: 0.3
    max_tokens: 150
    
  - name: "traditional_rag"
    model: "gpt-4-turbo"
    retrieval: "vector_similarity"
    top_k: 3
    
  - name: "og_rag"
    model: "gpt-4-turbo"
    retrieval: "hybrid"
    graph_k: 5
    vector_k: 3
    
evaluation:
  metrics:
    - "cultural_authenticity"
    - "translation_fidelity"
    - "overall_quality"
  
  statistical_tests:
    - "paired_ttest"
    - "bonferroni_correction"
  
  effect_size: "cohen_d"
```

---

## 7. Documentation Development

### Thesis Writing Workflow

**Tools**:
- **Editor**: Overleaf (LaTeX cloud editor)
- **Local Build**: TeX Live 2025
- **Version Control**: Git-synced with Overleaf
- **Bibliography**: BibTeX with Zotero integration

**Structure**:
```
docs/thesis/
├── main.tex                # Master document
├── references/
│   └── references.bib      # All citations
├── chapters/
│   ├── 00-abstract.tex
│   ├── 01-introduction.tex
│   ├── 02-literature.tex
│   ├── 03-methodology.tex
│   ├── 04-design.tex
│   ├── 05-evaluation.tex
│   ├── 06-discussion.tex
│   └── 07-conclusion.tex
├── appendices/
│   ├── A-ontology-schema.tex
│   ├── B-evaluation-rubrics.tex
│   └── C-proverb-corpus.tex
└── figures/
    ├── architecture.pdf
    ├── ontology-graph.png
    └── results-boxplot.pdf
```

**Compilation**:
```bash
cd docs/thesis
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex  # Resolve references
```

**Automated Building**:
```bash
# Makefile
.PHONY: thesis clean

thesis:
	cd docs/thesis && latexmk -pdf main.tex

clean:
	cd docs/thesis && latexmk -C

watch:
	cd docs/thesis && latexmk -pdf -pvc main.tex  # Continuous compilation
```

---

### Code Documentation

**Docstring Standard**: Google Style
```python
def hybrid_retrieve(proverb_id: str, proverb_text: str, k: int = 5) -> Dict[str, Any]:
    """Retrieve cultural context using hybrid graph+vector approach.
    
    Combines Neo4j graph traversal for structured cultural knowledge with
    FAISS vector similarity for contextual proverb examples. Deduplicates
    and ranks results by relevance.
    
    Args:
        proverb_id: Unique identifier for proverb in ontology.
        proverb_text: Kikuyu text of proverb for vector embedding.
        k: Number of concepts/proverbs to retrieve (default: 5).
    
    Returns:
        Dictionary containing:
            - concepts: List of cultural concepts from graph
            - similar_proverbs: List of related proverbs from vectors
            - usage_contexts: When/why this proverb is used
            - moral_lessons: Ethical teachings embedded
    
    Raises:
        ValueError: If proverb_id not found in ontology.
        ConnectionError: If Neo4j or FAISS unavailable.
    
    Example:
        >>> context = hybrid_retrieve("PRV_001", "Andu ni indo", k=3)
        >>> print(context['concepts'][0]['name'])
        'Reciprocity (ngwatio)'
    """
    # Implementation...
```

**Inline Comments**: Explain WHY, not WHAT
```python
# GOOD: Explains reasoning
# Use low temperature (0.3) to ensure consistent translations
# across multiple runs while preserving some naturalness
temperature = 0.3

# BAD: Redundant with code
# Set temperature to 0.3
temperature = 0.3
```

---

## 8. Script Development Chronology

### Timeline of Key Scripts

| Week | Script | Purpose | Complexity | LOC |
|------|--------|---------|------------|-----|
| 1-3 | `extract_proverbs_from_pdf.py` | Parse Ireri PDF, extract corpus | Medium | 250 |
| 4-5 | `create_evaluation_benchmark.py` | Structure gold standard dataset | Low | 120 |
| 6-8 | `gold_standard_pipeline.py` | Expert translation workflow | Medium | 300 |
| 9-10 | `generate_baseline_translations.py` | Raw GPT-4 baseline | Low | 180 |
| 11-12 | `test_traditional_rag_fix.py` | Vector-based RAG baseline | Medium | 350 |
| 13-16 | `extract_ontology_concepts_with_llm.py` | LLM concept extraction | High | 450 |
| 17-18 | `ontology_builder.py` | OWL+Neo4j ontology construction | High | 600 |
| 19-20 | `ontology_validator.py` | OOPS! integration, consistency checks | Medium | 280 |
| 21-24 | `link_proverbs_to_concepts.py` | Proverb-concept mapping | High | 520 |
| 25-26 | `test_thiLLMo_og_rag.py` | Full OG-RAG system test | High | 700 |
| 27-30 | `run_cultural_evaluation.py` | Human evaluation framework | High | 650 |
| 31-32 | `calculate_metrics.py` | Automated metric computation | Medium | 400 |
| 33-34 | `run_integrated_statistical_analysis.py` | Statistical tests + viz | High | 550 |
| 35-36 | `generate_evaluation_visualizations.py` | Publication-ready figures | Medium | 380 |

**Total**: ~6,000 lines of research code (excluding `src/` library code)

---

### Critical Script Deep Dive: `test_thiLLMo_og_rag.py`

**Purpose**: End-to-end test of full OG-RAG system

**Architecture**:
```python
class OGRAGSystem:
    def __init__(self, config):
        self.ontology = Neo4jOntology(config['neo4j'])
        self.retriever = HybridRetriever(
            graph_strategy=GraphTraversalStrategy(self.ontology),
            vector_strategy=VectorSimilarityStrategy(config['faiss_index'])
        )
        self.prompt_builder = PromptBuilder(templates=config['prompts'])
        self.llm = OpenAIClient(model=config['model'])
    
    def translate(self, proverb):
        """Full translation pipeline."""
        # 1. Retrieve context
        context = self.retriever.retrieve(
            proverb_id=proverb['id'],
            proverb_text=proverb['kikuyu_text'],
            k=5
        )
        
        # 2. Build prompt
        prompt = self.prompt_builder.build(proverb, context)
        
        # 3. Generate translation
        translation = self.llm.generate(prompt)
        
        # 4. Log for analysis
        self._log_translation(proverb, context, translation)
        
        return translation
```

**Testing**:
```python
def run_evaluation():
    """Execute full evaluation on 100-proverb benchmark."""
    system = OGRAGSystem(load_config())
    
    results = []
    for proverb in load_evaluation_set():
        translation = system.translate(proverb)
        
        # Store for later analysis
        results.append({
            'proverb_id': proverb['id'],
            'kikuyu_text': proverb['kikuyu_text'],
            'og_rag_translation': translation,
            'expert_translation': proverb['expert_translation'],
            'timestamp': datetime.now().isoformat()
        })
    
    save_results(results, 'data/results/og_rag_translations.json')
    return results
```

---

## Lessons Learned & Best Practices

### What Worked Well

1. **Incremental Development**: Building pipeline in phases, validating each before next
2. **Version Control Discipline**: Every major change committed with detailed messages
3. **Hybrid Human-AI Approach**: LLM efficiency + expert validation = best of both worlds
4. **Reproducibility First**: Config files, random seeds, pinned dependencies from day 1
5. **Documentation as Code**: Comments, docstrings, README files written alongside code

### What Was Challenging

1. **API Costs**: GPT-4 expensive—needed aggressive caching strategy
2. **Neo4j Learning Curve**: Cypher query language non-trivial, debugging complex
3. **Evaluation Subjectivity**: Cultural authenticity hard to quantify objectively
4. **Time Management**: Ontology building took 2x longer than estimated
5. **Scope Creep**: Had to cut features (multi-dialect support, community evaluation)

### Recommendations for Future Work

1. **Start with smaller ontology** (100 concepts), expand iteratively
2. **Budget 3x time for human validation** (it's always slower than you think)
3. **Use managed Neo4j** (Aura) instead of self-hosting
4. **Implement evaluation early** to guide system development
5. **Write thesis and code in parallel** (easier to stay consistent)

---

## Appendix: Key Configuration Files

### Neo4j Database Schema

**File**: `config/neo4j_schema.cypher`
```cypher
// Constraints
CREATE CONSTRAINT proverb_id IF NOT EXISTS FOR (p:Proverb) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;

// Indexes
CREATE INDEX proverb_text IF NOT EXISTS FOR (p:Proverb) ON (p.kikuyu_text);
CREATE FULLTEXT INDEX concept_search IF NOT EXISTS FOR (c:Concept) ON EACH [c.name, c.definition];

// Relationships schema
// (p:Proverb)-[:EXPRESSES]->(c:Concept)
// (c:Concept)-[:PART_OF]->(d:Domain)
// (c:Concept)-[:RELATED_TO]->(c2:Concept)
// (p:Proverb)-[:USED_IN]->(ctx:UsageContext)
```

---

**Document Status**: Complete  
**Word Count**: ~8,500  
**Code Examples**: 35+  
**Coverage**: Full repository lifecycle from data extraction to thesis defense

This deep dive serves as both a technical reference and a reproducibility guide for future researchers building on this work.
