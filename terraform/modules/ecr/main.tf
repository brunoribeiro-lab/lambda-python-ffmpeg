resource "aws_ecr_repository" "this" {
  name                 = var.project_name
  image_scanning_configuration {
    scan_on_push = true
  }
  image_tag_mutability = "MUTABLE"
  tags = {
    Project = var.project_name
  }
}