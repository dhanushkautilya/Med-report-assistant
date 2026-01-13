# 🩺 Medical Report Assistant  
### AI-powered clinical report generator using **LangChain**, **LangGraph**, **OpenAI**, and **Streamlit** with RAG for guideline integration

The **Medical Report Assistant** is an intelligent, local web application that helps clinicians generate comprehensive, guideline-compliant medical reports from patient data.  
Upload a **PDF medical report** or **paste clinical text**, and the app generates a structured report incorporating relevant medical guidelines via RAG (Retrieval-Augmented Generation).

Built with:
- **LangChain** → prompt orchestration & LLM pipeline  
- **LangGraph** → workflow graph for controlled multi-step processing  
- **FAISS** → vector search for guideline retrieval
- **Streamlit** → simple, clean web interface for upload & display  
- **OpenAI LLMs** → high-quality text generation  

> ⚠️ *This tool does NOT provide medical advice, diagnosis, or treatment recommendations. It only restructures and summarizes existing text with guideline references.*

---

## 🚀 Features

### 🔹 1. Intelligent Medical Report Generation
- Generates detailed, structured reports from clinical text:
  - Patient Presentation  
  - History  
  - Physical Exam  
  - Diagnostic Findings  
  - Impressions/Diagnoses  
  - Treatment Plan  
  - Follow-up  

### 🔹 2. PDF Extraction
- Upload **any text-based PDF**
- Text is automatically extracted and passed to the AI engine

### 🔹 3. RAG (Retrieval-Augmented Generation) with Medical Guidelines
- **Guideline Extraction**: Extracts and embeds text from medical guideline PDFs (e.g., ACC/AHA ACS guidelines) using PyPDF and OpenAI embeddings.
- **Smart Retrieval**: Uses FAISS vector search to retrieve relevant guideline sections based on the input report.
- **Guideline Incorporation**: Incorporates evidence-based recommendations into generated reports (e.g., antiplatelets for ACS).
- **Difference**: With RAG, reports are guideline-compliant and precise; without, they are generic summaries.

### 🔹 4. Simple, Local Web UI
- Built with Streamlit
- Upload a file or paste text
- Click one button → Get report
- Download output as a `.txt`
- Debug view shows retrieved guidelines

### 🔹 5. LangChain + LangGraph Pipeline
- Modular graph-based architecture  
- Easy to extend with additional nodes:
  - Medication extraction  
  - Allergies  
  - Problems list  
  - Clinical checklists  

---

## 🏗️ Architecture Overview


### Components:
- **Streamlit (`ui.py`)**
  - Handles file upload, text input, display, download

- **LangGraph Workflow (`pipeline.py`)**
  - 2-node graph:
    - `retrieve` → searches FAISS for relevant guidelines
    - `generate` → calls LangChain generation chain with retrieved guidelines  

- **LangChain Prompt + Model**
  - GPT-4o-mini (or any LLM you configure)
  - Guideline-aware report generation prompt

- **PDF Utilities (`pdf_utils.py`)**
  - Extracts text from PDF uploads and guidelines

- **Guidelines (`guidelines.txt`)**
  - Embedded medical guidelines for RAG retrieval

The graph design makes future multi-step processing easy.



## 🛠️ Installation & Setup
```bash
 1️⃣ Clone the repository
git clone https://github.com/<dhanushkautilya>/med-report-assistant.git
cd Main
cd med-report-assistant
2️⃣ Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add your OpenAI API key

Create .env in project root:

OPENAI_API_KEY="sk-..."

5️⃣ Run app
streamlit run ui.py


Your browser will open at:

http://localhost:8501


Upload a document → generate guideline-compliant report → download result.