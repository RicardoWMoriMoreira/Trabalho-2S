# Script PowerShell para popular o banco com dados de exemplo
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "🏗️  POPULADOR DE DADOS - Biblioteca" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Script para criar dados ricos de exemplo no MongoDB" -ForegroundColor Yellow
Write-Host ""

# Verificar se Python está disponível
$pythonPath = "C:\Users\$env:USERNAME\AppData\Local\Microsoft\WindowsApps\python.exe"
if (!(Test-Path $pythonPath)) {
    Write-Host "❌ Python não encontrado no caminho esperado" -ForegroundColor Red
    Write-Host "Tentando usar python do sistema..." -ForegroundColor Yellow
    $pythonPath = "python"
}

Write-Host "🚀 Executando script de população de dados..." -ForegroundColor Green
Write-Host ""

try {
    & $pythonPath "populate_sample_data.py"
} catch {
    Write-Host "❌ Erro ao executar o script: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Possíveis soluções:" -ForegroundColor Yellow
    Write-Host "1. Verifique se o Python está instalado" -ForegroundColor White
    Write-Host "2. Verifique se o MongoDB está rodando" -ForegroundColor White
    Write-Host "3. Execute: pip install pymongo" -ForegroundColor White
    Write-Host "4. Tente executar o arquivo POPULAR_DADOS.bat em vez deste" -ForegroundColor White
}

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Read-Host "Pressione Enter para sair"
