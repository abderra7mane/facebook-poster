
@echo off
setlocal enabledelayedexpansion

set PATH=%CD%\tools;%PATH%

echo.
echo obfuscating source files ...
echo.

set parent_dir=.
set output_dir=obfuscated

if exist "%output_dir%" (
	rmdir /s /q "%output_dir%"
)
mkdir "%output_dir%"

rem obfuscating *.py files

echo.
echo obfuscating %parent_dir%/*.py ...
echo.

set files=main

for %%f in (%files%) do (
	set input=%parent_dir%/%%f.py
	set output=%output_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

rem obfuscating poster/*.py files

set _dir=poster

echo.
echo obfuscating %parent_dir%/%_dir%/*.py ...
echo.

mkdir "%output_dir%/%_dir%"

set files=__init__

for %%f in (%files%) do (
	set input=%parent_dir%/%_dir%/%%f.py
	set output=%output_dir%/%_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

rem obfuscating common/*py files

set _dir=poster/common

echo.
echo obfuscating %parent_dir%/%_dir%/*.py ...
echo.

mkdir "%output_dir%/%_dir%"

set files=utils consts __init__

for %%f in (%files%) do (
	set input=%parent_dir%/%_dir%/%%f.py
	set output=%output_dir%/%_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

rem obfuscating facebook/*.py files

set _dir=poster/facebook

echo.
echo obfuscating %_dir%/*.py ...
echo.

mkdir "%output_dir%/%_dir%"

set files=profile postertask poster post graph fetcher exceptions datamanager __init__

for %%f in (%files%) do (
	set input=%parent_dir%/%_dir%/%%f.py
	set output=%output_dir%/%_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

rem obfuscating gui/*.py files

set _dir=poster/gui

echo.
echo obfuscating %_dir%/*.py ...
echo.

mkdir "%output_dir%/%_dir%"

set files=ui_poster ui_postdata ui_licensing ui_licenserequest ui_busydialog ui_about ui_settings tokenupdater settingsdialog posterui postdataui loginui licensingdialog licenserequestdialog fakelicensedialog trialdialog busydialog __init__

for %%f in (%files%) do (
	set input=%parent_dir%/%_dir%/%%f.py
	set output=%output_dir%/%_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

echo.
echo copying resources file ...
echo.

copy "%parent_dir%\poster\gui\resources_rc.py" "%output_dir%\poster\gui\"

rem obfuscating licensing/*.py files

set _dir=poster/licensing

echo.
echo obfuscating %_dir%/*.py ...
echo.

mkdir "%output_dir%/%_dir%"

set files=_utils request licenser license cipher __init__

for %%f in (%files%) do (
	set input=%parent_dir%/%_dir%/%%f.py
	set output=%output_dir%/%_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

rem obfuscating logging/*.py files

set _dir=poster/logging

echo.
echo obfuscating %_dir%/*.py ...
echo.

mkdir "%output_dir%/%_dir%"

set files=logger __init__

for %%f in (%files%) do (
	set input=%parent_dir%/%_dir%/%%f.py
	set output=%output_dir%/%_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

rem obfuscating packages/*.py files

set _dir=poster/packages

echo.
echo obfuscating %_dir%/*.py ...
echo.

mkdir "%output_dir%/%_dir%"

set files=wmi ntplib __init__

for %%f in (%files%) do (
	set input=%parent_dir%/%_dir%/%%f.py
	set output=%output_dir%/%_dir%/%%f.py
	echo obfuscating !input! -^> !output! ...
	call pyobf !input! !output!
)

echo.
echo done.
echo.
