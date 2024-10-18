from pydantic import BaseModel


class GetPresignedURL(BaseModel):
    filename: str
