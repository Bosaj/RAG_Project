#pour controller et faire la gestion des donnes 
from .base_controler import basecontroler
from fastapi import UploadFile
from models import ResponseSignal

class datacontroler(basecontroler):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576 # pour la convertion en byte


    def validation_upload(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False,ResponseSignal.FILE_UPLOAD_FAILED
        if file.size > self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False,ResponseSignal.FIle_SIZE_EXCEEDED
        return True,ResponseSignal.FILE_UPLOAD_SUCCESS
        
