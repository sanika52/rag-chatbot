from sentence_transformers import CrossEncoder


class RerankerService:

    def __init__(self):

        print("Loading BGE reranker...")

        self.model = CrossEncoder("BAAI/bge-reranker-base")

        print("BGE reranker loaded successfully!")

    def rerank(self, question: str, chunks: list, top_k: int = 5):

        if not question or not question.strip():
            return []

        if not chunks:
            return []

        pairs = []

        for chunk in chunks:

            text = chunk.get("text", "").strip()

            if not text:
                continue

            pairs.append((question, text))

        if not pairs:
            return []

        scores = self.model.predict(pairs)

        scored_chunks = []

        pair_index = 0

        for chunk in chunks:

            text = chunk.get("text", "").strip()

            if not text:
                continue

            chunk_copy = chunk.copy()

            chunk_copy["rerank_score"] = float(scores[pair_index])

            scored_chunks.append(chunk_copy)

            pair_index += 1

        # Highest BGE score = most relevant.
        scored_chunks.sort(key=lambda x: x["rerank_score"], reverse=True)

        return scored_chunks[:top_k]

    def score_sentences(self, question: str, sentences: list):

        if not question or not question.strip():
            return []

        if not sentences:
            return []

        pairs = [(question, sentence) for sentence in sentences]

        scores = self.model.predict(pairs)

        scored_sentences = []

        for sentence, score in zip(sentences, scores):

            scored_sentences.append({"text": sentence, "rerank_score": float(score)})

        scored_sentences.sort(key=lambda x: x["rerank_score"], reverse=True)

        return scored_sentences
