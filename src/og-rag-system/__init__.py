"""
OG-RAG System - Ontology-Grounded Retrieval Augmented Generation
==================================================================

This module implements the OG-RAG system for culturally faithful
Kikuyu proverb translation using Neo4j knowledge graph and LLMs.

Components:
- graph_retriever: Triple-strategy proverb retrieval from Neo4j
- context_builder: Format retrieved context for LLM prompts
- ograg_translator: End-to-end translation pipeline
"""

from .graph_retriever import GraphRetriever, RetrievedProverb
from .context_builder import ContextBuilder, CulturalContext
from .ograg_translator import OGRAGTranslator, TranslationResult

__all__ = [
    'GraphRetriever', 
    'RetrievedProverb',
    'ContextBuilder',
    'CulturalContext',
    'OGRAGTranslator',
    'TranslationResult'
]
