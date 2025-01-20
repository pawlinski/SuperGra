# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[("assets/fonts/Micro5-Regular.ttf", "assets/fonts/"), ("sounds/hurry-95692.mp3", "sounds/"), ("assets/swords_32.png", "assets/"), ("assets/viking_64.png", "assets/"), ("assets/ninja_64.png", "assets/"), ("assets/sword_32.png", "assets/"), ("sounds/sword-stab-pull-melee-weapon-236207.wav", "sounds/"), ("sounds/grunt2-85989.wav", "sounds/")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
