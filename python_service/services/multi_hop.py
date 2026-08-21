class MultiHopRetriever:

    def __init__(
        self,
        embedding_service,
        chroma_service
    ):

        self.embedding_service = embedding_service
        self.chroma_service = chroma_service

    def retrieve(
        self,
        question: str,
        user_id: int,
        document_ids: list[int],
        top_k: int = 5
    ):

        # -----------------------------------------
        # Hop 1
        # -----------------------------------------

        query_embedding = self.embedding_service.embed_query(
            question
        )

        first_results = self.chroma_service.search(
            query_embedding=query_embedding,
            user_id=user_id,
            document_ids=document_ids,
            top_k=top_k
        )

        if not first_results:
            return []

        all_results = []

        all_results.extend(first_results)

        return all_results