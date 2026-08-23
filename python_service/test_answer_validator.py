from services.answer_validator import AnswerValidator

validator = AnswerValidator()


def test_case(
    question: str,
    answer: str,
    context: str,
    expected: bool,
):
    result = validator.validate(
        question=question,
        answer=answer,
        context=context,
    )

    status = "PASS" if result == expected else "FAIL"

    print("=" * 80)
    print(f"QUESTION: {question}")
    print(f"ANSWER: {answer}")
    print(f"CONTEXT: {context}")
    print(f"EXPECTED: {expected}")
    print(f"RESULT:   {result}")
    print(f"STATUS:   {status}")
    print("=" * 80)
    print()


# ============================================================
# 1. DIRECT FACTUAL QUESTIONS
# ============================================================

test_case(
    question="What does FAIR stand for?",
    answer="Facebook AI Research",
    context=(
        "FAIR (Facebook AI Research) is an artificial intelligence "
        "research organization."
    ),
    expected=True,
)


test_case(
    question="What is FAISS?",
    answer="Facebook AI Similarity Search",
    context=(
        "FAISS (Facebook AI Similarity Search) is a library for "
        "efficient similarity search and clustering of dense vectors."
    ),
    expected=True,
)


test_case(
    question="When was Meta founded?",
    answer="2004",
    context="Meta was founded in 2004.",
    expected=True,
)


test_case(
    question="Which company develops Milvus?",
    answer="Zilliz",
    context="Milvus is developed by Zilliz.",
    expected=True,
)


# ============================================================
# 2. RELATIONSHIP QUESTIONS
# ============================================================

test_case(
    question="Does FAIR belong to Meta?",
    answer="Meta",
    context="FAIR is part of Meta.",
    expected=True,
)


test_case(
    question="Is FAIR a part of Meta?",
    answer="Meta",
    context="FAIR is part of Meta.",
    expected=True,
)


test_case(
    question="Who develops Milvus?",
    answer="Zilliz",
    context="Milvus is developed by Zilliz.",
    expected=True,
)


# ============================================================
# 3. UNSUPPORTED QUESTIONS
# ============================================================

test_case(
    question="What is the capital of France?",
    answer="Pune",
    context="The city of Pune is located in the Indian state of Maharashtra.",
    expected=False,
)


test_case(
    question="Who founded Zilliz?",
    answer="Zilliz",
    context="Zilliz is a company that develops and maintains Milvus.",
    expected=False,
)


test_case(
    question="How many employees does ChromaDB have?",
    answer="ChromaDB",
    context=(
        "ChromaDB is an open-source vector database designed for "
        "storing and querying embeddings."
    ),
    expected=False,
)


test_case(
    question="What programming language was used to develop FAISS?",
    answer="Python",
    context=(
        "FAISS (Facebook AI Similarity Search) is a library for "
        "efficient similarity search and clustering of dense vectors."
    ),
    expected=False,
)


# ============================================================
# 4. WRONG ANSWER PRESENT IN CONTEXT
# ============================================================

test_case(
    question="When was Meta founded?",
    answer="2015",
    context="Meta was founded in 2004. ExampleAI was founded in 2015.",
    expected=False,
)


test_case(
    question="Which company develops Milvus?",
    answer="Facebook",
    context="Milvus is developed by Zilliz. FAISS was developed by Facebook AI Research.",
    expected=False,
)


# ============================================================
# 5. ANSWER EXISTS BUT DOES NOT ANSWER THE QUESTION
# ============================================================

test_case(
    question="Who founded Zilliz?",
    answer="Milvus",
    context="Zilliz is a company that develops and maintains Milvus.",
    expected=False,
)


test_case(
    question="What is the capital of France?",
    answer="Pune",
    context=(
        "The city of Pune is located in the Indian state of Maharashtra. "
        "Pune is a major city in India."
    ),
    expected=False,
)


# ============================================================
# 6. FULL FORM QUESTIONS
# ============================================================

test_case(
    question="What is the full form of FAIR?",
    answer="Facebook AI Research",
    context="FAIR (Facebook AI Research) is an artificial intelligence research organization.",
    expected=True,
)


test_case(
    question="What is the full form of FAISS?",
    answer="Facebook AI Similarity Search",
    context="FAISS (Facebook AI Similarity Search) is a library for efficient similarity search.",
    expected=True,
)


# ============================================================
# 7. SAME ANSWER BUT WRONG ENTITY
# ============================================================

test_case(
    question="What does FAIR stand for?",
    answer="Facebook AI Similarity Search",
    context="FAISS (Facebook AI Similarity Search) is a library for similarity search.",
    expected=False,
)


test_case(
    question="What is the full form of FAISS?",
    answer="Facebook AI Research",
    context="FAISS was developed by Facebook AI Research (FAIR).",
    expected=False,
)


# ============================================================
# 8. EMPTY / INVALID INPUT
# ============================================================

test_case(
    question="",
    answer="Meta",
    context="FAIR is part of Meta.",
    expected=False,
)


test_case(
    question="Does FAIR belong to Meta?",
    answer="",
    context="FAIR is part of Meta.",
    expected=False,
)


test_case(
    question="Does FAIR belong to Meta?",
    answer="Meta",
    context="",
    expected=False,
)


# ============================================================
# 9. ANSWER IS ONLY A COMMON WORD
# ============================================================

test_case(
    question="What is the company?",
    answer="is",
    context="Meta is a technology company.",
    expected=False,
)


test_case(
    question="What is the company?",
    answer="a",
    context="Meta is a technology company.",
    expected=False,
)


# ============================================================
# 10. NEGATIVE RELATIONSHIP
# ============================================================

test_case(
    question="Does FAIR belong to Zilliz?",
    answer="Zilliz",
    context="FAIR is part of Meta. Milvus is developed by Zilliz.",
    expected=False,
)


# ============================================================
# 11. ENTITY PRESENT BUT WRONG RELATIONSHIP
# ============================================================

test_case(
    question="Does Meta develop Milvus?",
    answer="Meta",
    context="Meta is a technology company. Milvus is developed by Zilliz.",
    expected=False,
)


# ============================================================
# 12. MORE NATURAL QUESTIONS
# ============================================================

test_case(
    question="Who is responsible for developing Milvus?",
    answer="Zilliz",
    context="Milvus is developed by Zilliz.",
    expected=True,
)


test_case(
    question="Which organization developed FAISS?",
    answer="Facebook AI Research",
    context="FAISS was developed by Facebook AI Research (FAIR).",
    expected=True,
)


test_case(
    question="When did Meta start?",
    answer="2004",
    context="Meta was founded in 2004.",
    expected=True,
)
