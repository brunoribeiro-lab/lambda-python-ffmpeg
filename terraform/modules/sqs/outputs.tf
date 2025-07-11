output "main_queue_arn" {
  value = aws_sqs_queue.main.arn
}

output "main_queue_url" {
  value = aws_sqs_queue.main.id
}