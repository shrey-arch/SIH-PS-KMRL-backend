# crud.py
from sqlalchemy.orm import Session
from typing import List
import models
import schema  # ✅ use schemas (plural) if that's your file name


def create_document(db: Session, document: schema.DocumentCreate):
    db_document = models.Document(
        filename=document.filename,
        uploader=document.uploader,
        raw_text=None,   # Background task fills this
        summary=None,    # Background task fills this
        roles="",        # Default empty string (avoids None issues)
        approved=False
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_documents_by_role(db: Session, role: str):
    """Fetch all approved documents for a given role"""
    return db.query(models.Document).filter(
        models.Document.approved == True,
        models.Document.roles.contains(role)
    ).all()


def get_document(db: Session, doc_id: int):
    """Fetch a single document by ID"""
    return db.query(models.Document).filter(models.Document.id == doc_id).first()


def approve_document(db: Session, doc_id: int, roles: List[str]):
    """Approve a document and assign roles"""
    db_document = get_document(db, doc_id=doc_id)
    if db_document:
        db_document.approved = True
        db_document.roles = ",".join(roles)  # Store as comma-separated string
        db.commit()
        db.refresh(db_document)
    return db_document
