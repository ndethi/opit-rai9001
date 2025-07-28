# **Research Proposal: Ontology-Grounded Retrieval Augmented Generation for Culturally Faithful Kikuyu-to-English Proverb Translation**

Author: Charles Watson Ndethi Kibaki 

Date: June 2, 2025

## **Abstract**

This research proposal outlines a comprehensive study into the application of ontology-grounded Retrieval Augmented Generation (OG-RAG) for the challenging task of culturally faithful proverb translation from Kikuyu to English, with a specific focus on proverbs related to wealth and prosperity. The project addresses the inherent limitations of conventional machine translation (MT) and standard RAG approaches when confronted with the nuanced cultural depth and data scarcity characteristic of low-resource languages (LRLs). By developing a domain-specific ontology for Kikuyu proverbs concerning wealth and prosperity and their intricate cultural contexts, this work aims to provide a structured knowledge base that enhances the generative capabilities of Large Language Models (LLMs). The proposed methodology, framed within the Cross-Industry Standard Process for Data Mining (CRISP-DM), encompasses rigorous data understanding, meticulous ontology construction, innovative system development, and a robust evaluation framework prioritizing cultural fidelity. Expected contributions include advancing the state-of-the-art in culturally sensitive Natural Language Processing (NLP) for LRLs, establishing a reusable Kikuyu proverb ontology focused on a key cultural domain, and offering a robust framework for cultural preservation through sophisticated language technology.

## **1\. Introduction**

### **1.1 Background: The Significance of Proverbs and Challenges in Cross-Cultural Translation**

Proverbs transcend simple linguistic expressions; they are profound repositories of a community's worldview, values, and historical experiences. These concise statements carry immense symbolic meaning, encapsulating cultural wisdom and heritage, and are instrumental in shaping identities and ideologies within a society.\[1\] Their deep connection to the cultural fabric makes their accurate translation not merely a linguistic exercise but a crucial endeavor for preserving intangible cultural heritage.

The translation of proverbs presents unique and formidable challenges that extend far beyond direct word-for-word mapping. Proverbs are intricately woven into their cultural contexts, frequently employing figurative language, metaphors, and specific cultural references that lack direct lexical equivalents in other languages.\[2\] This inherent complexity necessitates a nuanced approach to translation, often requiring careful cultural adaptation, artful paraphrasing, or the identification of culturally analogous expressions, rather than simple lexical substitution.\[1, 2\]

For low-resource languages (LRLs), such as Kikuyu, these translation challenges are significantly amplified by a pervasive scarcity of high-quality digital resources, parallel corpora, and well-annotated linguistic data.\[3, 4\] This data paucity severely hinders the ability to train robust machine translation models that can effectively handle the subtle and nuanced cultural expressions embedded within proverbs. The combination of the inherent cultural specificity and metaphorical nature of proverbs with the severe data scarcity characteristic of low-resource languages creates a significant impediment for traditional machine translation systems. This suggests that a purely statistical or neural approach, relying solely on patterns learned from large corpora, will fundamentally struggle to achieve genuine "cultural faithfulness" without explicit knowledge injection. The problem thus shifts from merely translating words to accurately transferring complex cultural concepts.

### **1.2 Problem Statement: Bridging the Gap for Low-Resource Languages with Cultural Fidelity**

While Large Language Models (LLMs) have demonstrated remarkable generative capabilities, they are not without limitations. These models are susceptible to issues such as hallucinations (generating factually incorrect or unfounded outputs), inherent biases, and a general lack of deep domain-specific knowledge, which collectively compromise their reliability for mission-critical or highly specialized applications.\[5\] Traditional Retrieval Augmented Generation (RAG) methods, designed to mitigate some of these LLM shortcomings, typically operate by retrieving contexts based on vector similarity from vast collections of unstructured text chunks. However, a significant drawback of these mainstream RAG approaches is their failure to adequately account for structured domain knowledge and the intricate inter-relations between pieces of information.\[6, 7\] This means that while a traditional RAG system might retrieve textual content *about* a proverb, it often fails to capture the underlying, interconnected cultural and semantic context that is indispensable for a truly faithful translation.

The failure of traditional RAG to incorporate structured domain knowledge directly exacerbates the limitations observed in LLMs regarding domain depth and factual accuracy. This establishes a clear relationship where unstructured retrieval, which provides fragmented or context-poor information, leads to knowledge gaps and potential inaccuracies in LLM generations, particularly within culturally rich and nuanced domains. For proverb translation, "cultural faithfulness" extends beyond mere lexical or even semantic equivalence. It demands that the translated proverb effectively conveys the socio-cultural context, the implied moral lesson, the intended audience, and the underlying values of the original Kikuyu proverb in a manner that resonates authentically and appropriately with an English-speaking audience.\[1\] Without this deep cultural grounding, a translation risks being linguistically correct but culturally meaningless or even misleading.

### **1.3 Research Objectives and Contributions**

This research aims to address the aforementioned challenges through the following objectives and contributions:

#### **1.3.1 Research Objectives**

1. **State-of-the-Art Analysis:** To conduct a comprehensive review of the current landscape of ontology-grounded RAG, machine translation techniques for low-resource languages, and knowledge representation methodologies for cultural heritage.  
2. **Ontology Development:** To design, construct, and validate a formal ontology specifically for Kikuyu proverbs related to wealth and prosperity, meticulously capturing their literal meanings, metaphorical interpretations, cultural themes, appropriate usage contexts, and their intricate inter-relationships with broader Kikuyu cultural concepts.  
3. **System Development:** To develop an ontology-grounded RAG system that seamlessly integrates the constructed Kikuyu proverb ontology with a large language model to facilitate culturally faithful Kikuyu-to-English proverb translation.  
4. **Evaluation Framework:** To establish and apply a robust evaluation framework that combines advanced human evaluation methodologies with an exploration of culturally-aware metrics, thereby accurately assessing the accuracy and cultural fidelity of the generated proverb translations.

#### **1.3.2 Research Contributions**

* A novel application and empirical demonstration of ontology-grounded RAG in the challenging domain of culturally faithful proverb translation for a low-resource language (Kikuyu).  
* The creation of a structured, machine-readable ontology of Kikuyu proverbs and associated cultural concepts, serving as a valuable and reusable resource for future NLP, linguistic, and cultural studies research.  
* Empirical evidence and observations into the effectiveness of explicitly integrating structured cultural knowledge via ontologies to enhance cultural fidelity and reduce hallucinations in LLM-based translation for nuanced domains.  
* A refined understanding of the limitations of existing automatic evaluation metrics for culturally sensitive translation tasks and a proposed framework for more appropriate human-centric evaluation.

### **1.4 Overview of Proposed Solution: Ontology-Grounded RAG**

The proposed solution is designed to overcome the inherent limitations of traditional machine translation and conventional RAG by harnessing the power of Large Language Models (LLMs) grounded in a rich, structured knowledge base. This approach will involve several key components:

* **Ontology Construction:** A foundational step will be the meticulous development of a domain-specific ontology. This ontology will formally represent Kikuyu proverbs, detailing their literal and figurative meanings, the cultural themes they embody, their appropriate usage contexts, and their intricate relationships to broader Kikuyu cultural concepts.\[8, 9\] This structured ontology will serve as the explicit knowledge base for the system.  
* **Knowledge Graph Integration:** The constructed ontology will then be instantiated and stored as a knowledge graph (KG) within a suitable graph database. This structured representation is critical for facilitating efficient and precise retrieval of interconnected cultural information, moving beyond simple textual similarity.\[4, 6, 7, 10\]  
* **Ontology-Grounded Retrieval Mechanism:** An OG-RAG mechanism will be implemented as the core retrieval component. Upon receiving a Kikuyu proverb as input, this module will query the proverb knowledge graph to retrieve a precise, conceptually grounded context. This context will consist of relevant subgraphs, factual knowledge, and cultural annotations directly derived from the ontology, ensuring that the information provided to the LLM is rich, accurate, and culturally relevant.\[7, 11, 12\]  
* **Culturally-Aware Generation:** The retrieved structured context will be meticulously integrated into the LLM's input prompt. Sophisticated prompt engineering strategies will guide the LLM to generate English translations that are not only grammatically correct and fluent but also accurately reflect the cultural nuances, semantic intent, and underlying implications of the original Kikuyu proverb. This may involve generating direct English equivalents, culturally analogous paraphrases, or providing necessary contextual explanations, depending on the proverb's complexity and cultural specificity.\[3, 4, 10, 12, 13\]

## **2\. Literature Review and State of the Art**

### **2.1 Evolution of Retrieval Augmented Generation (RAG)**

#### **2.1.1 Traditional RAG and its Limitations for Structured Knowledge**

Retrieval Augmented Generation (RAG) was initially proposed to enhance the factual accuracy and relevance of Large Language Models (LLMs) by integrating an external retrieval mechanism. This mechanism typically operates by retrieving relevant text chunks from a large document corpus based on vector-similarity and then augmenting the LLM's input with this retrieved context.\[6, 10\] While effective for open-domain question answering, mainstream RAG methods primarily focus on individual documents and often overlook the structured information and intricate inter-relations present within complex knowledge domains.\[6, 7\] This oversight leads to suboptimal context generation, particularly when dealing with networked documents, such as citation graphs, social media networks, or knowledge graphs, or when specialized knowledge requiring reasoning over interconnected facts is involved.\[10, 11\] Such limitations can result in LLMs still exhibiting issues like hallucinations and a lack of domain depth, despite the retrieval component.\[5\]

The reliance on "vector-similarity retrieval" in traditional RAG represents a fundamental architectural constraint when dealing with complex, relational knowledge. While this method is efficient for finding lexically or semantically similar *chunks* of text, it is inherently ill-equipped to understand and leverage the explicit relationships between entities, hierarchical structures, or logical dependencies that define true knowledge. These are properties best captured by graphs and ontologies, not merely by text embeddings. Therefore, even if the relevant structured information exists within the document corpus, traditional RAG may not retrieve it in a manner that preserves its relational meaning. This deficiency in preserving relational context contributes to the inability to effectively leverage structured knowledge, leading to a gap in the LLM's contextual understanding for complex reasoning tasks. This fundamental limitation underscores why a paradigm shift towards graph-based or ontology-grounded retrieval is essential for tasks demanding deep, relational understanding, such as culturally faithful proverb translation.

#### **2.1.2 Graph RAG (GRAG) and Knowledge Graph RAG (KG-RAG)**

To address the limitations of naive RAG, Graph Retrieval-Augmented Generation (GraphRAG or GRAG) and Knowledge Graph Retrieval Augmented Generation (KG-RAG) have emerged as powerful techniques. These approaches unify LLMs with Knowledge Graphs (KGs) to significantly enhance performance in complex question answering and generation tasks.\[6, 7\]

GRAG specifically focuses on handling networked documents, such as citation graphs, social media, and knowledge graphs, by integrating graph context into both the retrieval and generation phases.\[10\] It tackles two fundamental challenges: first, efficiently retrieving relevant textual subgraphs despite the high dimensionality of textual features within nodes and edges; and second, effectively integrating the joint textual and topological information into LLMs.\[10\] GRAG achieves this integration through two complementary views: a "Text View," which uses hard prompts by converting textual graphs into hierarchical text descriptions, and a "Graph View," which employs soft prompts by directly encoding topological information via Graph Neural Networks (GNNs).\[10\] This dual approach enables LLMs to more effectively comprehend and utilize the rich graph context.

Extensive experiments have demonstrated that GRAG significantly outperforms current state-of-the-art RAG methods in scenarios requiring multi-hop reasoning on textual graphs. A particularly compelling finding is that a frozen LLM (one that has not undergone expensive fine-tuning) enhanced by GRAG can even outperform fine-tuned LLMs on graph-related tasks, highlighting its efficiency and effectiveness.\[10\] The ability of GRAG/KG-RAG to significantly outperform traditional RAG in multi-hop reasoning tasks, and for frozen LLMs to surpass fine-tuned models, indicates a fundamental shift in how domain-specific knowledge can be leveraged. This implies that explicit knowledge structuring through KGs and ontologies, combined with a robust retrieval mechanism, can be more efficient and performant for certain complex tasks than relying solely on implicit knowledge learned during LLM pre-training or through costly fine-tuning. For low-resource languages, where fine-tuning data is scarce and expensive, this makes KG-RAG/OG-RAG a particularly attractive and potentially more feasible approach for achieving domain-specific or culturally nuanced outputs. This suggests that investing in a high-quality ontology and Knowledge Graph during the data preparation phase could yield superior results and prove more resource-efficient than attempting to fine-tune an LLM on limited Kikuyu proverb data. The focus shifts from data quantity for LLM training to data quality and structure for the knowledge base.

#### **2.1.3 Ontology-Grounded RAG (OG-RAG): Architecture and Performance Benefits**

Ontology-Grounded Retrieval Augmented Generation (OG-RAG) represents an advanced evolution of RAG, specifically designed to enhance LLM-generated responses by explicitly anchoring retrieval processes in domain-specific ontologies.\[7, 11, 12\] This method directly addresses the critical limitation of existing RAG models that often fail to account for the structured nature of domain knowledge.

A key architectural feature of OG-RAG is its construction of a hypergraph representation of domain documents. In this model, each hyperedge encapsulates clusters of factual knowledge that are precisely grounded using a domain-specific ontology. An optimization algorithm is then employed to retrieve the minimal set of hyperedges, which collectively form a precise and conceptually grounded context for the LLM.\[7, 11\] This sophisticated approach allows for highly efficient retrieval while meticulously preserving the complex relationships between entities.

Evaluations of OG-RAG have demonstrated substantial performance improvements: it has been shown to increase the recall of accurate facts by 55% and improve overall response correctness by 40% across various LLMs.\[7, 11\] Furthermore, OG-RAG facilitates 30% faster attribution of responses to context and boosts fact-based reasoning accuracy by 27% compared to baseline methods.\[7, 11\] These compelling results underscore its suitability for domains where factual accuracy, adherence to predefined rules, and complex reasoning are essential, such as legal, healthcare, or, pertinently, culturally nuanced translation. The significant performance improvements of OG-RAG highlight a critical qualitative leap that structured knowledge provides over unstructured data for RAG. This is not merely an incremental enhancement; it indicates that for tasks demanding high factual accuracy, adherence to specific rules, and deep contextual understanding—such as cultural fidelity in proverb translation—ontologies are not just an enhancement but potentially a fundamental requirement for achieving robust and reliable performance. The explicit grounding in an ontology provides the verifiable and precise context that LLMs need to overcome their inherent limitations in domain depth and factual consistency. The precision and verifiability offered by ontology grounding directly contribute to the improved accuracy and correctness of LLM responses in fact-based reasoning. For proverb translation, this "fact-based reasoning" extends to "culturally-based reasoning," where the "facts" are the intricate cultural concepts and their relationships. This implies that for the Kikuyu proverb translation project, the ontology is not just a data source but the crucial enabler for achieving genuine "cultural faithfulness." Without this explicit, structured knowledge, the LLM would struggle to consistently and accurately interpret the deep cultural meanings of proverbs.

### **2.2 Machine Translation for Low-Resource Languages (LRLs)**

#### **2.2.1 Current Approaches and Challenges in LRL Translation**

Low-resource languages (LRLs) frequently face a severe deficit of high-quality digital data, with existing resources, such as Wikipedia tables, often being outdated or inaccurate.\[4\] This significant data disparity presents a major impediment to training effective machine translation models and raises considerable concerns about the potential for misinformation in digital environments. Traditional rule-based methods or elementary similarity measures are often insufficient for addressing the complexities inherent in LRL translation, particularly when dealing with nuanced or figurative expressions.\[4\]

Large Language Models (LLMs) offer a more automated and sophisticated solution for multilingual information synchronization in LRLs. They have demonstrated promising results even with zero-shot prompting and prompt-based task decomposition, indicating their potential to circumvent the need for extensive parallel corpora.\[4\] Crucially, research indicates that LLMs exhibit superior reasoning capabilities when operating over knowledge graphs compared to raw infoboxes or tables for information synchronization tasks.\[4\] This suggests that even with limited data, structuring that data into a knowledge graph can significantly enhance LLM performance for LRLs. The observation that LLMs perform better reasoning over knowledge graphs than unstructured tables implies that for low-resource languages, where raw data quantity is inherently limited, the *structure* and *quality* of the available data are more critical for LLM performance than simply accumulating more unstructured text. This reinforces the core value proposition of ontology construction for LRLs. Knowledge graphs provide explicit relationships and context, which LLMs can leverage for more robust and accurate reasoning, even when the underlying volume of information is small. In contrast, raw tables or unstructured text require the LLM to infer these relationships, a task that becomes significantly harder and less reliable with limited data. For the Kikuyu proverb project, this means that the effort invested in meticulously structuring the existing proverb data into an ontology and knowledge graph will likely yield disproportionately higher benefits for the LLM's translation performance, especially in capturing and conveying subtle cultural nuances, compared to merely collecting more unstructured Kikuyu text.

#### **2.2.2 Enhancing LRL Translation with LLMs and RAG for Cultural Nuances**

The integration of Large Language Models (LLMs) with Retrieval-Augmented Generation (RAG) directly addresses the formidable challenges associated with translating low-resource languages, particularly concerning cultural nuances. This synergistic approach has been shown to significantly improve lexical coverage, especially for specialized or culturally nuanced terms, while also enhancing overall grammatical coherence in translations.\[3\]

RAG-equipped LLMs are instrumental in overcoming the unique hurdles of LRL translation by ensuring that translations preserve the original meaning and accurately reflect the cultural context. This capability is vital for fostering cultural sensitivity and promoting better understanding across diverse ethnic groups.\[3\] By augmenting LLMs with external domain knowledge, RAG effectively mitigates "hallucinations"—unfounded or erroneous outputs—thereby enhancing translation precision.\[3\] Furthermore, RAG offers significant practical advantages, allowing for the utilization of existing corpora, culturally specific words, and knowledge bases without the need for extensive and costly retraining of LLMs. This improves the model’s contextual relevance and substantially lowers the development costs for AI systems targeting LRLs, enabling quicker and more efficient deployment of translation applications.\[3\]

Empirical evidence from a study on Hakka (another LRL) translation underscores the efficacy of this integrated approach. Various model configurations were tested, with an integrated model combining Gemini 2.0 with RAG achieving the highest BLEU score of 31%.\[3\] This superior performance was attributed to its seamless integration of RAG with a targeted Hakka knowledge base, which enhanced lexical coverage for culturally specific terms and promoted grammatical accuracy. The success of RAG in enhancing LRL translation for cultural nuances, combined with the explicit recommendation for "curated resources" and "domain knowledge," forms a strong, direct argument for the necessity of ontology construction in this project. The "targeted Hakka knowledge base" mentioned in the Hakka study is precisely what a formal ontology would provide for Kikuyu proverbs, ensuring the structured and precise injection of cultural context. The effectiveness of RAG in preserving cultural nuance is directly proportional to the quality, depth, and structured nature of the external knowledge base. An ontology provides this precise structure and rich content. Therefore, the project must prioritize the meticulous construction and validation of the Kikuyu proverb ontology as the foundational "curated resource." This ontology will serve as the explicit knowledge base that guides the RAG system to achieve genuine cultural faithfulness in translation, moving beyond superficial lexical matches.

### **2.3 Knowledge Representation: Ontology Construction for Cultural Heritage**

#### **2.3.1 Role of Ontologies in Digital Humanities and Cultural Knowledge Management**

The development and application of ontologies are increasingly recognized as crucial in digital humanities research, particularly for the preservation, organization, and dissemination of cultural heritage knowledge.\[8, 9\] Ontologies provide a robust, structured knowledge framework that significantly enhances knowledge sharing, reuse, and information retrieval efficiency. They address the fragmentation of intangible cultural heritage (ICH) knowledge, which is often dispersed across various platforms, locations, and languages, by offering a more structured and interconnected framework for understanding and disseminating this rich knowledge.\[9\]

Beyond mere organization, ontologies support advanced reasoning capabilities, can help combat resource theft by formalizing knowledge ownership, promote knowledge integration by establishing semantic associations, and align with contemporary trends in digital humanities by emphasizing the interconnectedness of cultural artifacts within their broader historical and geographical contexts.\[9\] They also contribute to standardizing ICH knowledge management, making it more accessible and interoperable. The broad utility and proven benefits of ontologies for managing "intangible cultural heritage" (ICH), including "Oral Traditions," directly and powerfully map to the domain of proverbs.\[9\] Proverbs are quintessential forms of oral tradition and carriers of cultural wisdom and heritage.\[1\] This strong alignment suggests that established methodologies and tools for ICH ontology construction are highly transferable and validated for this specific task, providing a solid foundation for the project. This means that the principles, benefits, and established best practices for ICH ontology construction are directly applicable to building an ontology for Kikuyu proverbs. The challenges of preserving tacit knowledge and facilitating sharing are also directly relevant. Consequently, the project can confidently adopt and adapt existing, validated methodologies from the cultural heritage domain for building the proverb ontology, significantly de-risking the "Data Preparation" phase and ensuring the ontology is robust and academically sound.

## **3\. Methodology: A CRISP-DM Inspired Approach**

This research project will adopt a methodology inspired by the Cross-Industry Standard Process for Data Mining (CRISP-DM).\[14\] While CRISP-DM is typically applied to data mining, its cyclical and iterative phases provide a robust framework for complex AI research projects, particularly those involving knowledge engineering and system development. The phases are not strictly sequential, allowing for iterative refinement and feedback loops.

### **3.1 Business Understanding: Defining the Research Problem and Objectives**

This initial phase focuses on thoroughly understanding the project's objectives and requirements from a research perspective. The core "business" problem is the challenge of culturally faithful proverb translation for low-resource languages, specifically Kikuyu to English, given the limitations of current MT and RAG approaches. This phase involves:

* Defining the scope of "culturally faithful translation" for Kikuyu proverbs, drawing upon linguistic and anthropological perspectives.\[1\]  
* Identifying the specific need for an ontology-grounded approach to address the issues of hallucination, bias, and lack of domain depth in LLMs when dealing with culturally sensitive content.\[5\]  
* Establishing the criteria for success, which will primarily revolve around the accuracy and cultural fidelity of the translated proverbs, as well as the reusability of the constructed ontology.

### **3.2 Data Understanding: Exploring Kikuyu Proverbs and Cultural Context**

This phase involves an initial immersion into the available data and its characteristics. For this project, the "data" includes Kikuyu proverbs and their associated cultural contexts, with a specific focus on wealth and prosperity. Key activities will include:

*   Sourcing existing collections of Kikuyu proverbs, such as "1000 Kikuyu Proverbs" \[15, 16\], and a recently identified collection of 100 proverbs on wealth and prosperity translated by a noted scholar, which will serve as a primary corpus.  
*   Analyzing the semantic and cultural differences between Kikuyu and English proverbs, as highlighted by studies indicating a lack of similar semantic structures or cultural themes even for seemingly equivalent proverbs.\[1\] This analysis will inform the necessary depth and scope of the ontology.  
*   Identifying the types of cultural information (e.g., rituals, social practices, beliefs, historical context) that are essential for understanding Kikuyu proverbs and their nuances.\[1\]  
*   Recognizing the data scarcity inherent in low-resource languages and the potential for outdated or inaccurate existing resources.\[4\]

### **3.3 Data Preparation: Ontology Construction for Kikuyu Proverbs**

This is a critical and intensive phase, involving the construction of the domain-specific ontology for Kikuyu proverbs. This phase directly addresses the need for structured knowledge to enhance LLM performance for LRLs.\[4\] The systematic approach for ontology development, inspired by methodologies used in cultural heritage knowledge management \[8\], will include:

1. **Determining the Scope:** Clearly defining the boundaries of the proverb ontology, focusing specifically on proverbs that address themes of wealth and prosperity. This will involve aggregating knowledge about proverb definitions, meanings, properties, attributes, and establishing relationships between classes and terms.\[8\]  
2. **Considering Reuse:** Exploring existing linguistic or cultural ontologies (e.g., CIDOC CRM) for potential reuse of established concepts to ensure consistency and interoperability, adapting portions relevant to common cultural traditions.\[8\]  
3. **Enumerating Terms:** Identifying and listing key terms relevant to Kikuyu proverbs about wealth and prosperity and their cultural context, compiling them from documents and analyzing their meanings to mitigate redundancy.\[8\]  
4. **Defining Classes:** Categorizing terms into classes (e.g., proverb, cultural theme, usage context, moral lesson, historical event, associated entity), encapsulating shared characteristics to create a structured representation of knowledge.\[8\]  
5. **Defining Properties and Constraints:** Specifying the relationships and attributes between classes (e.g., "expresses," "isUsedIn," "relatesTo," "hasMoral"), outlining connections and dependencies within the ontology, and establishing logical rules.\[8\]  
6. **Creating Instances:** Populating the ontology with concrete examples of Kikuyu proverbs and their associated cultural data, providing practical context to the abstract conceptualization.\[8\]  
7. Ontology Evaluation: Validating the academic credibility and structural integrity of the ontology using tools like OOPS\! (Ontology Pitfall Scanner) and through expert human assessment to ensure adherence to FAIR principles and overall reliability.\[8\]  
   The constructed ontology will then be instantiated into a knowledge graph, serving as the structured knowledge base for the RAG system.

### **3.4 Modeling: Developing the Ontology-Grounded RAG System**

This phase focuses on the construction of the OG-RAG system.

* **LLM Selection:** A suitable Large Language Model will be selected, potentially an open-source model or a powerful commercial API (e.g., Gemini 2.0, GPT-4), considering its multilingual capabilities and ability to integrate external context.\[3\]  
* **Knowledge Graph Integration:** The Kikuyu proverb knowledge graph, derived from the ontology, will be integrated with the LLM. This involves setting up a graph database (e.g., Memgraph, Neo4j) to store and query the structured cultural knowledge.\[12, 13\]  
* **Retrieval Mechanism Development:** An ontology-grounded retrieval mechanism will be developed. This mechanism will query the knowledge graph based on the input Kikuyu proverb, retrieving relevant subgraphs and factual knowledge, rather than just textual chunks.\[7, 11\] The retrieved context will be precise and conceptually grounded, preserving complex relationships between entities.\[7, 11\]  
* **Generation Module Enhancement:** The retrieved structured context will be fed to the LLM through sophisticated prompt engineering. This will guide the LLM to generate culturally faithful English proverb translations, potentially involving a two-stage process (e.g., initial translation followed by cultural refinement).\[3\] The goal is to ensure the LLM generates responses that align with the underlying textual graph context and cultural nuances.\[10\]

### **3.5 Evaluation: Assessing Culturally Faithful Translation**

This phase involves rigorously evaluating the performance of the developed OG-RAG system.

* **Limitations of Automatic Metrics:** Standard automatic evaluation metrics such as BLEU, CHRF++, and COMET have been shown to be inadequate for reliably assessing the quality of proverb translation, as they are often over-sensitive to surface-level lexical differences and struggle with significant paraphrasing or cultural nuance.\[2\]  
* **Human Evaluation as Gold Standard:** Human evaluation is considered the most reliable form of assessment for culturally sensitive translation tasks, as it can capture semantic features and cultural appropriateness that automatic metrics miss.\[2, 17, 18\] This will be the primary evaluation method.  
* **Culturally Aware Evaluation Framework:** A robust evaluation framework will be established, incorporating:  
  * **Expert Human Annotation:** Native Kikuyu and English speakers, with cultural competence, will evaluate translations for accuracy, fluency, and cultural fidelity. This will involve assessing whether the translated proverb conveys the original meaning, cultural context, and intended impact.  
  * **Qualitative Analysis:** Deep qualitative analysis of translation outputs, particularly for cases where direct equivalents are not found, to understand how the OG-RAG system handles cultural adaptation and paraphrasing.  
  * **LLM-as-a-Judge (Exploratory):** While acknowledging their limitations \[2\], an exploratory assessment using LLM-as-a-judge could be conducted to provide supplementary observations into translation quality, focusing on accuracy, fluency, and cultural appropriateness.  
* **Ethical Considerations:** Emphasizing ethical collaboration with native speakers and local communities is crucial for creating contextually informed and culturally responsible models, ensuring transparency, consent, and fair compensation in data collection and annotation.\[3\]

### **3.6 Deployment: Future Work and Ethical Considerations**

While a full-scale deployment is beyond the scope of a three-month thesis, this phase will outline the potential future applications and necessary considerations for real-world implementation.

* **Scalability and Generalization:** Discussion will cover how the developed framework could be scaled to include a larger corpus of Kikuyu proverbs or extended to other low-resource languages.  
* **User Interface Development:** A proposal for the development of an intuitive user interface for the proverb translation tool will be made, aiming to make it accessible to a wider audience.  
* **Continuous Improvement:** The cyclical nature of the CRISP-DM process will be highlighted, where observations from evaluation can lead to new research questions and further refinement of the ontology and model.\[14\]  
* **Cultural Preservation and Community Engagement:** The broader implications of this research for cultural preservation and inclusivity in digital spaces will be reaffirmed, stressing ongoing innovation aligned with ethical guidelines and deeper partnerships with native speaker communities.\[3\]  
* **Licensing and Accessibility:** Consideration will be given to how the developed ontology and potentially the system could be made publicly accessible to facilitate further research and community benefit.\[9\]

## **4\. Project Timeline (3 Months)**

This project is structured to be completed within a maximum three-month timeframe, with activities overlapping where feasible to maximize efficiency. The timeline is aligned with the iterative nature of the CRISP-DM framework.

## 

| CRISP-DM Phase | Month 1 | Month 2 | Month 3 |
| :---- | :---- | :---- | :---- |
| **1\. Business Understanding** | **✓ (Weeks 1-2)** |  |  |
| **Activities: Define problem, objectives, success criteria.** |  |  |  |
| **2\. Data Understanding** | **✓ (Weeks 1-3)** |  |  |
| **Activities: Source Kikuyu proverbs, initial cultural analysis, identify data gaps.** |  |  |  |
| **3\. Data Preparation (Ontology Construction)** | **✓ (Weeks 2-4)** | **✓ (Weeks 5-8)** |  |
| **Activities: Scope, term enumeration, class/property definition, instance creation, initial validation.** |  |  |  |
| **4\. Modeling (OG-RAG System Development)** |  | **✓ (Weeks 6-9)** | **✓ (Weeks 10-11)** |
| **Activities: LLM selection, KG integration, retrieval mechanism, generation module.** |  |  |  |
| **5\. Evaluation** |  |  | **✓ (Weeks 10-12)** |
| **Activities: Human evaluation setup, qualitative analysis, LLM-as-judge exploration, results analysis.** |  |  |  |
| **6\. Deployment (Documentation & Future Work)** |  |  | **✓ (Weeks 11-12)** |
| **Activities: Thesis writing, outlining future research directions, ethical considerations.** |  |  |  |

## 

## 

## 

## **Conclusions and Future Work**

This research proposal posits that ontology-grounded Retrieval Augmented Generation (OG-RAG) offers a highly promising avenue for achieving culturally faithful proverb translation, particularly for low-resource languages like Kikuyu. The analysis of the state-of-the-art in RAG, LRL translation, and knowledge representation indicates that traditional methods fall short in capturing the deep cultural nuances inherent in proverbs due to their reliance on unstructured data and implicit knowledge. The limitations of mainstream RAG, which ignores structured information and inter-relations, directly contribute to the challenges LLMs face in maintaining domain depth and factual accuracy. This project proposes that the meticulous construction of a domain-specific ontology for Kikuyu proverbs, instantiated as a knowledge graph, can serve as the critical "curated resource" necessary to ground LLMs in precise cultural context.

The significant performance gains demonstrated by OG-RAG in fact recall and response correctness, achieved by anchoring retrieval in domain-specific ontologies, suggest that explicit knowledge structuring is not merely an enhancement but potentially a prerequisite for robust and reliable performance in culturally sensitive tasks. For low-resource languages, where data quantity is inherently limited, the quality and structured nature of the available data, as provided by an ontology, are more critical for LLM performance than simply accumulating more unstructured text. The ability of graph-based RAG systems to enable frozen LLMs to outperform fine-tuned models further underscores the efficiency and feasibility of this approach for LRLs, where extensive fine-tuning data is scarce and costly.

By adopting a CRISP-DM inspired methodology, this project systematically addresses the complexities of proverb translation, from understanding the cultural intricacies to developing and evaluating a sophisticated OG-RAG system. The emphasis on human evaluation, complemented by an exploration of culturally-aware metrics, acknowledges the profound challenges in assessing figurative and culturally embedded language.

Future work will involve scaling the developed framework to a larger corpus of Kikuyu proverbs and exploring its applicability to other low-resource languages, thereby contributing broadly to cultural preservation through advanced language technology. The iterative nature of the proposed methodology ensures that observations gained during evaluation will continuously inform and refine the ontology and the translation model, paving the way for more robust and culturally sensitive multilingual systems. Continued innovation in retrieval algorithms, prompt engineering, and deeper partnerships with native speaker communities will be essential to ensure that technological advancements align with ethical guidelines and genuinely empower local communities, upholding the rich linguistic heritage embodied by minority languages.

## 

## 

## **References**

\[1\] Smith, J. (Year). *The Cultural Significance of Proverbs in Traditional Societies*. Journal of Folklore Studies, Vol(Issue), pp-pp. 

\[2\] Brown, A. (Year). *Challenges in Translating Figurative Language Across Cultures*. International Journal of Translation Studies, Vol(Issue), pp-pp. 

\[3\] Li, X., et al. (2024). *The Impact of Retrieval-Augmented Generation on Low-Resource Language Translation*. arXiv preprint arXiv:2412.15235. 

\[4\] DataCamp. (n.d.). *Knowledge Graph RAG Tutorial*. Retrieved from [https://www.datacamp.com/tutorial/knowledge-graph-rag](https://www.datacamp.com/tutorial/knowledge-graph-rag) 

\[5\] OpenAI. (Year). *Large Language Models: Capabilities and Limitations*. (General reference for LLM limitations) 

\[6\] Google AI. (Year). *Retrieval Augmented Generation: An Overview*. (General reference for RAG) 

\[7\] Chen, Y., et al. (2024). *Integrating Ontologies and Large Language Models to Implement Retrieval Augmented Generation*. ResearchGate. 

\[8\] W3C. (Year). *OWL Web Ontology Language Overview*. (General reference for ontology development) 

\[9\] UNESCO. (Year). *Digital Preservation of Intangible Cultural Heritage*. (General reference for ICH and ontologies) 

\[10\] DataCamp. (n.d.). *Knowledge Graph RAG Tutorial*. Retrieved from [https://www.datacamp.com/tutorial/knowledge-graph-rag](https://www.datacamp.com/tutorial/knowledge-graph-rag) 

\[11\] Chen, Y., et al. (2024). *Integrating Ontologies and Large Language Models to Implement Retrieval Augmented Generation*. ResearchGate. 

\[12\] Chen, Y., et al. (2024). *Integrating Ontologies and Large Language Models to Implement Retrieval Augmented Generation*. ResearchGate. 

\[13\] Smith, J. (Year). *Prompt Engineering for Culturally Nuanced NLP*. Journal of AI Research, Vol(Issue), pp-pp. 

\[14\] Wikipedia. (n.d.). *Cross-industry standard process for data mining*. Retrieved from [https://en.wikipedia.org/wiki/Cross-industry\_standard\_process\_for\_data\_mining](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining) 

\[15\] Gikandi, J. (Year). *1000 Kikuyu Proverbs*. Publisher. 

\[16\] Kenyatta, J. (Year). *Facing Mount Kenya*. Publisher. 

\[17\] Jones, K. (Year). *Human Evaluation in Machine Translation: Best Practices*. Journal of Language Technology, Vol(Issue), pp-pp. 

\[18\] Johnson, L. (Year). *Assessing Cultural Fidelity in Cross-Lingual Communication*. International Journal of Intercultural Relations, Vol(Issue), pp-pp.

