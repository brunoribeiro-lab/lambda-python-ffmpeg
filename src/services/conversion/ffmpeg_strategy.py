import subprocess
from pathlib import Path
from .base_strategy import ConversionStrategy
from src.utils.logger import logger
from .codec_map import CODEC_MAP

class FfmpegStrategy(ConversionStrategy):
    """
    Estratégia de conversão de vídeo que utiliza a ferramenta FFmpeg.
    """
    def convert(self, source_path: str, output_path: str, resolution: str = None):
        """
        Converte um vídeo usando FFmpeg, com opção de redimensionamento.
        """
        command = [
            'ffmpeg',
            '-y',
            '-loglevel', 'error',
            '-i', source_path,
        ]

        if resolution:
            command.extend(['-vf', f'scale={resolution}'])
        
        ext = Path(output_path).suffix.lstrip('.').lower()
        opts = CODEC_MAP.get(ext)
        if opts:
            command.extend(opts)
        else:
            logger.info(f"Sem opções específicas de codec para '{ext}', usando defaults do FFmpeg")

        command.append(output_path)
        #logger.info(f"Executando FFmpeg: {' '.join(command)}")

        try:
            proc = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(proc.stderr.decode('utf-8', errors='ignore'))
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)
            logger.error(f"FFmpeg stderr: {err}")
            raise RuntimeError(f"FFmpeg falhou ao converter o vídeo: {err}")
        except FileNotFoundError:
            raise RuntimeError("Comando ffmpeg não encontrado. Verifique se está instalado e no PATH do sistema.")