from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Optional
from src.services.conversion.codec_map import CODEC_MAP


@dataclass
class VideoParams:
    s3_input_url: str
    output_key: str
    output_format: str
    resolution: Optional[str] = None


def validate_event(event: dict) -> VideoParams:
    """
    Valida o evento (payload SQS), garantindo
    que exista apenas estes parâmetros no body:
      - s3_input_url
      - output_key
      - output_format (deve estar em CODEC_MAP)
      - resolution (formato WxH)
    Todos obrigatórios.
    """
    if 'Records' not in event or not event['Records']:
        raise ValueError("Nenhum registro encontrado no payload.")

    body_str = event['Records'][0].get('body')
    if not body_str:
        raise ValueError("Campo 'body' vazio no registro.")

    try:
        body = json.loads(body_str)
    except json.JSONDecodeError:
        raise ValueError("Corpo da mensagem não é um JSON válido.")

    # Campos obrigatórios
    required = ['s3_input_url', 'output_key', 'output_format']
    missing = [k for k in required if not body.get(k)]
    if missing:
        raise ValueError(
            f"Parâmetros obrigatórios ausentes ou vazios: {', '.join(missing)}")

    allowed = set(required + ['resolution'])
    extra = set(body.keys()) - allowed
    if extra:
        raise ValueError(
            f"Parâmetros inesperados no payload: {', '.join(sorted(extra))}")

    s3_input_url = body['s3_input_url']
    output_key = body['output_key']
    output_format = body['output_format'].lower()
    resolution = body.get("resolution")

    if output_format not in CODEC_MAP:
        suportados = ", ".join(sorted(CODEC_MAP.keys()))
        raise ValueError(
            f"Formato de saída inválido '{output_format}'. Formatos suportados: {suportados}")

    if resolution and not re.match(r'^\d+x\d+$', resolution):
        raise ValueError(
            f"Formato de resolução inválido '{resolution}'. Deve ser 'LARGURAxALTURA', ex: '640x360'"
        )

    ext_key = Path(output_key).suffix.lstrip('.').lower()
    if ext_key != output_format:
        raise ValueError(
            f"Extensão de 'output_key' ('{ext_key}') não corresponde a 'output_format' ('{output_format}')."
        )

    return VideoParams(
        s3_input_url=s3_input_url,
        output_key=output_key,
        output_format=output_format,
        resolution=resolution
    )
