@echo off
echo ============================================
echo SISTEMA DE GESTA DE BIBLIOTECA
echo ============================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo.
    echo ❌ ERRO: Python nao encontrado!
    echo.
    echo 📥 INSTALE PYTHON OFICIAL:
    echo    1. Acesse: https://www.python.org/downloads/
    echo    2. Baixe Python 3.11+
    echo    3. Marque "Add Python to PATH"
    echo    4. Instale e reinicie o terminal
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Python encontrado! Iniciando servidor...
echo.

cd /d "%~dp0"
python main.py

echo.
echo Servidor parado.
pause
