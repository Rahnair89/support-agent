# ADR-002: Private subnets with VPC endpoints, and a NAT gateway only for GitHub

Status: Accepted — 2026-09-27

## Context
- NFR-3 requires that the application has no public IP address and that only one
  client IP can reach it.
- The application calls four AWS services: Bedrock (model inference), CloudWatch
  Logs (logging), ECR (its own image, pulled by ECS), and Secrets Manager (the
  GitHub token, from Thursday).
- From Thursday it also calls GitHub's REST API to create issues. GitHub is on
  the public internet and has no AWS private equivalent.
- NFR-5 limits cost. A NAT gateway is the most expensive hourly component in
  this stack.

## Options considered

### 1. Public subnets with public IPs on the tasks
- Pros: simplest, no NAT gateway and no endpoints, cheapest.
- Cons: the application is directly addressable from the internet, which fails
  NFR-3. Not acceptable, and not what a customer's security team would accept
  either.

### 2. Private subnets with a NAT gateway only
- Pros: no public IPs; one component to manage; all destinations reachable.
- Cons: every AWS API call leaves the VPC and traverses the internet, when it
  does not need to; higher NAT data processing charges; weaker story when a
  security reviewer asks where the traffic goes.

### 3. Private subnets with VPC endpoints, plus NAT for GitHub only  (chosen)
- Pros: traffic to Bedrock, Logs, ECR and Secrets Manager stays on the AWS
  network and never reaches the internet; least-exposure posture for the
  services that matter most; the NAT gateway carries only GitHub traffic.
- Cons: six endpoints to create and understand; interface endpoints bill per
  hour per availability zone, so the saving over option 2 is small at this scale;
  the NAT gateway is still required, so egress is not fully eliminated.

## Decision
- Application tasks run in private subnets with `assign_public_ip = false`.
- Five interface endpoints: `bedrock-runtime`, `ecr.api`, `ecr.dkr`, `logs`,
  `secretsmanager`.
- One S3 gateway endpoint, because ECR stores image layers in S3 and image pulls
  fail without it.
- One NAT gateway, shared across both private subnets, used only for GitHub.
- Outbound rules on the application security group allow TCP 443 only.
- The Application Load Balancer sits in public subnets with inbound TCP 80
  restricted to a single /32, my home IP.
- The application security group allows inbound 8000 from the load balancer's
  security group, not from an IP range.

## Consequences

Positive
- All AWS service traffic stays inside the AWS network.
- Nothing except one IP address can reach the application, which keeps both the
  attack surface and the Bedrock bill under control.
- Referencing the load balancer's security group rather than its IP addresses
  means the rule keeps working as AWS scales the load balancer and its addresses
  change.

Negative
- NFR-3's "no public egress" goal is not fully met. GitHub's API requires
  internet access, so a NAT gateway remains. The mitigation is that egress is
  restricted to port 443 and the NAT carries no AWS-service traffic.
- A single NAT gateway is a single point of failure. Two, one per availability
  zone, would be correct in production; one is a deliberate cost decision here.
- The inbound /32 rule breaks whenever my home IP changes, which it does. The
  symptom is a hanging curl while every AWS-side check reports healthy. The fix
  is to re-read the IP and re-apply.

Discovered during implementation
- ECR image pulls need the S3 gateway endpoint as well as the two ECR interface
  endpoints. Without it the task stops with `CannotPullContainerError` and
  produces no application logs at all, because the container never starts.
