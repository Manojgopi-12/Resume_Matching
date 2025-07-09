from pydantic import BaseModel
from uuid import UUID

class ResumeOut(BaseModel):
    id: UUID
    filename: str
    raw_text: str

class QueryRequest(BaseModel):
    query: str
