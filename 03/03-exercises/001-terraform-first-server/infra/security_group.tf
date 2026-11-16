resource "aws_security_group" "web" {
  name        = "basic-course-web-sg"
  description = "SSH from me, HTTP from anywhere"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH from me"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.my_ip]
  }

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Project = var.project_tag }
}
