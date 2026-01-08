# How to Use the Presentation Guide - ELI5

**Purpose**: Explain how to use the PRESENTATION_GUIDE_ELI5.md document effectively during thesis defense preparation  
**Audience**: You (the presenter) preparing for defense  
**Created**: January 8, 2026

---

## What This Guide Is

Think of the PRESENTATION_GUIDE_ELI5.md as your **translation dictionary** between:
- Complex technical concepts in your thesis
- Simple explanations you can give in 30-60 seconds during your defense

It's like having a cheat sheet that helps you explain hard things to different audiences without sounding condescending or too technical.

---

## How the Guide Is Organized

### 1. Cultural Concepts Section
**What it covers**: Kikuyu-specific cultural systems (ngwatio, traditional banking)  
**Why it matters**: Your committee might not know anything about Kikuyu culture  
**How to use**: 
- Read the ELI10 version before your defense
- Memorize the "Key Point" one-liner
- Use the analogy when explaining (e.g., "ngwatio is like a social bank account")

**Example Defense Moment**:
- Committee asks: "What is ngwatio?"
- You answer: "It's like a social bank account where deposits and withdrawals are favors, not money. If I help you harvest crops today, you help me build my house tomorrow. The community tracks these obligations through memory and social pressure, not written records."
- Time: 30 seconds ✅

---

### 2. NLP/Translation Metrics Section
**What it covers**: BLEU, CHRF, COMET, Sentence-BERT, etc.  
**Why it matters**: You need to explain WHY traditional metrics fail for cultural translation  
**How to use**:
- Know the ELI5 version cold
- Have the technical details ready if asked
- Use the score examples to illustrate

**Example Defense Moment**:
- Committee asks: "Why didn't you just use BLEU?"
- You answer: "BLEU punishes creative translations. If the expert wrote 'People are wealth' and I wrote 'Community is prosperity,' BLEU gives 0% even though culturally it's accurate. BLEU counts word matches, not meaning preservation. For cultural proverbs, we NEED different words to capture cultural context, so COMET is better—it understands meaning, not just words."
- Time: 45 seconds ✅

---

### 3. Statistical Methods Section
**What it covers**: Cohen's d, hypothesis testing, paired t-tests, Bonferroni correction  
**Why it matters**: Committee will ask "Is this REALLY better or just noise?"  
**How to use**:
- Lead with the ELI10 version
- Have the formula ready if challenged
- Connect to your actual results

**Example Defense Moment**:
- Committee asks: "Cohen's d of 0.73—is that big?"
- You answer: "Cohen's d measures effect size. Think of it as 'how BIG is the improvement?' The scale is: 0.2 = small, 0.5 = medium, 0.8 = large. Our 0.73 is medium-to-large, meaning the improvement isn't just statistically significant—it's VISIBLE and SUBSTANTIAL in practice."
- Time: 30 seconds ✅

---

### 4. Datasets/Tools Section
**What it covers**: MuSiQue, HotpotQA, MedRAG, UMLS, OOPS!, OWL  
**Why it matters**: Shows you know the field, can connect your work to precedents  
**How to use**:
- Reference when making broader points
- Use MedRAG as precedent: "If ontologies work for medicine, why not culture?"
- Use UMLS as scale comparison: "Our 847 concepts vs. their 4 million"

**Example Defense Moment**:
- Committee asks: "Has anyone proven ontologies improve domain-specific AI?"
- You answer: "Yes—MedRAG for medicine. They showed domain-specific knowledge graphs dramatically improve medical question answering. UMLS has 4 million medical concepts. We apply the same principle to culture: 847 Kikuyu concepts. Smaller scale, same principle—structure helps when data is scarce."
- Time: 40 seconds ✅

---

## The Quick Reference Table - Your Safety Net

**Location**: Bottom of the guide (page 7)  
**Purpose**: One-sentence summaries for EVERY term  
**When to use**: Last-minute review 10 minutes before defense

**How it works**:
1. Scan the left column for the term you need
2. Read the right column for the fastest possible explanation
3. Expand with ELI5/ELI10 version if time permits

**Example**:
- Committee: "Remind me what Sentence-BERT does?"
- (Quick glance at table): "Converts sentences into numerical vectors to measure semantic similarity"
- (Expand if time): "Like giving every sentence an address in a city—similar meanings live in the same neighborhood"

---

## Presentation Tips Section - Audience Adaptation

The guide gives you 4 pre-planned audience strategies:

### General Audience (Non-Technical)
**Who**: University community, parents, friends  
**Strategy**: Use ELI5 versions, cultural concepts, analogies  
**Avoid**: Statistics, p-values, technical jargon  
**Example**: "Ontology is like a cultural encyclopedia for the AI"

### Academic Committee (Technical)
**Who**: Your defense committee (CS, linguistics, cultural studies mix)  
**Strategy**: Use ELI10 + show numbers + reference precedents  
**Balance**: Technical enough to show expertise, accessible enough for non-CS members  
**Example**: "Cohen's d = 0.73, p < 0.000001. MedRAG precedent shows ontologies work for domains."

### Computer Science Audience
**Who**: CS faculty, ML researchers  
**Strategy**: Full technical depth—embeddings, cosine similarity, Neo4j traversal  
**Go deep on**: Architecture, vector spaces, graph algorithms  
**Example**: "768-dimensional Sentence-BERT embeddings, cosine similarity for semantic search, hybrid with Cypher graph traversal"

### Cultural Studies Audience
**Who**: Anthropologists, linguists, cultural preservation folks  
**Strategy**: Emphasize cultural concepts, ethics, community benefit  
**Focus on**: Ngwatio, knowledge ownership, benefit-sharing  
**Example**: "Who owns cultural knowledge in AI systems? Our ontology uses restricted license—community permission required for commercial use"

---

## How to Practice with This Guide

### Week Before Defense: Deep Reading
1. Read each section 3 times
2. Highlight the ELI10 versions
3. Practice explaining each term OUT LOUD
4. Time yourself—aim for 30-60 seconds per term
5. Record yourself and listen back

### Day Before Defense: Speed Drills
1. Open the Quick Reference Table
2. Cover the right column
3. Test yourself: Can you give the one-sentence summary?
4. Uncover and check
5. Repeat until 100% accurate

### 1 Hour Before Defense: Final Review
1. Read ONLY the "Key Point" lines for cultural concepts
2. Scan the Quick Reference Table once
3. Re-read the Presentation Tips section
4. Remind yourself: "I know this cold. I can explain it to anyone."

---

## Common Defense Scenarios & How to Use the Guide

### Scenario 1: "Can you explain that in simpler terms?"
**What they're saying**: "You're being too technical"  
**How to respond**: Drop to ELI5 version immediately  
**Example**:
- You said: "Sentence-BERT generates 768-dimensional dense vector representations via siamese network architecture"
- Committee: "Can you simplify?"
- You say: (Switch to ELI5) "It's like giving every sentence an address in a giant city. Sentences with similar meanings live in the same neighborhood. We measure the distance between addresses to see how similar they are."

### Scenario 2: "But isn't BLEU the standard metric?"
**What they're challenging**: Your methodology choice  
**How to respond**: Use the BLEU section—show the problem, not just preference  
**Example**:
- You say: "BLEU works for European languages with lots of data. But for cultural translation, it fails. Here's why: (pull out score example from guide) 'People are wealth' vs 'Community is prosperity'—same meaning, BLEU gives 0%. COMET understands the meaning is preserved."

### Scenario 3: "Your effect size seems small"
**What they're challenging**: Statistical significance vs. practical significance  
**How to respond**: Use Cohen's d explanation—it's NOT small  
**Example**:
- You say: "Cohen's d = 0.73 is medium-to-large on the standard scale. In practical terms, it means the improvement is VISIBLE in real translations, not just a tiny technical gain. If you compare 10 translations side-by-side, you can SEE the difference without statistics."

### Scenario 4: "This seems specific to Kikuyu"
**What they're challenging**: Generalizability  
**How to respond**: Use MedRAG/UMLS precedent, show transferability  
**Example**:
- You say: "MedRAG proved ontologies work for medicine. We prove they work for culture. The PRINCIPLE is domain-agnostic: when you have hierarchical knowledge and scarce data, structure beats volume. Medicine had UMLS (4M concepts), we built cultural equivalent (847 concepts). Same architecture could apply to Swahili proverbs, Zulu oral literature, any culture with structured knowledge."

---

## What Each Section Tells You

| Section | What It Teaches You |
|---------|---------------------|
| **Cultural Concepts** | How to explain Kikuyu culture to non-Kikuyu committee members |
| **NLP Metrics** | Why your evaluation metrics are better than standard MT metrics |
| **Statistical Methods** | How to defend your statistical rigor and prove real improvement |
| **Datasets/Tools** | How to connect your work to established precedents in the field |
| **Quick Reference** | Emergency fallback for terms you blank on during Q&A |
| **Presentation Tips** | How to adapt on-the-fly based on who's asking questions |

---

## Meta-Lesson: Why This Guide Exists

**The Problem**: You've spent 2+ years on this research. You know it deeply. Too deeply.

**The Risk**: You'll use jargon, assume background knowledge, or over-explain simple things and under-explain complex ones.

**The Solution**: This guide forces you to think like your audience:
- What do they NOT know?
- What's the simplest accurate explanation?
- How do I build from simple → technical if they want more?

**The Practice**: Every term in this guide follows the pattern:
1. **ELI5**: What a 10-year-old could understand (simple analogy)
2. **ELI10**: What an educated adult could understand (conceptual + some detail)
3. **Technical**: What an expert needs (formulas, architecture, specifics)

**Your Defense Strategy**: Start at ELI10 for every question. Go to ELI5 if confused faces. Go to Technical if challenged or if CS faculty asks.

---

## Red Flags During Defense (and How the Guide Saves You)

### Red Flag 1: Committee Member's Eyes Glaze Over
**What it means**: Too technical, losing them  
**Guide solution**: Drop to ELI5 version immediately  
**Recovery**: "Let me explain that more simply: (analogy from guide)"

### Red Flag 2: Committee Member Leans Forward, Skeptical
**What it means**: They're challenging your rigor  
**Guide solution**: Go to Technical version with numbers  
**Recovery**: "Let me be more precise: (exact p-value, Cohen's d, formula from guide)"

### Red Flag 3: "Can You Repeat That?"
**What it means**: You talked too fast or used unknown term  
**Guide solution**: Use the one-sentence summary from Quick Reference Table  
**Recovery**: "Sorry, let me clarify: (read from table verbatim, slowly)"

### Red Flag 4: Long Silence After Your Answer
**What it means**: Either brilliant or confusing—can't tell which  
**Guide solution**: Add a concrete example from the guide  
**Recovery**: "Here's a concrete example: (pull proverb translation example from BLEU section)"

---

## Final Checklist: Did You Use the Guide Right?

**Before Defense:**
- [ ] Read entire guide 3x
- [ ] Practiced each ELI10 explanation out loud
- [ ] Memorized all "Key Point" one-liners
- [ ] Timed yourself: Can explain any term in 60 seconds or less
- [ ] Reviewed Quick Reference Table until instant recall

**During Defense:**
- [ ] Started every answer at ELI10 level
- [ ] Moved to ELI5 when faces looked confused
- [ ] Moved to Technical when challenged
- [ ] Used analogies from the guide (not made-up ones)
- [ ] Referenced precedents (MedRAG, UMLS) when discussing generalizability

**After Each Answer:**
- [ ] Checked committee faces: understanding or confusion?
- [ ] Adjusted next answer accordingly
- [ ] Used concrete examples when abstract explanation failed

---

## The Ultimate Test

Can you explain your ENTIRE thesis in 3 minutes using ONLY the ELI5 versions from this guide?

**Try it**:

"I studied how to teach AI to translate Kikuyu proverbs in a culturally accurate way. The problem: AI understands words but not culture. If you translate 'Andu ni indo' word-by-word, you get 'People are wealth'—technically correct but missing the deep economic philosophy about reciprocity systems called ngwatio.

My solution: Build a cultural encyclopedia (ontology) that teaches the AI about Kikuyu culture BEFORE it translates. Like giving it an open-book exam instead of closed-book. The ontology has 847 cultural concepts organized into themes like Reciprocity, Wisdom, Community.

When the AI translates now, it first looks up the cultural context, then generates a translation that preserves the meaning, not just the words. I tested three systems on 100 proverbs: Raw AI, Traditional retrieval, and my ontology system. Mine won by 5.3% on cultural authenticity—statistically significant with p < 0.000001 and Cohen's d = 0.73 (large effect).

The contribution: Proved that structured cultural knowledge can compensate for scarce data. If it works for Kikuyu, it can work for other endangered languages. We're not just translating words—we're preserving cultural knowledge systems."

**Time**: 2 minutes 45 seconds ✅

---

**Status**: Ready for defense  
**Confidence Level**: You know this inside-out  
**Remember**: Simple ≠ Simplistic. Clear ≠ Dumbed-down. You're teaching, not talking down.

**Final Advice**: The committee wants you to succeed. They're on your side. This guide helps you help them understand your brilliant work. Use it. Trust it. You've got this.
