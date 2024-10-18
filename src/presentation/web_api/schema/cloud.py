from pydantic import BaseModel


class GetPresignedURLSchema(BaseModel):
    filename: str
