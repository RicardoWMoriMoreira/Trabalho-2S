#!/usr/bin/env python3
"""
Script para limpar usuários inválidos do banco de dados
"""
from config.database import db_config

def clean_invalid_users():
    """Remove usuários com campos vazios ou inválidos"""
    print("=== LIMPANDO USUÁRIOS INVÁLIDOS ===")

    # Conectar ao banco
    if not db_config.connect():
        print("ERRO: Falha ao conectar ao banco")
        return False

    try:
        users_collection = db_config.users_collection

        # Buscar todos os usuários
        all_users = list(users_collection.find())
        print(f"Encontrados {len(all_users)} usuários no total")

        users_to_delete = []

        for user_doc in all_users:
            user_id = user_doc.get('id', '').strip()
            user_name = user_doc.get('name', '').strip()
            user_email = user_doc.get('email', '').strip()
            user_type = user_doc.get('type', '').strip()

            # Verificar se algum campo obrigatório está vazio
            if not user_id or not user_name or not user_email or not user_type:
                users_to_delete.append(user_doc['_id'])
                print(f"Usuário inválido encontrado - ID: '{user_id}', Nome: '{user_name}', Email: '{user_email}', Tipo: '{user_type}'")

        if users_to_delete:
            # Remover usuários inválidos
            result = users_collection.delete_many({"_id": {"$in": users_to_delete}})
            print(f"Removidos {result.deleted_count} usuários inválidos")
        else:
            print("Nenhum usuário inválido encontrado")

        # Verificar quantos usuários válidos restaram
        valid_users_count = users_collection.count_documents({
            "id": {"$ne": "", "$exists": True},
            "name": {"$ne": "", "$exists": True},
            "email": {"$ne": "", "$exists": True},
            "type": {"$ne": "", "$exists": True}
        })
        print(f"Usuários válidos restantes: {valid_users_count}")

        return True

    except Exception as e:
        print(f"ERRO: Falha ao limpar usuários: {e}")
        return False

    finally:
        db_config.disconnect()

if __name__ == "__main__":
    clean_invalid_users()
