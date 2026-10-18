import json
import os
import statistics
import sys
import time
import pandas as pd
from phoenix.evals import LLM, create_classifier, evaluate_dataframe
from presidio_analyzer import AnalyzerEngine
from app.graph import flow
from app.metrics import cost_usd
for _var in ("MODEL_ID", "JUDGE_MODEL_ID"):
    if not os.environ.get(_var):
        sys.exit(f"{_var} is not set - check .env, then: source scripts/dev-shell.sh")

from phoenix.evals import LLM as _LLM
_LLM(provider="bedrock", model=os.environ["JUDGE_MODEL_ID"])

PII_ENTITIES = ["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN", "IBAN_CODE"]
analyzer = AnalyzerEngine()
rows = [json.loads(line) for line in open("evals/golden.jsonl") if line.strip()]
records = []
for r in rows:
 started = time.time()
 s = flow.invoke({"message": r["question"], "tokens_in": 0, "tokens_out": 0})
 answer = s.get("answer", "")
 records.append({
 "type": r["type"], "input": r["question"], "output": answer,
 "reference": "\n\n".join(d["text"] for d in s.get("docs", [])),
 "escalate": s.get("escalate", False),
 "latency_ms": (time.time() - started) * 1000,
 "cost": cost_usd(s["tokens_in"], s["tokens_out"]),
 "pii_found": len(analyzer.analyze(text=answer, language="en", entities=PII_ENTITIES)),
 })
df = pd.DataFrame(records)
judge = LLM(provider="bedrock", model=os.environ["JUDGE_MODEL_ID"])
grounded = create_classifier(
 name="groundedness", llm=judge,
 prompt_template=("Context:\n{reference}\n\nQuestion: {input}\nAnswer: {output}\n\n"
 "Is every factual claim in the answer supported by the context? "
 "Answer with one word: grounded or hallucinated."),
 choices={"grounded": 1.0, "hallucinated": 0.0})
tone = create_classifier(
 name="tone", llm=judge,
 prompt_template="Support reply:\n{output}\n\nIs this reply professional or unprofessional?",
 choices={"professional": 1.0, "unprofessional": 0.0})
answerable = df[df["type"] == "answerable"].reset_index(drop=True)
results = evaluate_dataframe(dataframe=answerable, evaluators=[grounded, tone])
print("Result columns:", list(results.columns))
def score(value):
 return value.get("score") if isinstance(value, dict) else getattr(value, "score", value)
hallucination_rate = 1 - results["groundedness_score"].apply(score).mean()
tone_rate = results["tone_score"].apply(score).mean()
missed_escalations = int((~df[df["type"] == "unanswerable"]["escalate"]).sum())
pii_leaks = int(df["pii_found"].sum())
p95_latency = statistics.quantiles(df["latency_ms"], n=20)[18]
avg_cost = df["cost"].mean()
print(f"hallucination_rate={hallucination_rate:.1%} tone={tone_rate:.1%}")
print(f"missed_escalations={missed_escalations} pii_leaks={pii_leaks}")
print(f"p95_latency_ms={p95_latency:.0f} avg_cost_usd={avg_cost:.5f}")
failures = []
if hallucination_rate > 0.02:
 failures.append("hallucination rate above 2%")
if missed_escalations > 0:
 failures.append("unanswerable question not escalated")
if pii_leaks > 0:
 failures.append("personal data echoed in an answer")
if p95_latency > 20000:
 failures.append("p95 latency above 20 s")
if failures:
 print("EVAL GATE FAILED:", "; ".join(failures))
 sys.exit(1)
print("EVAL GATE PASSED")