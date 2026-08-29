from pathlib import Path
from datetime import datetime


def format_size(bytes_size):
    """Formata tamanho em bytes para legível"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f}{unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f}TB"


def get_filename(path):
    """Extrai nome do arquivo de um caminho"""
    if not path:
        return ""
    return Path(path).name


def get_file_info(arquivo):
    """Retorna informações do arquivo"""
    try:
        path = Path(arquivo)
        if not path.exists():
            return {"erro": "Arquivo não existe"}
        stat = path.stat()
        return {
            "nome": path.name,
            "extensao": path.suffix.lower().lstrip('.'),
            "tamanho": stat.st_size,
            "tamanho_formatado": format_size(stat.st_size),
            "modificado": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    except Exception as e:
        return {"erro": str(e)}


def calcular_reducao(tamanho_original, tamanho_novo):
    """Calcula percentual de redução"""
    if tamanho_original <= 0:
        return 0
    return ((tamanho_original - tamanho_novo) / tamanho_original * 100)


def gerar_nome_saida(arquivo, sufixo="_converted", nova_extensao=None):
    """
    Gera nome para arquivo de saída.

    nova_extensao: ex. '.json' -> troca a extensão do arquivo original.
    Se None, mantém a extensão original.

    NOTA: a versão anterior desta função ignorava troca de extensão;
    conversores contornavam isso embutindo a extensão no próprio sufixo
    (ex: "_converted.json"), o que gerava nomes duplicados tipo
    "arquivo_converted.json.csv". Corrigido aqui.
    """
    path = Path(arquivo)
    ext = nova_extensao if nova_extensao is not None else path.suffix
    return path.parent / f"{path.stem}{sufixo}{ext}"
