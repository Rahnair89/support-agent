# ADR-001: Host the support agent on ECS Fargate rather than Lambda

Status: Accepted — 2026-09-27

## Context
- Every request makes a model call through Amazon Bedrock. Observed responses
  take between 5 and 60 seconds.
- From Thursday the app needs a vector database (Qdrant) running alongside it,
  plus two embedding and reranking models baked into the image. The image is
  close to 1 GB.
- NFR-1 (p95 under 10 s), NFR-3 (no public IP on the application) and NFR-5
  (low cost, nothing running overnight) apply.
- One person builds and operates this, so operational effort is a real constraint.
- The environment is destroyed every night, so idle cost matters less than it
  would in production, but start-up time matters more.

## Options considered

### 1. AWS Lambda
- Pros: billed per invocation, scales to zero, no capacity to manage, fits the
  nightly-destroy pattern perfectly since there is nothing to destroy.
- Cons: a ~1 GB container image gives slow cold starts, which threatens NFR-1;
  there is no way to run a vector database next to the function, so retrieval
  would need a separate managed service and more moving parts; the 15-minute
  execution limit is not a problem today but constrains the longer multi-step
  agent workflows planned for Week 3.

### 2. ECS Fargate  (chosen)
- Pros: supports sidecar containers, so Qdrant runs in the same task and is
  reached over localhost with no extra service to secure; no limit on request
  duration; AWS manages the underlying servers; tasks run in private subnets
  with `assign_public_ip = false`, satisfying NFR-3; the same image runs on a
  laptop and in AWS, so failures reproduce locally.
- Cons: billed per hour whether or not anyone sends a request; a task takes one
  to two minutes to start and pass health checks.

### 3. EC2
- Pros: complete control, and cheapest at sustained high load.
- Cons: patching, AMI management, scaling and instance health all become mine.
  Disproportionate effort for a single container.

## Decision
ECS Fargate. One task, 1 vCPU and 4 GB memory, `X86_64` architecture, behind an
Application Load Balancer, running in private subnets.

## Consequences

Positive
- Qdrant runs as a sidecar, avoiding a separate managed vector database and the
  networking and credentials that would come with it.
- Long model responses are not truncated by a platform execution limit.
- The container that runs in AWS is byte-identical to the one tested locally,
  which made the model-configuration bug on 27 Sep quick to isolate.

Negative
- The stack bills hourly while idle, so it must be destroyed each night. Rebuild
  takes roughly 8 minutes, which is the effective recovery time (NFR-6).
- Deployments are slower than Lambda: a new task must reach RUNNING and pass
  health checks before traffic shifts, roughly two minutes per change.
- The ALB idle timeout had to be raised from the 60 s default to 120 s. Slower
  answers were being cut off as HTTP 504 before the model finished.

Accepted operational consequences
- `cpu_architecture` in the task definition must match the architecture the image
  was built for. Building `linux/arm64` on an x86 machine produced
  `exec format error` with no application logs, because the container never
  started. Both are now fixed at x86_64.
