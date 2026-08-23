from transformers import pipeline


class QAService:

    def __init__(self):

        print("Loading extractive QA model...")

        self.qa_pipeline = pipeline(
            "question-answering",
            model="distilbert-base-uncased-distilled-squad",
            tokenizer="distilbert-base-uncased-distilled-squad"
        )

        print("Extractive QA model loaded successfully!")

    def answer(
        self,
        question: str,
        context: str,
        threshold: float = 0.20
    ):

        if not context.strip():
            return {
                "answer": None,
                "score": 0.0,
                "is_answerable": False
            }

        result = self.qa_pipeline(
            question=question,
            context=context
        )

        score = float(result["score"])

        is_answerable = score >= threshold

        return {
            "answer": result["answer"] if is_answerable else None,
            "score": score,
            "is_answerable": is_answerable,
            "start": result["start"],
            "end": result["end"]
        }