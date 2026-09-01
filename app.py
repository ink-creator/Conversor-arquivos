import json
import os
import sys
import webview
from pathlib import Path

from utils.constants import INDEX_FILE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from utils.logger import setup_logger
from utils.helpers import get_file_info
from converters.document import DocumentConverter
from converters.data import DataConverter
from converters.image import ImageConverter

logger = setup_logger(__name__)


def _settings_file():
    """Return a writable per-user settings path that also works in a PyInstaller .exe."""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA") or (Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))

    folder = base / "FileConverter"
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "settings.json"


def _load_language():
    try:
        data = json.loads(_settings_file().read_text(encoding="utf-8"))
        return "en" if data.get("language") == "en" else "pt"
    except (OSError, ValueError, TypeError, AttributeError):
        return "pt"


def _save_language(language):
    language = "en" if language == "en" else "pt"
    path = _settings_file()
    temporary = path.with_suffix(".tmp")
    try:
        temporary.write_text(
            json.dumps({"language": language}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary.replace(path)
        return True
    except OSError as error:
        logger.warning(f"Could not save language preference: {error}")
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        return False


# Converter instances
doc_converter = DocumentConverter()
data_converter = DataConverter()
image_converter = ImageConverter()


EN_ERROR_EXACT = {
    "Arquivo não existe": "File does not exist",
    "Caminho não é um arquivo": "Path is not a file",
    "Arquivo vazio": "File is empty",
    "Dimensões devem ser maiores que 0": "Dimensions must be greater than 0",
    "Dimensões muito grandes (máx 10000px)": "Dimensions are too large (max 10000px)",
    "Dimensões devem ser números inteiros": "Dimensions must be integers",
    "Qualidade deve estar entre 1 e 100": "Quality must be between 1 and 100",
    "Qualidade deve ser número": "Quality must be a number",
    "JSON vazio": "JSON is empty",
    "Planilha vazia": "Spreadsheet is empty",
}

EN_ERROR_REPLACEMENTS = (
    ("Arquivo muito grande", "File is too large"),
    ("Formato não suportado. Use:", "Unsupported format. Use:"),
    ("Falha ao gerar PDF", "Failed to generate PDF"),
    (" erro(s)", " error(s)"),
)


def localize_error(message, language="pt"):
    """Return known backend validation messages in the active UI language."""
    text = str(message)
    if language != "en":
        return text

    if text in EN_ERROR_EXACT:
        return EN_ERROR_EXACT[text]

    for source, target in EN_ERROR_REPLACEMENTS:
        text = text.replace(source, target)
    return text


class Api:
    """API exposed to the frontend.

    Internal method names and response keys remain in Portuguese so existing
    JavaScript/Python integration and converters do not need to be renamed.
    """

    def __init__(self):
        self.last_output = None
        self._language = _load_language()

    def get_language(self):
        """Return the language persisted in the user's application settings."""
        self._language = _load_language()
        return {"ok": True, "language": self._language}

    def set_language(self, language="pt"):
        self._language = "en" if language == "en" else "pt"
        saved = _save_language(self._language)
        return {"ok": saved, "language": self._language}

    def _error(self, error):
        return localize_error(error, self._language)

    def _filters(self):
        if self._language == "en":
            return {
                "arquivo": (
                    "Documents and data (*.txt;*.pdf;*.docx;*.html;*.htm;*.rtf;"
                    "*.csv;*.json;*.xml;*.xlsx;*.yaml;*.yml)",
                    "All files (*.*)",
                ),
                "imagem": (
                    "Images (*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.gif)",
                    "All files (*.*)",
                ),
            }

        return {
            "arquivo": (
                "Documentos e dados (*.txt;*.pdf;*.docx;*.html;*.htm;*.rtf;"
                "*.csv;*.json;*.xml;*.xlsx;*.yaml;*.yml)",
                "Todos os arquivos (*.*)",
            ),
            "imagem": (
                "Imagens (*.png;*.jpg;*.jpeg;*.webp;*.bmp;*.gif)",
                "Todos os arquivos (*.*)",
            ),
        }

    def selecionar_arquivo(self, categoria="arquivo"):
        filters = self._filters()
        fallback = ("All files (*.*)",) if self._language == "en" else ("Todos os arquivos (*.*)",)
        file_types = filters.get(categoria, fallback)
        resultado = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
        )
        return resultado[0] if resultado else None

    # ==================== DOCUMENTS / DOCUMENTOS ====================

    def _conversion_result(self, action, label):
        try:
            arquivo_saida = action()
            self.last_output = str(arquivo_saida)
            return {
                "sucesso": True,
                "arquivo": str(arquivo_saida),
                "tamanho": arquivo_saida.stat().st_size,
            }
        except Exception as erro:
            logger.error(f"{label}: {erro}")
            return {"sucesso": False, "erro": self._error(erro)}

    def converter_txt_pdf(self, arquivo):
        return self._conversion_result(lambda: doc_converter.txt_para_pdf(arquivo), "TXT→PDF")

    def converter_txt_docx(self, arquivo):
        return self._conversion_result(lambda: doc_converter.txt_para_docx(arquivo), "TXT→DOCX")

    def converter_pdf_txt(self, arquivo):
        return self._conversion_result(lambda: doc_converter.pdf_para_txt(arquivo), "PDF→TXT")

    def converter_pdf_docx(self, arquivo):
        return self._conversion_result(lambda: doc_converter.pdf_para_docx(arquivo), "PDF→DOCX")

    def converter_docx_txt(self, arquivo):
        return self._conversion_result(lambda: doc_converter.docx_para_txt(arquivo), "DOCX→TXT")

    def converter_docx_pdf(self, arquivo):
        return self._conversion_result(lambda: doc_converter.docx_para_pdf(arquivo), "DOCX→PDF")

    def converter_html_pdf(self, arquivo):
        return self._conversion_result(lambda: doc_converter.html_para_pdf(arquivo), "HTML→PDF")

    def converter_html_txt(self, arquivo):
        return self._conversion_result(lambda: doc_converter.html_para_txt(arquivo), "HTML→TXT")

    def converter_rtf_txt(self, arquivo):
        return self._conversion_result(lambda: doc_converter.rtf_para_txt(arquivo), "RTF→TXT")

    # ==================== DATA / DADOS ====================

    def converter_csv_json(self, arquivo):
        return self._conversion_result(lambda: data_converter.csv_para_json(arquivo), "CSV→JSON")

    def converter_json_csv(self, arquivo):
        return self._conversion_result(lambda: data_converter.json_para_csv(arquivo), "JSON→CSV")

    def converter_csv_xml(self, arquivo):
        return self._conversion_result(lambda: data_converter.csv_para_xml(arquivo), "CSV→XML")

    def converter_xml_csv(self, arquivo):
        return self._conversion_result(lambda: data_converter.xml_para_csv(arquivo), "XML→CSV")

    def converter_json_xml(self, arquivo):
        return self._conversion_result(lambda: data_converter.json_para_xml(arquivo), "JSON→XML")

    def converter_xml_json(self, arquivo):
        return self._conversion_result(lambda: data_converter.xml_para_json(arquivo), "XML→JSON")

    def converter_csv_xlsx(self, arquivo):
        return self._conversion_result(lambda: data_converter.csv_para_xlsx(arquivo), "CSV→XLSX")

    def converter_xlsx_csv(self, arquivo):
        return self._conversion_result(lambda: data_converter.xlsx_para_csv(arquivo), "XLSX→CSV")

    def converter_json_xlsx(self, arquivo):
        return self._conversion_result(lambda: data_converter.json_para_xlsx(arquivo), "JSON→XLSX")

    def converter_xlsx_json(self, arquivo):
        return self._conversion_result(lambda: data_converter.xlsx_para_json(arquivo), "XLSX→JSON")

    def converter_yaml_json(self, arquivo):
        return self._conversion_result(lambda: data_converter.yaml_para_json(arquivo), "YAML→JSON")

    def converter_json_yaml(self, arquivo):
        return self._conversion_result(lambda: data_converter.json_para_yaml(arquivo), "JSON→YAML")

    def converter_yaml_xml(self, arquivo):
        return self._conversion_result(lambda: data_converter.yaml_para_xml(arquivo), "YAML→XML")

    def converter_xml_yaml(self, arquivo):
        return self._conversion_result(lambda: data_converter.xml_para_yaml(arquivo), "XML→YAML")

    # ==================== IMAGES / IMAGENS ====================

    def converter_imagem(self, arquivo, formato_saida):
        try:
            arquivo_saida = image_converter.converter_formato(arquivo, formato_saida)
            self.last_output = str(arquivo_saida)
            return {
                "sucesso": True,
                "arquivo": str(arquivo_saida),
                "tamanho": arquivo_saida.stat().st_size,
            }
        except Exception as erro:
            logger.error(f"Image conversion / conversão de imagem: {erro}")
            return {"sucesso": False, "erro": self._error(erro)}

    def comprimir_imagem(self, arquivo, qualidade=85):
        try:
            arquivo_saida, reducao = image_converter.comprimir(arquivo, qualidade)
            self.last_output = str(arquivo_saida)
            tamanho_original = Path(arquivo).stat().st_size
            tamanho_novo = arquivo_saida.stat().st_size
            return {
                "sucesso": True,
                "arquivo": str(arquivo_saida),
                "tamanho_original": tamanho_original,
                "tamanho_novo": tamanho_novo,
                "reducao_percentual": round(reducao, 1),
            }
        except Exception as erro:
            logger.error(f"Compression / compressão: {erro}")
            return {"sucesso": False, "erro": self._error(erro)}

    def redimensionar_imagem(self, arquivo, largura, altura, manter_proporcoes=True):
        try:
            arquivo_saida = image_converter.redimensionar(
                arquivo, largura, altura, manter_proporcoes
            )
            self.last_output = str(arquivo_saida)
            return {
                "sucesso": True,
                "arquivo": str(arquivo_saida),
                "tamanho": arquivo_saida.stat().st_size,
            }
        except Exception as erro:
            logger.error(f"Resize / redimensionamento: {erro}")
            return {"sucesso": False, "erro": self._error(erro)}

    # ==================== FILE MANAGEMENT / GERENCIAMENTO ====================

    def abrir_arquivo(self, arquivo):
        try:
            arquivo = Path(arquivo)
            if not arquivo.exists():
                return {"sucesso": False, "erro": self._error("Arquivo não existe")}

            if sys.platform == "win32":
                os.startfile(str(arquivo))
            elif sys.platform == "darwin":
                import subprocess
                subprocess.run(["open", str(arquivo)])
            else:
                import subprocess
                subprocess.run(["xdg-open", str(arquivo)])

            return {"sucesso": True}
        except Exception as erro:
            logger.error(f"Open file / abrir arquivo: {erro}")
            return {"sucesso": False, "erro": self._error(erro)}

    def abrir_pasta(self, arquivo):
        try:
            arquivo = Path(arquivo)
            if not arquivo.exists():
                return {"sucesso": False, "erro": self._error("Arquivo não existe")}

            pasta = arquivo.parent

            if sys.platform == "win32":
                import subprocess
                subprocess.Popen(["explorer", str(pasta)])
            elif sys.platform == "darwin":
                import subprocess
                subprocess.run(["open", str(pasta)])
            else:
                import subprocess
                subprocess.run(["xdg-open", str(pasta)])

            return {"sucesso": True}
        except Exception as erro:
            logger.error(f"Open folder / abrir pasta: {erro}")
            return {"sucesso": False, "erro": self._error(erro)}

    def obter_info_arquivo(self, arquivo):
        info = get_file_info(arquivo)
        if isinstance(info, dict) and info.get("erro"):
            info["erro"] = self._error(info["erro"])
        return info


# ==================== INITIALIZATION ====================

api = Api()

window = webview.create_window(
    "Conversor de Arquivos / File Converter",
    INDEX_FILE.as_uri(),
    js_api=api,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    min_size=(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT),
    resizable=True,
)


def ao_iniciar(window):
    """Start maximized while keeping native minimize/maximize/close controls."""
    window.maximize()


logger.info("Application started / Aplicação iniciada")
webview.start(ao_iniciar, window)
logger.info("Application closed / Aplicação finalizada")
