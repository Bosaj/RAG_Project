from pydantic import BaseModel, Field
from typing import Optional

class ProcessRequest(BaseModel):
    file_id: Optional[str] = None
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "1_ABCDEF123_example.txt",
                "chunk_size": 100,
                "overlap_size": 20,
                "do_reset": 0
            }
        }
