import os
import yaml
from aws_embedded_metrics import metric_scope
PRICING = yaml.safe_load(open("config/pricing.yaml"))
def cost_usd(tokens_in: int, tokens_out: int) -> float:
 return (tokens_in * PRICING["input_per_million"]
 + tokens_out * PRICING["output_per_million"]) / 1_000_000
@metric_scope
def record_conversation(latency_ms, tokens_in, tokens_out, chunks, escalated, metrics):
 metrics.set_namespace("SupportAgent")
 metrics.set_dimensions({"Service": "support-agent"})
 metrics.put_metric("llm.latency", latency_ms, "Milliseconds")
 metrics.put_metric("llm.tokens.total", tokens_in + tokens_out, "Count")
 metrics.put_metric("rag.chunks.retrieved", chunks, "Count")
 metrics.put_metric("conversation.escalated", 1 if escalated else 0, "Count")
 metrics.put_metric("llm.cost.usd", cost_usd(tokens_in, tokens_out), "None")
 metrics.put_metric("conversations", 1, "Count")
 metrics.set_property("prompt_version", os.environ.get("PROMPT_VERSION", "v1"))