
@echo off
cls

set PATH=%CD%\tools;%PATH%

call minify

copy obfuscate.bat minified\
cd minified\
call obfuscate

copy ..\dist.bat obfuscated\
copy ..\icon.ico obfuscated\
copy ..\versioninfo.py obfuscated\
cd obfuscated\
call dist

cd ..\..\

if exist minified\obfuscated\dist\poster.exe (
	move minified\obfuscated\dist .
) else (
	echo no distribution file were built !!!
)

echo.
echo removing temporary files ...
echo.

rmdir /s /q minified

echo.
echo done
echo.
