from transformers import pipeline


class QAService:

    def __init__(self):

        print("Loading extractive QA model...")

        self.qa_pipeline = pipeline(
            "question-answering",
            model="distilbert-base-uncased-distilled-squad",
            tokenizer="distilbert-base-uncased-distilled-squad",
        )

        print("Extractive QA model loaded successfully!")

    def answer_question(self, question: str, context: str):

        if not context or not context.strip():

            return {"answer": None, "score": 0.0}

        result = self.qa_pipeline(question=question, context=context)

        answer = result.get("answer", "").strip()
        score = float(result.get("score", 0.0))

        if not answer:

            return {"answer": None, "score": score}

        return {"answer": answer, "score": score}
