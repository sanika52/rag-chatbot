from services.reranker import RerankerService
from services.sentence_extractor import SentenceExtractor


def test_case(reranker, question, context):
    print("\n" + "=" * 80)
    print("QUESTION:")
    print(question)

    print("\nCONTEXT:")
    print(context)

    # --------------------------------------------------
    # Step 1: Split context into sentences
    # --------------------------------------------------

    sentences = SentenceExtractor.split_sentences(context)

    print("\n" + "-" * 80)
    print("SENTENCES")
    print("-" * 80)

    for i, sentence in enumerate(sentences, start=1):
        print(f"{i}. {sentence}")

    # --------------------------------------------------
    # Step 2: BGE rerank each sentence
    # --------------------------------------------------

    ranked_sentences = reranker.score_sentences(question=question, sentences=sentences)

    print("\n" + "-" * 80)
    print("BGE SENTENCE RANKING")
    print("-" * 80)

    for i, item in enumerate(ranked_sentences, start=1):
        print(f"{i}. " f"Score: {item['rerank_score']:.6f}")

        print(f"   {item['text']}")

    # --------------------------------------------------
    # Step 3: Best sentence
    # --------------------------------------------------

    if ranked_sentences:

        best_sentence = ranked_sentences[0]

        print("\n" + "=" * 80)
        print("BEST SENTENCE")
        print("=" * 80)

        print(f"Score: " f"{best_sentence['rerank_score']:.6f}")

        print(f"Text: " f"{best_sentence['text']}")

    else:

        print("\nNo sentences were ranked.")

    print("=" * 80)


# ======================================================
# Load BGE reranker
# ======================================================

print("Loading BGE reranker...")

reranker = RerankerService()

print("BGE reranker loaded successfully!")


# ======================================================
# TEST 1
# ======================================================

test_case(
    reranker=reranker,
    question="What does FAIR stand for?",
    context="""
FAIR (Facebook AI Research) is an artificial intelligence research organization.

FAIR is part of Meta.

Meta is a technology company.

Meta was founded in 2004.
""",
)


# ======================================================
# TEST 2
# ======================================================

test_case(
    reranker=reranker,
    question="Does FAIR belong to Meta?",
    context="""
FAIR (Facebook AI Research) is an artificial intelligence research organization.

FAIR is part of Meta.

Meta is a technology company.

Meta was founded in 2004.
""",
)


# ======================================================
# TEST 3
# ======================================================

test_case(
    reranker=reranker,
    question="When was Meta founded?",
    context="""
FAIR (Facebook AI Research) is an artificial intelligence research organization.

FAIR is part of Meta.

Meta is a technology company.

Meta was founded in 2004.
""",
)


# ======================================================
# TEST 4
# ======================================================

test_case(
    reranker=reranker,
    question="Which company develops Milvus?",
    context="""
Milvus is an open-source vector database designed for storing, indexing, and searching large collections of vector embeddings.

Milvus is developed by Zilliz.

Zilliz is a company that develops and maintains Milvus.

The Apache License 2.0 is a permissive open-source software license.
""",
)


# ======================================================
# TEST 5
# ======================================================

test_case(
    reranker=reranker,
    question="Who founded Zilliz?",
    context="""
Milvus is developed by Zilliz.

Zilliz is a company that develops and maintains Milvus.

The Apache License 2.0 is a permissive open-source software license.

Software released under the Apache License 2.0 can be used, modified, and distributed subject to the license terms.
""",
)


# ======================================================
# TEST 6 - NEGATIVE TEST
# ======================================================

test_case(
    reranker=reranker,
    question="What is the capital of France?",
    context="""
FAIR (Facebook AI Research) is an artificial intelligence research organization.

FAIR is part of Meta.

Meta was founded in 2004.

The city of Pune is located in the Indian state of Maharashtra.
""",
)
