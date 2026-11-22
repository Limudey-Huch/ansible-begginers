variable "aws_region" {
  type    = string
  default = "eu-north-1"
}

variable "ami_id" {
  type        = string
  default     = "ami-0848826c0bc5f2e6c" # Ubuntu 22.04 LTS, eu-north-1
  description = "Check https://cloud-images.ubuntu.com/locator/ec2/ if this is stale"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "project_tag" {
  type    = string
  default = "ansible-course-radar"
}
