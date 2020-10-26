# -*- mode: python -*-

block_cipher = pyi_crypto.PyiBlockCipher(key='Tx3gB5b#KlvY9j4$1fdC0xQgPo0u7')


a = Analysis(['main.py'],
             pathex=['C:\\Users\\root\\Desktop\\poster'],
             binaries=[],
             datas=[],
             hiddenimports=['sys', 'os', 'urlparse', 'random', 'time', 'json', 'base64', 'functools', 'binascii', 'datetime', 'struct', 'warnings', 'win32com.client', 'pywintypes', 're', 'uuid', 'socket', 'win32api', 'requests', 'sip', 'PyQt4.QtCore', 'PyQt4.QtGui', 'PyQt4.QtNetwork', 'PyQt4.QtWebKit', 'PyQt4.QtSvg', 'PyQt4.QtXml', 'Crypto.PublicKey.RSA', 'Crypto.Signature.PKCS1_v1_5', 'Crypto.Hash.SHA256', 'Crypto.Random', 'poster.common.consts', 'poster.common.utils', 'poster.facebook.profile', 'poster.facebook.postertask', 'poster.facebook.poster', 'poster.facebook.post', 'poster.facebook.graph', 'poster.facebook.fetcher', 'poster.facebook.exceptions', 'poster.facebook.datamanager', 'poster.gui.ui_poster', 'poster.gui.ui_postdata', 'poster.gui.ui_licensing', 'poster.gui.ui_licenserequest', 'poster.gui.ui_busydialog', 'poster.gui.ui_about', 'poster.gui.tokenupdater', 'poster.gui.resources_rc', 'poster.gui.posterui', 'poster.gui.postdataui', 'poster.gui.loginui', 'poster.gui.licensingdialog', 'poster.gui.licenserequestdialog', 'poster.gui.fakelicensedialog', 'poster.gui.busydialog', 'poster.licensing.request', 'poster.licensing.licenser', 'poster.licensing.license', 'poster.licensing.cipher', 'poster.licensing._utils', 'poster.logging.logger', 'poster.packages.wmi', 'poster.packages.ntplib'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='poster',
          debug=False,
          strip=False,
          upx=True,
          console=False , version='versioninfo.py', icon='icon.ico')
