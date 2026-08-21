from FlagEmbedding import FlagReranker


class RerankerService:

    def __init__(self):

        print("Loading BGE reranker model...")

        self.model = FlagReranker(
            "BAAI/bge-reranker-v2-m3",
            use_fp16=False
        )

        print("BGE reranker loaded successfully!")

    def rerank(
        self,
        question: str,
        chunks: list[dict],
        top_k: int
    ):

        if not chunks:
            return []

        pairs = []

        for chunk in chunks:

            pairs.append([
                question,
                chunk["text"]
            ])

        scores = self.model.compute_score(
            pairs,
            normalize=True
        )

        # If only one chunk is supplied,
        # compute_score may return a single float.
        if isinstance(scores, float):
            scores = [scores]

        for chunk, score in zip(chunks, scores):

            chunk["rerank_score"] = float(score)

        # Highest score = most relevant
        chunks.sort(
            key=lambda chunk: chunk["rerank_score"],
            reverse=True
        )

        return chunks[:top_k]