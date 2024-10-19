from pydantic import BaseModel, AnyUrl


class CreatePurchaseRequestSchema(BaseModel):
    purchase_url: AnyUrl
