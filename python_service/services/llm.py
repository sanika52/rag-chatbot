import os

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


class LLMService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = "llama-3.1-8b-instant"

    def generate_answer(
        self,
        question: str,
        context: str
    ):

        prompt = f"""
    You are an intelligent RAG assistant.

    Use ONLY the information provided in the context below.

    Instructions:

    - Read all of the retrieved context carefully before answering.
    - If the answer exists in the context, answer it clearly and naturally.
    - You may combine information from multiple retrieved passages.
    - Do not make up facts that are not present in the context.
    - If the context does not contain enough information, reply exactly:

    I couldn't find that information in the uploaded documents.

    -------------------------
    CONTEXT
    -------------------------

    {context}

    -------------------------
    QUESTION
    -------------------------

    {question}

    -------------------------
    ANSWER
    -------------------------
    """

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0,

            max_tokens=500
        )

        return response.choices[0].message.content