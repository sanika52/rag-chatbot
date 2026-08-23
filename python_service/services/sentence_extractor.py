import re


class SentenceExtractor:

    # --------------------------------------------------
    # Extract clean sentences from a chunk
    # --------------------------------------------------

    @staticmethod
    def extract_sentences(text: str):

        if not text or not text.strip():
            return []

        text = text.strip()

        # --------------------------------------------------
        # Remove section headings
        #
        # Examples:
        # === FAISS ===
        # === META ===
        # === COMPANY HISTORY ===
        # --------------------------------------------------

        text = re.sub(
            r"={2,}\s*[^=\n]+?\s*={2,}",
            " ",
            text,
        )

        # --------------------------------------------------
        # Remove common document title lines
        #
        # Example:
        # RAG EVALUATION DOCUMENT V2
        # --------------------------------------------------

        text = re.sub(
            r"^\s*RAG\s+EVALUATION\s+DOCUMENT[^\n]*\n?",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # --------------------------------------------------
        # Normalize newlines and whitespace
        # --------------------------------------------------

        text = re.sub(
            r"\s+",
            " ",
            text,
        ).strip()

        if not text:
            return []

        # --------------------------------------------------
        # Split into sentences
        # --------------------------------------------------

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        cleaned = []

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            # Ignore remaining heading-like fragments
            if re.fullmatch(
                r"={2,}.*={2,}",
                sentence,
            ):
                continue

            cleaned.append(sentence)

        return cleaned

    # --------------------------------------------------
    # Find supporting sentence
    # --------------------------------------------------

    @staticmethod
    def find_supporting_sentence(
        question: str,
        answer: str,
        context: str,
    ):

        if not question or not answer or not context:
            return None

        question = question.strip()
        answer = answer.strip()
        context = context.strip()

        sentences = SentenceExtractor.extract_sentences(context)

        if not sentences:
            return None

        # --------------------------------------------------
        # First:
        # Exact answer containment
        # --------------------------------------------------

        answer_lower = answer.lower()

        for sentence in sentences:

            if answer_lower in sentence.lower():
                return sentence.strip()

        # --------------------------------------------------
        # Second:
        # Normalize whitespace
        # --------------------------------------------------

        normalized_answer = " ".join(answer.split()).lower()

        for sentence in sentences:

            normalized_sentence = " ".join(sentence.split()).lower()

            if normalized_answer in normalized_sentence:
                return sentence.strip()

        # --------------------------------------------------
        # If answer itself isn't literally present,
        # return None.
        #
        # This is important for hallucination prevention.
        # --------------------------------------------------

        return None
