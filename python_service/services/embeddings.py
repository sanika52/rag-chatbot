from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self, model):
        self.model = model

    def embed_chunks(self, chunks):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )