# Terraform – lambda-python-ffmpeg

Este diretório contém a infraestrutura como código (IaC) em Terraform para provisionar os seguintes recursos na AWS:

- Um bucket S3 para armazenar vídeos convertidos  
- Uma fila SQS principal e sua DLQ  
- Um repositório ECR para a imagem Docker da função Lambda  
- Uma função Lambda em modo container com integração à SQS  

---

## Pré-requisitos

- Terraform >= 1.5.0  
- AWS CLI instalado e configurado (`aws configure`)  
- Credenciais AWS com permissão para criar S3, SQS, ECR, IAM e Lambda  
- Docker e AWS CLI (para o script de preparo de imagem)  

---

## Estrutura de diretórios

```text
terraform/
├── modules/           # Módulos reinvigoráveis: s3, sqs, ecr, lambda_function
├── outputs.tf         # Saídas principais do root module
├── provider.tf        # Configuração de provider AWS
├── scripts/           # Scripts auxiliares (prepare.sh)
│   └── prepare.sh     # Build e push da imagem :latest para o ECR
├── variables.tf       # Variáveis do root module
└── modules.tf         # Declaração de módulos filhos
```

---

## Passo a passo

1. Clone este repositório:
   ```bash
   git clone https://github.com/…/lambda-python-ffmpeg.git
   cd lambda-python-ffmpeg/terraform
   ```

2. Configure suas credenciais AWS (ou exporte variáveis de ambiente):
   ```bash
   aws configure
   # ou
   export AWS_ACCESS_KEY_ID=...
   export AWS_SECRET_ACCESS_KEY=...
   export AWS_REGION=us-east-1
   ```

3. Inicialize o Terraform:
   ```bash
   terraform init
   ```

4. (Opcional) Ajuste valores padrão em `variables.tf`:
   - `project_name` – prefixo para recursos  
   - `aws_region`    – região da AWS  

5. Gere e revise o plano:
   ```bash
   terraform plan -out=tfplan
   ```

6. Torne o script de preparo executável:
    ```bash
    chmod +x scripts/prepare.sh
    ```

7. Aplique as mudanças:
   ```bash
   terraform apply tfplan
   ```

8. Para destruir toda a stack:
   ```bash
   terraform destroy -auto-approve
   ```

---

## Principais Outputs

- `bucket_name`          – nome do bucket S3 criado  
- `sqs_queue_url`        – URL da fila SQS principal  
- `lambda_function_name` – nome da função Lambda  
- `ecr_image_uri`        – URI do repositório ECR (sem tag)  

Para exibir as saídas:
```bash
terraform output
```

---

## Script de Preparo (`scripts/prepare.sh`)

Este script verifica se a tag `latest` já existe no ECR; se não existir, faz o build local e faz push da imagem como `latest`. É chamado automaticamente pela pipeline ou manualmente antes do `terraform apply`.

```bash
bash scripts/prepare.sh
```

---