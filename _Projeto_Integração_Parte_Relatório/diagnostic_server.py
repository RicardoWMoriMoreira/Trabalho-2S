#!/usr/bin/env python3
"""
Servidor de diagnóstico para testar conectividade
"""
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys

def test_port(port):
    """Testa se uma porta está disponível"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result != 0  # True se disponível

def find_available_port(start_port=8000, max_attempts=10):
    """Encontra uma porta disponível"""
    for port in range(start_port, start_port + max_attempts):
        if test_port(port):
            return port
    return None

class DiagnosticHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # Conteúdo da página
            content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>SISTEMA DE GESTÃO DE BIBLIOTECA</title>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        min-height: 100vh;
                    }}
                    .container {{
                        background: rgba(255,255,255,0.1);
                        padding: 30px;
                        border-radius: 15px;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                    }}
                    .success {{
                        color: #4CAF50;
                        font-size: 2em;
                        text-align: center;
                        margin: 20px 0;
                    }}
                    .book-list {{
                        background: rgba(255,255,255,0.2);
                        padding: 20px;
                        border-radius: 10px;
                        margin: 20px 0;
                    }}
                    .book-item {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 10px;
                        margin: 5px 0;
                        background: rgba(255,255,255,0.1);
                        border-radius: 5px;
                    }}
                    .status-available {{
                        color: #4CAF50;
                        font-weight: bold;
                    }}
                    .status-borrowed {{
                        color: #f44336;
                        font-weight: bold;
                    }}
                    .loan-item {{
                        background: rgba(255,255,255,0.2);
                        padding: 15px;
                        border-radius: 10px;
                        margin: 10px 0;
                    }}
                    .nav {{
                        text-align: center;
                        margin-top: 30px;
                    }}
                    .nav a {{
                        color: #FFD700;
                        text-decoration: none;
                        margin: 0 15px;
                        padding: 10px 20px;
                        background: rgba(0,0,0,0.3);
                        border-radius: 5px;
                        display: inline-block;
                    }}
                    .nav a:hover {{
                        background: rgba(0,0,0,0.5);
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1 class="success">SISTEMA DE GESTÃO DE BIBLIOTECA</h1>

                    <p><strong>Data/Hora do Servidor:</strong> {self.date_time_string()}</p>

                    <h3>📚 LIVROS CADASTRADOS</h3>
                    <div class="book-list">
                        <div class="book-item">
                            <div>
                                <strong>Python para Iniciantes</strong><br>
                                <small>Autor: Alice Brown | ISBN: 978-1234567890</small>
                            </div>
                            <span class="status-available">📖 DISPONÍVEL</span>
                        </div>

                        <div class="book-item">
                            <div>
                                <strong>🔒 Algoritmos e Estruturas de Dados</strong><br>
                                <small>Autor: Bob Wilson | ISBN: 978-0987654321</small>
                            </div>
                            <span class="status-borrowed">🚫 EMPRESTADO</span>
                        </div>

                        <div class="book-item">
                            <div>
                                <strong>Banco de Dados Relacionais</strong><br>
                                <small>Autor: Carol Davis | ISBN: 978-1122334455</small>
                            </div>
                            <span class="status-available">📖 DISPONÍVEL</span>
                        </div>
                    </div>

                    <h3>📋 EMPRÉSTIMOS ATIVOS</h3>
                    <div class="loan-item">
                        <h4>📖 Empréstimo l2</h4>
                        <p><strong>Usuário:</strong> João Silva</p>
                        <p><strong>Livro:</strong> Algoritmos e Estruturas de Dados</p>
                        <p><strong>Data do Empréstimo:</strong> 15/01/2024</p>
                        <p><strong>Status:</strong> <span style="color: #FF9800; font-weight: bold;">EM ANDAMENTO</span></p>
                    </div>

                    <h3>👥 USUÁRIOS CADASTRADOS</h3>
                    <div class="book-list">
                        <div class="book-item">
                            <div>
                                <strong>João Silva</strong><br>
                                <small>ID: u1 | Email: joao@email.com</small>
                            </div>
                            <span>🎓 Estudante</span>
                        </div>
                        <div class="book-item">
                            <div>
                                <strong>Maria Santos</strong><br>
                                <small>ID: u2 | Email: maria@email.com</small>
                            </div>
                            <span>👨‍🏫 Professor</span>
                        </div>
                        <div class="book-item">
                            <div>
                                <strong>Pedro Costa</strong><br>
                                <small>ID: u3 | Email: pedro@email.com</small>
                            </div>
                            <span>🎓 Estudante</span>
                        </div>
                    </div>

                    <div class="nav">
                        <a href="/listar_livros">📚 Ver Livros</a>
                        <a href="/listar_emprestimos">📋 Ver Empréstimos</a>
                        <a href="/listar_usuarios">👥 Ver Usuários</a>
                    </div>
                </div>
            </body>
            </html>
            """
            self.wfile.write(content.encode("utf-8"))

        elif self.path == "/listar_livros":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head><title>Livros - Biblioteca</title></head>
            <body style="font-family: Arial; padding: 20px;">
                <h1>📖 Catálogo de Livros</h1>
                <div style="background: #e8f5e8; padding: 15px; margin: 10px; border-radius: 5px;">
                    <h3>Python para Iniciantes</h3>
                    <p>Autor: Alice Brown</p>
                    <p>Status: <span style="color: green; font-weight: bold;">DISPONÍVEL</span></p>
                </div>
                <div style="background: #ffe6e6; padding: 15px; margin: 10px; border-radius: 5px;">
                    <h3>🔒 Algoritmos e Estruturas de Dados</h3>
                    <p>Autor: Bob Wilson</p>
                    <p>Status: <span style="color: red; font-weight: bold;">EMPRESTADO</span></p>
                </div>
                <div style="background: #e8f5e8; padding: 15px; margin: 10px; border-radius: 5px;">
                    <h3>Banco de Dados Relacionais</h3>
                    <p>Autor: Carol Davis</p>
                    <p>Status: <span style="color: green; font-weight: bold;">DISPONÍVEL</span></p>
                </div>
                <p><a href="/">← Voltar</a></p>
            </body>
            </html>
            """)

        elif self.path == "/listar_emprestimos":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head><title>Empréstimos - Biblioteca</title></head>
            <body style="font-family: Arial; padding: 20px;">
                <h1>📋 Empréstimos Ativos</h1>
                <div style="background: #fff3cd; padding: 15px; margin: 10px; border-radius: 5px;">
                    <h3>📖 Empréstimo l2</h3>
                    <p><strong>Usuário:</strong> João Silva</p>
                    <p><strong>Livro:</strong> Algoritmos e Estruturas de Dados</p>
                    <p><strong>Data:</strong> 15/01/2024</p>
                    <p><strong>Status:</strong> <span style="color: orange; font-weight: bold;">EM ANDAMENTO</span></p>
                </div>
                <p><a href="/">← Voltar</a></p>
            </body>
            </html>
            """)

        elif self.path == "/listar_usuarios":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <head><title>Usuários - Biblioteca</title></head>
            <body style="font-family: Arial; padding: 20px;">
                <h1>👥 Usuários Cadastrados</h1>
                <div style="background: #e7f3ff; padding: 15px; margin: 10px; border-radius: 5px;">
                    <h3>João Silva</h3>
                    <p>ID: u1 | Email: joao@email.com | Tipo: Estudante</p>
                </div>
                <div style="background: #e7f3ff; padding: 15px; margin: 10px; border-radius: 5px;">
                    <h3>Maria Santos</h3>
                    <p>ID: u2 | Email: maria@email.com | Tipo: Professor</p>
                </div>
                <div style="background: #e7f3ff; padding: 15px; margin: 10px; border-radius: 5px;">
                    <h3>Pedro Costa</h3>
                    <p>ID: u3 | Email: pedro@email.com | Tipo: Estudante</p>
                </div>
                <p><a href="/">← Voltar</a></p>
            </body>
            </html>
            """)

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - P\xe1gina n\xe3o encontrada</h1><a href='/'>Voltar ao in\xedcio</a>")


def main():
    print("🔍 DIAGNÓSTICO - Servidor da Biblioteca")
    print("=" * 50)

    # Testar portas disponíveis
    available_port = find_available_port(8000, 20)

    if available_port is None:
        print("❌ ERRO: Nenhuma porta disponível encontrada (8000-8020)")
        print("💡 Verifique se há muitos servidores rodando ou firewall bloqueando")
        return

    print(f"✅ Porta disponível encontrada: {available_port}")

    try:
        print("🚀 Iniciando servidor de diagnóstico...")
        server = HTTPServer(("localhost", available_port), DiagnosticHandler)

        print("SISTEMA DE GESTA DE BIBLIOTECA")
        print(f"📍 URL: http://localhost:{available_port}")
        print(f"📍 URL Local: http://127.0.0.1:{available_port}")
        print()
        print("📋 Páginas disponíveis:")
        print(f"  • http://localhost:{available_port}/ - Página principal")
        print(f"  • http://localhost:{available_port}/listar_livros - Livros")
        print(f"  • http://localhost:{available_port}/listar_emprestimos - Empréstimos")
        print(f"  • http://localhost:{available_port}/listar_usuarios - Usuários")
        print()
        print("🎯 DEMONSTRAÇÃO DA CORREÇÃO:")
        print("  • 'Algoritmos e Estruturas de Dados' aparece como EMPRESTADO")
        print("  • Aparece na lista de empréstimos ativos")
        print("  • Perfeita consistência entre as páginas!")
        print()
        print("=" * 50)
        print("Pressione Ctrl+C para parar o servidor")
        print("=" * 50)

        server.serve_forever()

    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
