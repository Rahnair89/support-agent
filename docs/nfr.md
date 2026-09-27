# Non-functional requirements — support agent

These shaped the decisions recorded in the ADRs.

| # | Requirement | Target | How it is measured |
|---|---|---|---|
| NFR-1 | Latency | p95 under 10 s per answer | Response time in logs now; a CloudWatch metric from Week 2 |
| NFR-2 | Availability | 99% during working demos | ALB healthy host count; ECS service events |
| NFR-3 | Network exposure | No public IP on the application; only one client IP may reach the load balancer | Terraform review; `assign_public_ip = false`; ALB security group scoped to /32 |
| NFR-4 | Secret handling | No credentials in the image, in Git, or in plain environment variables | `.gitignore`, GitHub push protection, AWS Secrets Manager |
| NFR-5 | Cost | Under $3 per running day; nothing left running overnight | Cost Explorer filtered by `project` tag; nightly `terraform destroy` |
| NFR-6 | Reproducibility | The whole stack rebuilds from code in under 15 minutes | Timed `terraform apply` after a destroy |
| NFR-7 | Diagnosability | Any failure can be traced from a symptom to a cause using CLI commands alone | The runbook-style commands in docs/failure-table.md |

## Known gaps
- NFR-3 is partly met: outbound traffic to GitHub's API leaves through a NAT
  gateway, so egress is not fully private. See ADR-002.
- NFR-2 is a single task behind a single NAT gateway, so there is no redundancy.
  Acceptable for a demo; production would run at least two tasks across two AZs.
