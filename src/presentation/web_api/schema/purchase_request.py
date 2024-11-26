from pydantic import BaseModel


class CreatePurchaseRequestSchema(BaseModel):
    purchase_url: str
