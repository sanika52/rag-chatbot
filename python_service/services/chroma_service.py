import chromadb


class ChromaService:

    def __init__(self):

        self.client = chromadb.PersistentClient(path="chroma_db")

        self.collection = self.client.get_or_create_collection(name="documents")

    # --------------------------------------------------
    # Store document chunks
    # --------------------------------------------------

    def store_document(
        self, document_id, user_id, filename, stored_filename, chunks, embeddings
    ):

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            ids.append(f"{user_id}_{document_id}_{index}")

            documents.append(chunk["text"])

            metadatas.append(
                {
                    "user_id": user_id,
                    "document_id": document_id,
                    "filename": filename,
                    "stored_filename": stored_filename,
                    "page_number": chunk["page_number"],
                    "chunk_index": index,
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
        )

        return len(chunks)

    # --------------------------------------------------
    # Vector similarity search
    # --------------------------------------------------

    def search(
        self, query_embedding, user_id: int, document_ids: list[int], top_k: int = 5
    ):

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where={
                "$and": [{"user_id": user_id}, {"document_id": {"$in": document_ids}}]
            },
        )

        if not results["documents"][0]:
            return []

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(documents, metadatas, distances):

            retrieved_chunks.append(
                {"text": document, "metadata": metadata, "distance": distance}
            )

        return retrieved_chunks

    # --------------------------------------------------
    # Get neighboring chunks
    # --------------------------------------------------

    def get_neighbor_chunks(
        self, chunk, user_id: int, document_ids: list[int], window: int = 1
    ):
        """
        Retrieve neighboring chunks around a given chunk.

        Example:

            window = 1

            chunk 5
                ↓
            chunks 4, 5, 6
        """

        metadata = chunk["metadata"]

        document_id = metadata["document_id"]
        chunk_index = metadata["chunk_index"]

        # Determine the chunk range
        start_index = max(0, chunk_index - window)

        end_index = chunk_index + window

        # Get all chunks belonging to this document
        results = self.collection.get(
            where={"$and": [{"user_id": user_id}, {"document_id": document_id}]}
        )

        if not results["documents"]:
            return []

        neighbors = []

        for document, metadata in zip(results["documents"], results["metadatas"]):

            index = metadata["chunk_index"]

            if start_index <= index <= end_index:

                neighbors.append(
                    {"text": document, "metadata": metadata, "distance": None}
                )

        # Keep chunks in their original document order
        neighbors.sort(key=lambda x: x["metadata"]["chunk_index"])

        return neighbors

    # --------------------------------------------------
    # Collection information
    # --------------------------------------------------

    def count_chunks(self):

        return self.collection.count()

    # --------------------------------------------------
    # Get all chunks
    # --------------------------------------------------

    def get_all_chunks(self):

        return self.collection.get()

    # --------------------------------------------------
    # Delete document
    # --------------------------------------------------

    def delete_document(self, user_id, document_id):

        self.collection.delete(
            where={"$and": [{"user_id": user_id}, {"document_id": document_id}]}
        )
