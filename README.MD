# RAG Mentor
## Made By: Andy Liu

A Retrieval-Augmented Generation (RAG) chatbot that allows you to upload PDF documents and ask questions about their content. Built with FastAPI, React, ChromaDB, and Ollama.

### **Features:**

- **PDF Upload & Processing** - Upload PDFs and automatically extract and chunk text
- **Semantic Search** - Uses ChromaDB vector database for intelligent document retrieval
- **Conversational Memory** - Maintains chat history across sessions
- **Smart Text Chunking** - Uses LangChain's RecursiveCharacterTextSplitter for better context preservation
- **Local LLM** - Powered by Ollama (Gemma3 model)

### **Tech Stack:**

**Backend:**
- FastAPI - Modern Python web framework
- ChromaDB - Vector database for document embeddings
- Ollama - Local LLM inference
- LangChain - Text splitting utilities
- PyPDF2 - PDF text extraction

**Frontend:**
- React - UI framework
- Vite - Build tool

### **How It Works:**

1. **Document Upload**: PDFs are uploaded and text is extracted using PyPDF2
2. **Text Chunking**: Documents are split into semantic chunks using LangChain's RecursiveCharacterTextSplitter
3. **Vector Storage**: Chunks are embedded and stored in ChromaDB
4. **Query Processing**: User questions are embedded and matched against stored chunks
5. **Context Retrieval**: Top 3 most relevant chunks are retrieved
6. **Response Generation**: Context + conversation history is sent to Ollama's Gemma3 model
7. **Caching**: Responses are cached to speed up repeated queries
