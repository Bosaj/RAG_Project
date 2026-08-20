from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import os

class ProjectController(BaseController):
    
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        if not project_id or not project_id.strip():
            raise ValueError("project_id must not be empty")

        storage_root = os.path.abspath(self.files_dir)
        project_dir = os.path.abspath(os.path.join(storage_root, project_id))

        if os.path.commonpath([storage_root, project_dir]) != storage_root:
            raise ValueError("project_id must stay within the storage directory")

        os.makedirs(project_dir, exist_ok=True)
        return project_dir

