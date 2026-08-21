class Settings:

    # Retrieval
    TOP_K = 8
    # None = disable similarity filtering
    SIMILARITY_THRESHOLD = None

    # LLM
    MAX_CONTEXT_CHUNKS = 5

    # Chunking
    CHUNK_SIZE = 300  # Originally 1000
    CHUNK_OVERLAP = 50 # Originally 200