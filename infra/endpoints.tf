resource "aws_security_group" "vpce" {
 name = "support-agent-vpce"
 vpc_id = module.vpc.vpc_id
 ingress {
 description = "HTTPS from inside the VPC"
 from_port = 443
 to_port = 443
 protocol = "tcp"
 cidr_blocks = [module.vpc.vpc_cidr_block]
 }
}
resource "aws_vpc_endpoint" "interface" {
 for_each = toset(["bedrock-runtime", "ecr.api", "ecr.dkr", "logs", "secretsmanager"])
 vpc_id = module.vpc.vpc_id
 service_name = "com.amazonaws.${var.region}.${each.value}"
 vpc_endpoint_type = "Interface"
 subnet_ids = module.vpc.private_subnets
 security_group_ids = [aws_security_group.vpce.id]
 private_dns_enabled = true
}
resource "aws_vpc_endpoint" "s3" {
 vpc_id = module.vpc.vpc_id
 service_name = "com.amazonaws.${var.region}.s3"
 vpc_endpoint_type = "Gateway"
 route_table_ids = module.vpc.private_route_table_ids
}