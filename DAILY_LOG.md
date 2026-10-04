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
