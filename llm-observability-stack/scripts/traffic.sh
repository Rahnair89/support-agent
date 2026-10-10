#!/bin/bash
# Usage: ./scripts/traffic.sh 50
set -uo pipefail
ALB=$(terraform -chdir=$HOME/projects/support-agent/infra output -raw alb_dns)
COUNT=${1:-50}
QUESTIONS=("How do I fix AccessDenied on the AWS connector?" "How do I reset MFA?"
 "Why are assets missing from inventory?" "Our CrowdStrike connector hits rate limits")
for i in $(seq 1 "$COUNT"); do
 Q=${QUESTIONS[$((i % ${#QUESTIONS[@]}))]}
 CODE=$(curl -s -o /dev/null -w '%{http_code}' -X POST "http://$ALB/chat" \
 -H 'Content-Type: application/json' -d "{\"message\":\"$Q\"}")
 echo "request $i -> HTTP $CODE"
done
