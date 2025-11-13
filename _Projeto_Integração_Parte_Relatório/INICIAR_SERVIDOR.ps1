# Script PowerShell para iniciar o servidor de diagnóstico
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "SISTEMA DE GESTA DE BIBLIOTECA" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está disponível
$pythonPath = "C:\Users\$env:USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe"
if (!(Test-Path $pythonPath)) {
    Write-Host "❌ Python não encontrado no caminho esperado" -ForegroundColor Red
    Write-Host "Tentando usar python do sistema..." -ForegroundColor Yellow
    $pythonPath = "python"
}

Write-Host "🚀 Iniciando servidor de diagnóstico..." -ForegroundColor Green
Write-Host ""

try {
    & $pythonPath "diagnostic_server.py"
} catch {
    Write-Host "❌ Erro ao executar o servidor: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Tente executar o arquivo DIAGNOSTICO.bat em vez deste" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Read-Host "Pressione Enter para sair"
