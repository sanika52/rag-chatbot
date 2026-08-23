from services.embeddings import EmbeddingService
from services.chroma_service import ChromaService
from services.reranker import RerankerService
from services.qa import QAService
from services.answer_validator import AnswerValidator
from services.sentence_extractor import SentenceExtractor
from services.paraphraser import ParaphraserService
from config.settings import Settings


class RAGService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        chroma_service: ChromaService,
        reranker_service: RerankerService,
        qa_service: QAService,
        paraphraser_service: ParaphraserService,
    ):

        self.embedding_service = embedding_service
        self.chroma_service = chroma_service
        self.reranker_service = reranker_service
        self.qa_service = qa_service
        self.paraphraser_service = paraphraser_service

        self.answer_validator = AnswerValidator()
        self.sentence_extractor = SentenceExtractor()

    # ==================================================
    # Answer question
    # ==================================================

    def answer_question(
        self,
        question: str,
        user_id: int,
        document_ids: list[int],
        top_k: int = Settings.TOP_K,
    ):

        # ==================================================
        # Step 0: Validate documents
        # ==================================================

        if not document_ids:

            return {
                "answer": (
                    "Please select at least one document " "before asking a question."
                ),
                "sources": [],
            }

        # ==================================================
        # Step 1: Embed question
        # ==================================================

        query_embedding = self.embedding_service.embed_query(question)

        # ==================================================
        # Step 2: Initial vector retrieval
        # ==================================================

        retrieved_chunks = self.chroma_service.search(
            query_embedding=query_embedding,
            user_id=user_id,
            document_ids=document_ids,
            top_k=top_k,
        )

        if not retrieved_chunks:

            return {
                "answer": (
                    "I couldn't find any relevant information "
                    "in the selected documents."
                ),
                "sources": [],
            }

        # ==================================================
        # DEBUG: Initial retrieval
        # ==================================================

        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)

        print(f"\nInitial retrieval returned " f"{len(retrieved_chunks)} chunks:\n")

        for i, chunk in enumerate(retrieved_chunks, start=1):

            metadata = chunk["metadata"]

            print(f"--- Retrieved Chunk {i} ---")

            print(f"Distance: {chunk.get('distance')}")

            print(f"Document: {metadata.get('filename')}")

            print(f"Page: {metadata.get('page_number')}")

            print(f"Chunk index: {metadata.get('chunk_index')}")

            print("Text:")
            print(chunk["text"])

            print("-" * 80)

        # ==================================================
        # Step 3: BGE rerank chunks
        # ==================================================

        reranked_chunks = self.reranker_service.rerank(
            question=question,
            chunks=retrieved_chunks,
            top_k=Settings.RERANK_TOP_K,
        )

        if not reranked_chunks:

            return {
                "answer": (
                    "I couldn't find any relevant information "
                    "in the selected documents."
                ),
                "sources": [],
            }

        # ==================================================
        # DEBUG: Reranked chunks
        # ==================================================

        print("\n" + "=" * 80)
        print("AFTER BGE CHUNK RERANKING")
        print("=" * 80)

        print(f"\nReranker selected " f"{len(reranked_chunks)} chunks:\n")

        for i, chunk in enumerate(reranked_chunks, start=1):

            metadata = chunk["metadata"]

            print(f"--- Reranked Chunk {i} ---")

            print(f"Rerank score: " f"{chunk.get('rerank_score')}")

            print(f"Original distance: " f"{chunk.get('distance')}")

            print(f"Document: " f"{metadata.get('filename')}")

            print(f"Page: " f"{metadata.get('page_number')}")

            print(f"Chunk index: " f"{metadata.get('chunk_index')}")

            print("Text:")
            print(chunk["text"])

            print("-" * 80)

        # ==================================================
        # Step 4: Select best reranked chunk
        #
        # NO neighbour expansion.
        #
        # The highest BGE chunk score determines
        # which chunk we inspect.
        # ==================================================

        best_chunk = max(
            reranked_chunks,
            key=lambda chunk: chunk.get(
                "rerank_score",
                float("-inf"),
            ),
        )

        best_metadata = best_chunk["metadata"]

        print("\n" + "=" * 80)
        print("BEST RERANKED CHUNK")
        print("=" * 80)

        print(f"Rerank score: " f"{best_chunk.get('rerank_score')}")

        print(f"Document: " f"{best_metadata.get('filename')}")

        print(f"Page: " f"{best_metadata.get('page_number')}")

        print(f"Chunk index: " f"{best_metadata.get('chunk_index')}")

        print("Text:")
        print(best_chunk["text"])

        # ==================================================
        # Step 5: Extract sentences from best chunk
        # ==================================================

        sentences = self.sentence_extractor.extract_sentences(best_chunk["text"])

        if not sentences:

            return {
                "answer": (
                    "I couldn't find that information " "in the uploaded documents."
                ),
                "sources": [],
            }

        print("\n" + "=" * 80)
        print("SENTENCES FROM BEST CHUNK")
        print("=" * 80)

        for i, sentence in enumerate(sentences, start=1):

            print(f"\nSentence {i}:")
            print(sentence)

        # ==================================================
        # Step 6: BGE rerank EACH sentence
        #
        # This is the important change.
        #
        # Instead of sending the entire chunk to QA,
        # we find the sentence most relevant to the
        # user's question.
        # ==================================================

        sentence_results = self.reranker_service.score_sentences(
            question=question,
            sentences=sentences,
        )

        if not sentence_results:

            return {
                "answer": (
                    "I couldn't find that information " "in the uploaded documents."
                ),
                "sources": [],
            }

        # ==================================================
        # DEBUG: Sentence reranking
        # ==================================================

        print("\n" + "=" * 80)
        print("BGE SENTENCE RERANKING")
        print("=" * 80)

        for i, result in enumerate(
            sentence_results,
            start=1,
        ):

            print(f"\n--- Sentence Candidate {i} ---")

            print(f"Sentence rerank score: " f"{result.get('rerank_score')}")

            print(f"Sentence:\n" f"{result.get('text')}")

        # ==================================================
        # Step 7: Select most relevant sentence
        # ==================================================

        best_sentence_result = sentence_results[0]

        supporting_sentence = best_sentence_result["text"].strip()

        sentence_rerank_score = float(
            best_sentence_result.get(
                "rerank_score",
                0.0,
            )
        )

        print("\n" + "=" * 80)
        print("BEST SUPPORTING SENTENCE")
        print("=" * 80)

        print(f"Sentence rerank score: " f"{sentence_rerank_score}")

        print(f"Supporting sentence:\n" f"{supporting_sentence}")

        # ==================================================
        # Step 8: Run extractive QA ONLY on the
        # supporting sentence
        # ==================================================

        print("\n" + "=" * 80)
        print("RUNNING EXTRACTIVE QA")
        print("=" * 80)

        print("\nQA Context:")
        print(supporting_sentence)

        qa_result = self.qa_service.answer_question(
            question=question,
            context=supporting_sentence,
        )

        answer = qa_result.get("answer")

        qa_score = float(qa_result.get("score", 0.0))

        print(f"\nQA Answer: " f"{answer}")

        print(f"QA Score: " f"{qa_score}")

        # ==================================================
        # Step 9: Validate extracted answer
        #
        # The answer must be supported by the SAME
        # sentence that was selected by BGE.
        # ==================================================

        answer_supported = self.answer_validator.validate(
            question=question,
            answer=answer,
            context=supporting_sentence,
        )

        print("\n" + "=" * 80)
        print("ANSWER VALIDATION")
        print("=" * 80)

        print(f"QA Answer: " f"{answer}")

        print(f"QA Score: " f"{qa_score}")

        print(f"Answer supported by context: " f"{answer_supported}")

        # ==================================================
        # Step 10: Final answerability check
        #
        # IMPORTANT:
        # We are NOT using QA score as a ranking signal.
        #
        # QA score is only used as an optional confidence
        # check if Settings.QA_MIN_SCORE exists.
        #
        # The main retrieval decision has already been made
        # by BGE.
        # ==================================================

        if answer is None or not answer.strip() or not answer_supported:

            answer = "I couldn't find that information " "in the uploaded documents."

            answer_is_valid = False

        else:

            answer_is_valid = True

        # ==================================================
        # Step 11: Paraphrase the SUPPORTING SENTENCE
        #
        # We paraphrase the evidence sentence rather than
        # the raw QA span.
        #
        # This prevents outputs such as:
        #
        # "Meta"
        #
        # becoming awkward answers.
        #
        # Example:
        #
        # Question:
        # Does FAIR belong to Meta?
        #
        # Supporting sentence:
        # FAIR is part of Meta.
        #
        # Paraphrased answer:
        # FAIR is part of Meta.
        # ==================================================

        final_answer = answer

        if answer_is_valid:

            print("\n" + "=" * 80)
            print("RUNNING PARAPHRASER")
            print("=" * 80)

            print(f"\nOriginal supporting sentence:\n" f"{supporting_sentence}")

            try:

                paraphrased = self.paraphraser_service.paraphrase(supporting_sentence)

                if paraphrased and paraphrased.strip():

                    final_answer = paraphrased.strip()

                else:

                    final_answer = supporting_sentence

            except Exception as e:

                print("\nParaphraser error:")

                print(e)

                # Safe fallback:
                # use the original supporting sentence.
                final_answer = supporting_sentence

            print(f"\nFinal answer:\n" f"{final_answer}")

        # ==================================================
        # Step 12: Build sources
        #
        # We cite the document/page containing the
        # supporting sentence.
        # ==================================================

        grouped_sources = {}

        metadata = best_chunk["metadata"]

        document_id = metadata["document_id"]

        grouped_sources[document_id] = {
            "document_id": document_id,
            "filename": metadata["filename"],
            "stored_filename": metadata["stored_filename"],
            "pages": set(),
        }

        page = metadata.get("page_number")

        if page is not None:

            grouped_sources[document_id]["pages"].add(page)

        # ==================================================
        # Step 13: Format sources
        # ==================================================

        sources = []

        for source in grouped_sources.values():

            sources.append(
                {
                    "document_id": source["document_id"],
                    "filename": source["filename"],
                    "stored_filename": source["stored_filename"],
                    "pages": sorted(source["pages"]),
                }
            )

        # ==================================================
        # Step 14: Return result
        # ==================================================

        return {
            "answer": final_answer,
            "sources": sources,
        }
