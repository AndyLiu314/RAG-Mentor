from fastapi import APIRouter
from pydantic import BaseModel
import ollama

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = ollama.chat(
        model='gemma3:latest',
        messages=[{'role': 'user', 'content': request.message}],
        stream=False,
    )
    
    return ChatResponse(response=response['message']['content'])