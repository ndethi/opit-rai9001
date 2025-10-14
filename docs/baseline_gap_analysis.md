# Baseline Translation Gap Analysis Report
**Date:** October 14, 2025  
**Corpus:** 100 Kikuyu Proverbs (Ireri Collection - Wealth/Prosperity Domain)  
**Analysis Model:** GPT-4o  

---

## Executive Summary

This report identifies systematic failures in baseline MT systems when translating Kikuyu proverbs, informing **ontology construction priorities** for the OG-RAG system.

### Key Findings
- **Total Proverbs Analyzed:** 100
- **Complete Failures (All Systems):** 97 (97.0%)
- **Partial Failures (Some Systems):** 0 (0.0%)
- **Metaphor Preservation Failures:** 0 (0.0%)
- **Cultural Meaning Losses:** 0 (0.0%)

### Quality Scores (0-1 scale)
- **Semantic Similarity:** 0.115
- **Cultural Fidelity:** 0.067
- **Metaphor Preservation:** 0.045

---

## 1. System-Level Performance

### Failure Rates by MT System
- **nllb:** 98.0% failure rate
- **google:** 95.0% failure rate
- **cohere:** 70.0% failure rate
- **openai:** 26.0% failure rate

**Worst Performing System:** nllb  
**Best Performing System:** openai

### System Rankings
1. **openai** (Most reliable)
2. **cohere**
3. **google**
4. **nllb**

---

## 2. Missing Kikuyu Concepts

These concepts were consistently mistranslated across MT systems, indicating **HIGH PRIORITY** for ontology representation.

### Top 20 Missing Concepts
1. **wealth** - 20 failures 🔴 CRITICAL
2. **poverty** - 10 failures 🔴 CRITICAL
3. **ownership** - 4 failures 🟡 MEDIUM
4. **wealth acquisition** - 4 failures 🟡 MEDIUM
5. **debt** - 4 failures 🟡 MEDIUM
6. **greed** - 2 failures 🟡 MEDIUM
7. **investment** - 2 failures 🟡 MEDIUM
8. **impermanence of wealth** - 2 failures 🟡 MEDIUM
9. **wisdom** - 2 failures 🟡 MEDIUM
10. **hospitality** - 2 failures 🟡 MEDIUM
11. **self-reliance** - 2 failures 🟡 MEDIUM
12. **collaboration** - 2 failures 🟡 MEDIUM
13. **resource management** - 2 failures 🟡 MEDIUM
14. **stewardship** - 2 failures 🟡 MEDIUM
15. **pride** - 2 failures 🟡 MEDIUM
16. **thief** - 2 failures 🟡 MEDIUM
17. **patience** - 2 failures 🟡 MEDIUM
18. **utonga** - 2 failures 🟡 MEDIUM
19. **money management** - 1 failures 🟡 MEDIUM
20. **pursuit** - 1 failures 🟡 MEDIUM

### Critical Kikuyu Terms for Deep Ontology Representation
These terms appeared in 5+ failures and require rich semantic/cultural annotations:

- `wealth`
- `poverty`

---

## 3. Failed Metaphors

Metaphorical structures that MT systems consistently failed to preserve.

### Top 20 Failed Metaphors
1. comparison of money management to storks pursuing locusts (1 failures)
2. people as a source of wealth (1 failures)
3. country as a place of instability affecting wealth (1 failures)
4. unstable country (1 failures)
5. wealth accumulation (1 failures)
6. property distribution of an invalid (1 failures)
7. granary as a symbol of wealth accumulation (1 failures)
8. lawsuit leading to poverty (1 failures)
9. spending money to make money (1 failures)
10. land as a symbol of life's toil (1 failures)
11. land as a right (1 failures)
12. rich man's power to reclaim land (1 failures)
13. wealthy man eating a dying goat (1 failures)
14. interconnectedness of poverty and wealth (1 failures)
15. Value obtained through effort (1 failures)
16. comparison of goats to brideswealth (1 failures)
17. youth as a period of potential and opportunity (1 failures)
18. poverty as a state of lacking possessions (1 failures)
19. poverty vs. foolishness (1 failures)
20. virtue as true wealth (1 failures)

---

## 4. Gap Type Distribution

- **complete_failure:** 97 proverbs (97.0%)
- **complete_failure|metaphor_loss|cultural_loss:** 3 proverbs (3.0%)

---

## 5. Critical Failures (Sample)

Below are examples of **critical failures** where all MT systems produced poor translations.


### 1. MW_001: "Aikaragia mbia ta njuu ngigi."

**Expert Translation:** He looks after his money the way storks pursue locusts.  
**Expert Cultural Meaning:** Whoever has much always wants more.

**MT System Translations:**
- **OpenAI GPT-4o-mini:** It does not grow old like a big tree.
- **Gemini 1.5 Flash:** Aikharia mbia ta njigi.
- **GPT-3.5-turbo:** Aikaragia mbia ta njuu ngigi: Let the teeth that are above speak.
- **NLLB-200:** He was a man of many talents.

**Analysis:**
- **Failed Systems:** openai, google, cohere, nllb
- **Missing Concepts:** money management, greed, pursuit
- **Lost Cultural Meanings:** insatiable desire for wealth, mistrust due to greed
- **Failed Metaphors:** comparison of money management to storks pursuing locusts

**Scores:**
- Semantic: 0.03
- Cultural: 0.00
- Metaphor: 0.00

**Notes:** All systems failed to capture the essence of the proverb. The translations were either nonsensical or completely unrelated to the original meaning. Key concepts of greed and pursuit were lost, and the metaphorical structure comparing money management to storks and locusts was not preserved.

---

### 2. MW_002: "Andu ni indo."

**Expert Translation:** People are wealth.  
**Expert Cultural Meaning:** nan

**MT System Translations:**
- **OpenAI GPT-4o-mini:** People are things.
- **Gemini 1.5 Flash:** And touch it indo.
- **GPT-3.5-turbo:** Andu ni indo. (Kikuyu) ->  Hand is fire. (English)
- **NLLB-200:** People are things.

**Analysis:**
- **Failed Systems:** google, cohere, nllb
- **Missing Concepts:** wealth as derived from people
- **Lost Cultural Meanings:** importance of community and collaboration
- **Failed Metaphors:** people as a source of wealth

**Scores:**
- Semantic: 0.28
- Cultural: 0.15
- Metaphor: 0.12

**Notes:** OpenAI's translation was closest semantically but still missed the cultural depth. Google and Cohere produced translations that were nonsensical or unrelated to the original meaning. NLLB's translation was incorrect and failed to capture any aspect of the proverb. The main failure was the inability to convey the metaphorical and cultural significance of people as a source of wealth.

---

### 3. MW_003: "Bururi uri ngui ndungiciarikira indo."

**Expert Translation:** In an unstable country one cannot become wealthy  
**Expert Cultural Meaning:** nan

**MT System Translations:**
- **OpenAI GPT-4o-mini:** The land is a pot that does not overflow with things.
- **Gemini 1.5 Flash:** Burundi and I am telling us a god.
- **GPT-3.5-turbo:** Bururi (a type of ant) uri (with) ngui (stings) ndungiciarikira (it doesn't sting) indo (people).
- **NLLB-200:** Sleeping with a dog is not a good thing.

**Analysis:**
- **Failed Systems:** google, cohere, nllb
- **Missing Concepts:** bururi, ngui, ndungiciarikira
- **Lost Cultural Meanings:** instability leading to lack of wealth, importance of careful planning
- **Failed Metaphors:** country as a place of instability affecting wealth

**Scores:**
- Semantic: 0.08
- Cultural: 0.03
- Metaphor: 0.03

**Notes:** The majority of the systems failed to capture the core meaning of the proverb, which is about the instability of a country affecting wealth accumulation. OpenAI's translation was the closest but still missed the metaphorical and cultural context. Google, Cohere, and NLLB provided translations that were nonsensical and unrelated to the original proverb's meaning.

---

### 4. MW_004: "Bururi uri ngui ndungiciarikira indo."

**Expert Translation:** In an unstable country one cannot become wealthy.  
**Expert Cultural Meaning:** Political stability facilitates wealth.

**MT System Translations:**
- **OpenAI GPT-4o-mini:** A country is like a tree that does not forget its roots.
- **Gemini 1.5 Flash:** Burundi and I am telling us a god.
- **GPT-3.5-turbo:** Bururi (a type of ant) uri (that) ngui (bites) ndungiciarikira (the one who is sleeping) indo (on the path).
- **NLLB-200:** Sleeping with a dog is not a good thing.

**Analysis:**
- **Failed Systems:** google, cohere, nllb
- **Missing Concepts:** political stability, wealth, investment
- **Lost Cultural Meanings:** political stability facilitates wealth, importance of a stable environment for prosperity
- **Failed Metaphors:** unstable country, wealth accumulation

**Scores:**
- Semantic: 0.05
- Cultural: 0.03
- Metaphor: 0.00

**Notes:** OpenAI's translation is unrelated to the original meaning, focusing on roots rather than stability. Google's output is nonsensical and unrelated to the proverb. Cohere's translation misinterprets words and lacks coherence. NLLB's translation is completely off-topic, discussing dogs instead of political stability. All systems failed to capture the metaphorical and cultural essence of the proverb.

---

### 5. MW_005: "Cia kionje itigayagwo kiri muoyo/gitanakua."

**Expert Translation:** The property of an invalid are not distributed while the person is still alive.  
**Expert Cultural Meaning:** A poor man is unable to obtain any more than he possesses.

**MT System Translations:**
- **OpenAI GPT-4o-mini:** The thing that is tasted is not forgotten in the heart/it does not fade away.
- **Gemini 1.5 Flash:** You have you do it.
- **GPT-3.5-turbo:** A thorn that pricks you is in your heart/near your skin.
- **NLLB-200:** The brightness is not left alive/untouched.

**Analysis:**
- **Failed Systems:** google, nllb
- **Missing Concepts:** property distribution, invalid person
- **Lost Cultural Meanings:** importance of rightful acquisition, protection of vulnerable individuals
- **Failed Metaphors:** property distribution of an invalid

**Scores:**
- Semantic: 0.08
- Cultural: 0.05
- Metaphor: 0.03

**Notes:** The translations from Google and NLLB-200 are completely off-target, failing to capture any aspect of the original proverb. OpenAI and Cohere attempt a metaphorical structure but miss the cultural and semantic essence of the proverb. The key concepts of property distribution and the status of the invalid person are lost, leading to a critical failure in conveying the intended message.

---

## 6. Ontology Construction Priorities

Based on this gap analysis, the following areas require **deepest ontology representation**:

### Priority 1: Critical Kikuyu Concepts (5+ failures)
These concepts should have:
- Rich semantic definitions
- Multiple Kikuyu expressions/synonyms
- Cultural significance annotations
- Usage context examples
- Biblical parallels (where applicable)

**Target Concepts:**
- wealth
- poverty

### Priority 2: Metaphorical Structures
Metaphors require:
- Explicit vehicle-tenor mappings
- Cultural resonance explanations
- Mapping justifications
- Multiple examples

**Focus Areas:**
- comparison of money management to storks pursuing locusts
- people as a source of wealth
- country as a place of instability affecting wealth
- unstable country
- wealth accumulation

### Priority 3: Cultural Context
Proverbs with high cultural loss need:
- Expert cultural meaning annotations
- Teaching/moral dimensions
- Application contexts
- Thematic categorization

---

## 7. Recommendations for OG-RAG System

### Ontology Depth Requirements
1. **Entities:** Include all critical Kikuyu terms with cultural significance
2. **Metaphors:** Explicit vehicle-tenor-mapping-resonance structure
3. **Cultural Concepts:** Moral dimensions, Kikuyu expressions, explanations
4. **Relationships:** Rich property network (expresses, usesMetaphor, involvesEntity)

### Retrieval Strategy
- Prioritize subgraph retrieval for critical terms
- Include metaphor context in RAG prompts
- Surface cultural meanings for generation

### Evaluation Focus
- Test OG-RAG particularly on proverbs with complete baseline failures
- Measure improvement in cultural fidelity (currently lowest score)
- Validate metaphor preservation (second-lowest score)

---

## 8. Methodology Notes

**Analysis Approach:**
- LLM-based semantic comparison (GPT-4o at temperature 0.2)
- Structured JSON output for consistency
- Three-dimensional scoring: semantic, cultural, metaphorical

**Limitations:**
- LLM analysis introduces potential bias
- Cultural fidelity assessment limited by model's Kikuyu knowledge
- Some proverbs may have multiple valid translations

**Validation:**
- All failures manually reviewable in JSON output
- Scores averaged across 4 systems for robustness
- Priority rankings based on frequency, not individual judgments

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Next Step:** Manual ontology class hierarchy design informed by these priorities (Phase 2b)
