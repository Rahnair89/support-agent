variable "region" {
  type    = string
  default = "us-east-1"
}
variable "model_id" {
  type = string
}
variable "my_ip_cidr" {
  type        = string
  description = "Your laptop's public IP with /32, e.g. 49.207.10.20/32"
}
variable "prompt_version" {
 type = string
 default = "v1"
}
