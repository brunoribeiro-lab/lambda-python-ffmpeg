import os
import json
import boto3
import tempfile
from src.utils.validation import validate_event
from src.utils.logger import logger
from src.services.conversion.conversion import convert_video
from src.services.conversion.ffmpeg_strategy import FfmpegStrategy
from src.services.storage.s3_client import S3Client

def initler(event, context):
    """
    Função Lambda de inicialização para converter vídeos usando FFmpeg e S3.
    Esta função valida o evento, baixa o vídeo do S3, converte usando FFmpeg e faz o upload do resultado de volta ao S3.
    :param event: Evento recebido pela Lambda, contendo detalhes do vídeo a ser convertido.
    :param context: Contexto da execução da Lambda, não utilizado neste exemplo.
    :return: Resposta JSON com o status da conversão e a chave do vídeo convertido
    :raises ValueError: Se o evento não contiver registros ou se o parâmetro 's3_input_url' estiver ausente.
    :raises RuntimeError: Se ocorrer um erro ao baixar ou fazer upload do vídeo no S3, ou se o FFmpeg falhar na conversão.
    """
    try:
        params = validate_event(event)
        # Baixar o vídeo do S3 e salvar no diretório temporário
        download_path = S3Client().download_to_tmp(params.s3_input_url)
        # Conversão (por enquanto apenas ffmpeg está implementado)
        tmp_dir = tempfile.gettempdir()
        output_filename = os.path.basename(params.output_key)
        output_path = os.path.join(tmp_dir, output_filename)
        #logger.info(f"Converting video from {download_path} to {output_path} with resolution {params.resolution}")
        convert_video(download_path, output_path, FfmpegStrategy())
        # Upload do vídeo convertido de volta ao S3
        S3Client().upload_to_s3(output_path, params.output_key)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Conversão concluída com sucesso",
                "output_key": params.output_key
            })
        }
    except Exception as e:
        print(f"Erro na conversão: {e}")
        raise