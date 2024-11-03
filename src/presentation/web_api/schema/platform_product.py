from pydantic import BaseModel


class PurchasePlatformProductSchema(BaseModel):
    product_id: int
