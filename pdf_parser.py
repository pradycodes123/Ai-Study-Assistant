import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    if not os.path.isfile(pdf_path):
        raise ValueError("Invalid file path")

    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Not a PDF file")

    pages = []
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text)

    return "\n".join(pages)
