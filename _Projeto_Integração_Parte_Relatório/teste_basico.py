#!/usr/bin/env python3
"""
Arquivo de teste básico para verificar se o sistema está funcionando
"""

def testar_sistema():
    try:
        print("🔍 Testando imports básicos...")

        # Teste 1: Import básico do Python
        print("✅ Python OK")

        # Teste 2: Import do HTTP server
        from http.server import BaseHTTPRequestHandler, HTTPServer
        print("✅ HTTP Server OK")

        # Teste 3: Teste de path
        import sys
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent
        print(f"✅ Path OK: {BASE_DIR}")

        # Teste 4: Import do Model (básico)
        try:
            from Model import model as md
            print("✅ Model importado com sucesso")
        except Exception as e:
            print(f"❌ Erro no Model: {e}")
            return False

        # Teste 5: Import do Controller
        try:
            import controler as ctl
            print("✅ Controller importado com sucesso")
        except Exception as e:
            print(f"❌ Erro no Controller: {e}")
            return False

        # Teste 6: Instanciar controller
        try:
            controller = ctl.Controler(login_required=False)
            print("✅ Controller instanciado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao instanciar Controller: {e}")
            return False

        print("\n🎉 Todos os testes básicos passaram!")
        print("O problema pode estar na View ou ReportService")
        return True

    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    testar_sistema()
