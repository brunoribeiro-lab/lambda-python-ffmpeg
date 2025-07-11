module "s3" {
  source       = "./modules/s3"
  project_name = var.project_name
}

module "sqs" {
  source       = "./modules/sqs"
  project_name = var.project_name
}

module "ecr" {
  source       = "./modules/ecr"
  project_name = var.project_name
}

module "lambda" {
  source            = "./modules/lambda_function"
  project_name      = var.project_name
  ecr_image_uri     = "${module.ecr.repository_url}:latest"
  sqs_queue_arn     = module.sqs.main_queue_arn
  bucket_arn        = module.s3.bucket_arn
  depends_on        = [module.ecr, module.sqs]
}