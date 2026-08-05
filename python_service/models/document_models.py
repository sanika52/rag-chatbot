from pydantic import BaseModel


class ProcessDocumentRequest(BaseModel):
    file_path: str
    document_id: int
    user_id: int
    filename: str
    stored_filename: str