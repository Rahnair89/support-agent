# Failure table

| Symptom | Where I saw it | Cause | Fix |
|---|---|---|---|
| `pull access denied` on docker run | Terminal | Image tag misspelled (`lates`); Docker fell back to Docker Hub | `docker images` to check the tag before assuming a registry problem |
| Platform mismatch warning, slow start | docker run output | Image built for arm64 on an x86 machine | Rebuild with `--platform linux/amd64`; ECS needs `cpu_architecture = "X86_64"` |
| `Connection refused` on curl | Terminal | Container tab was closed, so nothing was listening | Keep the server tab open; curl from a second tab |
| Terraform reported success but the NAT gateway still existed | AWS CLI | `terraform destroy` ran from the repo root against an empty state file | Check `pwd` and `terraform state list`; verify with `describe-nat-gateways` |
| Credential errors in one tab only | Terraform, AWS CLI | `dev-shell.sh` had an unterminated quote and failed halfway | `bash -n script.sh` before sourcing |
| `/health` 200 but `/chat` 500 | curl, CloudWatch Logs | Container still had the Claude model ID; only `.env` was updated | Deployed config comes from `terraform.tfvars`, not `.env` |
| terraform destroy says "0 destroyed" but resources exist | Terminal | Ran from a directory with no .tf files, against an empty state | Use `terraform -chdir=infra destroy`; verify with `aws ec2 describe-nat-gateways` |
| Docker build fails with a SyntaxError on a line of prose | Build output | Document footer copied in with the code block | Rewrite with `cat > file <<'EOF'`; `grep -rn "<footer text>"` to find others |
| create-secret fails: SecretString length 0 | Terminal | `read -s` shows nothing, so a failed paste looks identical to a successful one | Check `echo ${#VAR}` before using the value |
