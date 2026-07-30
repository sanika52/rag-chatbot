from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
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
                    "page_number": page["page_number"]
                })

        return chunks