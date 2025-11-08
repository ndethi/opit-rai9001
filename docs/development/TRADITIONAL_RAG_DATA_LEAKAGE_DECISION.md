# Traditional RAG Data Leakage - Methodological Decision

**Date:** November 8, 2025  
**Issue:** Traditional RAG shows suspiciously high BLEU scores (19.27 avg, multiple 100.0 scores)  
**Question:** How do we handle this for thesis evaluation?

---

## The Problem: Evidence of Data Leakage

### Quantitative Evidence

| Method | Average BLEU | Perfect Matches (100.0) | Median |
|--------|-------------|------------------------|--------|
| Raw GPT-4 | 7.95 | 1-2 (simple proverbs) | 4.54 |
| **Traditional RAG** | **19.27** ⚠️ | **Multiple cases** | 6.44 |
| OG-RAG | 9.33 | 0 | 5.80 |

### Qualitative Evidence

**Sample Perfect Matches:**
```
MW_001 Expert:    "He looks after his money the way storks pursue locusts."
MW_001 Trad RAG:  "He looks after his money the way storks pursue locusts."
BLEU: 100.0

MW_002 Expert:    "People are wealth."
MW_002 Trad RAG:  "People are wealth."
BLEU: 100.0

MW_004 Expert:    "In an unstable country one cannot become wealthy."
MW_004 Trad RAG:  "In an unstable country one cannot become wealthy."
BLEU: 100.0
```

### Hypothesis

**Most Likely:** Traditional RAG is retrieving expert translations from the Neo4j knowledge graph where they were stored alongside Kikuyu proverbs during data population.

**Mechanism:**
1. During setup, proverbs + expert translations loaded into Neo4j
2. Traditional RAG retrieves "similar proverbs" from graph
3. Graph returns proverb nodes that include `expert_translation` property
4. Traditional RAG context includes these expert translations
5. LLM simply copies the expert translation from context

**Why OG-RAG doesn't have this problem:**
- OG-RAG retrieves **ontological concepts** (cultural themes, metaphors), not proverbs
- Concepts don't contain expert translations
- Forces LLM to generate new translation based on cultural context

---

## Decision Options

### Option 1: ❌ INVALIDATE Traditional RAG Entirely

**Action:** Remove Traditional RAG from comparison, compare only OG-RAG vs Raw GPT-4

**Pros:**
- Clean comparison (no contaminated data)
- Stronger argument for OG-RAG (17.4% improvement over baseline)
- Avoids defending questionable methodology

**Cons:**
- Loses the RAG vs RAG comparison
- Weaker thesis (only 2 methods compared)
- Doesn't demonstrate OG-RAG advantage over standard RAG approaches
- Wastes data collection effort

**Thesis Impact:**
- Research Question: Can only answer "Does OG-RAG improve over raw LLM?" not "Does ontology grounding improve over traditional RAG?"
- Contribution: Reduced - can't claim superiority over RAG approaches

**Recommendation:** ❌ **NOT RECOMMENDED** - Too much lost value

---

### Option 2: ✅ RE-RUN Traditional RAG (Preferred)

**Action:** Fix Traditional RAG implementation to exclude expert translations from retrieval, re-run evaluation

**Pros:**
- Clean, fair comparison across all 3 methods
- Demonstrates OG-RAG advantage over both baselines AND standard RAG
- Methodologically sound for thesis defense
- Answers full research question

**Cons:**
- Requires time investment (2-4 hours)
- May need to debug Neo4j queries
- Risk of encountering new technical issues
- Delays Step 2 (semantic similarity)

**Implementation Steps:**
1. Check Neo4j proverb node schema - confirm expert_translation property exists
2. Modify Traditional RAG retrieval to exclude expert_translation from context
3. Re-run evaluation on same 97 proverbs
4. Compare new results

**Expected Outcome:**
- Traditional RAG BLEU drops to 8-12 range (similar to Raw GPT-4 or slightly better)
- OG-RAG shows improvement over BOTH methods
- Thesis can claim "ontology grounding outperforms both raw prompting AND traditional RAG"

**Timeline Impact:**
- Today: 2-4 hours to fix and re-run
- Still achievable to complete Step 2 and 3 by end of weekend

**Recommendation:** ✅ **RECOMMENDED** - Best scientific integrity

---

### Option 3: 🟡 KEEP AS-IS and Document as Limitation

**Action:** Use current results, document data leakage as a limitation/finding in thesis

**Pros:**
- No additional time investment
- Can proceed immediately to Steps 2 & 3
- Interesting methodological finding to discuss
- Shows OG-RAG architecture advantage (concepts vs proverbs)

**Cons:**
- Weakens Traditional RAG comparison validity
- Thesis examiners may question methodology
- Can't claim clean comparison
- Reviewer might ask "Why didn't you fix this?"

**How to Frame in Thesis:**
```
"Traditional RAG showed artificially high BLEU scores (19.27) due to 
data leakage, where the system retrieved expert translations directly 
from the knowledge base rather than generating new translations. This 
finding itself validates a key architectural advantage of OG-RAG: by 
retrieving cultural concepts rather than example translations, OG-RAG 
forces genuine translation generation while still benefiting from 
cultural grounding."
```

**Thesis Impact:**
- Turn bug into feature (architectural advantage)
- Still have 3-method comparison (with caveat)
- Focus on OG-RAG vs Raw GPT-4 as main comparison
- Use Trad RAG as negative example

**Recommendation:** 🟡 **FALLBACK OPTION** - Use if time-constrained

---

### Option 4: 🟡 PARTIAL FIX - Filter Post-Hoc

**Action:** Identify and exclude perfect matches (100.0 BLEU), recalculate Traditional RAG average

**Pros:**
- Quick fix (30 minutes)
- Salvages some of the data
- Shows what Traditional RAG "actually" achieves

**Cons:**
- Not methodologically clean (arbitrary threshold)
- Still have contaminated data in remaining samples
- Hard to defend in thesis ("I removed the obvious cheating cases")
- Doesn't solve underlying problem

**Implementation:**
```python
# Filter out perfect matches
trad_rag_filtered = [score for score in trad_rag_scores if score < 100.0]
# Recalculate average
```

**Expected Result:**
- Traditional RAG drops from 19.27 to ~8-12 BLEU
- Still contaminated (near-perfect matches remain)

**Recommendation:** 🟡 **WEAK OPTION** - Only if Option 2 fails technically

---

## Recommended Decision Path

### Primary Plan: Option 2 (Re-run Traditional RAG)

**Timeline:**
1. **Now (30 min):** Investigate Neo4j schema and Traditional RAG query
2. **Next (1 hour):** Modify retrieval to exclude expert_translation
3. **Then (1 hour):** Re-run evaluation on 97 proverbs
4. **Validate (30 min):** Check BLEU scores are reasonable, no more 100.0s
5. **Total:** 3 hours

**Validation Criteria:**
- ✅ No more perfect matches (100.0 BLEU)
- ✅ Traditional RAG BLEU in 8-15 range (reasonable for RAG)
- ✅ OG-RAG still shows improvement over Traditional RAG
- ✅ Can defend methodology in thesis

**If successful:**
- Proceed to Step 2 (semantic similarity) tonight or tomorrow morning
- Have clean 3-method comparison for thesis
- Stronger research contribution

### Fallback Plan: Option 3 (Document as Finding)

**If Option 2 takes >4 hours or encounters blockers:**
- Document current results as-is
- Frame data leakage as architectural validation
- Focus thesis on OG-RAG vs Raw GPT-4 comparison
- Note Traditional RAG limitation in Chapter 5

---

## Impact on Thesis Schedule

### If we fix it (Option 2):

**Today (Nov 8):**
- ✅ Step 1 COMPLETE (comparative BLEU)
- 🔧 Fix Traditional RAG (3 hours)
- ⏸️ Step 2 delayed to tomorrow

**Saturday (Nov 9):**
- ✅ Step 2: Semantic similarity (2 hours)
- ✅ Step 3: Qualitative examples (2 hours)
- ✅ Supervisor meeting prep (2 hours)

**Still on track for:** Monday meeting with supervisor

### If we document as-is (Option 3):

**Today (Nov 8):**
- ✅ Step 1 COMPLETE
- ✅ Step 2: Semantic similarity (2 hours) 
- ✅ Step 3 started

**Saturday (Nov 9):**
- ✅ Step 3 complete
- ✅ Supervisor meeting prep
- ✅ Results summary report

**Benefit:** 1 day buffer

---

## Questions to Answer Before Deciding

### Q1: How critical is the 3-method comparison for your thesis?

**Research Questions:**
- RQ1: "Can OG-RAG improve translation quality?" → Only needs OG-RAG vs Raw GPT-4
- RQ2: "Does ontology grounding outperform traditional RAG?" → REQUIRES fixed Traditional RAG

**If RQ2 is central:** Must fix (Option 2)  
**If RQ2 is secondary:** Can document (Option 3)

### Q2: How much time do we have before supervisor meeting?

**If meeting is Nov 11-12:** Fix it (have weekend buffer)  
**If meeting is Nov 11 morning:** Document as-is (need prep time)

### Q3: What's in your thesis proposal?

**Check proposal:** Did you promise to compare OG-RAG to traditional RAG?  
**If yes:** Must fix to deliver on proposal  
**If no:** Documenting is acceptable

### Q4: What do you want your main contribution to be?

**Option A:** "OG-RAG is better than traditional RAG" → Need clean comparison (fix it)  
**Option B:** "OG-RAG is a novel approach to cultural translation" → Raw GPT-4 comparison sufficient (document)

---

## My Recommendation

### FIX IT (Option 2) - Here's Why:

1. **Scientific integrity:** Clean methodology is crucial for thesis defense
2. **Stronger contribution:** Can claim superiority over RAG approaches, not just raw prompting
3. **Time is available:** 3 hours today still leaves weekend for Steps 2-3
4. **Architectural insight:** Will confirm OG-RAG design advantage (concepts vs examples)
5. **Reviewer questions:** Better to fix now than defend contaminated data later

### What This Means:

**Today's Priority:**
1. ✅ Step 1 COMPLETE
2. 🔧 Fix Traditional RAG (next 3 hours)
3. ⏸️ Step 2 moves to tomorrow

**Tomorrow's Plan:**
- Step 2: Semantic similarity
- Step 3: Qualitative examples
- Supervisor meeting prep

**Risk Mitigation:**
- If fix takes >4 hours: Switch to Option 3 (document as-is)
- If fix works: Have stronger thesis with clean methodology

---

## Decision Required

**Please confirm your choice:**

- [ ] **Option 2:** Fix Traditional RAG (3 hours today, cleaner thesis)
- [ ] **Option 3:** Document as-is (proceed to Step 2 now, note limitation)
- [ ] **Option 1:** Remove Traditional RAG (not recommended)
- [ ] **Option 4:** Filter post-hoc (weak, not recommended)

**Once you decide, I'll proceed immediately with the chosen path.**

---

## Technical Preview: What Fixing Involves

If you choose Option 2, here's what we'll do:

### 1. Check Current Traditional RAG Implementation (15 min)
```bash
# Find how Traditional RAG queries Neo4j
grep -r "expert_translation" src/
grep -r "MATCH.*Proverb" src/rag-system/
```

### 2. Modify Query to Exclude Expert Translations (30 min)
```python
# Current (suspected):
context = graph.query("""
    MATCH (p:Proverb) WHERE ...
    RETURN p.kikuyu_text, p.expert_translation, p.cultural_context
""")

# Fixed:
context = graph.query("""
    MATCH (p:Proverb) WHERE ...
    RETURN p.kikuyu_text, p.cultural_context
    // Exclude p.expert_translation
""")
```

### 3. Re-run Evaluation (1 hour)
```bash
python scripts/run_ograg_evaluation.py --method traditional_rag
```

### 4. Validate Results (15 min)
```bash
# Check for perfect matches
grep "100.0" data/results/comparative_bleu_scores_fixed.csv
# Should return 0-2 cases max (simple proverbs)
```

**Total:** ~2-3 hours

---

**Your call - what do we do?** 🤔
