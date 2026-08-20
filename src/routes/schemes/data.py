from typing import Optional

from pydantic import BaseModel, Field, model_validator


class ProcessRequest(BaseModel):
    file_id: str = None
    chunk_size: Optional[int] = Field(default=100, gt=0)
    overlap_size: Optional[int] = Field(default=20, ge=0)
    do_reset: Optional[int] = Field(default=0, ge=0, le=1)

    @model_validator(mode="after")
    def validate_overlap(self):
        if self.overlap_size is not None and self.chunk_size is not None:
            if self.overlap_size >= self.chunk_size:
                raise ValueError("overlap_size must be smaller than chunk_size")
        return self
