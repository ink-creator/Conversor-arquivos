# File Converter

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![pywebview](https://img.shields.io/badge/pywebview-Desktop%20UI-blue)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![PyInstaller](https://img.shields.io/badge/PyInstaller-Windows%20EXE-lightgrey)
![MIT License](https://img.shields.io/badge/License-MIT-green)

[Windows installer](https://github.com/ink-creator/Conversor-arquivos/releases/latest) · [Demo video](assets/demo/conversor-arquivos-demo.mp4) · [Português](README.pt-BR.md)

Convert documents, structured data, and images through a simple desktop interface built with Python and pywebview.

![File Converter overview](assets/screenshots/files-overview.png)

## Demo

[![Watch the File Converter demo](assets/screenshots/files-overview.png)](assets/demo/conversor-arquivos-demo.mp4)

[Watch or download the demo video](assets/demo/conversor-arquivos-demo.mp4)

## Features

- Convert common document formats.
- Convert structured-data formats used by spreadsheets, APIs, and configuration files.
- Convert images between popular formats.
- Compress and resize images.
- Process multiple compatible files in batch.
- Detect the selected file format and show compatible output options.
- Choose a shared output folder for batch operations.
- Handle name conflicts with rename, overwrite, or skip policies.
- Open the converted file or its destination folder after processing.
- Run as a native desktop application through pywebview.
- Use the compiled Windows executable without installing Python.

### File Conversion

Select a file and the application automatically displays the compatible output formats.

The workflow is intentionally simple: choose the input, select an available conversion, and let the application create the new file.

![File conversion](assets/screenshots/files-conversion.png)

### Image Conversion and Tools

The Images tab supports format conversion as well as dedicated tools for compression and resizing.

After a successful conversion, shortcuts are available to open the generated file, open its folder, or start a new conversion.

![Image conversion and tools](assets/screenshots/images-conversion.png)

## Supported Formats

### Documents

Supported document formats include:

- TXT
- PDF
- DOCX
- HTML
- RTF

Available conversions include:

```text
TXT  → PDF
TXT  → DOCX

PDF  → TXT
PDF  → DOCX

DOCX → TXT
DOCX → PDF

HTML → PDF
HTML → TXT

RTF  → TXT
```

> [!NOTE]
> PDF and DOCX conversions are primarily text and paragraph based. Complex layouts, columns, and advanced tables may not be preserved exactly.

### Structured Data

Supported structured-data formats include:

- CSV
- JSON
- XML
- XLSX
- YAML

Available conversions include:

```text
CSV  ↔ JSON
CSV  ↔ XML
CSV  ↔ XLSX

JSON ↔ XML
JSON ↔ XLSX
JSON ↔ YAML

XML  ↔ YAML

XLSX ↔ JSON
```

### Images

Supported image formats include:

- PNG
- JPG
- JPEG
- WEBP
- BMP
- GIF

Images can be converted between compatible supported formats directly from the application.

## Batch Conversion

Multiple compatible files can be processed as a queue.

Each item can show whether it is waiting, being processed, completed, skipped, or failed. The queue continues processing the remaining files even if one item fails.

The output can be saved beside the original files or in a selected destination folder.

Conflict policies include:

- **Rename**
- **Overwrite**
- **Skip**

## Image Tools

### Compression

Images can be compressed with an adjustable quality value.

### Resize

Images can be resized by defining:

- Width
- Height
- Whether the original aspect ratio should be preserved

## Conversion Workflow

```text
Select one or more files
        ↓
Detect input format
        ↓
Show compatible outputs
        ↓
Choose conversion
        ↓
Choose destination and conflict policy
        ↓
Process conversion
        ↓
Open file or folder
```

## Smart Format Detection

When a file is selected, File Converter reads its extension and shows only compatible conversion options.

If the selected file belongs to another category, the interface can direct the workflow to the appropriate tab.

## After Conversion

After a successful operation, the application can provide shortcuts to:

- Open the converted file
- Open the destination folder
- Start a new conversion

Batch format conversions preserve the original base name and change the extension. The **Rename** conflict policy adds a numeric suffix when necessary.

Image tools can use suffixes such as:

```text
_converted
_compressed
_resized
```

## Windows Installer

A compiled Windows version is available through GitHub Releases.

[Download the latest Windows release](https://github.com/ink-creator/Conversor-arquivos/releases/latest)

The current release is **v1.0.1**, distributed as `Conversor.exe`.

Users of the executable do not need to install Python.

> [!NOTE]
> The application uses pywebview. On Windows, a WebView environment is required. On most updated Windows 10 and Windows 11 installations, Microsoft Edge WebView2 is already available.

## Running from Source

Clone the repository:

```bash
git clone https://github.com/ink-creator/Conversor-arquivos.git
cd Conversor-arquivos
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

## Building the Executable

The repository includes a PyInstaller configuration:

```text
build.spec
```

Build the desktop executable with:

```bash
pyinstaller build.spec
```

## Main Dependencies

- pywebview
- Pillow
- python-docx
- pypdf
- xhtml2pdf
- striprtf
- openpyxl
- PyYAML
- PyInstaller

## Technologies

Python, HTML, CSS, JavaScript, pywebview, PyInstaller, filesystem APIs, document-processing libraries, structured-data libraries, and image-processing libraries.

<details>
<summary>Project Structure</summary>

```text
Conversor-arquivos/
├── assets/
│   ├── demo/
│   │   └── conversor-arquivos-demo.mp4
│   └── screenshots/
│       ├── files-overview.png
│       ├── files-conversion.png
│       └── images-conversion.png
├── converters/
│   ├── document.py
│   ├── data.py
│   └── image.py
├── interface/
├── logs/
├── utils/
├── app.py
├── build.spec
├── requirements.txt
├── README.md
├── README.pt-BR.md
└── LICENSE
```

</details>

## License

Distributed under the [MIT License](LICENSE).
