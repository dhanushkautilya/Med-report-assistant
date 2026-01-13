# app/pipeline.py
import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from langgraph.graph import StateGraph

# ---- 1) Load .env explicitly from project root ---------------------------

# This file is app/pipeline.py → project root is one level up.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOTENV_PATH = PROJECT_ROOT / ".env"

# Force-load that specific .env file
load_dotenv(dotenv_path=DOTENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        f"OPENAI_API_KEY is not set. Tried to load from: {DOTENV_PATH}\n"
        "Make sure you have a .env file in the project root with:\n"
        "OPENAI_API_KEY=sk-your-key-here"
    )

# ---- Load and process guidelines for RAG ---------------------------

embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

guidelines_path = PROJECT_ROOT / "app" / "guidelines.txt"
with open(guidelines_path, "r") as f:
    guidelines_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_text(guidelines_text)
documents = [Document(page_content=doc) for doc in docs]

vectorstore = FAISS.from_documents(documents, embeddings)

# ---- 2) LangChain LLM + prompt ------------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    api_key=OPENAI_API_KEY,  # pass the key explicitly
)

report_prompt = ChatPromptTemplate.from_template(
    """
You are a clinical documentation assistant helping a physician generate a comprehensive medical report from patient data.

Task:
- Generate a detailed medical report based on the provided report text.
- Incorporate relevant recommendations from the Retrieved Guidelines Context where applicable (e.g., for cardiovascular conditions like ACS). If the guidelines are not directly relevant, generate a standard clinical report.
- Include sections such as: Patient Presentation, History, Physical Exam, Diagnostic Findings, Impressions/Diagnoses, Treatment Plan, and Follow-up.
- Adhere to evidence-based practices from the retrieved context when possible.
- Do NOT invent information not present in the report text.
- Summarize and structure the provided text into a coherent medical report.

Retrieved Guidelines Context:
{retrieved_guidelines}

Medical report text:
{report_text}

Generated Report:
"""
)

report_chain = report_prompt | llm | StrOutputParser()


# ---- 3) Graph state ------------------------------------------------------

class GraphState(TypedDict, total=False):
    report_text: str
    retrieved_guidelines: str
    generated_report: str


# ---- 4) Node functions ---------------------------------------------------

def ingest_node(state: GraphState) -> GraphState:
    # In future we can normalize/clean here
    return state


def retrieve_node(state: GraphState) -> GraphState:
    report_text = state.get("report_text", "")
    if not report_text.strip():
        state["retrieved_guidelines"] = "No report text provided."
        return state

    # Retrieve relevant guidelines based on the report text
    docs = vectorstore.similarity_search(report_text, k=10)  # Increased from 5 to 10 for more context
    retrieved = "\n\n".join([doc.page_content for doc in docs])
    state["retrieved_guidelines"] = retrieved
    return state


def generate_report_node(state: GraphState) -> GraphState:
    report_text = state.get("report_text", "") or ""
    retrieved_guidelines = state.get("retrieved_guidelines", "")
    if not report_text.strip():
        state["generated_report"] = "No text found in document."
        return state

    generated_report = report_chain.invoke({"report_text": report_text, "retrieved_guidelines": retrieved_guidelines})
    # Include retrieved guidelines in the output for debugging
    state["generated_report"] = f"Retrieved Guidelines:\n{retrieved_guidelines}\n\nGenerated Report:\n{generated_report}"
    return state


# ---- 5) Build & compile the LangGraph graph ------------------------------

def build_graph():
    g = StateGraph(GraphState)

    g.add_node("ingest", ingest_node)
    g.add_node("retrieve", retrieve_node)
    g.add_node("generate_report", generate_report_node)

    g.set_entry_point("ingest")
    g.add_edge("ingest", "retrieve")
    g.add_edge("retrieve", "generate_report")
    g.set_finish_point("generate_report")

    return g.compile()


graph_app = build_graph()


def generate_report_text(report_text: str) -> str:
    initial_state: GraphState = {"report_text": report_text}
    final_state: GraphState = graph_app.invoke(initial_state)
    return final_state.get("generated_report", "No report generated.")
