# services/document_processor.py
import os
import PyPDF2
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import crud
from database import SessionLocal  # ✅ import SessionLocal here
from sqlalchemy.orm import Session

# Load environment variables from .env file
load_dotenv()

# Hugging Face API setup
HF_API_KEY = os.getenv("HF_API_KEY")
hf_client = InferenceClient(api_key=HF_API_KEY)

def extract_text(file_path: str) -> str:
    """Extract text from PDF or text files"""
    print(f"DEBUG: Trying to extract text from {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    # Check file size
    file_size = os.path.getsize(file_path)
    print(f"DEBUG: File size: {file_size} bytes")
    
    try:
        if file_path.lower().endswith('.pdf'):
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                print(f"DEBUG: Extracted {len(text)} characters from PDF")
                return text
        else:
            # For other file types, assume plain text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(f"DEBUG: Extracted {len(content)} characters from text file")
                return content
    except Exception as e:
        error_msg = f"Error extracting text: {str(e)}"
        print(f"DEBUG: {error_msg}")
        return error_msg
    
def summarize_with_hf(text: str) -> str:
    """Generate a summary using Hugging Face API with correct summarization approach"""
    try:
        if not HF_API_KEY:
            return "Hugging Face API key not configured. Please check your .env file."

        # Truncate long input
        if len(text) > 2000:
            text = text[:2000] + "... [truncated]"

        # Use the correct approach for summarization models
        # For summarization models, we need to use a different endpoint
        response = hf_client.summarization(
            text,
            model="facebook/bart-large-cnn",
            parameters={"max_length": 200, "min_length": 50}
        )
        
        # Extract the summary from the response
        if isinstance(response, dict) and 'summary_text' in response:
            return response['summary_text']
        else:
            return str(response)
            
    except Exception as e:
        print(f"Hugging Face API error: {str(e)}")
        # Fallback to simple summarization
        if len(text) > 300:
            return f"Summary: {text[:300]}..."
        return "Summary unavailable due to API error"

def process_document_immediate(doc_id: int, file_path: str, db: Session):
    """Process a document immediately (not in background)"""
    print(f"🚀 Processing document {doc_id} immediately")
    print(f"📁 File path: {file_path}")
    
        # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found at {file_path}")
        return

    try:
        # Extract text from the document
        raw_text = extract_text(file_path)
        print(f"📄 Extracted text: '{raw_text}'")
        print(f"📄 Extracted text length: {len(raw_text)} characters")
        
        # Generate summary (simple version for demo reliability)
        if len(raw_text) > 300:
            summary = f"SUMMARY: {raw_text[:300]}..."
        else:
            summary = f"SUMMARY: {raw_text}"
        print(f"📝 Generated summary: {summary}")
        
        # Update the document in the database
        document = crud.get_document(db, doc_id)
        if document:
            document.raw_text = raw_text
            document.summary = summary
            db.commit()
            print(f"✅ Document {doc_id} updated successfully")
        else:
            print(f"❌ Document {doc_id} not found")
            
    except Exception as e:
        print(f"❌ Error in process_document: {str(e)}")
        import traceback
        traceback.print_exc()

def process_document(doc_id: int, file_path: str):
    """Process a document: extract text and generate summary"""
    # Create a new database session for the background task
    from database import SessionLocal
    db = SessionLocal()
    
    print(f"🚀 Processing document {doc_id}")
    
    try:
        # Extract text from the document
        raw_text = extract_text(file_path)
        print(f"📄 Extracted text length: {len(raw_text)} characters")
        
        # Generate summary (simple version for demo reliability)
        if len(raw_text) > 300:
            summary = f"SUMMARY: {raw_text[:300]}..."
        else:
            summary = f"SUMMARY: {raw_text}"
        print(f"📝 Generated summary: {summary}")
        
        # Update the document in the database
        document = crud.get_document(db, doc_id)
        if document:
            document.raw_text = raw_text
            document.summary = summary
            db.commit()
            print(f"✅ Document {doc_id} updated successfully")
        else:
            print(f"❌ Document {doc_id} not found")
            
    except Exception as e:
        print(f"❌ Error in process_document: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
