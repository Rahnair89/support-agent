import os
import time

import boto3
import requests
from strands.telemetry import StrandsTelemetry
StrandsTelemetry().setup_otlp_exporter()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.graph import flow

app = FastAPI(title="support-agent")
secrets = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))


class ChatIn(BaseModel):
    message: str


class TicketIn(BaseModel):
    message: str
    answer: str = ""
    sources: list[str] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(body: ChatIn):
    started = time.time()
    s = flow.invoke({"message": body.message})
    return {
        "answer": s.get("answer", "This needs a human. Use /ticket to escalate."),
        "category": s.get("category"),
        "sources": [d["source"] for d in s.get("docs", [])],
        "escalate": s.get("escalate", False),
        "latency_ms": int((time.time() - started) * 1000),
    }


@app.post("/ticket")
def ticket(body: TicketIn):
    token = secrets.get_secret_value(SecretId=os.environ["GITHUB_TOKEN_SECRET"])["SecretString"]
    issue_body = (f"**Customer question**\n{body.message}\n\n**Bot answer**\n{body.answer}\n\n"
                  "**Sources**\n" + "\n".join(f"- {src}" for src in body.sources))
    resp = requests.post(
        f"https://api.github.com/repos/{os.environ['TICKET_REPO']}/issues",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        json={"title": f"[support] {body.message[:60]}", "body": issue_body},
        timeout=15,
    )
    if resp.status_code >= 300:
        raise HTTPException(status_code=502, detail=resp.text)
    return {"issue_url": resp.json()["html_url"]}
