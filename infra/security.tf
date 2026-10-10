resource "aws_security_group" "alb" {
  name   = "support-agent-alb"
  vpc_id = module.vpc.vpc_id
  ingress {
    description = "HTTP from my laptop only"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.my_ip_cidr]
  }
  egress {
    description = "To targets inside the VPC"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }
}
resource "aws_security_group" "app" {
  name   = "support-agent-app"
  vpc_id = module.vpc.vpc_id
  ingress {
    description     = "App port from the ALB only"
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  egress {
    description = "HTTPS out: VPC endpoints, and GitHub via NAT"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
 description = "OTLP to OpenObserve inside the VPC"
 from_port = 5080
 to_port = 5080
 protocol = "tcp"
 cidr_blocks = [module.vpc.vpc_cidr_block]
 }
}