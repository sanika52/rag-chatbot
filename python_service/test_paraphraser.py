from services.paraphraser import ParaphraserService


paraphraser = ParaphraserService()


# ============================================================
# TEST 1
# Parentheses containing a full form
# ============================================================

question = "What is the full form of FAISS?"

context = """
FAISS (Facebook AI Similarity Search) is a library
for efficient similarity search and clustering of dense vectors.

It was developed by Facebook AI Research (FAIR).

FAIR is part of Meta.

Meta was founded in 2004.
"""

print("\n========================================")
print("TEST 1: FAISS FULL FORM")
print("========================================")

print("\nQUESTION:")
print(question)

print("\nORIGINAL CONTEXT:")
print(context)

result = paraphraser.paraphrase_for_question(
    question=question,
    context=context
)

print("\nTRANSFORMED EVIDENCE:")
print(result)


# ============================================================
# TEST 2
# Parentheses containing a full form of FAIR
# ============================================================

question = "What is the full form of FAIR?"

context = """
FAISS was developed by Facebook AI Research (FAIR).

Facebook AI Research (FAIR) is an artificial intelligence
research organization.

FAIR is part of Meta.

Meta was founded in 2004.
"""

print("\n========================================")
print("TEST 2: FAIR FULL FORM")
print("========================================")

print("\nQUESTION:")
print(question)

print("\nORIGINAL CONTEXT:")
print(context)

result = paraphraser.paraphrase_for_question(
    question=question,
    context=context
)

print("\nTRANSFORMED EVIDENCE:")
print(result)


# ============================================================
# TEST 3
# Multi-hop implicit information
# ============================================================

question = """
When was the company associated with the organization
that developed FAISS founded?
"""

context = """
FAISS was developed by Facebook AI Research (FAIR).

FAIR is part of Meta.

Meta is a technology company.

Meta was founded in 2004.
"""

print("\n========================================")
print("TEST 3: MULTI-HOP RELATIONSHIP")
print("========================================")

print("\nQUESTION:")
print(question)

print("\nORIGINAL CONTEXT:")
print(context)

result = paraphraser.paraphrase_for_question(
    question=question,
    context=context
)

print("\nTRANSFORMED EVIDENCE:")
print(result)