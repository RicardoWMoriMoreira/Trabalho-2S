#!/usr/bin/env python3
"""
Servidor HTTP simples para testar se funciona
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            response = f"""
            <html>
            <head><title>Teste Simples</title></head>
            <body>
                <h1>SISTEMA DE GESTÃO DE BIBLIOTECA</h1>
                <h2>Livros de Exemplo:</h2>
                <ul>
                    <li>📚 Python para Iniciantes - <strong>DISPONÍVEL</strong></li>
                    <li>🔒 Algoritmos e Estruturas de Dados - <strong>EMPRESTADO</strong></li>
                    <li>📚 Banco de Dados Relacionais - <strong>DISPONÍVEL</strong></li>
                </ul>
                <h2>Empréstimos Ativos:</h2>
                <ul>
                    <li>📖 Empréstimo l2 - Algoritmos e Estruturas de Dados (João Silva)</li>
                </ul>
                <p><a href="/menu">Ir para Menu</a></p>
            </body>
            </html>
            """
            self.wfile.write(response.encode("utf-8"))

        elif self.path == "/menu":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            response = """
            <html>
            <head><title>Menu - Biblioteca</title></head>
            <body>
                <h1>📚 Biblioteca Universitária</h1>
                <h2>Equipe 4</h2>
                <ul>
                    <li><a href="/">Página Inicial</a></li>
                    <li><a href="/listar_livros">📚 Listar Livros</a></li>
                    <li><a href="/listar_emprestimos">📋 Listar Empréstimos</a></li>
                    <li><a href="/listar_usuarios">👥 Listar Usuários</a></li>
                </ul>
            </body>
            </html>
            """
            self.wfile.write(response.encode("utf-8"))

        elif self.path == "/listar_livros":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            response = """
            <html>
            <head><title>Livros - Biblioteca</title></head>
            <body>
                <h1>📖 Catálogo de Livros</h1>
                <div style="background: #f0f0f0; padding: 20px; margin: 20px; border-radius: 10px;">
                    <h3>Python para Iniciantes</h3>
                    <p>Autor: Alice Brown</p>
                    <p>Status: <span style="color: green; font-weight: bold;">DISPONÍVEL</span></p>
                </div>
                <div style="background: #ffe6e6; padding: 20px; margin: 20px; border-radius: 10px;">
                    <h3>🔒 Algoritmos e Estruturas de Dados</h3>
                    <p>Autor: Bob Wilson</p>
                    <p>Status: <span style="color: red; font-weight: bold;">EMPRESTADO</span></p>
                </div>
                <div style="background: #f0f0f0; padding: 20px; margin: 20px; border-radius: 10px;">
                    <h3>Banco de Dados Relacionais</h3>
                    <p>Autor: Carol Davis</p>
                    <p>Status: <span style="color: green; font-weight: bold;">DISPONÍVEL</span></p>
                </div>
                <p><a href="/menu">← Voltar ao Menu</a></p>
            </body>
            </html>
            """
            self.wfile.write(response.encode("utf-8"))

        elif self.path == "/listar_emprestimos":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            response = f"""
            <html>
            <head><title>Empréstimos - Biblioteca</title></head>
            <body>
                <h1>📋 Controle de Empréstimos</h1>
                <div style="background: #fff3cd; padding: 20px; margin: 20px; border-radius: 10px;">
                    <h3>📖 Empréstimo l2</h3>
                    <p><strong>Usuário:</strong> João Silva</p>
                    <p><strong>Livro:</strong> Algoritmos e Estruturas de Dados</p>
                    <p><strong>Data:</strong> {datetime(2024, 1, 15).strftime('%d/%m/%Y')}</p>
                    <p><strong>Status:</strong> <span style="color: orange; font-weight: bold;">EM ANDAMENTO</span></p>
                </div>
                <p><a href="/menu">← Voltar ao Menu</a></p>
            </body>
            </html>
            """
            self.wfile.write(response.encode("utf-8"))

        elif self.path == "/listar_usuarios":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            response = """
            <html>
            <head><title>Usuários - Biblioteca</title></head>
            <body>
                <h1>👥 Usuários Cadastrados</h1>
                <div style="background: #e7f3ff; padding: 20px; margin: 20px; border-radius: 10px;">
                    <h3>João Silva</h3>
                    <p>ID: u1 | Email: joao@email.com | Tipo: Estudante</p>
                </div>
                <div style="background: #e7f3ff; padding: 20px; margin: 20px; border-radius: 10px;">
                    <h3>Maria Santos</h3>
                    <p>ID: u2 | Email: maria@email.com | Tipo: Professor</p>
                </div>
                <div style="background: #e7f3ff; padding: 20px; margin: 20px; border-radius: 10px;">
                    <h3>Pedro Costa</h3>
                    <p>ID: u3 | Email: pedro@email.com | Tipo: Estudante</p>
                </div>
                <p><a href="/menu">← Voltar ao Menu</a></p>
            </body>
            </html>
            """
            self.wfile.write(response.encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Pagina nao encontrada</h1><a href='/'>Voltar ao inicio</a>")


def main():
    print("🚀 Servidor Simples da Biblioteca")
    print("=" * 40)
    print("Iniciando servidor...")
    try:
        server = HTTPServer(("localhost", 8000), SimpleHandler)
        print("✅ Servidor rodando em http://localhost:8000")
        print("📋 Páginas disponíveis:")
        print("  http://localhost:8000/ - Página inicial")
        print("  http://localhost:8000/menu - Menu principal")
        print("  http://localhost:8000/listar_livros - Livros (com status correto)")
        print("  http://localhost:8000/listar_emprestimos - Empréstimos ativos")
        print("  http://localhost:8000/listar_usuarios - Usuários")
        print("=" * 40)
        print("Pressione Ctrl+C para parar o servidor")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")


if __name__ == "__main__":
    main()
