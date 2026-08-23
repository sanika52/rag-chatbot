from services.qa import QAService

print("=" * 80)
print("DIRECT EXTRACTIVE QA TEST")
print("=" * 80)

# Load the exact QA model we are currently using
qa_service = QAService()


# --------------------------------------------------
# TEST 1 — Exact answer in context
# --------------------------------------------------

question = "What is the full form of FAIR?"

context = """
FAIR (Facebook AI Research) is an artificial intelligence
research organization.

FAIR is part of Meta.

Meta is a technology company.

Meta was founded in 2004.
"""

print("\n" + "=" * 80)
print("TEST 1")
print("=" * 80)

print("\nQUESTION:")
print(question)

print("\nCONTEXT:")
print(context)

result = qa_service.answer_question(question=question, context=context)

print("\nANSWER:")
print(result["answer"])

print("\nSCORE:")
print(result["score"])


# --------------------------------------------------
# TEST 2 — Same information, slightly different question
# --------------------------------------------------

question = "What does FAIR stand for?"

print("\n" + "=" * 80)
print("TEST 2")
print("=" * 80)

print("\nQUESTION:")
print(question)

result = qa_service.answer_question(question=question, context=context)

print("\nANSWER:")
print(result["answer"])

print("\nSCORE:")
print(result["score"])


# --------------------------------------------------
# TEST 3 — Question whose answer is NOT present
# --------------------------------------------------

question = "What is the capital of France?"

print("\n" + "=" * 80)
print("TEST 3")
print("=" * 80)

print("\nQUESTION:")
print(question)

result = qa_service.answer_question(question=question, context=context)

print("\nANSWER:")
print(result["answer"])

print("\nSCORE:")
print(result["score"])
