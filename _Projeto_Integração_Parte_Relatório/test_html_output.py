#!/usr/bin/env python3
"""
Script para testar a saída HTML da listagem de usuários
"""
from View_and_Interface import view as vw
from Controller.controller import Controller
import re

def test_html_output():
    """Testa a saída HTML da listagem de usuários"""
    print("=== TESTANDO SAÍDA HTML ===")

    # Simular a geração do HTML como no view.py
    controller = Controller()
    todos_usuarios = controller.get_usuarios()

    print(f"Total de usuários no banco: {len(todos_usuarios)}")

    # Aplicar o mesmo filtro usado no view.py
    usuarios_validos = []

    for u in todos_usuarios:
        # Verificar se todos os campos existem e não são vazios
        id_valido = u.id is not None and str(u.id).strip() != ""
        name_valido = u.name is not None and str(u.name).strip() != ""
        email_valido = u.email is not None and str(u.email).strip() != ""
        type_valido = u.type is not None and str(u.type).strip() != ""

        if id_valido and name_valido and email_valido and type_valido:
            usuarios_validos.append(u)
        else:
            print(f"Usuário filtrado: ID='{u.id}', Name='{u.name}', Email='{u.email}', Type='{u.type}'")

    print(f"Usuários válidos após filtro: {len(usuarios_validos)}")

    if not usuarios_validos:
        resposta = '<div class="no-users">Nenhum usuário cadastrado com dados completos.</div>'
        print("HTML gerado: ", resposta)
    else:
        resposta = ""
        for usuario in usuarios_validos:
            # Define o ícone baseado no tipo de usuário
            if usuario.type == "Professor":
                icon = "👨‍🏫"
            elif usuario.type == "Funcionário":
                icon = "👔"
            else:
                icon = "👨‍🎓"

            # Gerar o HTML do card (igual ao view.py)
            card_html = f"""
                    <div class="user-card">
                        <div class="user-icon">{icon}</div>
                        <div class="user-name">{vw._esc(usuario.name)}</div>
                        <div class="user-info">
                            <div class="user-info-item">
                                <span class="user-info-label">ID:</span>
                                <span class="user-info-value">{vw._esc(usuario.id)}</span>
                            </div>
                            <div class="user-info-item">
                                <span class="user-info-label">Email:</span>
                                <span class="user-info-value">{vw._esc(usuario.email)}</span>
                            </div>
                            <div class="user-info-item">
                                <span class="user-info-label">Tipo:</span>
                                <span class="user-info-value">{vw._esc(usuario.type)}</span>
                            </div>
                        </div>
                    </div>
                    """

            resposta += card_html

        print("HTML gerado (primeiros 500 caracteres):")
        print(resposta[:500])

        # Verificar se há algum problema na estrutura HTML
        if 'user-info-value"></span>' in resposta:
            print("\nATENCAO: Encontrados valores vazios no HTML!")
            # Mostrar as linhas problemáticas
            lines = resposta.split('\n')
            for i, line in enumerate(lines):
                if 'user-info-value"></span>' in line:
                    print(f"Linha {i+1}: {line.strip()}")

if __name__ == "__main__":
    test_html_output()
