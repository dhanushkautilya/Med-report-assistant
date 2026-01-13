# ui.py
import streamlit as st

from app.pdf_utils import extract_text_from_pdf_bytes
from app.pipeline import generate_report_text


st.set_page_config(page_title="Medical Report Summary Assistant", layout="centered")

st.title("🩺 Medical Report Generation Assistant")
st.caption(
    "Upload a medical report or patient summary and generate a comprehensive report following ACC/AHA guidelines. "
    "This tool is for information organization only and does not provide medical advice."
)

st.markdown("### 1. Upload a document or paste text")

uploaded_file = st.file_uploader(
    "Upload a medical report (PDF). You can also paste text in the box below.",
    type=["pdf"],
)

text_input = st.text_area(
    "Or paste report text here:",
    height=200,
    placeholder="Paste clinical note, discharge summary, or radiology report text...",
)

summarize_button = st.button("⚙️ Generate Report")

summary_result = None

if summarize_button:
    if uploaded_file is None and not text_input.strip():
        st.error("Please upload a PDF or paste some text.")
    else:
        with st.spinner("Generating report..."):
            # Prefer PDF if provided; otherwise use text input
            if uploaded_file is not None:
                try:
                    file_bytes = uploaded_file.read()
                    report_text = extract_text_from_pdf_bytes(file_bytes)
                    if not report_text.strip():
                        st.warning("Could not extract text from the PDF. "
                                   "Try uploading a text-based PDF or paste the text manually.")
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
                    report_text = ""
            else:
                report_text = text_input

            if report_text.strip():
                summary_result = generate_report_text(report_text)
            else:
                summary_result = "No usable text found in the provided input."

if summary_result:
    st.markdown("### 2. Generated Report")
    st.write(summary_result)

    st.markdown("### 3. Download report")
    st.download_button(
        label="💾 Download as .txt",
        data=summary_result,
        file_name="medical_report.txt",
        mime="text/plain",
    )

st.markdown("---")
st.caption(
    "⚠️ This tool is for assisting clinicians in organizing information. "
    "It does not provide medical advice, diagnosis, or treatment recommendations. "
    "Always rely on professional judgment and local guidelines."
)
