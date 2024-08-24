from datetime import datetime, UTC
from decimal import Decimal

from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    joined_at: datetime = Field(default=datetime.now(UTC))
    commission: int = Field(default=15)
    total_withdrawn: Decimal = Field(default=0)


