# Thesis Presentation Guide - ELI5/ELI10 Explanations

**Purpose**: Simple explanations of technical terms for thesis defense presentations and non-specialist audiences  
**Created**: December 27, 2025  
**For**: thiLLMo dissertation defense

---

## Cultural Concepts

### Ngwatio (Reciprocity Systems)

**ELI10**: Imagine if instead of using money, your community kept track of favors. If you help someone harvest their crops today, they'll help you build your house tomorrow. Everyone remembers who helped who, and the community makes sure everyone participates fairly. That's ngwatio - a traditional Kikuyu system where people exchange labor and resources based on trust and memory, not cash.

**Key Point**: It's like a social bank account where deposits and withdrawals are favors, not money.

**Why It Matters**: Many Kikuyu proverbs reference ngwatio, so our translation system needs to understand this isn't just "trade" - it's a whole social system with rules about obligation, honor, and community relationships.

---

### Traditional Banking Systems

**ELI10**: Before modern banks, Kikuyu communities had their own ways of saving and lending. Groups of friends (called "chamas") would meet monthly - everyone puts in money, and one person takes the whole pot home. Next month, a different person gets the pot. It rotates until everyone has had a turn. This builds trust and helps people save for big purchases.

**Key Point**: Like a rotating savings club where your friends ARE the bank.

**Why It Matters**: Proverbs about wealth often reference these traditional systems, not Western banking, so direct translation misses the cultural context.

---

## NLP/Translation Metrics

### BLEU (Bilingual Evaluation Understudy)

**ELI5**: Imagine you translated a story from Kikuyu to English. BLEU checks how many words and phrases in your translation match a "perfect" translation done by an expert. The more matches, the higher your score (0-100%).

**ELI10**: BLEU looks for word-by-word matches. If the expert wrote "A good person is never poor" and you wrote "A virtuous individual is never destitute," BLEU would give you a LOW score even though the meanings are identical, because the words are different.

**The Problem**: BLEU punishes creative translations. For cultural proverbs, we sometimes NEED different words to capture the cultural meaning, but BLEU doesn't understand that.

**Score Example**: 
- Expert: "People are wealth"
- Translation: "People are wealth" → BLEU: 100% ✅
- Translation: "Community is prosperity" → BLEU: 0% ❌ (even if culturally accurate!)

---

### CHRF (Character n-gram F-score)

**ELI10**: Instead of comparing whole words like BLEU, CHRF compares small chunks of letters (2-3 characters at a time). This is more forgiving of small spelling differences or word variations.

**Example**:
- Expert: "wisdom"
- Translation: "wisdoms" → BLEU sees two different words, CHRF sees mostly matching letters

**Why It's Better**: CHRF catches partial matches. If you translate a word slightly differently but it has similar letters, CHRF gives partial credit.

---

### COMET (Crosslingual Optimized Metric for Evaluation of Translation)

**ELI10**: COMET is like a smart AI judge that understands meaning, not just word matches. It reads the original Kikuyu, the English translation, and the expert reference, then scores how well the meaning was preserved - even if different words were used.

**The Breakthrough**: COMET uses neural networks trained to understand that "A mature woman is never exempt from trouble" and "Wise women always face challenges" convey similar meanings, even with different words.

**Score Range**: -1.0 to 1.0 (higher is better)

**Why It Matters**: For cultural translation, COMET is much better than BLEU because it rewards preserving MEANING over matching WORDS.

---

### Sentence-BERT Embeddings

**ELI5**: Imagine every sentence is a point in space. Sentences with similar meanings are close together; sentences with different meanings are far apart. Sentence-BERT turns sentences into these "points" (called embeddings) so computers can measure how similar two sentences are.

**ELI10**: It's like giving every sentence a unique address in a giant city. Sentences that mean similar things live in the same neighborhood. We can measure the distance between addresses to see how similar sentences are.

**Technical**: Sentence-BERT converts text into 768-dimensional vectors. Cosine similarity between vectors measures semantic similarity.

**Example**:
- "People are wealth" → [0.2, 0.8, 0.1, ... 765 more numbers]
- "Community is prosperity" → [0.19, 0.79, 0.12, ... 765 more numbers]
- Distance: 0.05 (very close = similar meaning!)

---

### Lexical Jaccard Similarity

**ELI10**: Count how many words two sentences have in common, divided by the total unique words in both sentences.

**Formula**: (Shared words) / (All unique words combined)

**Example**:
- Sentence A: "The wise woman helps her community"
- Sentence B: "The elderly woman supports her village"
- Shared words: "The", "woman", "her" = 3 words
- All unique words: "The", "wise", "woman", "helps", "her", "community", "elderly", "supports", "village" = 9 words
- Jaccard: 3/9 = 0.33 (33% similarity)

**Weakness**: Ignores word order and meaning, just counts matches.

---

### Polysemous Terms

**ELI5**: Words that have multiple meanings depending on context.

**Example in English**:
- "Bank" → river bank? money bank?
- "Bat" → baseball bat? flying bat?

**Example in Kikuyu**:
- "Mũtĩ" → tree? medicine? lineage/family heritage?

**Why It Matters**: Our ontology helps the AI figure out which meaning is correct in each proverb. Without cultural context, the AI might translate "mũtĩ" as "tree" when the proverb actually means "ancestral heritage."

---

### Denotative Meaning

**ELI10**: The literal, dictionary definition of a word, without emotions or cultural context.

**Example**:
- "Home" 
  - **Denotative** (literal): A building where people live
  - **Connotative** (cultural): Family, safety, belonging, childhood memories

**In Translation**:
- Kikuyu: "Mũciĩ" literally means "homestead/house"
- But culturally: It means family unity, ancestral land, identity, cultural roots

**The Challenge**: Machine translation often captures denotative meaning (literal house) but misses connotative meaning (cultural home). Our ontology adds the cultural layer.

---

## Statistical Methods

### Statistical Power (Cohen's d)

**ELI10**: When we test if our system is better than the baseline, we want to know two things:
1. Is there a real difference? (significance)
2. How BIG is the difference? (effect size)

Cohen's d measures the SIZE of the improvement:
- **d = 0.2**: Small effect (barely noticeable)
- **d = 0.5**: Medium effect (clearly visible)
- **d = 0.8+**: Large effect (impossible to miss)

**Our Result**: OG-RAG vs Raw GPT-4 had Cohen's d ≈ 0.7 (medium-to-large effect)

**Translation**: Not only is our system statistically better, but the improvement is SUBSTANTIAL, not just a tiny technical gain.

---

### Hypothesis Testing

**ELI5**: We make a guess (hypothesis) and then test if the data supports it.

**ELI10**: 
1. **Null Hypothesis (H0)**: Our system is NO BETTER than the baseline (any difference is just random luck)
2. **Alternative Hypothesis (H1)**: Our system IS BETTER than the baseline (the difference is real)

We run statistical tests and calculate the probability that H0 is true. If that probability is very low (< 5%), we reject H0 and accept H1.

**Our Research**:
- H1: Ontology-grounded RAG improves cultural authenticity
- H2: Ontology-grounded RAG improves translation fidelity
- H3: OG-RAG outperforms Traditional RAG

All three hypotheses were confirmed (p < 0.000001).

---

### Paired t-tests

**ELI10**: Imagine testing two medicines on the same group of patients. You measure each patient's health BEFORE and AFTER each medicine, then compare the differences.

Paired t-test checks if the average improvement from Medicine A is significantly different from Medicine B, accounting for individual variation.

**Our Use**: We tested all three systems (OG-RAG, Traditional RAG, Raw GPT-4) on the SAME 100 proverbs. For each proverb, we compared the scores. Paired t-test tells us if the differences are real or just random noise.

**Result**: 
- OG-RAG vs Raw GPT-4: t = 7.468, **p < 0.000001** ✅ (huge difference!)
- OG-RAG vs Traditional RAG: t = 5.341, **p < 0.000001** ✅ (big difference!)

---

### Bonferroni Correction

**ELI10**: If you flip a coin 100 times, you might accidentally get 10 heads in a row just by chance. The more tests you run, the more likely you are to see "false positives" (patterns that don't actually mean anything).

Bonferroni correction adjusts your significance threshold when running multiple tests to avoid being fooled by random chance.

**Formula**: If you run 3 tests and want 95% confidence, instead of accepting p < 0.05, you require p < 0.05/3 = 0.0167.

**Our Case**: We ran 3 pairwise comparisons (OG-RAG vs GPT, OG-RAG vs TRAD, TRAD vs GPT), so technically we should use p < 0.0167 as our threshold. All our p-values were < 0.000001, so we easily pass even with Bonferroni correction.

---

### Krippendorff's Alpha

**ELI10**: When two people rate the same translations, how often do they agree? Krippendorff's alpha measures agreement while accounting for chance.

**Scale**:
- α = 0: Agreement no better than random guessing
- α = 0.67: Minimum acceptable agreement
- α = 0.80: Good agreement
- α = 1.0: Perfect agreement

**Note**: This metric is NOT used in our final thesis because we switched from two evaluators to a single expert evaluator. We kept the explanation because it was mentioned in earlier drafts.

---

## Datasets/Tools

### Musique Dataset

**ELI10**: A benchmark dataset for testing multi-hop question answering. Questions require connecting information from multiple documents to find the answer.

**Example Question**: "What is the capital of the country where the author of 'War and Peace' was born?"
- Step 1: Find author of 'War and Peace' → Leo Tolstoy
- Step 2: Find Tolstoy's birth country → Russia
- Step 3: Find capital of Russia → Moscow

**Why It Matters**: In literature review, we reference MuSiQue to show that multi-hop reasoning (connecting multiple pieces of knowledge) is an active research area. Our ontology enables similar multi-hop reasoning for cultural knowledge.

---

### HotpotQA

**ELI10**: Another multi-hop question-answering dataset requiring reasoning across multiple paragraphs.

**Example**: "What movie did the director of 'Inception' make before 'The Dark Knight'?"
- Find director of Inception → Christopher Nolan
- Find Nolan's movies before The Dark Knight → Batman Begins, The Prestige, etc.

**Relevance**: Demonstrates that structured knowledge graphs improve multi-hop reasoning - same principle we apply to cultural proverb translation.

---

### MedRAG

**ELI10**: A RAG (Retrieval-Augmented Generation) system designed for medical question answering. It retrieves relevant medical knowledge from databases, then uses that knowledge to answer clinical questions accurately.

**Why We Cite It**: MedRAG showed that domain-specific knowledge graphs (in their case, medical ontologies) dramatically improve AI accuracy in specialized domains. Our work applies the same principle to cultural knowledge.

**Example**: 
- Question: "Treatment for Type 2 diabetes?"
- MedRAG retrieves: Guidelines, drug interactions, patient history
- Generates: Evidence-based treatment recommendations

---

### UMLS (Unified Medical Language System)

**ELI10**: A massive medical ontology connecting over 4 million medical concepts across 200+ languages. It defines relationships between diseases, symptoms, treatments, drugs, anatomy, etc.

**Structure**: 
- Concepts: "Diabetes Mellitus Type 2"
- Relationships: causes → "hyperglycemia", treated_by → "metformin"

**Why We Reference It**: UMLS proves that large-scale ontologies can capture domain-specific knowledge effectively. Our Kikuyu cultural ontology (847 concepts) is smaller but follows similar principles for cultural domain.

---

### OOPS! (Ontology Pitfall Scanner)

**ELI10**: A tool that automatically checks ontologies for common mistakes (like circular definitions, missing labels, or contradictory relationships).

**Example Pitfalls**:
- ❌ Circular definition: "Wealth is prosperity, prosperity is wealth"
- ❌ Missing label: Concept has code "C_047" but no human-readable name
- ❌ Orphan class: Concept has no parent or children (isolated)

**Our Use**: We ran OOPS! on our Kikuyu cultural ontology to identify and fix structural issues before using it in the translation system.

---

### OWL (Web Ontology Language)

**ELI5**: A special language for writing ontologies that computers can understand and reason with.

**ELI10**: Think of it like a very strict grammar for defining knowledge. In OWL, you can write rules like:
- "Every Proverb must have exactly one KikuyuText property"
- "If Proverb X expresses Theme Y, and Theme Y is part of Domain Z, then Proverb X relates to Domain Z"

**Example OWL Code**:
```xml
<owl:Class rdf:about="Proverb">
  <rdfs:subClassOf>
    <owl:Restriction>
      <owl:onProperty rdf:resource="hasKikuyuText"/>
      <owl:cardinality>1</owl:cardinality>
    </owl:Restriction>
  </rdfs:subClassOf>
</owl:Class>
```

**Translation**: "Every Proverb must have exactly 1 Kikuyu text (no more, no less)."

**Why We Use It**: OWL lets us define our cultural ontology formally so the computer can automatically check for logical consistency and infer new relationships.

---

## Quick Reference Table

| Term | One-Sentence Summary |
|------|---------------------|
| **ngwatio** | Traditional Kikuyu reciprocity system based on exchanging labor/resources through social obligation |
| **BLEU** | Translation metric that counts word matches (punishes creative translations) |
| **CHRF** | Translation metric that counts character matches (more forgiving than BLEU) |
| **COMET** | AI-powered translation metric that understands meaning, not just words |
| **Sentence-BERT** | Converts sentences into numerical vectors to measure semantic similarity |
| **Jaccard Similarity** | Measures overlap: shared words / total unique words |
| **Polysemous** | Words with multiple meanings (context-dependent) |
| **Denotative** | Literal dictionary definition (without cultural context) |
| **Cohen's d** | Measures effect size (how BIG is the difference?) |
| **Hypothesis Testing** | Statistical method to prove a theory with data |
| **Paired t-test** | Compares two treatments on the same subjects |
| **Bonferroni** | Adjusts significance threshold when running multiple tests |
| **Krippendorff's α** | Measures agreement between multiple raters |
| **MuSiQue/HotpotQA** | Datasets for multi-hop reasoning benchmarks |
| **MedRAG** | Medical RAG system (proof that domain ontologies work) |
| **UMLS** | Massive medical ontology (4M+ concepts) |
| **OOPS!** | Tool that finds mistakes in ontologies |
| **OWL** | Formal language for writing ontologies |

---

## Presentation Tips

### For General Audience (Non-Technical)
- Use the **ELI5** versions
- Focus on cultural concepts (ngwatio, traditional banking) to connect with audience
- Use analogies: "ontology is like a cultural encyclopedia for the AI"
- Avoid statistics - just say "statistically significant improvement"

### For Academic Committee (Technical)
- Use the **ELI10** versions with technical details
- Show actual numbers: p-values, Cohen's d, score comparisons
- Explain why COMET > BLEU for cultural translation
- Reference MedRAG/UMLS as precedents in other domains

### For Computer Science Audience
- Full technical depth: vector embeddings, cosine similarity, OWL semantics
- Dive into architecture: how Neo4j graph traversal feeds into LLM prompts
- Discuss ontology engineering methodology
- Compare with other RAG implementations

### For Cultural Studies Audience
- Emphasize ngwatio, traditional knowledge systems
- Explain why cultural ontologies preserve meaning better than dictionaries
- Discuss ethical implications: who owns cultural knowledge in AI systems?
- Future work: community-driven ontology governance

---

**Document Status**: Ready for thesis defense preparation  
**Last Updated**: December 27, 2025  
**Next Steps**: Practice explaining each term in under 60 seconds
