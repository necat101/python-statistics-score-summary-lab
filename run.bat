@echo off
setlocal
cd /d "%~dp0"

echo == check.py ==
python check.py
if errorlevel 1 goto :fail
echo.
echo == unittest ==
python -m unittest -v
if errorlevel 1 goto :fail
goto :eof

:fail
exit /b %errorlevel%
