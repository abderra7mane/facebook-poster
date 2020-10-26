
@echo off
setlocal enabledelayedexpansion

echo.
echo building resource files...

echo.
echo building ui files...
echo.

set ui_folder=poster/rc/ui
set ui_build_folder=poster/gui
set ui_files=about busydialog postdata poster licensing licenserequest settings

for %%i in (%ui_files%) do (
	set ui_file=%ui_folder%/%%i.ui
	set ui_build_file=%ui_build_folder%/ui_%%i.py
	echo building !ui_file! -^> !ui_build_file!...
	call pyuic4 !ui_file! -o !ui_build_file!
)

echo.
echo building qrc files...
echo.

set qrc_folder=poster/rc/qrc
set qrc_build_folder=poster/gui
set qrc_files=resources

for %%i in (%qrc_files%) do (
	set qrc_file=%qrc_folder%/%%i.qrc
	set qrc_build_file=%qrc_build_folder%/%%i_rc.py
	echo building !qrc_file! -^> !qrc_build_file!...
	call pyrcc4 !qrc_file! -o !qrc_build_file!
)

echo.
echo done
echo.
