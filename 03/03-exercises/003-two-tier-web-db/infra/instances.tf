resource "aws_instance" "web" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.course.key_name
  vpc_security_group_ids = [aws_security_group.web.id]
  subnet_id              = data.aws_subnets.default.ids[0]

  tags = {
    Name    = "basic-course-web"
    Project = var.project_tag
    Role    = "web"
  }
}

resource "aws_instance" "db" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.course.key_name
  vpc_security_group_ids = [aws_security_group.db.id]
  subnet_id              = data.aws_subnets.default.ids[0]

  tags = {
    Name    = "basic-course-db"
    Project = var.project_tag
    Role    = "db"
  }
}
