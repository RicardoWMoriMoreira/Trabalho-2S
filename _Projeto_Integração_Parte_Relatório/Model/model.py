from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict

# Import opcional do MongoDB - funciona sem ele
try:
    from config.database import db_config
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    print("MongoDB não disponível - usando banco de dados em memória")


@dataclass
class User:
    id: str
    name: str
    email: str
    type: str

    def to_dict(self):
        """Converte o objeto para dicionário (para MongoDB)"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto User a partir de um dicionário (do MongoDB)"""
        # Filtra apenas os campos válidos para a classe User
        valid_fields = {'id', 'name', 'email', 'type'}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


@dataclass
class Book:
    id: str
    title: str
    author: str
    isbn: str
    available: bool

    def to_dict(self):
        """Converte o objeto para dicionário (para MongoDB)"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Book a partir de um dicionário (do MongoDB)"""
        # Filtra apenas os campos válidos para a classe Book
        valid_fields = {'id', 'title', 'author', 'isbn', 'available'}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        return cls(**filtered_data)


@dataclass
class Loan:
    id: str
    user_id: str
    book_id: str
    loan_date: datetime
    return_date: Optional[datetime] = None

    def to_dict(self):
        """Converte o objeto para dicionário (para MongoDB)"""
        data = asdict(self)
        # Converter datetime para string ISO para MongoDB
        data['loan_date'] = self.loan_date.isoformat()
        if self.return_date:
            data['return_date'] = self.return_date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Loan a partir de um dicionário (do MongoDB)"""
        # Filtra apenas os campos válidos para a classe Loan
        valid_fields = {'id', 'user_id', 'book_id', 'loan_date', 'return_date'}
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        # Converter strings ISO de volta para datetime
        if 'loan_date' in filtered_data:
            filtered_data['loan_date'] = datetime.fromisoformat(filtered_data['loan_date'])
        if filtered_data.get('return_date'):
            filtered_data['return_date'] = datetime.fromisoformat(filtered_data['return_date'])

        return cls(**filtered_data)


class DatabaseManager:
    """Gerenciador do banco de dados - MongoDB ou Memória"""

    def __init__(self):
        self.connected = False
        self.using_memory = not MONGODB_AVAILABLE

        # Dados em memória (fallback)
        self.memory_users = []
        self.memory_books = []
        self.memory_loans = []

    def connect(self):
        """Conecta ao banco de dados"""
        if self.using_memory:
            self.connected = True
            self.initialize_sample_data()
            return True
        else:
            self.connected = db_config.connect()
            if self.connected:
                self.initialize_sample_data()
            return self.connected

    def disconnect(self):
        """Desconecta do banco de dados"""
        db_config.disconnect()
        self.connected = False

    def initialize_sample_data(self):
        """Inicializa o banco com dados de exemplo se estiver vazio"""
        try:

            if self.using_memory:

                # Dados de exemplo para memória
                sample_users = [
                    User("u1", "João Silva", "joao@email.com", "Estudante"),
                    User("u2", "Maria Santos", "maria@email.com", "Professor"),
                    User("u3", "Pedro Costa", "pedro@email.com", "Estudante"),
                    User("u4", "Ana Oliveira", "ana@email.com", "Funcionário"),
                    User("u5", "Carlos Mendes", "carlos@email.com", "Professor")
                ]

                sample_books = [
                    Book("b1", "Python para Iniciantes", "João Autor", "978-1234567890", True),
                    Book("b2", "Algoritmos e Estruturas de Dados", "Maria Autora", "978-1234567891", False),  # emprestado
                    Book("b3", "Banco de Dados", "Pedro Autor", "978-1234567892", True),
                    Book("b4", "Cálculo I", "Ana Matemática", "978-1234567893", False),  # emprestado
                    Book("b5", "Engenharia de Software", "Carlos Dev", "978-1234567894", True)
                ]

                sample_loans = [
                    Loan("l1", "u1", "b2", datetime.now() - timedelta(days=5), None),  # ativo
                    Loan("l2", "u2", "b4", datetime.now() - timedelta(days=10), datetime.now() - timedelta(days=2)),  # devolvido
                    Loan("l3", "u3", "b1", datetime.now() - timedelta(days=3), None)   # ativo
                ]

                self.memory_users = sample_users
                self.memory_books = sample_books
                self.memory_loans = sample_loans

            else:
                # Código original para MongoDB

                # Verificar se já existem dados
                try:
                    users_count = db_config.users_collection.count_documents({})
                    print(f"Usuarios existentes: {users_count}")
                except Exception as count_error:
                    print(f"Erro ao contar usuarios: {count_error}")
                    users_count = 0

                try:
                    books_count = db_config.books_collection.count_documents({})
                    print(f"Livros existentes: {books_count}")
                except Exception as count_error:
                    print(f"Erro ao contar livros: {count_error}")
                    books_count = 0

                try:
                    loans_count = db_config.loans_collection.count_documents({})
                    print(f"Emprestimos existentes: {loans_count}")
                except Exception as count_error:
                    print(f"Erro ao contar emprestimos: {count_error}")
                    loans_count = 0

                if users_count == 0:
                    print("Inserindo usuarios de exemplo...")
                    sample_users = [
                        User("u1", "João Silva", "joao@email.com", "Estudante"),
                        User("u2", "Maria Santos", "maria@email.com", "Professor"),
                        User("u3", "Pedro Costa", "pedro@email.com", "Estudante")
                    ]

                    for user in sample_users:
                        try:
                            result = db_config.users_collection.insert_one(user.to_dict())
                            print(f"Usuario {user.name} inserido com ID: {result.inserted_id}")
                        except Exception as insert_error:
                            print(f"ERRO ao inserir usuario {user.name}: {insert_error}")

                if books_count == 0:
                    print("Inserindo livros de exemplo...")
                    sample_books = [
                        Book("b1", "Python para Iniciantes", "Alice Brown", "978-1234567890", False),  # emprestado (l1)
                        Book("b2", "Algoritmos e Estruturas de Dados", "Bob Wilson", "978-0987654321", False),  # emprestado (l2)
                        Book("b3", "Banco de Dados Relacionais", "Carol Davis", "978-1122334455", True)  # disponível
                    ]

                    for book in sample_books:
                        try:
                            result = db_config.books_collection.insert_one(book.to_dict())
                            print(f"Livro '{book.title}' inserido com ID: {result.inserted_id}")
                        except Exception as insert_error:
                            print(f"ERRO ao inserir livro {book.title}: {insert_error}")

                if loans_count == 0:
                    print("Inserindo emprestimos de exemplo...")
                    sample_loans = [
                        Loan("l1", "u1", "b1", datetime(2024, 1, 10)),
                        Loan("l2", "u1", "b2", datetime(2024, 1, 15))
                    ]

                    for loan in sample_loans:
                        try:
                            result = db_config.loans_collection.insert_one(loan.to_dict())
                            print(f"Emprestimo {loan.id} inserido com ID: {result.inserted_id}")
                        except Exception as insert_error:
                            print(f"ERRO ao inserir emprestimo {loan.id}: {insert_error}")


        except Exception as e:
            print(f"ERRO: Falha na inicialização de dados: {e}")
            import traceback
            traceback.print_exc()

    def adicionar_usuario(self, user: User):
        """Adiciona um novo usuário ao banco de dados"""
        try:
            result = db_config.users_collection.insert_one(user.to_dict())
            return result.inserted_id
        except Exception as e:
            print(f"ERRO: Falha ao adicionar usuario: {e}")
            return None

    def adicionar_livro(self, book: Book):
        """Adiciona um novo livro ao banco de dados"""
        try:
            result = db_config.books_collection.insert_one(book.to_dict())
            return result.inserted_id
        except Exception as e:
            print(f"ERRO: Falha ao adicionar livro: {e}")
            return None

    def adicionar_emprestimo(self, loan: Loan):
        """Adiciona um novo empréstimo ao banco de dados"""
        try:
            # Verificar se o livro está disponível
            book = self.get_livro_por_id(loan.book_id)
            if book and not book.available:
                print(f"ERRO: Livro '{book.title}' nao esta disponivel para emprestimo")
                return None

            result = db_config.loans_collection.insert_one(loan.to_dict())

            # Atualizar disponibilidade do livro
            if book:
                db_config.books_collection.update_one(
                    {"id": loan.book_id},
                    {"$set": {"available": False}}
                )

            return result.inserted_id
        except Exception as e:
            print(f"ERRO: Falha ao adicionar emprestimo: {e}")
            return None

    def get_usuarios(self) -> List[User]:
        """Retorna lista de todos os usuários"""
        if self.using_memory:
            return self.memory_users.copy()
        else:
            try:
                users_data = list(db_config.users_collection.find())
                return [User.from_dict(user_data) for user_data in users_data]
            except Exception as e:
                print(f"ERRO: Falha ao buscar usuarios: {e}")
                return []

    def get_livros(self) -> List[Book]:
        """Retorna lista de todos os livros"""
        if self.using_memory:
            return self.memory_books.copy()
        else:
            try:
                books_data = list(db_config.books_collection.find())
                return [Book.from_dict(book_data) for book_data in books_data]
            except Exception as e:
                print(f"ERRO: Falha ao buscar livros: {e}")
                return []

    def get_emprestimos(self) -> List[Loan]:
        """Retorna lista de todos os empréstimos"""
        if self.using_memory:
            return self.memory_loans.copy()
        else:
            try:
                loans_data = list(db_config.loans_collection.find())
                return [Loan.from_dict(loan_data) for loan_data in loans_data]
            except Exception as e:
                print(f"ERRO: Falha ao buscar emprestimos: {e}")
                return []

    def get_livros_disponiveis(self) -> List[Book]:
        """Retorna lista de livros disponíveis"""
        try:
            books_data = list(db_config.books_collection.find({"available": True}))
            return [Book.from_dict(book_data) for book_data in books_data]
        except Exception as e:
            print(f"ERRO: Falha ao buscar livros disponiveis: {e}")
            return []

    def get_usuario_por_id(self, user_id: str) -> Optional[User]:
        """Busca um usuário por ID"""
        try:
            user_data = db_config.users_collection.find_one({"id": user_id})
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            print(f"ERRO: Falha ao buscar usuario {user_id}: {e}")
            return None

    def get_livro_por_id(self, book_id: str) -> Optional[Book]:
        """Busca um livro por ID"""
        try:
            book_data = db_config.books_collection.find_one({"id": book_id})
            return Book.from_dict(book_data) if book_data else None
        except Exception as e:
            print(f"ERRO: Falha ao buscar livro {book_id}: {e}")
            return None

    def get_emprestimo_por_id(self, loan_id: str) -> Optional[Loan]:
        """Busca um empréstimo por ID"""
        try:
            loan_data = db_config.loans_collection.find_one({"id": loan_id})
            return Loan.from_dict(loan_data) if loan_data else None
        except Exception as e:
            print(f"ERRO: Falha ao buscar emprestimo {loan_id}: {e}")
            return None

    def get_emprestimos_por_usuario(self, user_id: str) -> List[Loan]:
        """Retorna empréstimos de um usuário específico"""
        try:
            loans_data = list(db_config.loans_collection.find({"user_id": user_id}))
            return [Loan.from_dict(loan_data) for loan_data in loans_data]
        except Exception as e:
            print(f"ERRO: Falha ao buscar emprestimos do usuario {user_id}: {e}")
            return []

    def get_emprestimos_por_livro(self, book_id: str) -> List[Loan]:
        """Retorna empréstimos de um livro específico"""
        try:
            loans_data = list(db_config.loans_collection.find({"book_id": book_id}))
            return [Loan.from_dict(loan_data) for loan_data in loans_data]
        except Exception as e:
            print(f"ERRO: Falha ao buscar emprestimos do livro {book_id}: {e}")
            return []

    def devolver_livro(self, loan_id: str) -> bool:
        """Marca um empréstimo como devolvido"""
        try:
            # Buscar o empréstimo
            loan = self.get_emprestimo_por_id(loan_id)
            if not loan:
                print(f"ERRO: Emprestimo {loan_id} nao encontrado")
                return False

            if loan.return_date:
                print(f"AVISO: Emprestimo {loan_id} ja foi devolvido")
                return False

            # Atualizar empréstimo com data de devolução
            return_date = datetime.now()
            result = db_config.loans_collection.update_one(
                {"id": loan_id},
                {"$set": {"return_date": return_date.isoformat()}}
            )

            if result.modified_count > 0:
                # Atualizar disponibilidade do livro
                db_config.books_collection.update_one(
                    {"id": loan.book_id},
                    {"$set": {"available": True}}
                )

                # Buscar o livro para mostrar o nome
                book = self.get_livro_por_id(loan.book_id)
                book_title = book.title if book else "Livro desconhecido"

                return True
            else:
                print(f"ERRO: Falha ao atualizar emprestimo {loan_id}")
                return False

        except Exception as e:
            print(f"ERRO: Falha ao devolver livro: {e}")
            return False

    # ========================================
    # PIPELINES DE AGGREGATION - RELATÓRIOS
    # ========================================

    def get_relatorio_livros_mais_emprestados(self, limit: int = 10) -> List[Dict]:
        """
        Pipeline: Livros mais emprestados
        Usa aggregation pipeline para contar empréstimos por livro
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$book_id",
                    "total_emprestimos": {"$sum": 1},
                    "emprestimos_ativos": {
                        "$sum": {"$cond": [{"$eq": ["$return_date", None]}, 1, 0]}
                    }
                }
            },
            {
                "$lookup": {
                    "from": "livros",
                    "localField": "_id",
                    "foreignField": "id",
                    "as": "livro_info"
                }
            },
            {"$unwind": "$livro_info"},
            {
                "$project": {
                    "livro_id": "$_id",
                    "titulo": "$livro_info.title",
                    "autor": "$livro_info.author",
                    "isbn": "$livro_info.isbn",
                    "total_emprestimos": 1,
                    "emprestimos_ativos": 1,
                    "disponivel": "$livro_info.available"
                }
            },
            {"$sort": {"total_emprestimos": -1}},
            {"$limit": limit}
        ]

        try:
            result = list(db_config.loans_collection.aggregate(pipeline))
            return result
        except Exception as e:
            print(f"ERRO: Falha na pipeline de livros mais emprestados: {e}")
            return []

    def get_relatorio_usuarios_mais_ativos(self, limit: int = 10) -> List[Dict]:
        """
        Pipeline: Usuários que mais fizeram empréstimos
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$user_id",
                    "total_emprestimos": {"$sum": 1},
                    "emprestimos_ativos": {
                        "$sum": {"$cond": [{"$eq": ["$return_date", None]}, 1, 0]}
                    }
                }
            },
            {
                "$lookup": {
                    "from": "usuarios",
                    "localField": "_id",
                    "foreignField": "id",
                    "as": "usuario_info"
                }
            },
            {"$unwind": "$usuario_info"},
            {
                "$project": {
                    "usuario_id": "$_id",
                    "nome": "$usuario_info.name",
                    "email": "$usuario_info.email",
                    "tipo": "$usuario_info.type",
                    "total_emprestimos": 1,
                    "emprestimos_ativos": 1
                }
            },
            {"$sort": {"total_emprestimos": -1}},
            {"$limit": limit}
        ]

        try:
            result = list(db_config.loans_collection.aggregate(pipeline))
            return result
        except Exception as e:
            print(f"ERRO: Falha na pipeline de usuarios mais ativos: {e}")
            return []

    def get_estatisticas_gerais(self) -> Dict:
        """
        Pipeline: Estatísticas gerais da biblioteca
        """
        try:
            # Estatísticas de usuários
            usuarios_stats = list(db_config.users_collection.aggregate([
                {
                    "$group": {
                        "_id": "$type",
                        "count": {"$sum": 1}
                    }
                }
            ]))

            # Estatísticas de livros
            livros_result = list(db_config.books_collection.aggregate([
                {
                    "$group": {
                        "_id": None,
                        "total_livros": {"$sum": 1},
                        "livros_disponiveis": {
                            "$sum": {"$cond": [{"$eq": ["$available", True]}, 1, 0]}
                        },
                        "livros_emprestados": {
                            "$sum": {"$cond": [{"$eq": ["$available", False]}, 1, 0]}
                        }
                    }
                }
            ]))
            livros_stats = livros_result[0] if livros_result else {
                "total_livros": 0, "livros_disponiveis": 0, "livros_emprestados": 0
            }

            # Estatísticas de empréstimos
            emprestimos_result = list(db_config.loans_collection.aggregate([
                {
                    "$group": {
                        "_id": None,
                        "total_emprestimos": {"$sum": 1},
                        "emprestimos_ativos": {
                            "$sum": {"$cond": [{"$eq": ["$return_date", None]}, 1, 0]}
                        },
                        "emprestimos_finalizados": {
                            "$sum": {"$cond": [{"$ne": ["$return_date", None]}, 1, 0]}
                        }
                    }
                }
            ]))
            emprestimos_stats = emprestimos_result[0] if emprestimos_result else {
                "total_emprestimos": 0, "emprestimos_ativos": 0, "emprestimos_finalizados": 0
            }

            return {
                "usuarios_por_tipo": usuarios_stats,
                "livros": livros_stats,
                "emprestimos": emprestimos_stats
            }

        except Exception as e:
            print(f"ERRO: Falha ao gerar estatisticas gerais: {e}")
            return {}

    def get_relatorio_emprestimos_por_periodo(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Pipeline: Empréstimos realizados em um período específico
        """
        pipeline = [
            {
                "$match": {
                    "loan_date": {
                        "$gte": start_date.isoformat(),
                        "$lte": end_date.isoformat()
                    }
                }
            },
            {
                "$lookup": {
                    "from": "usuarios",
                    "localField": "user_id",
                    "foreignField": "id",
                    "as": "usuario"
                }
            },
            {
                "$lookup": {
                    "from": "livros",
                    "localField": "book_id",
                    "foreignField": "id",
                    "as": "livro"
                }
            },
            {"$unwind": "$usuario"},
            {"$unwind": "$livro"},
            {
                "$project": {
                    "emprestimo_id": "$id",
                    "data_emprestimo": "$loan_date",
                    "data_devolucao": "$return_date",
                    "usuario": {
                        "id": "$usuario.id",
                        "nome": "$usuario.name",
                        "tipo": "$usuario.type"
                    },
                    "livro": {
                        "id": "$livro.id",
                        "titulo": "$livro.title",
                        "autor": "$livro.author"
                    },
                    "status": {
                        "$cond": {
                            "if": {"$eq": ["$return_date", None]},
                            "then": "Ativo",
                            "else": "Finalizado"
                        }
                    }
                }
            },
            {"$sort": {"data_emprestimo": -1}}
        ]

        try:
            result = list(db_config.loans_collection.aggregate(pipeline))
            return result
        except Exception as e:
            print(f"ERRO: Falha na pipeline de emprestimos por periodo: {e}")
            return []

    def get_relatorio_livros_atrasados(self) -> List[Dict]:
        """
        Pipeline: Livros emprestados há mais de 30 dias (atrasados)
        """
        # Considera atraso após 30 dias
        limite_dias = 30
        data_limite = datetime.now() - timedelta(days=limite_dias)

        pipeline = [
            {
                "$match": {
                    "return_date": None,  # Ainda não devolvido
                    "loan_date": {"$lt": data_limite.isoformat()}
                }
            },
            {
                "$lookup": {
                    "from": "usuarios",
                    "localField": "user_id",
                    "foreignField": "id",
                    "as": "usuario"
                }
            },
            {
                "$lookup": {
                    "from": "livros",
                    "localField": "book_id",
                    "foreignField": "id",
                    "as": "livro"
                }
            },
            {"$unwind": "$usuario"},
            {"$unwind": "$livro"},
            {
                "$project": {
                    "emprestimo_id": "$id",
                    "data_emprestimo": "$loan_date",
                    "usuario": {
                        "id": "$usuario.id",
                        "nome": "$usuario.name",
                        "email": "$usuario.email",
                        "tipo": "$usuario.type"
                    },
                    "livro": {
                        "id": "$livro.id",
                        "titulo": "$livro.title",
                        "autor": "$livro.author",
                        "isbn": "$livro.isbn"
                    }
                }
            },
            {"$sort": {"data_emprestimo": 1}}  # Mais antigos primeiro
        ]

        try:
            result = list(db_config.loans_collection.aggregate(pipeline))

            # Calcular dias de atraso em Python (mais confiável)
            for item in result:
                loan_date = datetime.fromisoformat(item['data_emprestimo'])
                item['dias_atraso'] = (datetime.now() - loan_date).days

            return result
        except Exception as e:
            print(f"ERRO: Falha na pipeline de livros atrasados: {e}")
            return []

    def get_relatorio_popularidade_por_categoria(self) -> List[Dict]:
        """
        Pipeline: Análise de popularidade por tipo de usuário
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "usuarios",
                    "localField": "user_id",
                    "foreignField": "id",
                    "as": "usuario"
                }
            },
            {"$unwind": "$usuario"},
            {
                "$group": {
                    "_id": "$usuario.type",
                    "total_emprestimos": {"$sum": 1},
                    "emprestimos_ativos": {
                        "$sum": {"$cond": [{"$eq": ["$return_date", None]}, 1, 0]}
                    },
                    "usuarios_unicos": {"$addToSet": "$user_id"}
                }
            },
            {
                "$project": {
                    "categoria_usuario": "$_id",
                    "total_emprestimos": 1,
                    "emprestimos_ativos": 1,
                    "numero_usuarios_unicos": {"$size": "$usuarios_unicos"},
                    "media_emprestimos_por_usuario": {
                        "$round": [
                            {"$divide": ["$total_emprestimos", {"$size": "$usuarios_unicos"}]},
                            2
                        ]
                    }
                }
            },
            {"$sort": {"total_emprestimos": -1}}
        ]

        try:
            result = list(db_config.loans_collection.aggregate(pipeline))
            return result
        except Exception as e:
            print(f"ERRO: Falha na pipeline de popularidade por categoria: {e}")
            return []


# Instância global do gerenciador de banco de dados
db_manager = DatabaseManager()


# Funções de compatibilidade (mantém a mesma interface do código existente)
def adicionar_usuario(user: User):
    """Adiciona um novo usuário ao sistema"""
    return db_manager.adicionar_usuario(user)


def adicionar_livro(book: Book):
    """Adiciona um novo livro ao sistema"""
    return db_manager.adicionar_livro(book)


def adicionar_emprestimo(loan: Loan):
    """Adiciona um novo empréstimo ao sistema"""
    return db_manager.adicionar_emprestimo(loan)


def get_usuarios() -> List[User]:
    """Retorna lista de todos os usuários"""
    return db_manager.get_usuarios()


def get_livros() -> List[Book]:
    """Retorna lista de todos os livros"""
    return db_manager.get_livros()


def get_emprestimos() -> List[Loan]:
    """Retorna lista de todos os empréstimos"""
    return db_manager.get_emprestimos()


def get_livros_disponiveis() -> List[Book]:
    """Retorna lista de livros disponíveis"""
    return db_manager.get_livros_disponiveis()


def get_emprestimos_por_usuario(user_id: str) -> List[Loan]:
    """Retorna empréstimos de um usuário específico"""
    return db_manager.get_emprestimos_por_usuario(user_id)


def get_emprestimos_por_livro(book_id: str) -> List[Loan]:
    """Retorna empréstimos de um livro específico"""
    return db_manager.get_emprestimos_por_livro(book_id)


def devolver_livro(loan_id: str) -> bool:
    """Marca um empréstimo como devolvido"""
    return db_manager.devolver_livro(loan_id)
