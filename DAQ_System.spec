"""
PyInstaller spec file for DAQ System
Builds a single .exe that includes frontend, backend, and connection folder
"""

block_cipher = None

# Include setuptools package files so pkg_resources runtime hook can find metadata
import setuptools
setuptools_path = os.path.dirname(setuptools.__file__)

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend', 'backend'),
        ('frontend', 'frontend'),
        ('connection', 'connection'),
        ('backend/.env', 'backend'),
        (setuptools_path, 'setuptools'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.font',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'tkinter.scrolledtext',
        'tkinter.constants',
        # Ensure HTTP client libraries used by the frontend are bundled
        'requests',
        'urllib3',
        'certifi',
        'idna',
        'charset_normalizer',
        'chardet',
        'uvicorn.lifespan.on',
        'uvicorn.protocols.http.flow_control',
        'sqlalchemy',
        'mysql.connector',
        'fastapi',
        'pydantic',
        'starlette',
        'setuptools',
        'pkg_resources',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Determine icon path (if it exists)
import os
icon_path = 'frontend/assets/icon.ico' if os.path.exists('frontend/assets/icon.ico') else None

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DAQ_System',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Build with no console window (GUI mode)
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DAQ_System'
)
