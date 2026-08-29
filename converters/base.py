from abc import ABC, abstractmethod
from pathlib import Path
from utils.logger import setup_logger
from utils.validators import validar_arquivo

logger = setup_logger(__name__)


class BaseConverter(ABC):
    """Classe base para todos os converters"""

    def __init__(self, tipo='data'):
        self.tipo = tipo
        self.logger = logger

    @abstractmethod
    def converter(self, arquivo, *args, **kwargs):
        """Implementar conversão específica"""
        pass

    def validar_entrada(self, arquivo):
        """Valida arquivo antes de converter"""
        resultado = validar_arquivo(arquivo, self.tipo)

        if not resultado['valido']:
            self.logger.error(f"Validação falhou: {resultado['erro']}")
            raise ValueError(resultado['erro'])

        return resultado

    def salvar_saida(self, dados, caminho_saida):
        """Salva dados no arquivo de saída"""
        try:
            caminho_saida = Path(caminho_saida)
            caminho_saida.parent.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Arquivo salvo: {caminho_saida}")
            return caminho_saida
        except Exception as e:
            self.logger.error(f"Erro ao salvar: {e}")
            raise
