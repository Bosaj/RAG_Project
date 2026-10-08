"""
Graph Store & RDF Knowledge Graph Integration for Hybrid GraphRAG.
Provides entity-relation graph extraction, local SPARQL querying, and graph-assisted context enrichment.
"""

from typing import Any, Dict, List, Optional
import os

try:
    import rdflib
    from rdflib import Graph, Literal, RDF, RDFS, URIRef
    from rdflib.namespace import FOAF, OWL, XSD
except ImportError:
    rdflib = None


class KnowledgeGraphStore:
    """
    In-memory and file-backed RDF Knowledge Graph store for Hybrid GraphRAG.
    """

    def __init__(self, custom_ontology_path: Optional[str] = None):
        self.is_available = rdflib is not None
        self.graph = rdflib.Graph() if self.is_available else None
        self.custom_namespace = rdflib.Namespace("http://ragproject.org/ontology#") if self.is_available else None

        if self.is_available and custom_ontology_path and os.path.exists(custom_ontology_path):
            self.load_ontology(custom_ontology_path)

    def load_ontology(self, file_path: str, format: str = "turtle") -> bool:
        """Load an RDF/OWL ontology into the active knowledge graph."""
        if not self.is_available:
            return False
        try:
            self.graph.parse(file_path, format=format)
            return True
        except Exception as e:
            print(f"Failed to load ontology: {e}")
            return False

    def add_relation(self, subject: str, predicate: str, obj: str, is_literal: bool = False) -> None:
        """Add a triple relation (Subject -> Predicate -> Object) to the knowledge graph."""
        if not self.is_available:
            return

        s = URIRef(f"http://ragproject.org/entity/{subject.strip().replace(' ', '_')}")
        p = URIRef(f"http://ragproject.org/ontology/{predicate.strip().replace(' ', '_')}")
        o = Literal(obj, datatype=XSD.string) if is_literal else URIRef(f"http://ragproject.org/entity/{obj.strip().replace(' ', '_')}")

        self.graph.add((s, p, o))

    def query_triples_for_entity(self, entity_keyword: str) -> List[Dict[str, str]]:
        """
        Query all associated knowledge triples for an entity keyword using SPARQL.
        """
        if not self.is_available or not self.graph:
            return []

        clean_keyword = entity_keyword.strip().lower()
        sparql = f"""
        SELECT ?subject ?predicate ?object
        WHERE {{
            ?subject ?predicate ?object .
            FILTER (
                CONTAINS(LCASE(STR(?subject)), "{clean_keyword}") ||
                CONTAINS(LCASE(STR(?object)), "{clean_keyword}")
            )
        }}
        LIMIT 25
        """
        results = []
        try:
            qres = self.graph.query(sparql)
            for row in qres:
                results.append({
                    "subject": str(row.subject).split("/")[-1].replace("_", " "),
                    "predicate": str(row.predicate).split("/")[-1].replace("_", " "),
                    "object": str(row.object).split("/")[-1].replace("_", " ")
                })
        except Exception as e:
            print(f"SPARQL error: {e}")
        return results

    def get_graph_context_summary(self, query: str) -> str:
        """
        Extract relevant factual triple chains matching keywords in the user's prompt.
        """
        if not self.is_available or len(self.graph) == 0:
            return ""

        words = [w.strip() for w in query.split() if len(w.strip()) > 3]
        matched_facts = []

        for word in words:
            triples = self.query_triples_for_entity(word)
            for t in triples:
                fact = f"- [{t['subject']}] --({t['predicate']})--> [{t['object']}]"
                if fact not in matched_facts:
                    matched_facts.append(fact)

        if not matched_facts:
            return ""

        return "### 🕸️ Knowledge Graph Verified Facts:\n" + "\n".join(matched_facts[:15]) + "\n"
