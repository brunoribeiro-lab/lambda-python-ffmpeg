import subprocess
import os
from src.services.conversion.base_strategy import ConversionStrategy


def convert_video(source_path: str, output_path: str, strategy: ConversionStrategy):
    """
    Converte o vídeo usando alguma estratégia de conversão. Que pode ser
    uma estratégia baseada em FFmpeg ou outra ferramenta de conversão.
    """
    try:
        strategy.convert(source_path, output_path)
    except Exception as e:
        # Re-lança a exceção para ser tratada pelo chamador (lambda_handler)
        raise e
