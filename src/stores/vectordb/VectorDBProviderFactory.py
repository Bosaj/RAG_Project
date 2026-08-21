from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController

class VectorDBProviderFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            from .providers import QdrantDBProvider

            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            )
        
        if provider == VectorDBEnums.LANCEDB.value:
            from .providers.LanceDBProvider import LanceDBProvider

            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)

            return LanceDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            )
        
        raise ValueError(f"Unsupported vector database provider: {provider!r}")
