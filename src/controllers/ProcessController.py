from .BaseController import BaseController
from .ProjectController import ProjectController
import os

from models import ProcessingEnum


class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1].lower()

    def get_file_path(self, file_id: str):
        if not file_id or not file_id.strip():
            return None

        storage_root = os.path.realpath(self.project_path)
        file_path = os.path.realpath(os.path.join(storage_root, file_id))

        if os.path.commonpath([storage_root, file_path]) != storage_root:
            return None

        return file_path

    def get_file_loader(self, file_id: str):
        file_path = self.get_file_path(file_id=file_id)

        if file_path is None or not os.path.isfile(file_path):
            return None

        file_ext = self.get_file_extension(file_id=file_id)

        if file_ext == ProcessingEnum.TXT.value:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            from langchain_community.document_loaders import PyMuPDFLoader

            return PyMuPDFLoader(file_path)

        return None

    def get_file_content(self, file_id: str):
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()

        return None

    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int = 100, overlap_size: int = 20):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero")
        if overlap_size < 0 or overlap_size >= chunk_size:
            raise ValueError("overlap_size must be non-negative and smaller than chunk_size")

        from langchain_text_splitters import RecursiveCharacterTextSplitter

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks
