from services.embeddings import EmbeddingService
from services.chroma_service import ChromaService
from services.llm import LLMService
from config.settings import Settings


class RAGService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_service: ChromaService,
        llm_service: LLMService
    ):

        self.embedding_service = embedding_service
        self.chroma_service = chroma_service
        self.llm_service = llm_service

    def answer_question(
        self,
        question: str,
        user_id: int,
        document_ids: list[int],
        top_k: int = Settings.TOP_K
    ):

        if not document_ids:
            return {
                "answer": "Please select at least one document before asking a question.",
                "sources": []
            }

        # --------------------------------------------------
        # Step 1: Embed the question
        # --------------------------------------------------

        query_embedding = self.embedding_service.embed_query(
            question
        )

        # --------------------------------------------------
        # Step 2: Retrieve relevant chunks
        # --------------------------------------------------

        retrieved_chunks = self.chroma_service.search(
            query_embedding=query_embedding,
            user_id=user_id,
            document_ids=document_ids,
            top_k=top_k
        )

        if not retrieved_chunks:
            return {
                "answer": "I couldn't find any relevant information in the selected documents.",
                "sources": []
            }

        # --------------------------------------------------
        # Step 3: Remove weak matches
        # --------------------------------------------------

        # SIMILARITY_THRESHOLD =Settings.SIMILARITY_THRESHOLD

        # retrieved_chunks = [
        #     chunk
        #     for chunk in retrieved_chunks
        #     if chunk["distance"] <= SIMILARITY_THRESHOLD
        # ]

        # if not retrieved_chunks:
        #     return {
        #         "answer": "I couldn't find any relevant information in the selected documents.",
        #         "sources": []
        #     }

        # --------------------------------------------------
        # Step 4: Build context
        # --------------------------------------------------

        context_parts = []

        for chunk in retrieved_chunks:

            metadata = chunk["metadata"]

            context_parts.append(
                f"""
        Document: {metadata["filename"]}
        Page: {metadata["page_number"]}

        {chunk["text"]}
        """
            )

        context = "\n\n".join(context_parts)

        # --------------------------------------------------
        # Step 5: Generate answer
        # --------------------------------------------------

        answer = self.llm_service.generate_answer(
            question=question,
            context=context
        )

        # --------------------------------------------------
        # Step 6: Build unique citations
        # --------------------------------------------------

        grouped_sources = {}

        for chunk in retrieved_chunks:

            metadata = chunk["metadata"]

            document_id = metadata["document_id"]

            if document_id not in grouped_sources:

                grouped_sources[document_id] = {
                    "document_id": document_id,
                    "filename": metadata["filename"],
                    "stored_filename": metadata["stored_filename"],
                    "pages": set()
                }

            page = metadata["page_number"]

            if page is not None:
                grouped_sources[document_id]["pages"].add(page)

        sources = []

        for source in grouped_sources.values():

            sources.append(
                {
                    "document_id": source["document_id"],
                    "filename": source["filename"],
                    "stored_filename": source["stored_filename"],
                    "pages": sorted(source["pages"])
                }
            )

        return {
            "answer": answer,
            "sources": sources
        }