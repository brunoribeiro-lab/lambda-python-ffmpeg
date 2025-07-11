#!/bin/bash
set -e

# entra no diretório raiz do repositório (onde está o Dockerfile)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

REPO_NAME="lambda-python-ffmpeg"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
ECR_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME"

echo "Verificando se existe tag 'latest' em $ECR_URI..."
LATEST_EXISTS=$(aws ecr list-images \
  --repository-name "$REPO_NAME" \
  --filter tagStatus=TAGGED \
  --query 'imageIds[?imageTag==`latest`].imageTag' \
  --output text)

if [ -n "$LATEST_EXISTS" ]; then
  echo "✅ Tag 'latest' já existe. Pulando build/push."
  exit 0
fi

echo "🚀 Tag 'latest' não encontrada. Iniciando build & push..."

# build (agora roda na raiz e encontra o Dockerfile)
docker build -t "$REPO_NAME" .

# tag
docker tag "$REPO_NAME:latest" "$ECR_URI:latest"

# login e push
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
docker push "$ECR_URI:latest"

echo "🎉 Imagem disponível em $ECR_URI:latest"