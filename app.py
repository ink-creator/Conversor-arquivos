import os
import sys
import webview
from pathlib import Path

from utils.constants import INDEX_FILE, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from utils.logger import setup_logger
from utils.helpers import format_size, get_file_info
from converters.document import DocumentConverter
from converters.data import DataConverter
from converters.image import ImageConverter

logger = setup_logger(__name__)

# Instanciar converters
doc_converter = DocumentConverter()
data_converter = DataConverter()
image_converter = ImageConverter()


class Api:
    """API exposta para o frontend"""
    
    def __init__(self):
        self.last_output = None
    
    FILTROS = {
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
        """Abre diálogo para selecionar arquivo, filtrado por categoria
        ('arquivo' = documentos/dados, 'imagem' = imagens)."""
        file_types = self.FILTROS.get(categoria, ("Todos os arquivos (*.*)",))
        resultado = window.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
        )
        return resultado[0] if resultado else None
    
    # ==================== DOCUMENTOS ====================
    
    def converter_txt_pdf(self, arquivo):
        try:
            arquivo_saida = doc_converter.txt_para_pdf(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro TXT→PDF: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_txt_docx(self, arquivo):
        try:
            arquivo_saida = doc_converter.txt_para_docx(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro TXT→DOCX: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_pdf_txt(self, arquivo):
        try:
            arquivo_saida = doc_converter.pdf_para_txt(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro PDF→TXT: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_pdf_docx(self, arquivo):
        try:
            arquivo_saida = doc_converter.pdf_para_docx(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro PDF→DOCX: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_docx_txt(self, arquivo):
        try:
            arquivo_saida = doc_converter.docx_para_txt(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro DOCX→TXT: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_docx_pdf(self, arquivo):
        try:
            arquivo_saida = doc_converter.docx_para_pdf(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro DOCX→PDF: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_html_pdf(self, arquivo):
        try:
            arquivo_saida = doc_converter.html_para_pdf(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro HTML→PDF: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_html_txt(self, arquivo):
        try:
            arquivo_saida = doc_converter.html_para_txt(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro HTML→TXT: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_rtf_txt(self, arquivo):
        try:
            arquivo_saida = doc_converter.rtf_para_txt(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro RTF→TXT: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    # ==================== DADOS ====================
    
    def converter_csv_json(self, arquivo):
        try:
            arquivo_saida = data_converter.csv_para_json(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro CSV→JSON: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_json_csv(self, arquivo):
        try:
            arquivo_saida = data_converter.json_para_csv(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro JSON→CSV: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_csv_xml(self, arquivo):
        try:
            arquivo_saida = data_converter.csv_para_xml(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro CSV→XML: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_xml_csv(self, arquivo):
        try:
            arquivo_saida = data_converter.xml_para_csv(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro XML→CSV: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_json_xml(self, arquivo):
        try:
            arquivo_saida = data_converter.json_para_xml(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro JSON→XML: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_xml_json(self, arquivo):
        try:
            arquivo_saida = data_converter.xml_para_json(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro XML→JSON: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_csv_xlsx(self, arquivo):
        try:
            arquivo_saida = data_converter.csv_para_xlsx(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro CSV→XLSX: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_xlsx_csv(self, arquivo):
        try:
            arquivo_saida = data_converter.xlsx_para_csv(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro XLSX→CSV: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_json_xlsx(self, arquivo):
        try:
            arquivo_saida = data_converter.json_para_xlsx(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro JSON→XLSX: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_xlsx_json(self, arquivo):
        try:
            arquivo_saida = data_converter.xlsx_para_json(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro XLSX→JSON: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_yaml_json(self, arquivo):
        try:
            arquivo_saida = data_converter.yaml_para_json(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro YAML→JSON: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_json_yaml(self, arquivo):
        try:
            arquivo_saida = data_converter.json_para_yaml(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro JSON→YAML: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_yaml_xml(self, arquivo):
        try:
            arquivo_saida = data_converter.yaml_para_xml(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro YAML→XML: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def converter_xml_yaml(self, arquivo):
        try:
            arquivo_saida = data_converter.xml_para_yaml(arquivo)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro XML→YAML: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    # ==================== IMAGENS ====================
    
    def converter_imagem(self, arquivo, formato_saida):
        try:
            arquivo_saida = image_converter.converter_formato(arquivo, formato_saida)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro conversão imagem: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
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
                "reducao_percentual": round(reducao, 1)
            }
        except Exception as erro:
            logger.error(f"Erro compressão: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def redimensionar_imagem(self, arquivo, largura, altura, manter_proporcoes=True):
        try:
            arquivo_saida = image_converter.redimensionar(arquivo, largura, altura, manter_proporcoes)
            self.last_output = str(arquivo_saida)
            return {"sucesso": True, "arquivo": str(arquivo_saida), "tamanho": arquivo_saida.stat().st_size}
        except Exception as erro:
            logger.error(f"Erro redimensionamento: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    # ==================== GERENCIAMENTO ====================
    
    def abrir_arquivo(self, arquivo):
        try:
            arquivo = Path(arquivo)
            if not arquivo.exists():
                return {"sucesso": False, "erro": "Arquivo não existe"}
            
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
            logger.error(f"Erro ao abrir arquivo: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def abrir_pasta(self, arquivo):
        try:
            arquivo = Path(arquivo)
            if not arquivo.exists():
                return {"sucesso": False, "erro": "Arquivo não existe"}
            
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
            logger.error(f"Erro ao abrir pasta: {erro}")
            return {"sucesso": False, "erro": str(erro)}
    
    def obter_info_arquivo(self, arquivo):
        return get_file_info(arquivo)


# ==================== INICIALIZAÇÃO ====================

api = Api()

window = webview.create_window(
    "Conversor",
    INDEX_FILE.as_uri(),
    js_api=api,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    min_size=(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT),
    resizable=True,
)


def ao_iniciar(window):
    """Abre já maximizada, mas com a barra de título nativa do Windows
    (minimizar/maximizar/fechar) visível. fullscreen=True faria a janela
    ocupar a tela sem NENHUM controle nativo — não é o que foi pedido."""
    window.maximize()


logger.info("Aplicação iniciada")
webview.start(ao_iniciar, window)
logger.info("Aplicação finalizada")
