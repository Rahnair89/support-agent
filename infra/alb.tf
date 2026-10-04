resource "aws_lb" "main" {
  name               = "support-agent"
  load_balancer_type = "application"
  subnets            = module.vpc.public_subnets
  security_groups    = [aws_security_group.alb.id]
  idle_timeout       = 120 # LLM answers can take longer than the 60 s default
}
resource "aws_lb_target_group" "agent" {
  name        = "support-agent"
  port        = 8000
  protocol    = "HTTP"
  target_type = "ip" # required for Fargate
  vpc_id      = module.vpc.vpc_id
  health_check {
    path                = "/health"
    matcher             = "200"
    interval            = 15
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.agent.arn
  }
}