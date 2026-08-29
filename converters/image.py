from PIL import Image
from pathlib import Path
from utils.helpers import gerar_nome_saida, calcular_reducao
from utils.validators import validar_qualidade, validar_dimensoes, validar_arquivo
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ImageConverter:
    """Converte e manipula imagens"""

    def __init__(self):
        self.tipo = 'image'
        self.logger = logger

    def converter_formato(self, arquivo, formato_saida, qualidade=95):
        """Converte imagem para outro formato"""
        val = validar_arquivo(arquivo, self.tipo)
        if not val['valido']:
            raise ValueError(val['erro'])
        arquivo = Path(arquivo)

        self.logger.info(f"Convertendo imagem→{formato_saida}: {arquivo}")

        try:
            val_qualidade = validar_qualidade(qualidade)
            if not val_qualidade['valido']:
                raise ValueError(val_qualidade['erro'])

            img = Image.open(arquivo)

            if formato_saida.lower() in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[-1])
                else:
                    rgb_img.paste(img)
                img = rgb_img

            # BUG ORIGINAL: gerar_nome_saida(arquivo, f"_converted.{formato_saida}")
            # gerava "foto_converted.jpg.png" (extensão antiga + nova, ambas).
            # Corrigido: extensão nova passada como parâmetro dedicado.
            arquivo_saida = gerar_nome_saida(arquivo, "_converted", f".{formato_saida.lower()}")

            if formato_saida.lower() in ['jpg', 'jpeg']:
                img.save(arquivo_saida, 'JPEG', quality=qualidade, optimize=True)
            elif formato_saida.lower() == 'webp':
                img.save(arquivo_saida, 'WEBP', quality=qualidade)
            elif formato_saida.lower() == 'png':
                img.save(arquivo_saida, 'PNG', optimize=True)
            else:
                img.save(arquivo_saida)

            self.logger.info(f"Sucesso: {arquivo_saida}")
            return arquivo_saida

        except Exception as e:
            self.logger.error(f"Erro na conversão: {e}")
            raise

    def comprimir(self, arquivo, qualidade=85):
        """Comprime imagem mantendo formato"""
        val = validar_arquivo(arquivo, self.tipo)
        if not val['valido']:
            raise ValueError(val['erro'])
        arquivo = Path(arquivo)

        val_qualidade = validar_qualidade(qualidade)
        if not val_qualidade['valido']:
            raise ValueError(val_qualidade['erro'])

        self.logger.info(f"Comprimindo imagem (q={qualidade}): {arquivo}")

        try:
            img = Image.open(arquivo)
            formato = arquivo.suffix.lower().lstrip('.')

            arquivo_saida = gerar_nome_saida(arquivo, "_compressed")

            if formato in ['jpg', 'jpeg']:
                img.save(arquivo_saida, 'JPEG', quality=qualidade, optimize=True)
            elif formato == 'webp':
                img.save(arquivo_saida, 'WEBP', quality=qualidade)
            else:
                img.save(arquivo_saida, optimize=True)

            reducao = calcular_reducao(
                arquivo.stat().st_size,
                arquivo_saida.stat().st_size
            )

            self.logger.info(f"Compressão concluída. Redução: {reducao:.1f}%")
            return arquivo_saida, reducao

        except Exception as e:
            self.logger.error(f"Erro na compressão: {e}")
            raise

    def redimensionar(self, arquivo, largura, altura, manter_proporcoes=True):
        """Redimensiona imagem"""
        val = validar_arquivo(arquivo, self.tipo)
        if not val['valido']:
            raise ValueError(val['erro'])

        val_dim = validar_dimensoes(largura, altura)
        if not val_dim['valido']:
            raise ValueError(val_dim['erro'])

        arquivo = Path(arquivo)
        largura, altura = int(largura), int(altura)

        self.logger.info(f"Redimensionando {arquivo} para {largura}x{altura}")

        try:
            img = Image.open(arquivo)

            if manter_proporcoes:
                img.thumbnail((largura, altura), Image.Resampling.LANCZOS)
            else:
                img = img.resize((largura, altura), Image.Resampling.LANCZOS)

            arquivo_saida = gerar_nome_saida(arquivo, "_resized")
            img.save(arquivo_saida, optimize=True)

            self.logger.info(f"Sucesso: {arquivo_saida}")
            return arquivo_saida

        except Exception as e:
            self.logger.error(f"Erro no redimensionamento: {e}")
            raise
