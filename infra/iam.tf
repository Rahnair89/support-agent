data "aws_iam_policy_document" "ecs_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

# Execution role: used by ECS itself to pull the image and write logs
resource "aws_iam_role" "execution" {
  name               = "support-agent-execution"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Task role: used by YOUR code inside the container
resource "aws_iam_role" "task" {
  name               = "support-agent-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_assume.json
}

data "aws_secretsmanager_secret" "github" {
  name = "support-agent/github-token"
}

data "aws_iam_policy_document" "task" {
  statement {
    sid     = "InvokeBedrockModels"
    actions = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
    resources = [
      "arn:aws:bedrock:*::foundation-model/*",
      "arn:aws:bedrock:${var.region}:${data.aws_caller_identity.me.account_id}:inference-profile/*",
    ]
  }

  statement {
    sid       = "ReadGithubToken"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [data.aws_secretsmanager_secret.github.arn]
  }
}

resource "aws_iam_role_policy" "task" {
  name   = "support-agent-task"
  role   = aws_iam_role.task.id
  policy = data.aws_iam_policy_document.task.json
}
data "aws_secretsmanager_secret" "o2" {
 name = "observability/openobserve"
}
# Execution role: inject O2_AUTH into the collector container
resource "aws_iam_role_policy" "execution_secrets" {
 name = "read-openobserve-secret"
 role = aws_iam_role.execution.id
 policy = jsonencode({
 Version = "2012-10-17"
 Statement = [{
 Effect = "Allow"
 Action = ["secretsmanager:GetSecretValue"]
 Resource = [data.aws_secretsmanager_secret.o2.arn]
 }]
 })
}
# Task role: collector writes spans to X-Ray; ECS Exec needs ssmmessages
resource "aws_iam_role_policy_attachment" "task_xray" {
 role = aws_iam_role.task.name
 policy_arn = "arn:aws:iam::aws:policy/AWSXrayWriteOnlyAccess"
}
resource "aws_iam_role_policy" "task_exec" {
 name = "ecs-exec"
 role = aws_iam_role.task.id
 policy = jsonencode({
 Version = "2012-10-17"
 Statement = [{
 Effect = "Allow"
 Action = ["ssmmessages:CreateControlChannel", "ssmmessages:CreateDataChannel",
 "ssmmessages:OpenControlChannel", "ssmmessages:OpenDataChannel"]
 Resource = "*"
 }]
 })
}