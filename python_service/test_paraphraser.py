from services.paraphraser import ParaphraserService


def test_case(paraphraser, evidence):

    print("\n" + "=" * 80)

    print("SUPPORTING EVIDENCE:")
    print(evidence)

    result = paraphraser.paraphrase(evidence)

    print("\nPARAPHRASED EVIDENCE:")
    print(result)

    print("=" * 80)


# --------------------------------------------------
# Load paraphraser
# --------------------------------------------------

paraphraser = ParaphraserService()


# --------------------------------------------------
# Test 1
# --------------------------------------------------

test_case(
    paraphraser=paraphraser,
    evidence="FAIR is part of Meta.",
)


# --------------------------------------------------
# Test 2
# --------------------------------------------------

test_case(
    paraphraser=paraphraser,
    evidence=(
        "FAIR (Facebook AI Research) is an artificial intelligence "
        "research organization."
    ),
)


# --------------------------------------------------
# Test 3
# --------------------------------------------------

test_case(
    paraphraser=paraphraser,
    evidence="Meta was founded in 2004.",
)


# --------------------------------------------------
# Test 4
# --------------------------------------------------

test_case(
    paraphraser=paraphraser,
    evidence="Milvus is developed by Zilliz.",
)


# --------------------------------------------------
# Test 5
# --------------------------------------------------

test_case(
    paraphraser=paraphraser,
    evidence="Zilliz is a company that develops and maintains Milvus.",
)


# --------------------------------------------------
# Test 6
# --------------------------------------------------

test_case(
    paraphraser=paraphraser,
    evidence="FAISS was developed by Facebook AI Research (FAIR).",
)
