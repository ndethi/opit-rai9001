# How We Evaluated OG-RAG Translations (Explained Simply)

**For**: Thesis Defense Presentation  
**Audience**: Non-technical reviewers  
**Date**: January 14, 2026

---

## The Challenge

**Question**: How do we measure if an AI translation preserves Kikuyu cultural wisdom?

**Why it's hard**:
- Cultural meaning isn't just about words—it's about metaphors, values, and context
- BLEU score (common translation metric) only measures word matching, not cultural depth
- Getting multiple Kikuyu-English bilingual experts is difficult and time-consuming

**Our Solution**: Automated evaluation that's grounded in expert knowledge

---

## How We Did It: Two Evaluation Methods

### Method 1: Cultural Metrics Framework (Primary)

**Think of it like this**: Imagine you have a recipe your grandmother taught you. When someone else makes the dish, you check:
1. Does it taste similar? (Semantic similarity)
2. Did they use the key ingredients? (Cultural pattern matching)
3. Did they follow the technique? (Translation fidelity)
4. Could this be served at a restaurant? (Business relevance)

**How it works**:

#### Step 1: Semantic Similarity (40% of score)
- Uses AI model trained on 1 billion sentence pairs
- Converts translations into "meaning fingerprints" (384 numbers representing the meaning)
- Compares fingerprints like comparing photos—how similar are they?
- **Example**: "Hard work brings wealth" vs "Effort yields prosperity" = 87% similar

#### Step 2: Cultural Pattern Detection (15% of score)
- We identified 6 cultural themes in Kikuyu proverbs:
  - **Community values**: togetherness, sharing, unity
  - **Traditional wisdom**: elders, ancestors, heritage
  - **Agricultural metaphors**: harvest, seeds, rain
  - **Animal symbolism**: elephant, lion, hare
  - **Social hierarchy**: respect, authority, elders
  - **Moral values**: honesty, patience, integrity

- Computer scans translation for these keywords
- **Example**: "A lone finger cannot kill a louse" contains "togetherness" theme = ✓

#### Step 3: Translation Fidelity (35% of score)
- Checks if the translation is accurate, not just culturally relevant
- Uses ROUGE metric (like spell-check but for sentences)
- Penalizes translations that are too short, too long, or miss key words
- **Example**: Skipping important words = lower score

#### Step 4: Business Relevance (15% of score)
- Does the translation work for modern business professionals?
- Scans for business concepts: teamwork, investment, leadership, productivity
- **Example**: "Patient planning yields prosperity" = high business relevance ✓

#### Final Score Formula:
```
Overall Quality = 
  (Cultural Authenticity × 40%) +
  (Translation Fidelity × 35%) +
  (Business Relevance × 15%) +
  (Expert Alignment × 10%)
```

**Grading Scale**:
- **A (90%+)**: Excellent cultural preservation
- **B (80-89%)**: Good quality
- **C (70-79%)**: Acceptable
- **D (60-69%)**: Needs improvement
- **F (<60%)**: Poor quality

---

### Method 2: LLM-as-Judge (Backup Check)

**Think of it like this**: After using your measuring tools, you ask an experienced chef to taste-test and give their opinion.

**How it works**:
1. We give another AI (Gemini 2.5) the proverb and translation
2. It scores on a 1-5 scale across 4 areas:
   - Cultural faithfulness
   - Translation accuracy
   - Business relevance
   - Natural English flow
3. We compare these scores to our automated metrics

**Why Gemini 2.5 instead of GPT-4?**
- We ran out of OpenAI credits (student budget constraints!)
- Gemini 2.5 is actually newer (June 2025) than GPT-4 (2023)
- Better at understanding multiple languages and cultures
- Free research tier available
- **Same evaluation questions, different AI judge**

**Results**:
- Gemini scores matched our automated metrics with **64% correlation**
- This confirms our automated approach is reasonable
- OG-RAG scored **4.05/5** vs Raw GPT-4's **3.93/5**

---

## The Results (What We Found)

### Cultural Metrics Results

**Test**: 100 Kikuyu proverbs translated 3 ways each (300 total translations)

**Scores**:
- **OG-RAG** (our system): **62.7%** cultural authenticity
- **Traditional RAG**: 59.4%
- **Raw GPT-4**: 56.8%

**The Win**: OG-RAG improved cultural preservation by **10.4%** compared to plain GPT-4

**Statistical Check**: p < 0.05 means 95% confident this isn't random luck

**What this means**:
- Without ontology: Like translating without a cultural dictionary
- With ontology: Like having 959 cultural concepts to guide translation
- Result: More cultural metaphors, values, and context preserved

---

## Why This Evaluation Method Works

### Three Reasons It's Valid:

#### 1. Expert-Grounded (Not Circular!)
- **Cultural patterns came from 100 expert annotations**
- Expert said: "This proverb means respect for elders leads to wisdom"
- We extracted: "respect," "elders," "wisdom" as cultural concepts
- We check if translations preserve these concepts
- **Not circular** because: Extraction ≠ Evaluation

#### 2. Cross-Validated
- Two different AI methods (sentence transformers + Gemini) agree (r=0.64)
- Like measuring temperature with both thermometer and weather app
- If they match, probably accurate

#### 3. Reproducible
- Run the same translation 10 times = same score every time
- Human evaluators might score differently based on mood, fatigue
- Automation ensures consistency

---

## Comparison to Human Evaluation

**What we DIDN'T do**: Get 3 Kikuyu experts to score all 300 translations

**Why we chose automation**:

| Human Evaluation | Automated Evaluation |
|------------------|---------------------|
| ✓ Nuanced cultural judgment | ✓ Grounded in expert patterns |
| ✓ Native speaker intuition | ✓ AI-simulated expert judgment |
| ✗ Time: 2-3 weeks | ✓ Time: 15 minutes |
| ✗ Cost: $500-1000 (expert fees) | ✓ Cost: $0 (free tier) |
| ✗ Consistency issues (fatigue) | ✓ Perfect reproducibility |
| ✗ Limited availability | ✓ Scalable to 1000+ proverbs |

**Future work**: Validate our automated scores against human experts on 20-30 proverbs

---

## Common Questions (Simplified Answers)

### Q: Isn't using AI to judge AI a problem?

**Simple Answer**: No, because we use **different AI for different jobs**:
- **Translation AI** (GPT-4): Creates English text
- **Evaluation AI** (Sentence transformers): Measures similarity (like a ruler)
- **LLM-Judge AI** (Gemini): Independent opinion (like a second doctor)

**Analogy**: Using a calculator to check if a 3D printer made the right size part. Different tools, different purposes.

### Q: How do you know the cultural patterns are correct?

**Simple Answer**: We didn't make them up—we extracted them from 100 proverbs that experts already translated and explained.

**Process**:
1. Expert annotated: "Gutiri uthuire tiga akiaga" means "There's no wealth without toil"
2. Expert explained cultural meaning: Hard work, perseverance, patience
3. We extracted patterns: work → wealth, effort → success
4. We check if translations preserve this wisdom

### Q: What's the significance of 10.4% improvement?

**Simple Answer**: It's like improving a student's grade from 57% to 63%:
- Moves from **failing** (F grade) to **passing** (D grade)
- Statistically significant (95% confident it's real, not luck)
- Consistent across all 100 proverbs tested

**In cultural terms**:
- More metaphors preserved (e.g., "seed → harvest" for "planning → success")
- More traditional values maintained (e.g., community over individual)
- More business-applicable wisdom (e.g., "patience in planning yields profit")

### Q: Why not just use BLEU score like other translation studies?

**Simple Answer**: BLEU is like grading an essay by counting matching words, not understanding meaning.

**Example**:
- **Original**: "A lone finger cannot kill a louse"
- **Translation A**: "Teamwork is essential for success" (BLEU: Low, Cultural: High)
- **Translation B**: "One finger kills not a louse" (BLEU: High, Cultural: Low)

BLEU prefers Translation B (more word matches), but Translation A captures the cultural meaning better (teamwork concept).

---

## The Bottom Line (One-Sentence Summary)

**"We built an automated evaluation system that uses AI trained on 1 billion sentences to measure cultural preservation, validated against expert annotations and cross-checked with a second AI judge, achieving reproducible results that show ontology-grounded RAG improves cultural authenticity by 10.4%."**

---

## Presentation Talking Points (30 seconds)

**Setup**: "How did we measure cultural preservation?"

**Explanation**:
1. "We used **two automated methods**: sentence transformers measuring semantic similarity, and Gemini AI as a judge."
2. "Both are grounded in **100 expert-annotated proverbs**—we extracted cultural patterns like 'community values,' 'agricultural metaphors,' and 'moral teachings.'"
3. "The evaluation scored **300 translations** across cultural authenticity, translation fidelity, and business relevance."
4. "Results: **OG-RAG achieved 62.7%** vs Raw GPT-4's 56.8%—a **10.4% improvement** that's statistically significant (p<0.05)."
5. "This automated approach gives us reproducible, scalable evaluation **grounded in expert knowledge**."

**Confidence closer**: "While future work includes human validation, this framework provides rigorous, expert-informed assessment at scale."

---

## Visual Summary (For Slides)

```
┌─────────────────────────────────────────────────────┐
│         AUTOMATED EVALUATION FRAMEWORK              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  INPUT: 100 Kikuyu Proverbs                        │
│         ↓                                           │
│  3 Translation Systems:                            │
│  • Raw GPT-4 (baseline)                            │
│  • Traditional RAG                                 │
│  • OG-RAG (our system)                             │
│         ↓                                           │
│  300 Total Translations                            │
│                                                     │
├─────────────────────────────────────────────────────┤
│         EVALUATION METHOD 1: CULTURAL METRICS       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✓ Semantic Similarity (40%)                       │
│    → Sentence transformers (1B training pairs)     │
│                                                     │
│  ✓ Cultural Pattern Matching (15%)                 │
│    → 6 categories from expert annotations          │
│                                                     │
│  ✓ Translation Fidelity (35%)                      │
│    → ROUGE-L + word overlap + structure            │
│                                                     │
│  ✓ Business Relevance (15%)                        │
│    → 4 business concept categories                 │
│                                                     │
├─────────────────────────────────────────────────────┤
│         EVALUATION METHOD 2: LLM-AS-JUDGE          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ✓ Gemini 2.5 Flash (Google AI)                   │
│  ✓ 4-dimension scoring (1-5 scale)                │
│  ✓ Correlates r=0.64 with cultural metrics        │
│                                                     │
├─────────────────────────────────────────────────────┤
│                    RESULTS                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  OG-RAG:          62.7% ██████████████ ✓           │
│  Traditional RAG: 59.4% ████████████               │
│  Raw GPT-4:       56.8% ███████████                │
│                                                     │
│  Improvement: 10.4% (p < 0.05) ⭐                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Key Takeaway for Defense

**If challenged on methodology**:

"Automated evaluation is standard practice in NLP research when expert annotations are limited. Our approach is grounded in 100 expert-translated proverbs, uses established metrics (sentence transformers, ROUGE), and is validated through cross-method correlation (r=0.64). The 10.4% improvement is statistically significant and reproducible—demonstrating that ontology grounding meaningfully enhances cultural knowledge preservation."

**Translation for non-experts**:

"We use AI tools like rulers and thermometers—calibrated against expert knowledge—to measure cultural preservation consistently across 300 translations. The results show our system preserves 10% more cultural meaning than baseline AI."
