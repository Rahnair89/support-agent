## Day 0 — 2026-09-18: first Strands agent on Bedrock

## Day 1 — 2026-09-23
- Built: FastAPI app, Docker image for linux/amd64, pushed to ECR
- Blocked: platform mismatch warning, then connection refused
- Unblocked by: rebuilt with --platform linux/amd64; kept the container tab open
- Tomorrow: Terraform VPC, NAT and endpoints

## Day 2 — 2026-09-26
- Built: VPC, public and private subnets, NAT gateway, 5 interface endpoints, S3 gateway endpoint, all in Terraform
- Blocked: PDF heading pasted into variables.tf; SSO session expired; missing region on a CLI call; terraform run from the repo root wrote an empty state file; unterminated quote broke dev-shell.sh
- Unblocked by: reading the file and line each error named; bash -n before sourcing; checking NAT gateways directly instead of trusting "destroy complete"
- Tomorrow: ALB, ECS service, ADR-001 and ADR-002

## Day 4 (part 2) — 2026-10-04
- Built: fixed and validated Thursday's full stack — hybrid RAG ingest and search,
  LangGraph triage/retrieve/respond/escalate flow, versioned prompts, /chat and
  /ticket endpoints, Qdrant sidecar and Secrets Manager wiring in Terraform.
- Blocked (five separate failures):
  1. PDF page footer was copied into scripts/download_models.py, breaking the
     Docker build at the model-download step.
  2. infra/ecs.tf lost a closing brace and infra/iam.tf had a stray "z" (zdata)
     plus a statement block nested inside a resources list.
  3. terraform apply failed on a data block because the Secrets Manager secret
     support-agent/github-token had never been created.
  4. read -s captured nothing, so create-secret failed with SecretString length 0.
  5. terraform destroy run from the repo root reported "0 destroyed" while
     examining no configuration at all. Second time this has happened.
- Unblocked by: rewriting files with cat > file <<'EOF' to preserve content
  exactly; running compileall, terraform fmt and terraform validate before any
  apply; verifying AWS state with describe-nat-gateways / describe-load-balancers
  / list-clusters rather than trusting a destroy message.
- Confirmed: nothing left running in AWS (all three checks returned []).
- Tomorrow: finish Thursday — deploy.sh, terraform -chdir=infra apply, confirm
  "Ingested N chunks" in the app log stream, test /chat and /ticket through the
  ALB, then Friday's prompt comparison, tracing and demo.

## Day 5 — 2026-10-06
- Prompt comparison: v2 adds a required structure (one-sentence cause, numbered
  steps, "Escalate if" line) and a 200-word cap.
- Result: escalation count unchanged at 3/10, sources identical, total output
  dropped from X to Y words.
- Shipping v2: same safety behaviour, answers a customer can act on without
  re-reading, and fewer output tokens per conversation.

## Day 5 — 2026-10-06 (Week 1 Friday)

### Built
- prompts/respond.v2.md: one deliberate change — required structure (one-sentence
  cause, numbered steps, "Escalate if" line) plus a 200-word cap.
- infra/release.auto.tfvars with prompt_version, so the deployed prompt can be
  changed without touching code or rebuilding the image. Week 3's AI SRE edits
  this file to roll back a bad release.
- OpenTelemetry tracing on the retrieve step: rag.chunks.retrieved, rag.top_score
  and prompt.version as span attributes, printed to the console exporter.

### Prompt comparison result
- Escalations: v1 = __ / 10, v2 = __ / 10  (must be 3 — fill in)
- Sources retrieved: identical / different  (should be identical)
- Total words: v1 = __, v2 = __
- Shipping: v__ because __________

### The finding of the week
/chat returned 200 OK with a plausible answer, but the trace showed only ONE
model call. Triage had classified "Our AWS connector says AccessDenied on
AssumeRole" as "urgent", which routes straight to escalate and skips retrieval
entirely. The HTTP response gave no hint; the span tree did.

Fix: rewrote prompts/triage.v1.md with explicit negative examples — an
AccessDenied error, a rate limit or one user locked out are "bug" or "account",
never "urgent". Nova Lite over-triggers on security-sounding words without that
boundary.

Lesson: a correct-looking answer can hide a skipped pipeline step. This is
exactly what traces are for, and exactly the failure mode a customer would
report as "the answer was wrong" when the real cause is upstream routing.

### Blocked
- graph.py lost its indentation again when the tracing change was pasted as a
  fragment. Sixth occurrence this week.
- Fix adopted: rewrite whole files with cat > file <<'EOF', then run
  python -m compileall -q src scripts before starting anything.

### Tomorrow / remaining
- Steps 5-9: deploy, find the spans in CloudWatch Logs Insights, write the
  README with the Mermaid diagram, record the demo, destroy.

## Week 1, Day 5 — Friday

**Built:** Prompt versioning via `PROMPT_VERSION` with fallback to `.v1.md`.
Wrote `prompts/respond.v2.md` adding required structure (one-line cause,
numbered steps, explicit "Escalate if") and a 200-word cap. Added
OpenTelemetry spans to `retrieve` emitting rag.chunks.retrieved,
rag.top_score and prompt.version.

**Measured:** Same 10 questions through both versions.
- v1: 6 escalations, 1279 words
- v2: 5 escalations, 850 words (33% shorter, same sources cited)

**Decision: ship v2 on answer quality. The escalation comparison is void.**

**Why it is void:** the escalate node decides with
`"ESCALATE" in answer` — a substring match on generated prose. Three
questions flipped between versions, in both directions. All three were
connector issues whose KB articles end with conditional advice ("escalate if
this persists past an hour"). Whether the flag fired depended only on whether
the model echoed that phrase in capitals. v2's prompt mandates an
"Escalate if" section, which structurally biases it toward matching. The flag
measures wording, not whether the ticket needs a human. With ~3 genuine KB
gaps in the set, both versions over-escalate — v1 by roughly double.

**Fix queued for Monday:** stop inferring control flow from prose. Either
require a machine-only final line (`ROUTE: escalate` / `ROUTE: resolved`),
parse it, and strip it before display; or make escalation its own node with
its own prompt returning a single token, so the routing decision is traceable
and independent of answer phrasing.

**Learned:** Three bad measurements before a usable one. (1) The harness ran
against a stopped Qdrant, produced two empty files, and still printed a
verdict — it could not distinguish "no difference" from "no data".
(2) Counting with `grep -ci escalate` matched the word in prose as well as the
flag, reporting 19 where the real count was 6. (3) The flag itself was
matching prose. Each time the number looked plausible and was counting the
wrong thing.

---

# Week 1 Retrospective

**Shipped:** A containerised RAG support agent — hybrid retrieval (dense Titan
embeddings + BM25 sparse, fused with RRF, reranked with a cross-encoder) over a
20-article knowledge base, routed through a LangGraph flow with triage,
retrieve, respond and escalate nodes, served by FastAPI. Deployed to ECS
Fargate behind an ALB in a private subnet, reaching Bedrock and ECR through VPC
interface endpoints, with the GitHub token in Secrets Manager.

**Four failures worth keeping:**

1. *Configuration lived in two places.* `/health` returned 200 while `/chat`
   returned 500 with an AccessDenied naming a model I thought I had stopped
   using. `.env` had moved to Nova Lite; `terraform.tfvars` still had Claude.
   The health check passed because it never touches the model. A health check
   that does not exercise the dependency is not a health check.

2. *`terraform destroy` reported "0 destroyed" while a NAT gateway kept
   billing* — twice. Both times I ran it from the repo root, which has no `.tf`
   files, so Terraform found an empty configuration and destroyed nothing
   truthfully. Fix: `terraform -chdir=infra destroy`, then verify against the
   API with `aws ec2 describe-nat-gateways`. A tool reporting success is not
   evidence the thing happened.

3. *A span was missing from the trace.* I assumed the instrumentation was
   broken. The trace showed one model call, 55 tokens in and 2 out — so
   `retrieve` had not been skipped by the tracer, it had never run. Triage was
   classifying "AccessDenied on AssumeRole" as `urgent`, routing straight to
   escalate. Fixed with explicit negative examples in the triage prompt. The
   trace answered a question I had framed wrongly, faster than reading code.

4. *The escalation metric was matching prose.* Detailed in Day 5. Control flow
   inferred from generated text means any wording change silently rewires the
   graph.

**Running theme:** every significant failure this week looked like success at
the layer I was watching — 200 OK, "0 destroyed", a clean comparison verdict.
Each diagnosis came from checking the layer below the one reporting success.
