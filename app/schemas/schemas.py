# app/schemas/schemas.py

from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    tenant: str
    answer: str
