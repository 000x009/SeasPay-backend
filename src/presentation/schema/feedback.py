from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, Field


class CreateFeedback(BaseModel):
    stars: int = Field(le=5)
    comment: Optional[str] = Field(default=None, max_length=5000)
    created_at: datetime = Field(default=datetime.now(UTC))
