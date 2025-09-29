from pydantic import BaseModel
from typing import List, Optional

class DocumentCreate(BaseModel):
    filename: str
    uploader: str


class DocumentOut(BaseModel):
    id: int
    filename: str
    uploader: str
    raw_text: Optional[str] = None
    summary: Optional[str] = None
    roles: Optional[str] = None
    approved: bool

    class Config:
        from_attributes = True


# 👇 Schema for approval requests
class ApproveRequest(BaseModel):
    roles: List[str]
