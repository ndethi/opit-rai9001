# DoCEIS 2026 Abstract Submission
## For Supervisor Review

**Conference**: 17th DoCEIS - Doctoral Conference on Computing, Electrical and Industrial Systems  
**Date**: June 17-19, 2026  
**Location**: Lisbon Metropolitan, Portugal  
**Theme**: Technological Innovation to Tackle Societal Challenges  
**Submission Type**: Regular Paper on Ongoing PhD Thesis (12 pages)  
**Deadline**: Full paper submission February 13, 2026

---

## Title
**thiLLMo: Ontology-Grounded RAG for Culturally Faithful Kikuyu Proverb Translation**

## Author Information
Charles Watson Ndethi Kibaki  
Open Institute of Technology (OPIT)  
MSc in Responsible AI  
Email: charleswatsonndeth.k@students.opit.com

---

## Abstract (250 words)

Low-resource African languages face a critical preservation challenge as traditional knowledge risks being lost in the digital age. This paper presents thiLLMo, an Ontology-Grounded Retrieval Augmented Generation (OG-RAG) system addressing the societal challenge of culturally faithful translation for Kikuyu proverbs—a vital component of intangible cultural heritage. Unlike conventional RAG systems that rely on unstructured vector similarity, thiLLMo integrates a formal cultural ontology (959 concepts, 6,445 relationships) with Large Language Models to enable culturally grounded translation.

Evaluation on 100 Kikuyu proverbs demonstrates statistically significant improvements: 10.5% in cultural authenticity (p < 0.001) and 19.8% in overall translation fidelity compared to baseline approaches. The system addresses three societal challenges: preserving endangered cultural knowledge, advancing AI technologies for underserved communities, and demonstrating responsible AI practices through community-centered development.

The OG-RAG architecture consists of four integrated components: (1) a formal OWL ontology capturing Kikuyu cultural concepts and relationships, (2) a Neo4j knowledge graph enabling structured retrieval, (3) an ontology-grounded retrieval mechanism that extracts precise cultural context, and (4) culturally-aware LLM generation preserving metaphorical meaning and cultural authenticity.

This work contributes both a novel OG-RAG architecture for cultural translation and practical evidence that structured cultural knowledge can enhance AI systems while maintaining community ownership and cultural sovereignty. The methodology demonstrates that community-centered development is not merely ethically preferable but technically superior—expert validation during ontology construction directly improves system accuracy. Results suggest viable pathways for sophisticated AI applications in low-resource languages without requiring massive training corpora, offering a scalable model for AI equity.

---

## Keywords
Cultural preservation, Low-resource languages, Ontology-grounded RAG, Knowledge graphs, African languages, Responsible AI, Kikuyu language, Intangible cultural heritage

---

## Research Motivation (1 paragraph)

The rapid digitalization of global knowledge systems creates an urgent preservation challenge for indigenous languages. Kikuyu proverbs (*thimo*) encode centuries of cultural wisdom about social systems, economic practices, and moral frameworks—knowledge that cannot be preserved through simple lexical translation. Existing machine translation systems, even state-of-the-art LLMs, fail catastrophically on culturally nuanced content, either hallucinating generic equivalents or producing culturally inappropriate interpretations. This research addresses a critical societal need: enabling cultural preservation and knowledge transmission for underserved communities in an AI-driven world, while ensuring technological solutions respect cultural sovereignty and community ownership.

---

## Central Research Question

**How can we achieve culturally faithful translation of low-resource language proverbs when confronted with both data scarcity (inherent to underserved languages) and the need for deep cultural grounding (beyond current LLM capabilities)?**

This question bridges three domains: cultural knowledge representation, modern RAG architectures, and low-resource NLP.

---

## Relation to Conference Theme (1 page)

### Societal Challenge 1: Cultural Preservation in the Digital Age

UNESCO identifies intangible cultural heritage (ICH) as critically endangered, with oral traditions particularly vulnerable to loss as indigenous communities increasingly adopt dominant languages. African languages face disproportionate risk: despite representing over 2,000 languages and 1.4 billion speakers, they remain severely underrepresented in digital language technologies, creating a *digital extinction* risk where cultural knowledge cannot be preserved, transmitted, or accessed in modern formats.

Kikuyu proverbs exemplify this challenge. These compact linguistic artifacts encode:
- **Economic systems**: Traditional wealth management, reciprocity practices (*ngwatio*), resource distribution
- **Social structures**: Kinship obligations, generational roles, community governance
- **Moral frameworks**: Ethics of prosperity, concepts of fairness, obligations to others
- **Environmental knowledge**: Agricultural practices, seasonal patterns, resource stewardship

Without culturally faithful translation systems, this knowledge remains inaccessible to diaspora communities, researchers, and future generations—a form of *cultural data loss* that mirrors biodiversity extinction.

**Innovation Response**: thiLLMo addresses this by creating machine-readable formal representations of cultural knowledge that can be preserved, transmitted, and accessed through modern AI systems while maintaining community control over cultural narratives.

### Societal Challenge 2: AI Equity for Underserved Communities

Current AI language technologies exhibit severe inequality. High-resource languages (English, Mandarin, Spanish) benefit from sophisticated translation, question-answering, and generation systems, while low-resource African languages are functionally excluded from the AI revolution. This technological disparity mirrors and reinforces existing global inequalities, denying underserved communities access to AI benefits in education, healthcare, commerce, and cultural preservation.

The challenge is particularly acute for culturally nuanced applications. Generic multilingual models like NLLB-200 achieve lexical translation but fail on cultural semantics—they can translate words but not meaning, producing outputs that are linguistically correct yet culturally nonsensical or even offensive.

**Innovation Response**: The OG-RAG architecture demonstrates that sophisticated AI applications are achievable for low-resource languages without requiring massive training corpora, by strategically combining structured knowledge representation with generative models. This offers a scalable pathway for AI equity that doesn't depend on data availability that may never materialize for underserved languages.

### Societal Challenge 3: Responsible AI Development and Cultural Sovereignty

Mainstream AI development often treats cultural knowledge as extractive data—something to be collected, processed, and deployed without community consent, ownership, or benefit-sharing. This continues colonial patterns of knowledge appropriation, where indigenous knowledge enriches external parties while source communities receive no recognition or compensation.

The challenge extends beyond ethics to technical correctness: AI systems developed without community participation systematically misrepresent cultural knowledge, encoding biases and inaccuracies that compound over time as systems are deployed and propagated.

**Innovation Response**: thiLLMo's development methodology centers community ownership throughout the process—from ontology design to evaluation criteria to benefit-sharing frameworks. Cultural experts are not consultants but co-creators who maintain authority over cultural representation. The project demonstrates that technically superior systems emerge when communities guide development.

### Bridging Technology with Human-Centered Values

These three challenges converge in a single insight: technological innovation must be *shaped by* rather than *imposed on* the communities it serves. thiLLMo demonstrates that culturally responsive AI systems require:
- **Formal knowledge representation** that respects cultural complexity
- **Community participation** as a technical requirement, not ethical decoration
- **Evaluation frameworks** that prioritize cultural fidelity over narrow technical metrics
- **Transparent architectures** that maintain community control over cultural narratives

The system addresses conference themes of sustainability (cultural sustainability), resilience (preserving knowledge for future generations), and responsible innovation (community-centered development). By demonstrating measurable improvements in cultural preservation technology while maintaining ethical development practices, thiLLMo offers a model for tackling societal challenges through innovation that respects human dignity and cultural diversity.

---

## Key Contributions

1. **Novel OG-RAG Architecture**: Ontology-grounded retrieval augmented generation specifically designed for culturally nuanced translation, extending prior work on knowledge graph RAG to the cultural heritage domain.

2. **Empirical Validation**: Rigorous comparative evaluation demonstrating that structured cultural knowledge integration yields statistically significant improvements:
   - Cultural Authenticity: 24.9% improvement over traditional RAG (p < 0.001, Cohen's d = 1.08)
   - Translation Fidelity: 12.8% improvement over traditional RAG (p < 0.001)
   - Metaphorical Preservation: 43.7% improvement over raw LLM baseline

3. **Kikuyu Cultural Ontology**: First formal ontology of Kikuyu cultural knowledge comprising 959 concepts, 6,445 relationships, and 100 proverb instances—a reusable knowledge base for future research.

4. **Community-Centered Methodology**: Replicable framework for responsible AI development in cultural contexts, demonstrating that expert participation improves technical accuracy while ensuring cultural sovereignty.

5. **Evaluation Framework**: Multi-dimensional cultural fidelity assessment combining expert human evaluation with culturally-aware metrics, offering a model for evaluating AI systems in cultural domains.

---

## Expected Impact

**Technical Impact**: Demonstrates viable architectural patterns for sophisticated NLP applications in low-resource languages without requiring massive training corpora—a scalable model applicable to 2,000+ African languages.

**Societal Impact**: Contributes to digital preservation of Kikuyu intangible cultural heritage by formalizing oral knowledge in accessible, structured formats while maintaining community ownership.

**Methodological Impact**: Validates community-centered development as technically superior (not just ethically preferable), establishing frameworks for culturally responsive AI that can guide future work in underserved communities globally.

---

## Supervisor Review Questions

1. **Abstract Clarity**: Does the abstract effectively communicate the research problem, approach, and contributions within 250 words?

2. **Thematic Alignment**: Is the connection to "Technological Innovation to Tackle Societal Challenges" compelling and well-articulated?

3. **Technical Depth**: Are the quantitative results (10.5%, 19.8% improvements) presented with appropriate context and significance?

4. **Positioning**: Should we emphasize different aspects (technical innovation vs. societal impact vs. methodological contribution)?

5. **Submission Type**: Do you agree with "Regular Papers on Ongoing PhD Thesis" (12 pages) as the appropriate category, given the work was completed at Master's level?

6. **Keywords**: Are the selected keywords appropriate for discoverability in engineering/AI conferences?

7. **Strategic Value**: Is DoCEIS 2026 (Springer IFIP AICT, indexed in Web of Science/SCOPUS) a good publication venue for this work?

---

## Next Steps After Supervisor Approval

1. ✅ Finalize abstract based on feedback
2. ⚠️ Check DoCEIS website for exact formatting guidelines (https://doceis.dee.fct.unl.pt/)
3. ⚠️ Complete full 12-page paper (draft already prepared)
4. ⚠️ Anonymize for double-blind review
5. ⚠️ Submit by **February 13, 2026** deadline

---

**Document prepared**: January 24, 2026  
**Status**: Awaiting supervisor review  
**Deadline**: February 13, 2026 (full paper submission)
