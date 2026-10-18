from enum import Enum


class VectorDBEnums(Enum):
    QDRANT = "QDRANT"
    LANCEDB = "LANCEDB"
    TURBOVEC = "TURBOVEC"
    LIGHTRAG = "LIGHTRAG"


class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"
