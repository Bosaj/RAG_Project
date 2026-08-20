from typing import Optional

from pydantic import BaseModel, Field


class PushRequest(BaseModel):
    do_reset: Optional[int] = Field(default=0, ge=0, le=1)


class SearchRequest(BaseModel):
    text: str = Field(min_length=1)
    limit: Optional[int] = Field(default=5, gt=0, le=100)
