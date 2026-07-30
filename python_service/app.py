from services.chroma_service import ChromaService
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer

from services.document_processor import DocumentProcessor
from services.chunker import TextChunker
from services.embeddings import EmbeddingService
from models.document_models import ProcessDocumentRequest


# Global embedding service
embedding_service = None
chroma_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global embedding_service
    global chroma_service

    print("Loading BGE-M3 embedding model...")

    model = SentenceTransformer("BAAI/bge-m3")

    embedding_service = EmbeddingService(model)
    chroma_service = ChromaService()

    print("BGE-M3 loaded successfully!")

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "RAG Chatbot API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/process-document")
def process_document(request: ProcessDocumentRequest):

    try:

        # Step 1 - Extract text
        pages = DocumentProcessor.extract_text(request.file_path)

        # Step 2 - Chunk text
        chunker = TextChunker()
        chunks = chunker.split(pages)

        # Step 3 - Generate embeddings
        embeddings = embedding_service.embed_chunks(chunks)
        stored_chunks = chroma_service.store_document(
            document_id=request.document_id,
            user_id=request.user_id,
            filename=request.filename,
            chunks=chunks,
            embeddings=embeddings
        )

        total_characters = sum(
            len(page["text"])
            for page in pages
        )

        return {
             "success": True,
             "document_id": request.document_id,
             "user_id": request.user_id,
             "characters": total_characters,
             "chunks": len(chunks),
             "stored_chunks": stored_chunks,
             "embedding_dimension": len(embeddings[0])
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


