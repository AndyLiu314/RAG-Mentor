import subprocess
import time
import requests

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes import chat, upload

ollama_process = None

def ensure_ollama_running():
    global ollama_process

    try:
        requests.get("http://localhost:11434")
        print("✓ Ollama is already running")
        return True
    
    except requests.exceptions.ConnectionError:
        print("Starting Ollama...")
        try:
            ollama_process = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)           
            for _ in range(10):
                time.sleep(1)
                try:
                    requests.get("http://localhost:11434")
                    print("✓ Ollama started successfully")
                    return True
                
                except requests.exceptions.ConnectionError:
                    continue

            print("✗ Failed to start Ollama")
            return False
        
        except FileNotFoundError:
            print("✗ Ollama not found. Please install Ollama first.")
            return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_ollama_running()
    yield
    if ollama_process:
        print("Stopping Ollama...")
        ollama_process.terminate()
        ollama_process.wait(timeout=5)
        print("✓ Ollama stopped")

app = FastAPI(title="RAG Mentor", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])

@app.get("/")
def root():
    return {"message": "RAG Mentor"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
