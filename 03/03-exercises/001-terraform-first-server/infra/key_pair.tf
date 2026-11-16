resource "tls_private_key" "course" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "course" {
  key_name   = "basic-course-key"
  public_key = tls_private_key.course.public_key_openssh
}

resource "local_sensitive_file" "private_key" {
  content         = tls_private_key.course.private_key_pem
  filename        = "${path.module}/basic-course-key.pem"
  file_permission = "0400"
}
