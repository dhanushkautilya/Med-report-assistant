# app/pipeline.py
import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

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

# ---- 2) LangChain LLM + prompt ------------------------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.1,
    api_key=OPENAI_API_KEY,  # pass the key explicitly
)

summary_prompt = ChatPromptTemplate.from_template(
    """
You are a clinical documentation assistant helping a physician review a medical report.

Task:
- Summarize the report clearly and concisely for a busy doctor.
- Include: presenting problem, key history, important findings, impressions/diagnoses if clearly stated, and any mentioned follow-up.
- Do NOT invent diagnoses or give treatment recommendations.
- Only restate information that appears in the report.

Medical report text:
```{report_text}```
"""
)

summary_chain = summary_prompt | llm | StrOutputParser()


# ---- 3) Graph state ------------------------------------------------------

class GraphState(TypedDict, total=False):
    report_text: str
    summary: str


# ---- 4) Node functions ---------------------------------------------------

def ingest_node(state: GraphState) -> GraphState:
    # In future we can normalize/clean here
    return state


def summarize_node(state: GraphState) -> GraphState:
    report_text = state.get("report_text", "") or ""
    if not report_text.strip():
        state["summary"] = "No text found in document."
        return state

    summary = summary_chain.invoke({"report_text": report_text})
    state["summary"] = summary
    return state


# ---- 5) Build & compile the LangGraph graph ------------------------------

def build_graph():
    g = StateGraph(GraphState)

    g.add_node("ingest", ingest_node)
    g.add_node("summarize", summarize_node)

    g.set_entry_point("ingest")
    g.add_edge("ingest", "summarize")
    g.set_finish_point("summarize")

    return g.compile()


graph_app = build_graph()


def summarize_report_text(report_text: str) -> str:
    initial_state: GraphState = {"report_text": report_text}
    final_state: GraphState = graph_app.invoke(initial_state)
    return final_state.get("summary", "No summary produced.")
