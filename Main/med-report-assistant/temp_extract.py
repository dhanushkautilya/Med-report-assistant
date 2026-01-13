# temp_extract.py (run this once, then delete)
from app.pdf_utils import extract_text_from_pdf_bytes
import os

# PDF is in the project root with this name
pdf_path = "kumbhani-et-al-2025-2025-acute-coronary-syndromes-guideline-at-a-glance.pdf"
if not os.path.exists(pdf_path):
    print(f"PDF file '{pdf_path}' not found.")
    exit(1)

with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()

extracted_text = extract_text_from_pdf_bytes(pdf_bytes)

# Overwrite guidelines.txt with the new text
guidelines_path = os.path.join("app", "guidelines.txt")
with open(guidelines_path, "w") as f:
    f.write(extracted_text)

print("Guidelines updated successfully!")