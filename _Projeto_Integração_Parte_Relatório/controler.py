from Model import model as md
from datetime import datetime


class Controler():
    def __init__(self, login_required=True):
        self.login_required = login_required

    def devolver_livro(self, loan_id):
        """Devolve um livro"""
        return md.devolver_livro(loan_id)

    def get_usuarios(self):
        """Retorna todos os usuários"""
        return md.get_usuarios()

    def get_livros(self):
        """Retorna todos os livros"""
        return md.get_livros()

    def get_emprestimos(self):
        """Retorna todos os empréstimos"""
        return md.get_emprestimos()

    def get_livros_disponiveis(self):
        """Retorna livros disponíveis"""
        return md.get_livros_disponiveis()

    def get_emprestimos_por_usuario(self, user_id):
        """Retorna empréstimos de um usuário"""
        return md.get_emprestimos_por_usuario(user_id)

    def get_usuario_por_id(self, user_id):
        """Busca usuário por ID"""
        return md.db_manager.get_usuario_por_id(user_id)

    def get_livro_por_id(self, book_id):
        """Busca livro por ID"""
        return md.db_manager.get_livro_por_id(book_id)

    def get_emprestimo_por_id(self, loan_id):
        """Busca empréstimo por ID"""
        return md.db_manager.get_emprestimo_por_id(loan_id)


# Classe para autenticação (seguindo padrão do projeto de referência)
class Ctrl_User(md.User):
    def __init__(self, user_id, name, email, user_type):
        super().__init__(user_id, name, email, user_type)

    def autenticar(self):
        # Implementação simples - em produção seria mais robusta
        return True
