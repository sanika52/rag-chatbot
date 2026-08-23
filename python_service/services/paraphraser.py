from transformers import pipeline


class ParaphraserService:

    def __init__(self):

        print("Loading paraphrasing model...")

        self.paraphrase_pipeline = pipeline(
            "text2text-generation",
            model="Vamsi/T5_Paraphrase_Paws",
            tokenizer="Vamsi/T5_Paraphrase_Paws",
        )

        print("Paraphrasing model loaded successfully!")

    def paraphrase(self, text: str):

        if not text or not text.strip():
            return text

        result = self.paraphrase_pipeline(
            text.strip(),
            max_new_tokens=64,
            num_return_sequences=1,
            do_sample=False,
        )

        paraphrased = result[0].get("generated_text", "").strip()

        if not paraphrased:
            return text

        return paraphrased
