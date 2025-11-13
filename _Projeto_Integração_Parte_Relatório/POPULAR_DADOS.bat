@echo off
chcp 65001 >nul
echo ============================================
echo 🏗️  POPULADOR DE DADOS - Biblioteca
echo ============================================
echo.
echo Script para criar dados ricos de exemplo no MongoDB
echo.

REM Tentar executar com python
python populate_sample_data.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro ao executar com 'python'
    echo Tentando com 'python3'...
    echo.

    REM Tentar executar com python3
    python3 populate_sample_data.py

    if %errorlevel% neq 0 (
        echo.
        echo ❌ Erro ao executar com 'python3'
        echo.
        echo 💡 Possíveis soluções:
        echo 1. Verifique se o Python está instalado
        echo 2. Verifique se o MongoDB está rodando
        echo 3. Execute: pip install pymongo
        echo.
        goto :end
    )
)

:end
echo.
echo ============================================
pause
