from sqlalchemy import Column, Integer, String, Boolean, Text
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    uploader = Column(String)
    raw_text = Column(Text)
    summary = Column(Text)
    roles = Column(String)  # comma-separated: "engineer,hr,passenger"
    approved = Column(Boolean, default=False)