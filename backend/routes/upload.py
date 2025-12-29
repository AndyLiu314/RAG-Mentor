from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import PyPDF2
import io
from routes.chromadb_client import ChromaDBClient

router = APIRouter()

class UploadResponse(BaseModel):
    message: str
    chunks_added: int
    filename: str

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

@router.post("/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    contents = await file.read()
    pdf_file = io.BytesIO(contents)
    
    text = extract_text_from_pdf(pdf_file)
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")
    
    chunks = chunk_text(text)
    
    db = ChromaDBClient()
    
    metadatas = [
        {
            "source": file.filename,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]
    
    ids = [f"{file.filename}_chunk_{i}" for i in range(len(chunks))]
    
    db.add_documents(
        collection_name="documents",
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )
    
    return UploadResponse(
        message=f"Successfully processed {file.filename}",
        chunks_added=len(chunks),
        filename=file.filename
    )
