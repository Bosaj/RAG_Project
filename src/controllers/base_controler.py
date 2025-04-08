# pour tout les element commune de controler
from helpers.config import get_settings,Settings
import os

class basecontroler:
    def __init__(self):     
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir =  os.path.join(
            self.base_dir,
            "files"
        )
       