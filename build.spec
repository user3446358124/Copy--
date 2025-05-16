# -*- mode: python -*-
import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['Main.py'],  # 替换为你的主程序文件名
    pathex=[],
    binaries=[],
    datas=[('rulesets', 'rulesets'),
    ('images/favicon.ico', 'images')
    ],  # 包含规则集目录
    hiddenimports=['chardet'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Copy--',  # 指定输出名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为True会显示控制台窗口
    icon='images\\favicon.ico'  # 可选图标文件
)
