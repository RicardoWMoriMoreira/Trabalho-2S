#!/usr/bin/env python3
"""
Script para limpar e reinicializar o banco de dados
"""
from config.database import db_config

def clean_database():
    """Limpa todas as coleções do banco de dados"""
    print("=== LIMPANDO BANCO DE DADOS ===")

    # Conectar ao banco
    if not db_config.connect():
        print("❌ Falha ao conectar ao banco")
        return False

    try:
        # Limpar todas as coleções
        db_config.users_collection.delete_many({})
        db_config.books_collection.delete_many({})
        db_config.loans_collection.delete_many({})

        print("SISTEMA DE GESTA DE BIBLIOTECA")
        return True

    except Exception as e:
        print(f"ERRO: Erro ao limpar banco: {e}")
        return False

    finally:
        db_config.disconnect()

if __name__ == "__main__":
    clean_database()
