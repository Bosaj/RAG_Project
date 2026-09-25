from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class DataChunk(BaseModel):
    id: ObjectId | None = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId
    chunk_asset_id: ObjectId

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [{"key": [("chunk_project_id", 1)], "name": "chunk_project_id_index_1", "unique": False}]


class RetrievedDocument(BaseModel):
    text: str
    score: float
