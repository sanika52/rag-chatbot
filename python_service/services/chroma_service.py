import chromadb


class ChromaService:

    def __init__(self):

        # Create/Open persistent Chroma database
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        # Create/Open collection
        self.collection = self.client.get_or_create_collection(
            name="rag_documents"
        )

    def store_document(
        self,
        document_id,
        user_id,
        filename,
        chunks,
        embeddings
        ):

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            ids.append(f"{user_id}_{document_id}_{index}")

            documents.append(chunk["text"])

            metadatas.append({
                "user_id": user_id,
                "document_id": document_id,
                "filename": filename,
                "page_number": chunk["page_number"],
                "chunk_index": index
            })

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

        return len(chunks)    

    def count_chunks(self):
        """Return total number of chunks stored."""
        return self.collection.count()

    def get_all_chunks(self):
        """Return everything stored in ChromaDB."""
        return self.collection.get()

    def delete_document(self, document_id, user_id):
        """Delete all chunks belonging to one document."""
        self.collection.delete(
            where={
                "$and": [
                    {"user_id": user_id},
                    {"document_id": document_id}
                ]
            }
        )