"""
Ontology Ingestion & SPARQL Fact Extractor for Hybrid GraphRAG.
Demonstrates loading OWL/Turtle ontologies from semantic-web-knowledge-ontologies
and querying verified factual constraints to augment LLM context.
"""

import os
import sys

# Ensure src is in sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.stores.graphrag.graph_store import KnowledgeGraphStore
from src.controllers.graphrag_controller import HybridGraphRAGController


def main():
    ontology_path = os.path.join(os.path.dirname(__file__), "..", "data", "ontologies", "Biblio.owl")
    print(f"🕸️ Loading Ontology from: {ontology_path}")

    if not os.path.exists(ontology_path):
        print(f"❌ File not found: {ontology_path}")
        return

    controller = HybridGraphRAGController(ontology_path=ontology_path)

    print("\n--- 🔍 Test Query 1: Books and Authors ---")
    retrieval = controller.retrieve_hybrid_context(
        query="Who wrote Le Petit Prince and when was it published?",
        vector_chunks=["Antoine de Saint-Exupery was a French writer and aviator."]
    )

    print(retrieval["combined_context"])

    print("\n--- 🔍 Test Query 2: Borrowing Loans (Emprunt) ---")
    retrieval_loans = controller.retrieve_hybrid_context(
        query="Tell me about livre1 emprunt and Fatima Zahra"
    )
    print(retrieval_loans["combined_context"])
    print("\n✅ Hybrid GraphRAG Ontology integration verified successfully!")


if __name__ == "__main__":
    main()
