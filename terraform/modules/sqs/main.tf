resource "aws_sqs_queue" "dlq" {
  name = "${var.project_name}-dlq"
}

resource "aws_sqs_queue" "main" {
  name                          = "${var.project_name}-queue"
  delay_seconds                 = 0
  max_message_size              = 262144    # 256 KB
  message_retention_seconds     = 86400     # 1 dia
  visibility_timeout_seconds    = 300       # 5 minutos, deve ser maior que o timeout da Lambda

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 3         # Número de tentativas antes de enviar para o Lambda
  })
}