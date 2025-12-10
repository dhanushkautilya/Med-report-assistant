# 🩺 Medical Report Summary Assistant  
### AI-powered clinical document analyzer using **LangChain**, **LangGraph**, **OpenAI**, and **Streamlit**

The **Medical Report Summary Assistant** is an intelligent, local web application that helps clinicians and researchers quickly understand long or complex medical documents.  
Upload a **PDF medical report** or **paste clinical text**, and the app generates a concise, physician-friendly summary that you can read instantly or download for later use.

Built with:
- **LangChain** → prompt orchestration & LLM pipeline  
- **LangGraph** → workflow graph for controlled multi-step processing  
- **Streamlit** → simple, clean web interface for upload & display  
- **OpenAI LLMs** → high-quality text summarization  

> ⚠️ *This tool does NOT provide medical advice, diagnosis, or treatment recommendations. It only restructures and summarizes existing text.*

---

## 🚀 Features

### 🔹 1. Intelligent Medical Summarization
- Extracts the key details from clinical reports:
  - Presenting problem  
  - Relevant history  
  - Important findings  
  - Mentioned diagnoses  
  - Follow-up items or next steps  

### 🔹 2. PDF Extraction
- Upload **any text-based PDF**
- Text is automatically extracted and passed to the AI engine

### 🔹 3. Simple, Local Web UI
- Built with Streamlit
- Upload a file or paste text
- Click one button → Get summary
- Download output as a `.txt`

### 🔹 4. LangChain + LangGraph Pipeline
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
    - `ingest` → loads text
    - `summarize` → calls LangChain summarizer chain  

- **LangChain Prompt + Model**
  - GPT-4.1-mini (or any LLM you configure)
  - Clinical-safe summarization prompt

- **PDF Utilities (`pdf_utils.py`)**
  - Extracts text from PDF uploads

The graph design makes future multi-step processing easy.



## 🛠️ Installation & Setup

 1️⃣ Clone the repository
```bash
git clone https://github.com/<dhanushkautilya>/med-report-assistant.git
cd med-report-assistant
cd Main
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


Upload a document → generate summary → download result.