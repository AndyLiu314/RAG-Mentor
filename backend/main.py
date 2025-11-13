from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat, documents

app = FastAPI(title="RAG Mentor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
# app.include_router(documents.router, prefix="/api/documents", tags=["documents"])

@app.get("/")
def root():
    return {"message": "RAG Mentor"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)