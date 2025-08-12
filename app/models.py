from pydantic import BaseModel, Field
from typing import List, Optional

class IngestRequest(BaseModel):
    tenant_id: str = Field(..., examples=["acme"])
    paths: List[str] = Field(..., examples=["data/*.pdf", "data/*.txt"])

class QueryRequest(BaseModel):
    tenant_id: str
    question: str
    top_k: Optional[int] = 5
