# -*- mode: python -*-

block_cipher = None


a = Analysis(['PI-ICRAnalyzer.py'],
             pathex=['\\\\intranet.nscl.msu.edu\\files\\user\\sandler\\My Documents\\GitHub\\PI-ICR-Gui'],
             binaries=[],
             datas=[],
             hiddenimports=['sklearn.utils._cython_blas', 'sklearn.neighbors.typedefs','sklearn.neighbors.quad_tree', 'sklearn.tree', 'sklearn.tree._utils'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PI-ICRAnalyzer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
