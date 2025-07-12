from abc import ABC, abstractmethod

class ConversionStrategy(ABC):
    
    """
    A interface abstrata para as diferentes estratégias de conversão de vídeo.
    Define o contrato que todas as estratégias concretas devem seguir.
    """
    @abstractmethod
    def convert(self, source_path: str, output_path: str, **kwargs):
        """
        Executa a conversão do vídeo.
        :param source_path: Caminho do arquivo de entrada.
        :param output_path: Caminho do arquivo de saída.
        :param kwargs: Argumentos adicionais para a conversão (ex: resolution).
        """
        pass