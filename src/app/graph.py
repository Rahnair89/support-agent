import os
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from opentelemetry import trace
from strands import Agent
from strands.models import BedrockModel

from app.prompts import load_prompt
from rag.common import CFG
from rag.search import hybrid_search

tracer = trace.get_tracer("support-agent")


class State(TypedDict, total=False):
    message: str
    category: str
    docs: list
    answer: str
    escalate: bool


def llm(prompt_name: str) -> Agent:
    return Agent(model=BedrockModel(model_id=os.environ["MODEL_ID"]),
                 system_prompt=load_prompt(prompt_name), callback_handler=None)


def triage(s: State) -> State:
    return {"category": str(llm("triage")(s["message"])).strip().lower()}


def retrieve(s: State) -> State:
    with tracer.start_as_current_span("retrieve") as span:
        docs = hybrid_search(s["message"], CFG)
        span.set_attribute("rag.chunks.retrieved", len(docs))
        span.set_attribute("rag.top_score", docs[0]["score"] if docs else 0.0)
        span.set_attribute("prompt.version", os.environ.get("PROMPT_VERSION", "v1"))
        return {"docs": docs}


def respond(s: State) -> State:
    context = "\n\n".join(f"[{d['source']}]\n{d['text']}" for d in s.get("docs", []))
    prompt = f"Context:\n{context}\n\nCustomer question: {s['message']}"
    return {"answer": str(llm("respond")(prompt))}


def escalate(s: State) -> State:
    docs = s.get("docs", [])
    weak_retrieval = not docs or docs[0]["score"] < CFG["min_rerank_score"]
    needs_human = s.get("category") == "urgent" or "ESCALATE" in s.get("answer", "")
    return {"escalate": weak_retrieval or needs_human}


def route_after_triage(s: State) -> str:
    return "escalate" if s.get("category") == "urgent" else "retrieve"


builder = StateGraph(State)
builder.add_node("triage", triage)
builder.add_node("retrieve", retrieve)
builder.add_node("respond", respond)
builder.add_node("escalate", escalate)
builder.add_edge(START, "triage")
builder.add_conditional_edges("triage", route_after_triage)
builder.add_edge("retrieve", "respond")
builder.add_edge("respond", "escalate")
builder.add_edge("escalate", END)
flow = builder.compile()
