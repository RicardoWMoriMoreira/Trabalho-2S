"""
Configuração do banco de dados MongoDB
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DatabaseConfig:
    def __init__(self):
        # Configurações padrão do MongoDB
        self.mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('DATABASE_NAME', 'biblioteca_universitaria')

        # Nomes das coleções
        self.collection_users = os.getenv('COLLECTION_USERS', 'usuarios')
        self.collection_books = os.getenv('COLLECTION_BOOKS', 'livros')
        self.collection_loans = os.getenv('COLLECTION_LOANS', 'emprestimos')

        # Cliente MongoDB
        self.client = None
        self.db = None

    def connect(self):
        """Conecta ao MongoDB"""
        try:
            self.client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.database_name]

            # Testa a conexão
            self.client.admin.command('ping')
            print(f"SISTEMA DE GESTA DE BIBLIOTECA")
            print(f"Banco de dados: {self.database_name}")
            return True

        except ConnectionFailure as e:
            print(f"ERRO: Falha ao conectar ao MongoDB: {e}")
            print("Verifique se o MongoDB esta rodando.")
            print("Para instalar MongoDB:")
            print("  Windows: https://www.mongodb.com/try/download/community")
            print("  Linux: sudo apt install mongodb")
            print("  macOS: brew install mongodb-community")
            return False
        except Exception as e:
            print(f"ERRO inesperado na conexao: {e}")
            return False

    def disconnect(self):
        """Desconecta do MongoDB"""
        if self.client:
            self.client.close()
            print("DESCONECTADO: MongoDB")

    def get_collection(self, collection_name):
        """Retorna uma coleção específica"""
        if self.db is None:
            raise Exception("Banco de dados não conectado. Chame connect() primeiro.")
        # Garantir que a collection existe
        if collection_name not in self.db.list_collection_names():
            print(f"Criando collection: {collection_name}")
        return self.db[collection_name]

    # Métodos específicos para cada coleção
    @property
    def users_collection(self):
        return self.get_collection(self.collection_users)

    @property
    def books_collection(self):
        return self.get_collection(self.collection_books)

    @property
    def loans_collection(self):
        return self.get_collection(self.collection_loans)

# Instância global da configuração
db_config = DatabaseConfig()
