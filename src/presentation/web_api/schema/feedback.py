from datetime import datetime, UTC
from typing import Optional, List

from pydantic import BaseModel, Field


class CreateFeedbackSchema(BaseModel):
    stars: int = Field(le=5)
    comment: Optional[str] = Field(default=None, max_length=5000)
    photo: Optional[List[str]] = Field(default=None)
