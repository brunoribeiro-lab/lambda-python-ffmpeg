import json
from src.utils.logger import logger
from src.handlers.converter import initler


def lambda_handler(event, context):
    """
    Função Lambda para processar eventos SQS e converter vídeos usando FFmpeg.
    """
    try:
        initler(event, context)
    except Exception as e:
        logger.error(f"Erro ao processar o evento: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps(f"Erro no processamento: {str(e)}")}

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda processado')
    }
