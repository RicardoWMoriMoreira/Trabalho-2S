@echo off
echo ============================================
echo SISTEMA DE GESTA DE BIBLIOTECA
echo ============================================
echo.

echo Tentando iniciar o servidor Node.js...
echo.

cd /d "%~dp0"
node server.js

echo.
echo Servidor parado.
pause
