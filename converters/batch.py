import os
import shutil
import tempfile
from pathlib import Path


class BatchConverter:
    """Run one conversion into an explicit output directory.

    Existing converters always write beside their input. Batch jobs therefore run
    from an isolated staging directory and publish only the completed output. This
    keeps source folders clean and makes conflict handling predictable.
    """

    CONVERSIONS = {
        "txt": {"pdf", "docx"},
        "pdf": {"txt", "docx"},
        "docx": {"txt", "pdf"},
        "html": {"pdf", "txt"},
        "rtf": {"txt"},
        "csv": {"json", "xml", "xlsx"},
        "json": {"csv", "xml", "xlsx", "yaml"},
        "xml": {"csv", "json", "yaml"},
        "xlsx": {"csv", "json"},
        "yaml": {"json", "xml"},
    }
    IMAGE_FORMATS = {"png", "jpg", "jpeg", "webp", "bmp", "gif"}
    POLICIES = {"sobrescrever", "renomear", "ignorar"}

    def __init__(self, document_converter, data_converter, image_converter):
        self.document_converter = document_converter
        self.data_converter = data_converter
        self.image_converter = image_converter

    @staticmethod
    def _normal_extension(extension):
        extension = str(extension).lower().lstrip(".")
        return {"htm": "html", "yml": "yaml"}.get(extension, extension)

    @staticmethod
    def _unique_path(path):
        if not path.exists():
            return path
        counter = 1
        while True:
            candidate = path.with_name(f"{path.stem} ({counter}){path.suffix}")
            if not candidate.exists():
                return candidate
            counter += 1

    def _target_path(self, source, operation, output_dir, policy):
        kind = operation.get("tipo")
        if kind == "converter":
            extension = self._normal_extension(operation.get("destino", ""))
            supported_outputs = self.IMAGE_FORMATS | {
                output for outputs in self.CONVERSIONS.values() for output in outputs
            }
            if extension not in supported_outputs:
                raise ValueError("Formato de saída não suportado")
            filename = f"{source.stem}.{extension}"
        elif kind == "comprimir":
            filename = f"{source.stem}_compressed{source.suffix.lower()}"
        elif kind == "redimensionar":
            filename = f"{source.stem}_resized{source.suffix.lower()}"
        else:
            raise ValueError("Operação em lote não suportada")

        target = output_dir / filename
        try:
            same_as_source = target.resolve() == source.resolve()
        except OSError:
            same_as_source = False
        if same_as_source:
            target = output_dir / f"{source.stem}_converted{target.suffix}"

        if target.exists():
            if policy == "ignorar":
                return target, True
            if policy == "renomear":
                target = self._unique_path(target)
        return target, False

    def _convert_staged(self, staged_source, operation):
        kind = operation.get("tipo")
        source_extension = self._normal_extension(staged_source.suffix)

        if kind == "converter":
            target_extension = self._normal_extension(operation.get("destino", ""))
            if source_extension in self.IMAGE_FORMATS:
                if target_extension not in self.IMAGE_FORMATS:
                    raise ValueError("Formato de saída não suportado")
                quality = int(operation.get("qualidade", 95))
                return self.image_converter.converter_formato(
                    staged_source, target_extension, quality
                )

            if target_extension not in self.CONVERSIONS.get(source_extension, set()):
                raise ValueError("Conversão não suportada")
            converter = (
                self.document_converter
                if source_extension in {"txt", "pdf", "docx", "html", "rtf"}
                else self.data_converter
            )
            method = getattr(converter, f"{source_extension}_para_{target_extension}")
            return method(staged_source)

        if source_extension not in self.IMAGE_FORMATS:
            raise ValueError("Esta operação aceita apenas imagens")
        if kind == "comprimir":
            output, _reduction = self.image_converter.comprimir(
                staged_source, int(operation.get("qualidade", 85))
            )
            return output
        if kind == "redimensionar":
            return self.image_converter.redimensionar(
                staged_source,
                operation.get("largura"),
                operation.get("altura"),
                bool(operation.get("manter_proporcoes", True)),
            )
        raise ValueError("Operação em lote não suportada")

    @staticmethod
    def _publish(staged_output, target):
        """Copy to the destination filesystem and atomically replace the target."""
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix=f".{target.stem}-", suffix=target.suffix, dir=target.parent, delete=False
            ) as handle:
                temporary = Path(handle.name)
            shutil.copy2(staged_output, temporary)
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def convert_item(self, arquivo, operacao, pasta_saida=None, conflito="renomear"):
        source = Path(arquivo)
        if not source.exists():
            raise ValueError("Arquivo não existe")
        if not source.is_file():
            raise ValueError("Caminho não é um arquivo")
        if conflito not in self.POLICIES:
            raise ValueError("Política de conflito inválida")
        if not isinstance(operacao, dict):
            raise ValueError("Operação em lote inválida")

        output_dir = Path(pasta_saida) if pasta_saida else source.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        target, skipped = self._target_path(source, operacao, output_dir, conflito)
        if skipped:
            return {"sucesso": True, "ignorado": True, "arquivo": str(target)}

        with tempfile.TemporaryDirectory(prefix="file-converter-") as staging:
            staged_source = Path(staging) / source.name
            shutil.copy2(source, staged_source)
            staged_output = Path(self._convert_staged(staged_source, operacao))
            self._publish(staged_output, target)

        return {
            "sucesso": True,
            "ignorado": False,
            "arquivo": str(target),
            "tamanho": target.stat().st_size,
        }
