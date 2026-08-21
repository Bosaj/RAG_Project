from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import List
from models.db_schemes import RetrievedDocument
import json
import uuid

class LanceDBProvider(VectorDBInterface):

    def __init__(self, db_path: str, distance_method: str = "cosine"):
        self.db = None
        self.db_path = db_path
        self.distance_method = distance_method or DistanceMethodEnums.COSINE.value
        self.logger = logging.getLogger(__name__)

    def connect(self):
        try:
            import lancedb
            self.db = lancedb.connect(self.db_path)
            self.logger.info(f"Connected to LanceDB at {self.db_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to LanceDB: {e}")
            return False

    def disconnect(self):
        self.db = None

    def is_collection_existed(self, collection_name: str) -> bool:
        if self.db is None:
            return False
        try:
            return collection_name in self.db.table_names()
        except Exception:
            return False

    def list_all_collections(self) -> List:
        if self.db is None:
            return []
        try:
            return list(self.db.table_names())
        except Exception:
            return []

    def get_collection_info(self, collection_name: str) -> dict:
        if not self.is_collection_existed(collection_name):
            return None
        try:
            table = self.db.open_table(collection_name)
            return {
                "name": collection_name,
                "vectors_count": table.count_rows(),
                "status": "ready"
            }
        except Exception as e:
            self.logger.error(f"Failed to get collection info: {e}")
            return None

    def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            try:
                self.db.drop_table(collection_name)
                return True
            except Exception as e:
                self.logger.error(f"Failed to drop table: {e}")
                return False
        return False

    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        try:
            import pyarrow as pa
            if do_reset and self.is_collection_existed(collection_name):
                self.delete_collection(collection_name)

            if self.is_collection_existed(collection_name):
                return True

            schema = pa.schema([
                pa.field("id", pa.string()),
                pa.field("vector", pa.list_(pa.float32(), embedding_size)),
                pa.field("text", pa.string()),
                pa.field("metadata", pa.string())
            ])

            self.db.create_table(collection_name, schema=schema)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create collection: {e}")
            return False

    def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         record_id: str = None):
        if not record_id:
            record_id = str(uuid.uuid4())

        return self.insert_many(
            collection_name=collection_name,
            texts=[text],
            vectors=[vector],
            metadata=[metadata or {}],
            record_ids=[record_id]
        )

    def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          record_ids: list = None, batch_size: int = 50):
        if not self.is_collection_existed(collection_name):
            return False

        if record_ids is None:
            record_ids = [str(uuid.uuid4()) for _ in range(len(texts))]

        if metadata is None:
            metadata = [{} for _ in range(len(texts))]

        try:
            table = self.db.open_table(collection_name)
            data = []
            for i in range(len(texts)):
                data.append({
                    "id": record_ids[i],
                    "vector": vectors[i],
                    "text": texts[i],
                    "metadata": json.dumps(metadata[i]) if metadata[i] else "{}"
                })

            table.add(data)
            return True
        except Exception as e:
            self.logger.error(f"Failed to insert many: {e}")
            return False

    def search_by_vector(self, collection_name: str, vector: list, limit: int) -> List[RetrievedDocument]:
        if not self.is_collection_existed(collection_name):
            return []

        try:
            table = self.db.open_table(collection_name)
            results = table.search(vector).limit(limit).to_list()

            retrieved_docs = []
            for res in results:
                score = 1.0 - float(res.get("_distance", 0.0))
                retrieved_docs.append(
                    RetrievedDocument(
                        text=res["text"],
                        score=score
                    )
                )
            return retrieved_docs
        except Exception as e:
            self.logger.error(f"Failed to search: {e}")
            return []