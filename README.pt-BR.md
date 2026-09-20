# Conversor de Arquivos

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![pywebview](https://img.shields.io/badge/pywebview-Desktop%20UI-blue)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![PyInstaller](https://img.shields.io/badge/PyInstaller-Windows%20EXE-lightgrey)
![MIT License](https://img.shields.io/badge/License-MIT-green)

[Instalador para Windows](https://github.com/ink-creator/Conversor-arquivos/releases/latest) · [Vídeo de demonstração](assets/demo/conversor-arquivos-demo.mp4) · [English](README.md)

Converta documentos, dados estruturados e imagens através de uma interface desktop simples construída com Python e pywebview.

![Visão geral do Conversor de Arquivos](assets/screenshots/files-overview.png)

## Demonstração

[![Assistir à demonstração do Conversor de Arquivos](assets/screenshots/files-overview.png)](assets/demo/conversor-arquivos-demo.mp4)

[Assistir ou baixar o vídeo de demonstração](assets/demo/conversor-arquivos-demo.mp4)

## Funcionalidades

- Converta formatos comuns de documentos.
- Converta formatos de dados usados por planilhas, APIs e arquivos de configuração.
- Converta imagens entre formatos populares.
- Comprima e redimensione imagens.
- Processe vários arquivos compatíveis em lote.
- Detecte o formato selecionado e mostre apenas saídas compatíveis.
- Escolha uma pasta de saída compartilhada para operações em lote.
- Resolva conflitos de nomes com políticas de renomear, sobrescrever ou ignorar.
- Abra o arquivo convertido ou sua pasta após o processamento.
- Execute o programa como aplicação desktop através do pywebview.
- Utilize o executável do Windows sem precisar instalar Python.

### Conversão de Arquivos

Selecione um arquivo e o aplicativo mostra automaticamente os formatos de saída compatíveis.

O fluxo é propositalmente simples: escolha a entrada, selecione uma conversão disponível e deixe o programa criar o novo arquivo.

![Conversão de arquivos](assets/screenshots/files-conversion.png)

### Conversão e Ferramentas de Imagem

A aba de imagens suporta conversão de formatos e também possui ferramentas específicas para compressão e redimensionamento.

Depois de uma conversão bem-sucedida, há atalhos para abrir o arquivo gerado, abrir sua pasta ou iniciar uma nova conversão.

![Conversão e ferramentas de imagem](assets/screenshots/images-conversion.png)

## Formatos Suportados

### Documentos

Os formatos de documento suportados incluem:

- TXT
- PDF
- DOCX
- HTML
- RTF

As conversões disponíveis incluem:

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
> As conversões de PDF e DOCX são principalmente baseadas em texto e parágrafos. Layouts complexos, colunas e tabelas avançadas podem não ser preservados exatamente.

### Dados Estruturados

Os formatos de dados suportados incluem:

- CSV
- JSON
- XML
- XLSX
- YAML

As conversões disponíveis incluem:

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

### Imagens

Os formatos de imagem suportados incluem:

- PNG
- JPG
- JPEG
- WEBP
- BMP
- GIF

As imagens podem ser convertidas entre formatos compatíveis diretamente pela aplicação.

## Conversão em Lote

Vários arquivos compatíveis podem ser processados em uma fila.

Cada item pode indicar se está aguardando, sendo processado, concluído, ignorado ou se apresentou erro. A fila continua processando os demais arquivos mesmo que um deles falhe.

A saída pode ser salva ao lado dos arquivos originais ou em uma pasta escolhida.

As políticas de conflito incluem:

- **Renomear**
- **Sobrescrever**
- **Ignorar**

## Ferramentas de Imagem

### Compressão

Imagens podem ser comprimidas usando um nível de qualidade ajustável.

### Redimensionamento

Imagens podem ser redimensionadas definindo:

- Largura
- Altura
- Se a proporção original deve ser preservada

## Fluxo de Conversão

```text
Selecionar um ou mais arquivos
        ↓
Detectar formato de entrada
        ↓
Mostrar saídas compatíveis
        ↓
Escolher conversão
        ↓
Escolher destino e política de conflito
        ↓
Processar conversão
        ↓
Abrir arquivo ou pasta
```

## Detecção Automática de Formato

Quando um arquivo é selecionado, o Conversor de Arquivos lê sua extensão e mostra somente as opções de conversão compatíveis.

Caso o arquivo pertença a outra categoria, a interface pode direcionar o fluxo para a aba apropriada.

## Depois da Conversão

Após uma operação bem-sucedida, o aplicativo pode oferecer atalhos para:

- Abrir o arquivo convertido
- Abrir a pasta de destino
- Iniciar uma nova conversão

Conversões em lote preservam o nome-base original e alteram a extensão. A política **Renomear** adiciona um sufixo numérico quando necessário.

As ferramentas de imagem podem usar sufixos como:

```text
_converted
_compressed
_resized
```

## Instalador para Windows

Uma versão compilada para Windows está disponível através do GitHub Releases.

[Baixar a versão mais recente para Windows](https://github.com/ink-creator/Conversor-arquivos/releases/latest)

A versão atual é a **v1.0.1**, distribuída como `Conversor.exe`.

Quem utiliza o executável não precisa instalar Python.

> [!NOTE]
> A aplicação utiliza pywebview. No Windows, é necessário um ambiente WebView. Na maioria das instalações atualizadas do Windows 10 e Windows 11, o Microsoft Edge WebView2 já está disponível.

## Executando pelo Código-Fonte

Clone o repositório:

```bash
git clone https://github.com/ink-creator/Conversor-arquivos.git
cd Conversor-arquivos
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
python app.py
```

## Gerando o Executável

O repositório possui uma configuração do PyInstaller:

```text
build.spec
```

Gere o executável desktop com:

```bash
pyinstaller build.spec
```

## Principais Dependências

- pywebview
- Pillow
- python-docx
- pypdf
- xhtml2pdf
- striprtf
- openpyxl
- PyYAML
- PyInstaller

## Tecnologias

Python, HTML, CSS, JavaScript, pywebview, PyInstaller, APIs do sistema de arquivos, bibliotecas de processamento de documentos, dados estruturados e imagens.

<details>
<summary>Estrutura do Projeto</summary>

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

## Licença

Distribuído sob a [Licença MIT](LICENSE).
