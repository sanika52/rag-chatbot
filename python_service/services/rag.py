from services.embeddings import EmbeddingService
from services.chroma_service import ChromaService
from services.llm import LLMService
from services.reranker import RerankerService
from config.settings import Settings


class RAGService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_service: ChromaService,
        llm_service: LLMService,
        reranker_service: RerankerService
    ):

        self.embedding_service = embedding_service
        self.chroma_service = chroma_service
        self.llm_service = llm_service
        self.reranker_service = reranker_service

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
        # Step 2: Retrieve candidate chunks from Chroma
        # --------------------------------------------------

        retrieved_chunks = self.chroma_service.search(
            query_embedding=query_embedding,
            user_id=user_id,
            document_ids=document_ids,
            top_k=top_k
        )

        # --------------------------------------------------
        # DEBUG: Inspect Chroma retrieval
        # --------------------------------------------------

        print("\n" + "=" * 70)

        print(f"QUESTION: {question}")

        print("=" * 70)

        print(
            f"\nChroma retrieved "
            f"{len(retrieved_chunks)} candidate chunks:\n"
        )

        for i, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):

            metadata = chunk["metadata"]

            print(f"--- Chroma Chunk {i} ---")

            print(
                f"Distance: "
                f"{chunk.get('distance')}"
            )

            print(
                f"Document: "
                f"{metadata.get('filename')}"
            )

            print(
                f"Page: "
                f"{metadata.get('page_number')}"
            )

            print("Text:")

            print(chunk["text"])

            print("-" * 70)

        if not retrieved_chunks:

            return {
                "answer": "I couldn't find any relevant information in the selected documents.",
                "sources": []
            }

        # --------------------------------------------------
        # Step 3: BGE Reranking
        # --------------------------------------------------

        reranked_chunks = self.reranker_service.rerank(
            question=question,
            chunks=retrieved_chunks,
            top_k=Settings.MAX_CONTEXT_CHUNKS
        )

        # --------------------------------------------------
        # DEBUG: Inspect reranked chunks
        # --------------------------------------------------

        print("\n" + "=" * 70)

        print("AFTER BGE RERANKING")

        print("=" * 70)

        print(
            f"\nKeeping "
            f"{len(reranked_chunks)} chunks:\n"
        )

        for i, chunk in enumerate(
            reranked_chunks,
            start=1
        ):

            metadata = chunk["metadata"]

            print(f"--- Reranked Chunk {i} ---")

            print(
                f"Rerank score: "
                f"{chunk.get('rerank_score')}"
            )

            print(
                f"Original Chroma distance: "
                f"{chunk.get('distance')}"
            )

            print(
                f"Document: "
                f"{metadata.get('filename')}"
            )

            print(
                f"Page: "
                f"{metadata.get('page_number')}"
            )

            print("Text:")

            print(chunk["text"])

            print("-" * 70)

        print("=" * 70 + "\n")

        # --------------------------------------------------
        # Step 4: Build context
        # --------------------------------------------------

        context_parts = []

        for chunk in reranked_chunks:

            metadata = chunk["metadata"]

            context_parts.append(
                f"""
Document: {metadata["filename"]}
Page: {metadata["page_number"]}

{chunk["text"]}
"""
            )

        context = "\n\n".join(
            context_parts
        )

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

        for chunk in reranked_chunks:

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

                grouped_sources[
                    document_id
                ]["pages"].add(page)

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