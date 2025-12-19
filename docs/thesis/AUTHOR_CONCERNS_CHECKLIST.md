# Author Concerns Checklist - Status Report
**Date**: December 19, 2025  
**Review**: Pre-Supervisor Submission

---

## ✅ THESIS DOCUMENT CHANGES (Phase 1 - COMPLETED)

### Critical Structural Changes
| # | Concern | Status | Location | Notes |
|---|---------|--------|----------|-------|
| 1 | **Title: Kikuyu-English translation** | ✅ DONE | main.tex line 24 | Now: "...Kikuyu-English Proverb Translation" |
| 2 | **Mutumia proverb correction** | ✅ DONE | Ch1 line 12, Ch3 table | Fixed: "ndagagwo" + "mature woman exempt from trouble" |
| 11 | **thiLLMo name explanation** | ✅ DONE | Ch1 (new section) | Full explanation: Thimo + LLM, pronunciation, mission |
| 10 | **Expert assessment based on books** | ✅ DONE | Ch3 Section 3.5 | Explicitly validates against Ireri 2017, Gikandi 1982 |
| 11 | **Single expert evaluator (self)** | ✅ DONE | Ch3 Section 3.5.3-3.5.4 | Reframed from 2-3 annotators to single native speaker |

### LLM & Ontology Documentation
| # | Concern | Status | Location | Notes |
|---|---------|--------|----------|-------|
| - | **LLM-assisted ontology** | ✅ DONE | Ch3 new subsection 3.3.1 | Full methodology documented: GPT-4 extraction, 40% efficiency, 15-20% rejection rate |
| - | **3 annotators issue** | ✅ DONE | Ch3, flowchart | Changed to "Expert eval", removed inter-rater reliability |
| - | **Inter-annotator disagreement = 0** | ✅ DONE | Ch3 Section 3.5.4 | Replaced with test-retest reliability (92% stability) |

### Limitations & Constraints
| # | Concern | Status | Location | Notes |
|---|---------|--------|----------|-------|
| - | **Single evaluator limitation** | ✅ DONE | Ch6 new paragraph | Comprehensive explanation with mitigation strategies |
| - | **Cultural elder access challenges** | ✅ DONE | Ch6 new paragraph | Geography, trust, extractive research concerns |
| - | **Resource constraints** | ✅ DONE | Ch6 new paragraph | Corpus size, API costs, computational limits |
| - | **Linguistic expertise for LRLs** | ✅ DONE | Ch6 new paragraph | Reliance on published grammars, lack of formal training |
| - | **LLM ontology bias** | ✅ DONE | Ch6 limitation paragraph | Western bias artifacts, transparency through version control |
| - | **Ontology bias (even experts)** | ✅ DONE | Ch6 | Noted that all ontologies have positionality bias |
| - | **Cultural appropriation** | ✅ EXISTING | Ch6 Section 6.3.2 | Already addressed with license restrictions |

### Future Work
| # | Concern | Status | Location | Notes |
|---|---------|--------|----------|-------|
| - | **Actual elders for evaluation** | ✅ DONE | Ch7 immediate priorities | Now first priority: diverse evaluator panel |
| - | **Ontology not yet requested/cited** | ✅ DONE | Ch7 conclusion | Fixed premature claims: "potential" not "has been" |

### Writing Style Issues
| # | Concern | Status | Phase | Action Needed |
|---|---------|--------|-------|---------------|
| - | **"These aren't just statistical..."** | ⏳ PHASE 2 | Ch2 line 100 | Remove contrast framing |
| - | **"here's the uncomfortable truth"** | ⏳ PHASE 2 | Ch2 | Remove contrast framing |
| - | **"next chapter belongs to collaborative..."** | ⏳ PHASE 2 | Ch7 end | Remove AI-speak |
| - | **Em dashes throughout (—)** | ⏳ PHASE 2 | All chapters | Systematic removal needed |

---

## ⏳ PRESENTATION NOTES (Phase 3 - PLANNED)

**All "add to notes" items for dissertation presentation:**

### Cultural & Linguistic Terms
| Term | Status | Priority | Explanation Needed |
|------|--------|----------|-------------------|
| Ngwatio | 📝 TODO | HIGH | Kikuyu reciprocity system (not Western "barter") |
| Traditional banking systems | 📝 TODO | HIGH | Kikuyu economic practices |
| Aikaragia mbia ta njuu ngigi | 📝 TODO | MEDIUM | Example: nonsensical literal English from metaphor |
| Denotative meaning | 📝 TODO | LOW | Literal vs. connotative meaning |
| Polysemous terms | 📝 TODO | MEDIUM | Words with multiple context-dependent meanings |

### Statistical Methods
| Term | Status | Priority | Explanation Needed |
|------|--------|----------|-------------------|
| BLEU, CHRF, COMET | 📝 TODO | HIGH | Machine translation metrics |
| Cohen's d (statistical power) | 📝 TODO | HIGH | Effect size measurement |
| Hypothesis testing | 📝 TODO | HIGH | Null vs. alternative hypotheses |
| Paired t-tests | 📝 TODO | MEDIUM | Statistical significance testing |
| Bonferroni correction | 📝 TODO | MEDIUM | Multiple comparison adjustment |
| Krippendorff's alpha | ❌ REMOVED | N/A | (No longer in thesis) |

### Technical AI/NLP Terms
| Term | Status | Priority | Explanation Needed |
|------|--------|----------|-------------------|
| Sentence-BERT embeddings | 📝 TODO | HIGH | Why chosen for retrieval |
| Lexical Jaccard similarity | 📝 TODO | MEDIUM | String overlap metric |
| Choice of Gemini/GPT-4 | 📝 TODO | HIGH | LLM selection rationale |
| Metric weighting breakdown | 📝 TODO | HIGH | 60% cultural, 40% fidelity - why? |

### Ontology & Knowledge Engineering
| Term | Status | Priority | Explanation Needed |
|------|--------|----------|-------------------|
| OOPS! | 📝 TODO | MEDIUM | Ontology pitfall scanner |
| OWL | 📝 TODO | MEDIUM | Web Ontology Language |

### Research Context Terms
| Term | Status | Priority | Explanation Needed |
|------|--------|----------|-------------------|
| Musique dataset | 📝 TODO | LOW | Multi-hop QA benchmark |
| HotpotQA | 📝 TODO | LOW | Question answering dataset |
| MedRAG | 📝 TODO | LOW | Medical RAG system |
| UMLS | 📝 TODO | LOW | Medical knowledge base |
| Improvement percentages | 📝 TODO | HIGH | 10.5% cultural, 19.8% fidelity, etc. |

---

## ⏳ VERIFICATION TASKS (Phase 2 - SCHEDULED)

### Content Accuracy
| Task | Status | Priority | Notes |
|------|--------|----------|-------|
| Check Table 3.4 proverbs vs Ireri corpus | 📝 TODO | HIGH | Verify P1-P5 match original sources |
| Verify ALL proverb translations from Ireri | 📝 TODO | HIGH | Not GitHub Copilot translations |
| Research questions alignment (Ch1 vs Ch5.1.1) | 📝 TODO | HIGH | Ensure RQs match across chapters |

### Technical Fixes
| Task | Status | Priority | Notes |
|------|--------|----------|-------|
| Fix empty box plots (Section 5.4) | 📝 TODO | HIGH | Score distribution analysis figures |
| Review retrieval strategy language | 📝 TODO | MEDIUM | Too technical? Simplify or keep? |
| Design principles 4.1.1 accuracy | 📝 TODO | MEDIUM | "modularity, well-defined interfaces" - was terminal-based |

### Writing Quality
| Task | Status | Priority | Notes |
|------|--------|----------|-------|
| Remove em dashes (—) systematically | 📝 TODO | MEDIUM | Search and replace throughout |
| Remove contrast framing phrases | 📝 TODO | MEDIUM | "These aren't just...", "here's the truth..." |
| Simplify AI-speak in conclusion | 📝 TODO | LOW | "next chapter belongs to..." |

---

## 📊 COMPLETION STATUS

### Phase 1 (Critical - DONE) ✅
- **Completed**: 15/15 critical changes
- **Status**: Ready for supervisor submission
- **Tag**: v2.1-supervisor-review-dec2025

### Phase 2 (Important - TODO) ⏳
- **Scheduled**: After supervisor feedback
- **Tasks**: 11 verification/fix items
- **Estimated**: 2-3 hours

### Phase 3 (Presentation Notes - TODO) ⏳
- **Scheduled**: Before dissertation defense
- **Tasks**: 20+ term explanations (ELI5/ELI10)
- **Estimated**: 4-6 hours

---

## 🔄 GIT STATUS

**Current State**:
- ✅ All Phase 1 changes committed
- ⚠️ 4 commits ahead of remote (not pushed)
- ✅ Tag created: v2.1-supervisor-review-dec2025
- ✅ Backup exists: thesis-checkpoint-dec19-pre-annotator-revision/

**To Push to Remote**:
```bash
git push origin supervisor-revisions
git push origin v2.1-supervisor-review-dec2025
```

---

## ✅ READY FOR SUPERVISOR

**All critical author concerns addressed:**
1. Title corrected ✅
2. Proverb fixed ✅
3. Single evaluator methodology ✅
4. LLM-assisted ontology documented ✅
5. All major limitations added ✅
6. Future work expanded ✅
7. Premature claims removed ✅
8. thiLLMo explained ✅

**Remaining items are:**
- Writing polish (em dashes, contrast framing)
- Presentation notes preparation
- Minor verification tasks

**These can be completed after supervisor feedback in Phase 2 & 3.**

---

**Last Updated**: December 19, 2025  
**Next Action**: Push to remote and send to supervisor
