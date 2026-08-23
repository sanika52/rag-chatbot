from services.sentence_extractor import SentenceExtractor


def test_case(question, answer, context):

    print("\n" + "=" * 80)

    print("QUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)

    print("\nCONTEXT:")
    print(context)

    evidence = SentenceExtractor.find_supporting_sentence(
        question=question,
        answer=answer,
        context=context,
    )

    print("\nSUPPORTING EVIDENCE:")
    print(evidence)

    print("=" * 80)


# --------------------------------------------------
# Test 1
# --------------------------------------------------

test_case(
    question="Does FAIR belong to Meta?",
    answer="Meta",
    context="FAIR is part of Meta.",
)


# --------------------------------------------------
# Test 2
# --------------------------------------------------

test_case(
    question="What does FAIR stand for?",
    answer="Facebook AI Research",
    context=(
        "FAIR (Facebook AI Research) is an artificial "
        "intelligence research organization."
    ),
)


# --------------------------------------------------
# Test 3
# --------------------------------------------------

test_case(
    question="When was Meta founded?",
    answer="2004",
    context="Meta was founded in 2004.",
)


# --------------------------------------------------
# Test 4
# --------------------------------------------------

test_case(
    question="Which company develops Milvus?",
    answer="Zilliz",
    context="Milvus is developed by Zilliz.",
)


# --------------------------------------------------
# Test 5
# --------------------------------------------------

test_case(
    question="Who founded Zilliz?",
    answer="Zilliz",
    context=("Zilliz is a company that develops and maintains Milvus."),
)


# --------------------------------------------------
# Test 6
# --------------------------------------------------

test_case(
    question="What is the capital of France?",
    answer="Pune",
    context=("The city of Pune is located in the Indian state " "of Maharashtra."),
)
