import sys
from pathlib import Path


def _base_dir():
    """Diretório de recursos somente-leitura (HTML, etc).
    Dentro do .exe (PyInstaller), recursos ficam em sys._MEIPASS."""
    if getattr(sys, 'frozen', False):
        return Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent))
    return Path(__file__).resolve().parent.parent


def _writable_dir():
    """Diretório gravável (logs). NUNCA usar _MEIPASS aqui: é uma pasta
    temporária apagada ao fechar o app."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = _base_dir()
WRITABLE_DIR = _writable_dir()

CONVERTERS_DIR = BASE_DIR / "converters"
INTERFACE_DIR = BASE_DIR / "interface"
UTILS_DIR = BASE_DIR / "utils"
LOGS_DIR = WRITABLE_DIR / "logs"

# HTML
INDEX_FILE = INTERFACE_DIR / "index.html"

# Limites
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
UPLOAD_TIMEOUT = 300  # 5 min

# Formatos suportados
ALLOWED_FORMATS = {
    'data': ['csv', 'json', 'xml', 'xlsx', 'yaml', 'yml'],
    'image': ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif'],
    'document': ['txt', 'pdf', 'docx', 'html', 'htm', 'rtf'],
}

# Qualidade padrão
DEFAULT_IMAGE_QUALITY = 85
DEFAULT_COMPRESSION_QUALITY = 90

# Interface
WINDOW_WIDTH = 560
WINDOW_HEIGHT = 720
WINDOW_MIN_WIDTH = 420
WINDOW_MIN_HEIGHT = 560

# Logging
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
