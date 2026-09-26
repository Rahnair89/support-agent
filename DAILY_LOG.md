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
