from pydantic import BaseModel


class SearchRequest(BaseModel):
    question: str
    user_id: int
    document_ids: list[int]
    top_k: int = 5

class ChatRequest(BaseModel):
    question: str
    user_id: int
    document_ids: list[int]