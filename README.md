[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
# lambda-python-ffmpeg

Ferramenta serverless para conversão de vídeos usando FFmpeg em uma função AWS Lambda (container image), com fila SQS de orquestração e bucket S3 de armazenamento.

## Estrutura do Repositório

- `src/`              – código-fonte da Lambda  
- `test_lambda.py`    – teste local da função  
- `docker-compose.yml`– definindo serviço Lambda container local  
- `.github/workflows/terraform.yml` – pipeline IaC (Terraform)  
- `.github/workflows/deploy.yml`    – pipeline de build e deploy da imagem  

## Funcionalidades

- Consumir mensagens de uma fila SQS contendo parâmetros de conversão  
- Baixar vídeo de entrada de um bucket S3 (via URL)  
- Converter vídeo para `output_format` e `resolution` usando FFmpeg  
- Enviar o arquivo convertido de volta ao S3  

## Teste Local

1. Suba o container Lambda com Docker Compose:  
   ```bash
   docker compose up -d
   ```
2. Execute o teste dentro do container:  
   ```bash
   docker-compose run --rm --entrypoint python lambda-test test_lambda.py
   ```
3. Verifique saída e logs no console.

## Deploy da Função

A action `Deploy Lambda` em `.github/workflows/deploy.yml` faz build da imagem, push para ECR e atualiza a Lambda. Utilize a trigger manual (`workflow_dispatch`) definindo a versão (ex: `0.1`).

## Infraestrutura (Terraform)

Toda a infra (S3, SQS, ECR, IAM e Lambda) é provisionada via Terraform.  
Para detalhes de setup e uso, consulte:

👉 [terraform/README.md](terraform/README.md)

## Contribuição

1. Abra uma Issue para discutir mudanças.  
2. Fork do repositório e crie sua branch (`git checkout -b feature/xyz`).  
3. Faça commits claros e envie um Pull Request.  

## Licença

MIT License

[contributors-shield]: https://img.shields.io/github/contributors/brunoribeiro-lab/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/brunoribeiro-lab/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/brunoribeiro-lab/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/brunoribeiro-lab/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/brunoribeiro-lab/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/brunoribeiro-lab/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/brunoribeiro-lab/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/brunoribeiro-lab/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/brunoribeiro-lab/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/brunoribeiro-lab/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/bruno-ribeiro-46675922a/