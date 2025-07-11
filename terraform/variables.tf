variable "aws_region" {
  description = "Região da AWS para provisionar os recursos."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto, usado como prefixo para os recursos."
  type        = string
  default     = "lambda-python-ffmpeg"
}
