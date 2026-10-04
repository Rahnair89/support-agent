#!/bin/bash
set -euo pipefail
ACCT=$(aws sts get-caller-identity --query Account --output text)
REGISTRY=$ACCT.dkr.ecr.us-east-1.amazonaws.com
aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY
# Windows or Intel Mac: change linux/arm64 to linux/amd64
docker buildx build --platform linux/arm64 -t $REGISTRY/support-agent:latest --push .
if aws ecs describe-services --cluster support-agent --services support-agent \
 --query 'services[0].status' --output text 2>/dev/null | grep -q ACTIVE; then
 aws ecs update-service --cluster support-agent --service support-agent \
 --force-new-deployment --query 'service.deployments[0].rolloutState' --output text
fi
