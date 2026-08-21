from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer

from models.document_models import ProcessDocumentRequest
from models.request_models import ChatRequest

from services.chunker import TextChunker
from services.chroma_service import ChromaService
from services.document_processor import DocumentProcessor
from services.embeddings import EmbeddingService
from services.llm import LLMService
from services.rag import RAGService
from services.reranker import RerankerService


# Global services
embedding_service = None
chroma_service = None
llm_service = None
reranker_service = None
rag_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):

    global embedding_service
    global chroma_service
    global llm_service
    global reranker_service
    global rag_service

    # --------------------------------------------------
    # Load embedding model
    # --------------------------------------------------

    print("Loading BGE-M3 embedding model...")

    model = SentenceTransformer("BAAI/bge-m3")

    embedding_service = EmbeddingService(model)

    print("BGE-M3 loaded successfully!")

    # --------------------------------------------------
    # Initialize services
    # --------------------------------------------------

    chroma_service = ChromaService()

    llm_service = LLMService()

    reranker_service = RerankerService()

    # --------------------------------------------------
    # Initialize RAG service
    # --------------------------------------------------

    rag_service = RAGService(
        embedding_service=embedding_service,
        chroma_service=chroma_service,
        llm_service=llm_service,
        reranker_service=reranker_service
    )

    print("All RAG services initialized successfully!")

    yield


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    lifespan=lifespan
)


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "status": "running",
        "service": "RAG Chatbot API"
    }


# --------------------------------------------------
# Health
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# Process Document
# --------------------------------------------------

@app.post("/process-document")
def process_document(
    request: ProcessDocumentRequest
):

    try:

        # ----------------------------------------------
        # Step 1 - Extract text
        # ----------------------------------------------

        pages = DocumentProcessor.extract_text(
            request.file_path
        )

        # ----------------------------------------------
        # Step 2 - Chunk text
        # ----------------------------------------------

        chunker = TextChunker()

        chunks = chunker.split(
            pages
        )

        # ----------------------------------------------
        # Step 3 - Generate embeddings
        # ----------------------------------------------

        embeddings = embedding_service.embed_chunks(
            chunks
        )

        # ----------------------------------------------
        # Step 4 - Store in ChromaDB
        # ----------------------------------------------

        stored_chunks = chroma_service.store_document(
            document_id=request.document_id,
            user_id=request.user_id,
            filename=request.filename,
            stored_filename=request.stored_filename,
            chunks=chunks,
            embeddings=embeddings
        )

        # ----------------------------------------------
        # Statistics
        # ----------------------------------------------

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


# --------------------------------------------------
# Chat
# --------------------------------------------------

@app.post("/chat")
def chat(
    request: ChatRequest
):

    return rag_service.answer_question(
        question=request.question,
        user_id=request.user_id,
        document_ids=request.document_ids
    )