#!/usr/bin/env python3
"""
Servidor de teste simples para verificar se Python está funcionando
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

class TesteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SISTEMA DE GESTA DE BIBLIOTECA</title>
        </head>
        <body>
            <h1>SISTEMA DE GESTA DE BIBLIOTECA</h1>
            <p>Servidor de teste funcionando!</p>
            <p><a href="/menu">Ir para Menu</a></p>
        </body>
        </html>
        """

        self.wfile.write(html.encode('utf-8'))

def main():
    print("SISTEMA DE GESTA DE BIBLIOTECA")
    print("Servidor de teste iniciando...")

    try:
        server = HTTPServer(('localhost', 8000), TesteHandler)
        print("Servidor rodando em http://localhost:8000")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
