from uuid import UUID
from typing import Dict

from pydantic import BaseModel


class FulfillProductApplicationSchema(BaseModel):
    application_id: UUID
    login_data: Dict[str, str]
