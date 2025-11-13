#!/usr/bin/env python3
"""
Script para testar a conexão com MongoDB
"""
from Model.model import db_manager

def test_mongodb_connection():
    """Testa a conexão com MongoDB e operações básicas"""
    print("🧪 Testando conexão com MongoDB...")
    print("=" * 50)

    # Testar conexão
    if not db_manager.connect():
        print("❌ Falha na conexão com MongoDB")
        return False

    try:
        # Testar busca de dados
        print("📊 Testando operações de leitura...")

        usuarios = db_manager.get_usuarios()
        livros = db_manager.get_livros()
        emprestimos = db_manager.get_emprestimos()

        print(f"✅ Usuários encontrados: {len(usuarios)}")
        print(f"✅ Livros encontrados: {len(livros)}")
        print(f"✅ Empréstimos encontrados: {len(emprestimos)}")

        # Mostrar alguns dados de exemplo
        if usuarios:
            print(f"👤 Primeiro usuário: {usuarios[0].name} ({usuarios[0].email})")

        if livros:
            print(f"📖 Primeiro livro: {livros[0].title} - {livros[0].author}")

        if emprestimos:
            print(f"🔄 Primeiro empréstimo: {emprestimos[0].id} - Usuário: {emprestimos[0].user_id}")

        print("\n✅ Todos os testes passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro durante os testes: {e}")
        return False

    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    success = test_mongodb_connection()
    if success:
        print("\nSISTEMA DE GESTA DE BIBLIOTECA")
        print("📝 Você pode executar a aplicação com: python src/main.py")
    else:
        print("\n❌ Problemas com MongoDB. Verifique a instalação e configuração.")
