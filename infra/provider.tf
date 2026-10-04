terraform {
  required_version = ">= 1.10"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
provider "aws" {
  region = var.region
  default_tags {
    tags = {
      project = "support-agent"
      env     = "dev"
      agent   = "support"
    }
  }
}
data "aws_caller_identity" "me" {}
