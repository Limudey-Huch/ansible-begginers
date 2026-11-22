resource "tls_private_key" "radar" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "aws_key_pair" "radar" {
  key_name   = "radar-course-key-tf"
  public_key = tls_private_key.radar.public_key_openssh
}

resource "local_sensitive_file" "private_key" {
  content         = tls_private_key.radar.private_key_pem
  filename        = "${path.module}/radar-course-key-tf.pem"
  file_permission = "0400"
}
