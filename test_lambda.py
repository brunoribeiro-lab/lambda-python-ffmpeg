import json
from lambda_function import lambda_handler

# Suporte avi, mov, flv, mkv
event = {
    "Records": [
        {
            "body": json.dumps({
                # URL do vídeo de entrada
                "s3_input_url": "https://lambda-python-ffmpeg.s3.us-east-1.amazonaws.com/sample.mp4",
                # Destino no S3 para o vídeo convertido
                "output_key": "converted/sample_converted.mkv",
                # Formato de saída desejado
                "output_format": "mkv",
                # Resolução desejada
                "resolution": "640x360"
            })
        }
    ]
}


class Context:
    """
    Mock de contexto para simular o ambiente Lambda.
    """
    def __init__(self):
        self.function_name = "lambda_python_ffmpeg"
        self.memory_limit_in_mb = 128
        self.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:lambda_python_ffmpeg"
        self.aws_request_id = "test-request-id"


context = Context()
response = lambda_handler(event, context)

print(json.dumps(response, indent=2))
