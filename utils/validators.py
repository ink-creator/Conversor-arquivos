from pathlib import Path
from utils.constants import ALLOWED_FORMATS, MAX_FILE_SIZE
from utils.logger import setup_logger

logger = setup_logger(__name__)


def validar_arquivo(arquivo, tipo='data'):
    """
    Valida arquivo antes de processar

    Returns:
        dict: {"valido": bool, "erro": str, "tamanho": int}
    """
    try:
        path = Path(arquivo)

        if not path.exists():
            return {"valido": False, "erro": "Arquivo não existe"}

        if not path.is_file():
            return {"valido": False, "erro": "Caminho não é um arquivo"}

        # Tamanho
        size = path.stat().st_size
        if size > MAX_FILE_SIZE:
            mb = size / 1024 / 1024
            return {"valido": False, "erro": f"Arquivo muito grande ({mb:.1f}MB > 500MB)"}

        if size == 0:
            return {"valido": False, "erro": "Arquivo vazio"}

        # Extensão
        ext = path.suffix.lower().lstrip('.')
        if ext not in ALLOWED_FORMATS.get(tipo, []):
            formatos = ', '.join(ALLOWED_FORMATS.get(tipo, []))
            return {"valido": False, "erro": f"Formato não suportado. Use: {formatos}"}

        return {"valido": True, "tamanho": size}

    except Exception as e:
        logger.error(f"Erro ao validar arquivo: {e}")
        return {"valido": False, "erro": str(e)}


def validar_dimensoes(largura, altura):
    """Valida dimensões para redimensionamento"""
    try:
        w = int(largura)
        h = int(altura)

        if w < 1 or h < 1:
            return {"valido": False, "erro": "Dimensões devem ser maiores que 0"}

        if w > 10000 or h > 10000:
            return {"valido": False, "erro": "Dimensões muito grandes (máx 10000px)"}

        return {"valido": True}

    except ValueError:
        return {"valido": False, "erro": "Dimensões devem ser números inteiros"}


def validar_qualidade(qualidade):
    """Valida qualidade de compressão"""
    try:
        q = int(qualidade)
        if q < 1 or q > 100:
            return {"valido": False, "erro": "Qualidade deve estar entre 1 e 100"}
        return {"valido": True}
    except ValueError:
        return {"valido": False, "erro": "Qualidade deve ser número"}
