# app/pdf_utils.py
from typing import List
from pypdf import PdfReader
from io import BytesIO


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """
    Extract text from an in-memory PDF (e.g., uploaded via the web UI).

    Returns a single string with the text of all pages joined with blank lines.
    """
    reader = PdfReader(BytesIO(file_bytes))
    text_chunks: List[str] = []

    for page in reader.pages:
        page_text = page.extract_text() or ""
        text_chunks.append(page_text)

    full_text = "\n\n".join(text_chunks).strip()
    return full_text


# temp_extract.py (run this once, then delete)
from app.pdf_utils import extract_text_from_pdf_bytes
import os

# Assuming the PDF is in the project root; adjust path if needed
with open("acc_guidelines.pdf", "rb") as f:
    pdf_bytes = f.read()

extracted_text = extract_text_from_pdf_bytes(pdf_bytes)

# Overwrite guidelines.txt with the new text
guidelines_path = os.path.join("app", "guidelines.txt")
with open(guidelines_path, "w") as f:
    f.write(extracted_text)

print("Guidelines updated successfully!")