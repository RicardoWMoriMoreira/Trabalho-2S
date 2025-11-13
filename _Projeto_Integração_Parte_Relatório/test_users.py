#!/usr/bin/env python3
"""
Script para testar a listagem de usuários
"""
from Model.model import db_manager

def test_listar_usuarios():
    """Testa a listagem de usuários"""
    print("=== TESTANDO LISTAGEM DE USUÁRIOS ===")

    # Conectar ao banco
    if not db_manager.connect():
        print("❌ Falha ao conectar ao banco")
        return

    try:
        # Buscar usuários
        usuarios = db_manager.get_usuarios()
        print(f"Encontrados {len(usuarios)} usuários:")

        for i, usuario in enumerate(usuarios, 1):
            print(f"{i}. ID: '{usuario.id}', Nome: '{usuario.name}', Email: '{usuario.email}', Tipo: '{usuario.type}'")

        # Verificar se há dados vazios
        usuarios_com_problemas = [u for u in usuarios if not u.id or not u.name or not u.email or not u.type]
        if usuarios_com_problemas:
            print("\nATENCAO: Usuarios com dados vazios:")
            for usuario in usuarios_com_problemas:
                print(f"   ID: '{usuario.id}', Nome: '{usuario.name}', Email: '{usuario.email}', Tipo: '{usuario.type}'")
        else:
            print("\nSISTEMA DE GESTA DE BIBLIOTECA")

    except Exception as e:
        print(f"❌ Erro ao testar usuários: {e}")

    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    test_listar_usuarios()
