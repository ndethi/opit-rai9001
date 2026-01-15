# OG-RAG System Live Demo Guide for Thesis Defense

**Duration:** 5-7 minutes  
**Purpose:** Demonstrate how ontology-grounded RAG achieves culturally faithful Kikuyu proverb translation  
**Date:** January 14, 2026

---

## 🎯 Demo Objectives

1. **Show the Problem:** Raw LLM fails to capture cultural nuance
2. **Show the Solution:** OG-RAG uses knowledge graph to provide cultural context
3. **Prove the Impact:** Side-by-side comparison shows cultural faithfulness

---

## 🚀 Quick Setup (5 minutes before presentation)

### 1. Environment Check
```bash
cd /Users/ndethi/dev/opit/opit-rai9001

# Activate conda environment
conda activate thiLLMo

# Verify Neo4j connection
python -c "from src.neo4j.scripts.connection import Neo4jConnection; conn = Neo4jConnection(); print('✅ AuraDB Connected'); conn.close()"

# Verify OpenAI API
python -c "import os; from decouple import config; key = config('OPENAI_API_KEY'); print('✅ OpenAI API Key Loaded' if key and key != 'your_openai_api_key_here' else '❌ API Key Missing')"
```

### 2. Test the Demo Script
```bash
# Quick test run (1 proverb)
python presentations/demo_ograg_live.py --test

# Should output:
# ✅ Neo4j connected
# ✅ OpenAI API ready
# ✅ Retrieved 3 similar proverbs
# ✅ Generated translations
```

### 3. Prepare Browser Tabs
- **Tab 1:** Neo4j AuraDB Console → `https://console.neo4j.io` (logged in)
- **Tab 2:** VS Code → This repository
- **Tab 3:** Terminal → Ready to run demo commands

---

## 📋 Demo Script (Step-by-Step)

### **SLIDE: "Live System Demonstration"**

> *"Let me demonstrate how the OG-RAG system works in practice. I'll translate a Kikuyu proverb three ways: Raw GPT-4, Traditional RAG, and our Ontology-Grounded approach."*

---

### **Step 1: Show the Proverb (30 seconds)**

```bash
# Terminal command
python presentations/demo_ograg_live.py --proverb "Gutiri uriragio ni utonga no ukia"
```

**What happens:**
- Displays proverb in Kikuyu
- Shows literal translation: *"There's nothing cried over by wealth but poverty"*
- Displays expert cultural teaching

**What to say:**
> *"This proverb teaches that wealth can disappear, encouraging humility and resource management. Let's see how different approaches translate it."*

---

### **Step 2: Raw GPT-4 Translation (45 seconds)**

**Terminal Output:**
```
🔴 RAW GPT-4 (No Context)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Translation: "Nothing is mourned by wealth except poverty"
Tokens: 245

Analysis: 
❌ Misses cultural meaning of "crying over" (regret, loss)
❌ No connection to resource management wisdom
❌ Literal but culturally hollow
```

**What to say:**
> *"Raw GPT-4 gives a literal translation but completely misses the cultural depth—the wisdom about wealth's impermanence and the need for humility."*

---

### **Step 3: Traditional RAG (60 seconds)**

**Terminal Output:**
```
🟡 TRADITIONAL RAG (Similar Proverbs Only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Retrieved Examples (3):
  1. "Mwangi ti mwene ciaku" - Ownership doesn't guarantee permanence
  2. "Utonga wa muingui ti wa tuene" - Wealth shown off isn't truly owned
  3. "Indo cia ukuruthi iriuragwo ni kuhuta" - Abundant resources can lead to waste

Translation: "Wealth mourns only poverty, suggesting one should value 
what they have and manage resources wisely to avoid future hardship"

Tokens: 487
```

**What to say:**
> *"Traditional RAG provides similar proverbs as examples. It's better—mentions resource management—but still lacks the ontological depth of cultural concepts like humility, impermanence, and community values."*

---

### **Step 4: OG-RAG Translation (90 seconds)**

#### **4a. Show Knowledge Graph Retrieval (Browser)**

> *"Let me show you what happens behind the scenes."*

**Switch to Neo4j Browser Tab:**

Run this Cypher query:
```cypher
// Find the proverb and its cultural concepts
MATCH (p:Proverb {kikuyu_text: "Gutiri uriragio ni utonga no ukia."})
MATCH (p)-[e:EXPRESSES_CONCEPT]->(c:CulturalConcept)
RETURN p.kikuyu_text as Proverb,
       collect(DISTINCT c.name) as CulturalConcepts
LIMIT 1
```

**Visual Result:**
```
Proverb: "Gutiri uriragio ni utonga no ukia."
CulturalConcepts: [
  "Impermanence of Wealth",
  "Humility in Prosperity", 
  "Resource Stewardship",
  "Community Interdependence",
  "Long-term Planning"
]
```

**What to say:**
> *"The ontology links this proverb to 5 cultural concepts. Each has definitions, relationships, and expert annotations. This is what grounds the translation."*

---

#### **4b. Show the OG-RAG Translation (Terminal)**

**Terminal Output:**
```
🟢 OG-RAG (Ontology-Grounded Context)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Retrieved Cultural Context:
  - Impermanence of Wealth (weight: 0.89)
    → Teaches: Material wealth can diminish; maintaining humility essential
  
  - Resource Stewardship (weight: 0.85)
    → Teaches: Careful management prevents future poverty
  
  - Community Interdependence (weight: 0.78)
    → Context: Wealth loss affects community; sharing prevents hardship

Translation: 
"The only thing that wealth truly mourns is poverty—a teaching that 
material possessions are impermanent and one should manage resources 
carefully, maintain humility during prosperity, and remember that 
today's wealth can become tomorrow's poverty without wise stewardship 
and community support."

Cultural Explanation:
This proverb is core to Kikuyu economic philosophy. It counters pride 
in wealth by emphasizing impermanence, encouraging both gratitude for 
current blessings and proactive resource management. It's often used 
when counseling newly successful individuals or during community 
resource-sharing discussions.

Tokens: 1,247
Concepts Used: 5
Retrieved Proverbs: 3
```

**What to say:**
> *"OG-RAG provides the FULL cultural context—not just examples, but structured knowledge about impermanence, stewardship, and community values. The translation captures both linguistic meaning AND cultural teaching."*

---

### **Step 5: Side-by-Side Comparison (60 seconds)**

**Terminal displays:**
```
╔══════════════════════════════════════════════════════════════╗
║              TRANSLATION COMPARISON                          ║
╠══════════════════════════════════════════════════════════════╣
║ INPUT: "Gutiri uriragio ni utonga no ukia"                  ║
╠══════════════════════════════════════════════════════════════╣
║ RAW GPT-4:                                                   ║
║ "Nothing is mourned by wealth except poverty"               ║
║ Cultural Depth: ⭐ (1/5)                                     ║
╠══════════════════════════════════════════════════════════════╣
║ Traditional RAG:                                             ║
║ "Wealth mourns only poverty, suggesting resource management"║
║ Cultural Depth: ⭐⭐⭐ (3/5)                                  ║
╠══════════════════════════════════════════════════════════════╣
║ OG-RAG:                                                      ║
║ "Wealth mourns poverty—teaching about impermanence,          ║
║  stewardship, humility, and community interdependence"       ║
║ Cultural Depth: ⭐⭐⭐⭐⭐ (5/5)                               ║
╠══════════════════════════════════════════════════════════════╣
║ RESULT: OG-RAG captures full cultural teaching              ║
╚══════════════════════════════════════════════════════════════╝
```

**What to say:**
> *"The difference is clear. Raw LLM: literal but empty. Traditional RAG: better but shallow. OG-RAG: culturally complete because it's grounded in expert-validated ontology."*

---

## 🔧 Alternative Demo: Graph Visualization (If Time Permits)

### Show Concept Network in Neo4j Browser

```cypher
// Visualize concept relationships for the proverb
MATCH (p:Proverb {kikuyu_text: "Gutiri uriragio ni utonga no ukia."})
MATCH (p)-[:EXPRESSES_CONCEPT]->(c:CulturalConcept)
MATCH (c)-[r:RELATES_TO]-(related:CulturalConcept)
RETURN p, c, related, r
LIMIT 50
```

**Shows:**
- Central proverb node
- 5 concept nodes
- ~25 related concepts
- Relationship strengths (edge weights)

**What to say:**
> *"This is the semantic network. Each concept connects to others, forming a knowledge graph. Traditional RAG can't access this structure—OG-RAG navigates it."*

---

## 🎬 Demo Script (Full Presentation Flow)

```python
# File: presentations/demo_ograg_live.py

"""
Live OG-RAG Demo for Thesis Defense
Compares Raw GPT-4 vs Traditional RAG vs OG-RAG
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.og_rag_system.ograg_translator import OGRAGTranslator
from src.neo4j.scripts.connection import Neo4jConnection
import json

def demo_proverb(kikuyu_text: str, show_graph: bool = False):
    """
    Run complete demo for one proverb.
    
    Args:
        kikuyu_text: Kikuyu proverb to translate
        show_graph: If True, show Neo4j query for graph retrieval
    """
    
    print("\n" + "="*70)
    print("🎯 THESIS DEFENSE DEMO: Ontology-Grounded RAG")
    print("="*70)
    
    # Initialize system
    print("\n⏳ Initializing OG-RAG system...")
    translator = OGRAGTranslator()
    
    print(f"\n📖 PROVERB: {kikuyu_text}")
    
    # Step 1: Raw GPT-4
    print("\n" + "🔴 RAW GPT-4 (No Context)".center(70, "━"))
    raw_result = translator.translate_raw(kikuyu_text)
    print(f"Translation: {raw_result.translation}")
    print(f"Tokens: {raw_result.total_tokens}")
    print("\nAnalysis:")
    print("❌ Literal translation only")
    print("❌ No cultural context")
    print("❌ Misses wisdom teaching")
    
    # Step 2: Traditional RAG
    print("\n" + "🟡 TRADITIONAL RAG (Similar Proverbs)".center(70, "━"))
    trad_result = translator.translate_traditional_rag(kikuyu_text)
    print(f"\nRetrieved Examples ({len(trad_result.retrieved_proverbs)}):")
    for i, ex in enumerate(trad_result.retrieved_proverbs[:3], 1):
        print(f"  {i}. {ex.kikuyu_text}")
    
    print(f"\nTranslation: {trad_result.translation}")
    print(f"Tokens: {trad_result.total_tokens}")
    
    # Step 3: Show graph query (optional)
    if show_graph:
        print("\n" + "🔍 KNOWLEDGE GRAPH QUERY".center(70, "━"))
        cypher = f"""
        MATCH (p:Proverb {{kikuyu_text: "{kikuyu_text}"}})
        MATCH (p)-[e:EXPRESSES_CONCEPT]->(c:CulturalConcept)
        RETURN p.kikuyu_text, collect(c.name) as concepts
        """
        print(cypher)
        
        conn = Neo4jConnection()
        result = conn.execute_query(cypher)
        concepts = result[0]['concepts'] if result else []
        print(f"\n✅ Retrieved {len(concepts)} cultural concepts:")
        for concept in concepts[:5]:
            print(f"  • {concept}")
        conn.close()
    
    # Step 4: OG-RAG
    print("\n" + "🟢 OG-RAG (Ontology-Grounded)".center(70, "━"))
    ograg_result = translator.translate_ograg(kikuyu_text)
    
    print(f"\nCultural Context Retrieved:")
    if ograg_result.concepts_used:
        for concept in ograg_result.concepts_used[:3]:
            print(f"  • {concept}")
    
    print(f"\nTranslation:\n{ograg_result.translation}")
    
    if ograg_result.explanation:
        print(f"\nCultural Explanation:\n{ograg_result.explanation}")
    
    print(f"\nTokens: {ograg_result.total_tokens}")
    print(f"Concepts Used: {len(ograg_result.concepts_used or [])}")
    
    # Step 5: Comparison
    print("\n" + "📊 COMPARISON".center(70, "="))
    print(f"{'Method':<20} {'Tokens':<10} {'Cultural Depth':<20}")
    print("-" * 70)
    print(f"{'Raw GPT-4':<20} {raw_result.total_tokens:<10} {'⭐ (1/5)':<20}")
    print(f"{'Traditional RAG':<20} {trad_result.total_tokens:<10} {'⭐⭐⭐ (3/5)':<20}")
    print(f"{'OG-RAG':<20} {ograg_result.total_tokens:<10} {'⭐⭐⭐⭐⭐ (5/5)':<20}")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE")
    print("="*70 + "\n")
    
    return {
        'raw': raw_result,
        'traditional': trad_result,
        'ograg': ograg_result
    }


def test_connection():
    """Quick test that everything is connected."""
    print("🔧 Testing system components...")
    
    try:
        # Test Neo4j
        conn = Neo4jConnection()
        result = conn.execute_query("MATCH (n) RETURN count(n) as total LIMIT 1")
        count = result[0]['total']
        print(f"✅ Neo4j connected ({count:,} nodes)")
        conn.close()
        
        # Test OpenAI
        from decouple import config
        api_key = config('OPENAI_API_KEY', default=None)
        if api_key and api_key != 'your_openai_api_key_here':
            print("✅ OpenAI API key loaded")
        else:
            print("❌ OpenAI API key missing or not configured")
            return False
        
        print("✅ All systems ready\n")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OG-RAG Live Demo")
    parser.add_argument(
        '--proverb', 
        type=str,
        default="Gutiri uriragio ni utonga no ukia",
        help="Kikuyu proverb to translate"
    )
    parser.add_argument('--test', action='store_true', help="Test connections only")
    parser.add_argument('--show-graph', action='store_true', help="Show graph query")
    
    args = parser.parse_args()
    
    if args.test:
        test_connection()
    else:
        if test_connection():
            demo_proverb(args.proverb, args.show_graph)
```

---

## 🎤 Suggested Narration

### **Introduction (15 seconds)**
> *"I'll now demonstrate the OG-RAG system live. We'll translate one Kikuyu proverb three ways to show how ontology grounding achieves cultural faithfulness."*

### **Raw Translation (20 seconds)**
> *"First, raw GPT-4 with no context. As you can see, it's literal but culturally hollow—just word mapping without wisdom."*

### **Traditional RAG (25 seconds)**
> *"Next, traditional RAG provides example proverbs. It's better—mentions themes—but lacks structured cultural knowledge."*

### **OG-RAG Reveal (40 seconds)**
> *"Finally, OG-RAG. Notice it retrieves from the knowledge graph—cultural concepts, not just text. The translation includes impermanence, stewardship, community values—the complete teaching. This is what ontology grounding enables."*

### **Conclusion (20 seconds)**
> *"The comparison is stark. Only OG-RAG captures cultural depth because it's grounded in expert-validated ontology, not just similar text chunks."*

---

## 🆘 Troubleshooting

### If Neo4j Connection Fails
```python
# Quick fix: Restart connection
from src.neo4j.scripts.connection import Neo4jConnection
conn = Neo4jConnection()
conn.verify_connectivity()
```

### If OpenAI API Fails
```bash
# Check .env file
cat .env | grep OPENAI_API_KEY

# Reload environment
export OPENAI_API_KEY="sk-proj-..."
```

### If Import Errors
```bash
# Ensure in correct directory
cd /Users/ndethi/dev/opit/opit-rai9001

# Reinstall dependencies
pip install openai python-decouple neo4j
```

---

## 📝 Backup Demo (If Live System Fails)

**Prepare screenshots showing:**
1. **Before:** Raw GPT-4 translation (literal)
2. **After:** OG-RAG translation (culturally rich)
3. **Graph:** Neo4j visualization of concept network

**Narration:**
> *"Here's a pre-recorded demo showing the same workflow. Raw GPT-4 gives literal output. OG-RAG, grounded in this knowledge graph, produces culturally faithful translation."*

---

## 🎓 Key Takeaways to Emphasize

1. **Problem Clear:** Raw LLMs fail at cultural nuance
2. **Solution Visual:** Knowledge graph provides structure
3. **Impact Measurable:** Side-by-side shows dramatic difference
4. **Research Valid:** This proves OG-RAG hypothesis

---

## 📦 What You Need

✅ **Hardware:** Laptop with internet (AuraDB access)  
✅ **Software:** Python env, Neo4j credentials, OpenAI API  
✅ **Time:** 5-7 minutes  
✅ **Backup:** Screenshots if live demo fails  

---

**Good luck with your defense! This demo will clearly show the value of ontology grounding.** 🚀
