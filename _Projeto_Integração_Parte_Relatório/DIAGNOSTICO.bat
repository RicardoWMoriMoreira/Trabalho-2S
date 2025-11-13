@echo off
cd /d "%~dp0"
echo.
echo ===========================================
echo 🔍 DIAGNÓSTICO - Biblioteca Universitária
echo ===========================================
echo.
echo Este arquivo executará um servidor de diagnóstico
echo que automaticamente encontra uma porta disponível
echo e demonstra que a correção está funcionando.
echo.
echo ===========================================
echo.
echo Iniciando diagnóstico...
echo.
"C:\Users\ri_wa\AppData\Local\Microsoft\WindowsApps\python.exe" diagnostic_server.py
echo.
echo ===========================================
echo DIAGNÓSTICO CONCLUÍDO
echo ===========================================
pause
