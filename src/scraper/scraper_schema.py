from pydantic import BaseModel

class ScraperTextSchema(BaseModel):
    text: str

class ScraperFAQSchema(BaseModel):
    title: str
    text: str