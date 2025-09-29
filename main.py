from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from database import SessionLocal, engine
import models
import crud
import schema
from schema import ApproveRequest   # 👈 import new schema
from services.document_processor import process_document

app = FastAPI(title="KMRL Backend API", version="1.0.0")

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "KMRL Backend is running!"}

@app.post("/upload_doc/", response_model=schema.DocumentOut)
async def upload_doc(
    uploader: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save the file to data/uploads
    file_location = f"data/uploads/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create document in database
    document_data = schema.DocumentCreate(
        filename=file.filename,
        uploader=uploader
    )
    db_document = crud.create_document(db=db, document=document_data)
    
    # Process document IMMEDIATELY (not in background)
    from services.document_processor import process_document_immediate
    process_document_immediate(db_document.id, file_location, db)
    
    # Refresh to get the updated document with text and summary
    db.refresh(db_document)
    
    return db_document

@app.get("/docs/{role}", response_model=List[schema.DocumentOut])
def get_docs(role: str, db: Session = Depends(get_db)):
    documents = crud.get_documents_by_role(db, role=role)
    return documents

from schema import ApproveRequest

@app.post("/approve_doc/{doc_id}")
def approve_doc(doc_id: int, req: ApproveRequest, db: Session = Depends(get_db)):
    db_document = crud.approve_document(db, doc_id=doc_id, roles=req.roles)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"success": True, "doc": db_document}
