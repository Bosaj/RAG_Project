"""
Hybrid GraphRAG Controller.
Fuses dense vector store context retrieval with ontological Knowledge Graph facts.
"""

from typing import Any, Dict, List, Optional
from src.stores.graphrag.graph_store import KnowledgeGraphStore


class HybridGraphRAGController:
    """
    Orchestrates Hybrid Retrieval-Augmented Generation:
    1. Dense Vector Search (semantic context)
    2. Ontological Triples Search (verifiable factual constraints)
    3. Context Fusion for LLM Prompting
    """

    def __init__(self, vector_db_controller: Optional[Any] = None, ontology_path: Optional[str] = None):
        self.vector_db_controller = vector_db_controller
        self.kg_store = KnowledgeGraphStore(custom_ontology_path=ontology_path)

    def ingest_structured_facts(self, facts: List[Dict[str, str]]) -> int:
        """
        Batch-ingest structured entity-relation facts.
        Format: [{'subject': 'X', 'predicate': 'Y', 'object': 'Z'}]
        """
        count = 0
        for f in facts:
            if "subject" in f and "predicate" in f and "object" in f:
                self.kg_store.add_relation(f["subject"], f["predicate"], f["object"])
                count += 1
        return count

    def retrieve_hybrid_context(self, query: str, vector_chunks: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Perform hybrid retrieval combining vector chunks and graph facts.
        """
        # 1. Fetch graph facts
        graph_facts = self.kg_store.get_graph_context_summary(query)

        # 2. Extract vector context
        vector_context = ""
        if vector_chunks:
            vector_context = "### 📄 Document Semantic Context:\n" + "\n".join(vector_chunks)

        # 3. Fuse context
        combined_prompt_context = f"{graph_facts}\n{vector_context}".strip()

        return {
            "query": query,
            "has_graph_facts": bool(graph_facts),
            "combined_context": combined_prompt_context,
            "graph_summary": graph_facts,
            "vector_context": vector_context
        }
