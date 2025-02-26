# -*- mode: python ; coding: utf-8 -*-

import os

# Función para agregar archivos a la lista datas
def add_files_to_datas(directory, base_path=""):
    datas = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, directory)
            if relative_path == ".":
                dest_path = "."
            else:
                dest_path = relative_path
            datas.append((file_path, dest_path))
    return datas

# Lista de archivos adicionales
datas = []

# Agregar archivos de las carpetas necesarias
datas += add_files_to_datas("controllers")
datas += add_files_to_datas("views")
datas += add_files_to_datas("models")
datas += add_files_to_datas("patterns")
datas += add_files_to_datas("database")
datas += add_files_to_datas("img")

# Agregar el archivo de ícono
datas.append(("img/iconoinstitucional.ico", "."))

a = Analysis(
    ['main.py'],
    pathex=[],  # Agrega aquí la ruta de tu proyecto si es necesario
    binaries=[],
    datas=datas,  # Usar la lista de archivos adicionales
    hiddenimports=['wx', 'sqlalchemy', 'bcrypt'],  # Agrega las dependencias aquí
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    upx_dir="C:/upx-5.0.0-win64/upx",
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Cambia a True si es una aplicación de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/iconoinstitucional.ico',  # Especificar el ícono aquí
)