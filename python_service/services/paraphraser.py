from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class ParaphraserService:

    def __init__(self):

        print("Loading dedicated paraphrasing model...")

        self.model_name = "Vamsi/T5_Paraphrase_Paws"

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name
        )

        print("Paraphrasing model loaded successfully!")

    def paraphrase_for_question(
        self,
        question: str,
        context: str
    ):

        prompt = f"""
You are an evidence transformation model for a document
question-answering system.

Your task is to rewrite the retrieved document context
into clear, self-contained evidence that can be used to
answer the user's question.

Question:
{question}

Retrieved context:
{context}

Rules:

1. Use ONLY information contained in the retrieved context.

2. Do NOT use outside knowledge.

3. Do NOT invent facts.

4. Preserve all important facts, names, numbers, dates,
   and relationships from the retrieved context that are
   relevant to the question.

5. You may make information explicit when it is clearly
   encoded in the retrieved text.

   For example:

   "FAISS (Facebook AI Similarity Search)"

   may be rewritten as:

   "FAISS stands for Facebook AI Similarity Search."

6. You may interpret common textual structures such as:

   abbreviation (full form)
   name (description)
   product (company)
   entity (relationship)

   when the relationship is explicitly represented by
   the retrieved text.

7. Do NOT infer information that requires outside knowledge
   or unsupported reasoning.

8. Do NOT answer the user's question directly.

9. Produce only the transformed evidence.

Transformed evidence:
"""

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=300,
            num_beams=5,
            num_return_sequences=1
        )

        result = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return result