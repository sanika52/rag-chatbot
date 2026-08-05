from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import Settings

class TextChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=Settings.CHUNK_SIZE,
            chunk_overlap=Settings.CHUNK_OVERLAP,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def split(self, pages):

        chunks = []

        for page in pages:

            page_chunks = self.splitter.split_text(
                page["text"]
            )

            for chunk in page_chunks:

                chunks.append({
                     "text": chunk,
                     "page_number": page.get("page_number") or 1
                })                 

        return chunks