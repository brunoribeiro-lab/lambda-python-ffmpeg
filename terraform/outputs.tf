output "bucket_name" {
  description = "Nome do bucket S3 onde os vídeos convertidos serão salvos."
  value       = module.s3.bucket_name
}

output "sqs_queue_url" {
  description = "URL da fila SQS para enviar os jobs de conversão."
  value       = module.sqs.main_queue_url
}

output "lambda_function_name" {
  description = "Nome da função Lambda criada."
  value       = module.lambda.lambda_function_name
}

output "ecr_image_uri" {
  description = "URI da imagem que será usada pela Lambda"
  value       = module.ecr.repository_url
}
