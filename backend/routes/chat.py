from fastapi import APIRouter
from pydantic import BaseModel
import ollama
from routes.chromadb_client import ChromaDBClient
from typing import List, Optional

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str

db = ChromaDBClient()

conversation_memory = {}

def get_conversation_history(session_id: str) -> List[dict]:
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    return conversation_memory[session_id]

def add_to_history(session_id: str, role: str, content: str):
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    
    conversation_memory[session_id].append({
        "role": role,
        "content": content
    })
    
    if len(conversation_memory[session_id]) > 10:
        conversation_memory[session_id] = conversation_memory[session_id][-10:]

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session_id = request.session_id
    
    # Query ChromaDB for relevant context
    try:
        results = db.query_documents(
            collection_name="documents",
            query_texts=[request.message],
            n_results=3
        )
        
        context_docs = results['documents'][0] if results['documents'] else []
        context = "\n\n".join(context_docs)

    except Exception as e:
        print(f"ChromaDB query failed: {e}")
        context = ""

    history = get_conversation_history(session_id)

    messages = []

    if context:
        system_message = f"""You are a helpful assistant. Use the following context to answer questions when relevant:
                         Context:
                         {context}

                         Remember previous messages in this conversation and provide coherent, contextual responses."""
        messages.append({"role": "system", "content": system_message})
    
    messages.extend(history)
    
    messages.append({"role": "user", "content": request.message})
    
    response = ollama.chat(
        model='gemma3:latest',
        messages=messages,
        stream=False,
    )
    
    assistant_response = response['message']['content']
    
    add_to_history(session_id, "user", request.message)
    add_to_history(session_id, "assistant", assistant_response)
    
    return ChatResponse(response=assistant_response)

@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    if session_id in conversation_memory:
        del conversation_memory[session_id]
    return {"message": f"History cleared for session {session_id}"}
