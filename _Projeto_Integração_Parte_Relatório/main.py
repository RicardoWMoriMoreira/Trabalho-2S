from Model import model as md
from View_and_Interface import view as vw
import controler as ctl
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs


def main():
    print("SISTEMA DE GESTÃO DE BIBLIOTECA")
    servidor = HTTPServer(("localhost", 8000), vw.BibliotecaController)
    servidor.serve_forever()


if __name__ == "__main__":
    main()
