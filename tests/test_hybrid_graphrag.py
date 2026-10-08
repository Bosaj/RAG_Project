"""
Unit tests for Hybrid GraphRAG integration.
"""

import pytest
from src.stores.graphrag.graph_store import KnowledgeGraphStore
from src.controllers.graphrag_controller import HybridGraphRAGController


def test_kg_store_initialization():
    store = KnowledgeGraphStore()
    assert store is not None
    if store.is_available:
        store.add_relation("FastMCP", "is_framework_for", "ModelContextProtocol")
        facts = store.query_triples_for_entity("FastMCP")
        assert len(facts) >= 1
        assert facts[0]["subject"] == "FastMCP"


def test_hybrid_controller_fusion():
    controller = HybridGraphRAGController()
    if controller.kg_store.is_available:
        controller.ingest_structured_facts([
            {"subject": "Antigravity", "predicate": "supports", "object": "MCP"},
            {"subject": "CrewAI", "predicate": "orchestrates", "object": "MultiAgents"}
        ])

        result = controller.retrieve_hybrid_context(
            query="Tell me about Antigravity and MCP",
            vector_chunks=["Antigravity is an advanced agentic coding environment."]
        )

        assert "Antigravity" in result["combined_context"]
        assert result["has_graph_facts"] is True
