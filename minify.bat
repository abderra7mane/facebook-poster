
@echo off
setlocal enabledelayedexpansion

set PATH=%CD%\tools;%PATH%

set tmp_dir=.tmp

if exist "%tmp_dir%" (
	rmdir /s /q "%tmp_dir%"
)
if exist minified (
	rmdir /s /q minified
)

echo.
echo minifying files ...
echo.

set files=main.py

set poster_dir=poster
set poster_files=__init__

set _dir=%poster_dir%
set _files=%poster_files%
for %%f in (%_files%) do (
	set files=!files! %_dir%\%%f.py
)

set common_dir=%poster_dir%\common
set common_files=utils consts __init__

set _dir=%common_dir%
set _files=%common_files%
for %%f in (%_files%) do (
	set files=!files! %_dir%\%%f.py
)

set facebook_dir=%poster_dir%\facebook
set facebook_files=profile postertask poster post graph fetcher exceptions datamanager __init__

set _dir=%facebook_dir%
set _files=%facebook_files%
for %%f in (%_files%) do (
	set files=!files! %_dir%\%%f.py
)

set gui_dir=%poster_dir%\gui
set gui_files=ui_poster ui_postdata ui_licensing ui_licenserequest ui_busydialog ui_about ui_settings tokenupdater settingsdialog resources_rc posterui postdataui loginui licensingdialog licenserequestdialog fakelicensedialog trialdialog busydialog __init__

set _dir=%gui_dir%
set _files=%gui_files%
for %%f in (%_files%) do (
	set files=!files! %_dir%\%%f.py
)

set licensing_dir=%poster_dir%\licensing
set licensing_files=_utils request licenser license cipher __init__

set _dir=%licensing_dir%
set _files=%licensing_files%
for %%f in (%_files%) do (
	set files=!files! %_dir%\%%f.py
)

set logging_dir=%poster_dir%\logging
set logging_files=logger __init__

set _dir=%logging_dir%
set _files=%logging_files%
for %%f in (%_files%) do (
	set files=!files! %_dir%\%%f.py
)

set packages_dir=%poster_dir%\packages
set packages_files=wmi ntplib __init__

set _dir=%packages_dir%
set _files=%packages_files%
for %%f in (%_files%) do (
	set files=!files! %_dir%\%%f.py
)

set options=--obfuscate-import-methods --obfuscate-builtins

call pyminifier -d %tmp_dir% %files%

echo.
echo rebuilding structure ...
echo.

set _dir=%tmp_dir%\%poster_dir%
set _files=%poster_files%
mkdir "%_dir%"
for %%f in (%_files%) do (
	if "%%f" == "__init__" (
		copy "%tmp_dir%\%%f.py" "%_dir%\"
	) else (
		move "%tmp_dir%\%%f.py" "%_dir%\"
	)
)

set _dir=%tmp_dir%\%common_dir%
set _files=%common_files%
mkdir "%_dir%"
for %%f in (%_files%) do (
	if "%%f" == "__init__" (
		copy "%tmp_dir%\%%f.py" "%_dir%\"
	) else (
		move "%tmp_dir%\%%f.py" "%_dir%\"
	)
)

set _dir=%tmp_dir%\%facebook_dir%
set _files=%facebook_files%
mkdir "%_dir%"
for %%f in (%_files%) do (
	if "%%f" == "__init__" (
		copy "%tmp_dir%\%%f.py" "%_dir%\"
	) else (
		move "%tmp_dir%\%%f.py" "%_dir%\"
	)
)

set _dir=%tmp_dir%\%gui_dir%
set _files=%gui_files%
mkdir "%_dir%"
for %%f in (%_files%) do (
	if "%%f" == "__init__" (
		copy "%tmp_dir%\%%f.py" "%_dir%\"
	) else (
		move "%tmp_dir%\%%f.py" "%_dir%\"
	)
)

set _dir=%tmp_dir%\%licensing_dir%
set _files=%licensing_files%
mkdir "%_dir%"
for %%f in (%_files%) do (
	if "%%f" == "__init__" (
		copy "%tmp_dir%\%%f.py" "%_dir%\"
	) else (
		move "%tmp_dir%\%%f.py" "%_dir%\"
	)
)

set _dir=%tmp_dir%\%logging_dir%
set _files=%logging_files%
mkdir "%_dir%"
for %%f in (%_files%) do (
	if "%%f" == "__init__" (
		copy "%tmp_dir%\%%f.py" "%_dir%\"
	) else (
		move "%tmp_dir%\%%f.py" "%_dir%\"
	)
)

set _dir=%tmp_dir%\%packages_dir%
set _files=%packages_files%
mkdir "%_dir%"
for %%f in (%_files%) do (
	if "%%f" == "__init__" (
		copy "%tmp_dir%\%%f.py" "%_dir%\"
	) else (
		move "%tmp_dir%\%%f.py" "%_dir%\"
	)
)

del "%tmp_dir%\__init__.py"
move "%tmp_dir%" minified

echo.
echo done
echo.
