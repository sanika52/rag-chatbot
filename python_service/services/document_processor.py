from pathlib import Path
from pypdf import PdfReader
from docx import Document


class DocumentProcessor:

    @staticmethod
    def extract_text(file_path: str):
        """
        Extract text from PDF, DOCX or TXT files.

        Returns:
        [
            {
                "page_number": 1,
                "text": "..."
            }
        ]
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = path.suffix.lower()

        if extension == ".pdf":
            return DocumentProcessor._extract_pdf(path)

        elif extension == ".docx":
            return DocumentProcessor._extract_docx(path)

        elif extension == ".txt":
            return DocumentProcessor._extract_txt(path)

        else:
            raise ValueError(f"Unsupported file type: {extension}")

    @staticmethod
    def _extract_pdf(path: Path):

        reader = PdfReader(path)

        pages = []

        for page_number, page in enumerate(reader.pages, start=1):

            page_text = page.extract_text()

            if page_text and page_text.strip():

                pages.append({
                    "page_number": page_number,
                    "text": page_text
                })

        return pages

    @staticmethod
    def _extract_docx(path: Path):

        document = Document(path)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        )

        return [
            {
                "page_number": 1,
                "text": text
            }
        ]

    @staticmethod
    def _extract_txt(path: Path):

        with open(path, "r", encoding="utf-8") as file:
            text = file.read()

        return [
            {
                "page_number": 1,
                "text": text
            }
        ]