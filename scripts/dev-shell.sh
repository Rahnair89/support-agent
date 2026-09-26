# Usage (from the repo root):  source scripts/dev-shell.sh
source .venv/bin/activate
set -a; source .env; set +a
export PYTHONPATH=src
aws sts get-caller-identity >/dev/null 2>&1 || aws sso login --profile $AWS_PROFILE
echo Ready: $(aws sts get-caller-identity --query Account --output text) in $AWS_REGION
