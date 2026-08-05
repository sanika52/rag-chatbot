import chromadb


class ChromaService:

    def __init__(self):

        self.client = chromadb.PersistentClient(path="chroma_db")

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def store_document(
        self,
        document_id,
        user_id,
        filename,
        stored_filename,
        chunks,
        embeddings
    ):

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            ids.append(
                f"{user_id}_{document_id}_{index}"
            )

            documents.append(
                chunk["text"]
            )

            metadatas.append(
                {
                    "user_id": user_id,
                    "document_id": document_id,
                    "filename": filename,
                    "stored_filename": stored_filename,
                    "page_number": chunk["page_number"],
                    "chunk_index": index
                }
            )
        
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        return len(chunks)

    def search(
        self,
        query_embedding,
        user_id: int,
        document_ids: list[int],
        top_k: int = 5
    ):

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            where={
                "$and": [
                    {
                        "user_id": user_id
                    },
                    {
                        "document_id": {
                            "$in": document_ids
                        }
                    }
                ]
            }
        )

        if not results["documents"][0]:
            return []

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance
                }
            )

        return retrieved_chunks

    def count_chunks(self):

        return self.collection.count()

    def get_all_chunks(self):

        return self.collection.get()

    def delete_document(
        self,
        user_id,
        document_id
    ):

        self.collection.delete(
            where={
                "$and": [
                    {
                        "user_id": user_id
                    },
                    {
                        "document_id": document_id
                    }
                ]
            }
        )