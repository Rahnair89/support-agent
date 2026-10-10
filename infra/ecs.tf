locals {
  image = "${data.aws_caller_identity.me.account_id}.dkr.ecr.${var.region}.amazonaws.com/support-agent:latest"
}

resource "aws_cloudwatch_log_group" "agent" {
  name              = "/ecs/support-agent"
  retention_in_days = 7
}

resource "aws_ecs_cluster" "main" {
  name = "support-agent"
}

resource "aws_ecs_task_definition" "agent" {
  family                   = "support-agent"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 4096
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  container_definitions = jsonencode([
    {
      name         = "qdrant"
      image        = "qdrant/qdrant:latest"
      essential    = true
      portMappings = [{ containerPort = 6333 }]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.agent.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "qdrant"
        }
      }
    },
    {
      name         = "app"
      image        = local.image
      essential    = true
      portMappings = [{ containerPort = 8000 }]
      dependsOn    = [{ containerName = "qdrant", condition = "START" }]
      environment = [
        { name = "MODEL_ID", value = var.model_id },
        { name = "AWS_REGION", value = var.region },
        { name = "QDRANT_URL", value = "http://localhost:6333" },
        { name = "PROMPT_VERSION", value = var.prompt_version },
        { name = "TICKET_REPO", value = "Rahnair89/support-agent" },
        { name = "GITHUB_TOKEN_SECRET", value = "support-agent/github-token" },
        { name = "OTEL_SERVICE_NAME", value = "support-agent" },
        { name = "OTEL_EXPORTER_OTLP_ENDPOINT", value = "http://localhost:4318" },
        {
 name = "otel-collector"
 image = "public.ecr.aws/aws-observability/aws-otel-collector:latest"
 essential = false
 environment = [{ name = "AOT_CONFIG_CONTENT", value = file("${path.module}/collector.yaml") }]
 secrets = [
 { name = "O2_AUTH", valueFrom = "${data.aws_secretsmanager_secret.o2.arn}:basic::" },
 ]
 logConfiguration = {
 logDriver = "awslogs"
 options = {
 awslogs-group = aws_cloudwatch_log_group.agent.name
 awslogs-region = var.region
 awslogs-stream-prefix = "collector"
 }
 }
 }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.agent.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "app"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "agent" {
  name                              = "support-agent"
  cluster                           = aws_ecs_cluster.main.id
  task_definition                   = aws_ecs_task_definition.agent.arn
  desired_count                     = 1
  launch_type                       = "FARGATE"
  health_check_grace_period_seconds = 120
  enable_execute_command = true

  network_configuration {
    subnets          = module.vpc.private_subnets
    security_groups  = [aws_security_group.app.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.agent.arn
    container_name   = "app"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.http, aws_vpc_endpoint.interface, aws_vpc_endpoint.s3]
}
