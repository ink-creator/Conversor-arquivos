# -*- mode: python ; coding: utf-8 -*-
# Build: pyinstaller build.spec
#
# Gera um único .exe (onefile, sem janela de console) com a pasta
# interface/ embutida. Recursos são lidos via utils/constants.py, que
# detecta sys._MEIPASS automaticamente quando rodando congelado.

from PyInstaller.utils.hooks import collect_all

datas = [('interface', 'interface')]
binaries = []
hiddenimports = []

# xhtml2pdf/reportlab/pyhanko usam alguns imports dinâmicos que o
# PyInstaller não detecta sozinho por análise estática.
for pacote in ('xhtml2pdf', 'reportlab', 'pyhanko', 'svglib'):
    d, b, h = collect_all(pacote)
    datas += d
    binaries += b
    hiddenimports += h

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Conversor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # sem janela de terminal (app gráfico)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icone.ico',  # descomente e aponte para um .ico se tiver um
)
