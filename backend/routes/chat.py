from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from routes.chromadb_client import ChromaDBClient

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

db = ChromaDBClient()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Query ChromaDB for relevant context
    try:
        results = db.query_documents(
            collection_name="documents",
            query_texts=[request.message],
            n_results=3
        )
        
        context_docs = results['documents'][0] if results['documents'] else []
        context = "\n\n".join(context_docs)
        
        if context:
            prompt = f"""Based on the following context, please answer the question.
            Context:
            {context}

            Question: {request.message}

            Answer:"""
        else:
            prompt = request.message
            
    except Exception as e:
        print(f"ChromaDB query failed: {e}")
        prompt = request.message
    
    response = ollama.chat(
        model='gemma3:latest',
        messages=[{'role': 'user', 'content': prompt}],
        stream=False,
    )
    
    return ChatResponse(response=response['message']['content'])
