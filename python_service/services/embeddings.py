from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model: SentenceTransformer):
        self.model = model

    def embed_chunks(self, chunks):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings

    def embed_query(self, question: str):

        embedding = self.model.encode(
            question,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding