import re


class AnswerValidator:

    def __init__(self):
        pass

    # --------------------------------------------------
    # Normalize text
    # --------------------------------------------------

    @staticmethod
    def normalize(text: str) -> str:

        if not text:
            return ""

        text = text.lower().strip()

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        return text

    # --------------------------------------------------
    # Tokenize
    # --------------------------------------------------

    @staticmethod
    def tokenize(text: str):

        return re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )

    # --------------------------------------------------
    # Check whether answer is actually present
    # in the supporting sentence
    # --------------------------------------------------

    def answer_occurs_in_context(
        self,
        answer: str,
        context: str,
    ) -> bool:

        answer_normalized = self.normalize(answer)
        context_normalized = self.normalize(context)

        if not answer_normalized or not context_normalized:
            return False

        # Exact phrase match
        if answer_normalized in context_normalized:
            return True

        # Token-level fallback
        answer_tokens = self.tokenize(answer)
        context_tokens = self.tokenize(context)

        if not answer_tokens:
            return False

        context_token_set = set(context_tokens)

        return all(token in context_token_set for token in answer_tokens)

    # --------------------------------------------------
    # Extract important words from question
    #
    # These are generic English stop words only.
    # Nothing is document-specific.
    # --------------------------------------------------

    @staticmethod
    def important_question_words(question: str):

        stop_words = {
            "what",
            "which",
            "who",
            "when",
            "where",
            "why",
            "how",
            "does",
            "do",
            "did",
            "is",
            "are",
            "was",
            "were",
            "will",
            "can",
            "could",
            "would",
            "should",
            "the",
            "a",
            "an",
            "of",
            "for",
            "to",
            "in",
            "on",
            "at",
            "with",
            "and",
            "or",
            "be",
            "been",
            "being",
            "tell",
            "me",
            "about",
        }

        words = AnswerValidator.tokenize(question)

        return [word for word in words if word not in stop_words]

    # --------------------------------------------------
    # Check whether the question's important entities
    # occur in the supporting sentence.
    #
    # Example:
    #
    # Question:
    # Does FAIR belong to Meta?
    #
    # Sentence:
    # FAIR is part of Meta.
    #
    # FAIR + Meta are present -> potentially valid.
    # --------------------------------------------------

    def question_entities_present(
        self,
        question: str,
        context: str,
    ) -> bool:

        important_words = self.important_question_words(question)

        if not important_words:
            return True

        context_tokens = set(self.tokenize(context))

        matched = [word for word in important_words if word in context_tokens]

        # At least one important entity should be
        # grounded in the supporting sentence.
        return len(matched) > 0

    # --------------------------------------------------
    # Detect whether the question expects a specific
    # type of relationship.
    #
    # This is generic linguistic reasoning, not
    # knowledge about our particular document.
    # --------------------------------------------------

    @staticmethod
    def question_type(question: str):

        question_lower = question.lower()

        if (
            "stand for" in question_lower
            or "full form" in question_lower
            or "abbreviation" in question_lower
        ):
            return "definition"

        if (
            "when" in question_lower
            or "what year" in question_lower
            or "which year" in question_lower
        ):
            return "temporal"

        if "how many" in question_lower or "how much" in question_lower:
            return "quantity"

        if "who" in question_lower:
            return "person_or_organization"

        if (
            "does" in question_lower
            or "do" in question_lower
            or "did" in question_lower
            or "is" in question_lower
            or "are" in question_lower
            or "was" in question_lower
            or "were" in question_lower
        ):
            return "yes_no_or_relationship"

        return "general"

    # --------------------------------------------------
    # Validate numeric answers
    #
    # Particularly useful for questions such as:
    #
    # When was Meta founded?
    # -> 2004
    #
    # How many employees...?
    # -> 500
    # --------------------------------------------------

    def validate_numeric_answer(
        self,
        question: str,
        answer: str,
        context: str,
    ) -> bool:

        answer_numbers = re.findall(
            r"\b\d+(?:\.\d+)?\b",
            answer,
        )

        context_numbers = re.findall(
            r"\b\d+(?:\.\d+)?\b",
            context,
        )

        if not answer_numbers:
            return True

        return all(number in context_numbers for number in answer_numbers)

    # --------------------------------------------------
    # Validate definition / full-form questions
    #
    # Example:
    #
    # Question:
    # What does FAIR stand for?
    #
    # Answer:
    # Facebook AI Research
    #
    # Sentence:
    # FAIR (Facebook AI Research) is an organization...
    #
    # -> True
    #
    # But:
    #
    # Question:
    # What is the full form of FAISS?
    #
    # Answer:
    # Facebook AI Research
    #
    # Sentence:
    # FAISS was developed by Facebook AI Research (FAIR).
    #
    # -> False
    # --------------------------------------------------

    def validate_definition(
        self,
        question: str,
        answer: str,
        context: str,
    ) -> bool:

        question_lower = question.lower()
        context_lower = context.lower()
        answer_lower = answer.lower().strip()

        # Extract the likely abbreviation/entity
        question_words = self.important_question_words(question)

        if not question_words:
            return False

        # Look for:
        #
        # FAIR (Facebook AI Research)
        #
        # FAISS (Facebook AI Similarity Search)
        #
        for entity in question_words:

            pattern = (
                rf"\b{re.escape(entity)}\s*" rf"\(\s*{re.escape(answer_lower)}\s*\)"
            )

            if re.search(
                pattern,
                context_lower,
            ):
                return True

        # Also support:
        #
        # FAIR stands for Facebook AI Research
        #
        pattern = rf"\b[a-zA-Z0-9]+\s+stands\s+for\s+" rf"{re.escape(answer_lower)}"

        if re.search(
            pattern,
            context_lower,
        ):
            return True

        return False

    # --------------------------------------------------
    # Main validation
    # --------------------------------------------------

    def validate(
        self,
        question: str,
        answer: str,
        context: str,
    ) -> bool:

        # --------------------------------------------------
        # Basic validation
        # --------------------------------------------------

        if not question or not question.strip():
            return False

        if not answer or not answer.strip():
            return False

        if not context or not context.strip():
            return False

        question = question.strip()
        answer = answer.strip()
        context = context.strip()

        # --------------------------------------------------
        # Very short meaningless answers
        # --------------------------------------------------

        if len(answer) < 2:
            return False

        # --------------------------------------------------
        # Answer must occur in supporting sentence
        # --------------------------------------------------

        if not self.answer_occurs_in_context(
            answer,
            context,
        ):
            return False

        # --------------------------------------------------
        # Question entities must be grounded in the
        # supporting sentence.
        # --------------------------------------------------

        if not self.question_entities_present(
            question,
            context,
        ):
            return False

        # --------------------------------------------------
        # Question type
        # --------------------------------------------------

        q_type = self.question_type(question)

        # --------------------------------------------------
        # Numeric questions
        # --------------------------------------------------

        if q_type in {
            "temporal",
            "quantity",
        }:

            if not self.validate_numeric_answer(
                question,
                answer,
                context,
            ):
                return False

        # --------------------------------------------------
        # Definition / full-form questions
        # --------------------------------------------------

        if q_type == "definition":

            if not self.validate_definition(
                question,
                answer,
                context,
            ):
                return False

        # --------------------------------------------------
        # Final validation
        # --------------------------------------------------

        return True
