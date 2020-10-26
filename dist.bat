
@echo off
setlocal enabledelayedexpansion

set PATH=%CD%\tools;%PATH%

echo.
echo building distribution file...
echo.

set script=main.py
set icon=icon.ico
set versioninfo=versioninfo.py
set key=Tx3gB5b#KlvY9j4$1fdC0xQgPo0u7
set output=poster
set options=--windowed --onefile

set modules=sys os urlparse random time json base64 functools binascii datetime struct warnings win32com.client pywintypes re uuid socket win32api requests sip "PyQt4.QtCore" "PyQt4.QtGui" "PyQt4.QtNetwork" "PyQt4.QtWebKit" "PyQt4.QtSvg" "PyQt4.QtXml" Crypto.PublicKey.RSA Crypto.Signature.PKCS1_v1_5 Crypto.Hash.SHA256 Crypto.Random "poster.common.consts" "poster.common.utils" "poster.facebook.profile" "poster.facebook.postertask" "poster.facebook.poster" "poster.facebook.post" "poster.facebook.graph" "poster.facebook.fetcher" "poster.facebook.exceptions" "poster.facebook.datamanager" "poster.gui.ui_poster" "poster.gui.ui_postdata" "poster.gui.ui_licensing" "poster.gui.ui_licenserequest" "poster.gui.ui_busydialog" "poster.gui.ui_about" "poster.gui.ui_settings" "poster.gui.tokenupdater" "poster.gui.settingsdialog" "poster.gui.resources_rc" "poster.gui.posterui" "poster.gui.postdataui" "poster.gui.loginui" "poster.gui.licensingdialog" "poster.gui.licenserequestdialog" "poster.gui.fakelicensedialog" "poster.gui.trialdialog" "poster.gui.busydialog" "poster.licensing.request" "poster.licensing.licenser" "poster.licensing.license" "poster.licensing.cipher" "poster.licensing._utils" "poster.logging.logger" "poster.packages.wmi" "poster.packages.ntplib"

set hidden=

for %%m in (%modules%) do (
	set hidden=!hidden! --hidden-import %%m
)

call pyinstaller %script% --name %output% --key %key% --icon %icon% --version-file %versioninfo% %options% %hidden%

echo.
echo done
echo.
