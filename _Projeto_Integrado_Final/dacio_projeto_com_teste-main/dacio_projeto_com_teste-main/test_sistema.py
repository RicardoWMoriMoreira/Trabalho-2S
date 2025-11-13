"""
Testes básicos de integração do sistema de biblioteca
"""
import unittest
from models import (
    UsuarioService, TipoUsuario, StatusUsuario,
    Livro, adicionar_livro, listar_livros, remover_livro, buscar_livro_por_id,
    LoanController, LoanError, ValidationError, NotFoundError,
    RelatorioService
)


class TestSistemaIntegrado(unittest.TestCase):
    
    def setUp(self):
        """Prepara o ambiente de teste"""
        # Limpar dados antes de cada teste
        import models.livro as livro_module
        livro_module._livros.clear()
        
        self.usuario_service = UsuarioService()
        self.loan_controller = LoanController(self.usuario_service)
        self.relatorio_service = RelatorioService(self.loan_controller, self.usuario_service)
        
        # Adicionar usuário de teste
        self.usuario = self.usuario_service.cadastrar(
            nome="Teste Usuario",
            matricula="TST12345",
            tipo="ALUNO",
            email="teste@email.com"
        )
    
    def test_cadastro_usuario(self):
        """Testa cadastro de usuário"""
        self.assertIsNotNone(self.usuario.id)
        self.assertEqual(self.usuario.nome, "Teste Usuario")
        self.assertEqual(self.usuario.matricula, "TST12345")
    
    def test_cadastro_livro(self):
        """Testa cadastro de livro"""
        livro = Livro(id=1, titulo="Teste Livro", autor="Autor Teste", estoque=5)
        adicionar_livro(livro)
        
        livros = listar_livros()
        self.assertEqual(len(livros), 1)
        self.assertEqual(livros[0].titulo, "Teste Livro")
    
    def test_emprestimo_completo(self):
        """Testa fluxo completo de empréstimo"""
        # Cadastrar livro
        livro = Livro(id=1, titulo="Livro Teste", autor="Autor", estoque=3)
        adicionar_livro(livro)
        
        # Empréstimo
        loan = self.loan_controller.registrar_emprestimo(
            user_id=self.usuario.id,
            book_id=1
        )
        
        self.assertIsNotNone(loan)
        self.assertEqual(loan.user_id, self.usuario.id)
        self.assertEqual(loan.book_id, 1)
        
        # Verificar estoque
        livro_atualizado = buscar_livro_por_id(1)
        self.assertEqual(livro_atualizado.estoque, 2)
    
    def test_devolucao_completa(self):
        """Testa fluxo completo de devolução"""
        # Cadastrar livro
        livro = Livro(id=2, titulo="Livro 2", autor="Autor", estoque=2)
        adicionar_livro(livro)
        
        # Empréstimo
        loan = self.loan_controller.registrar_emprestimo(
            user_id=self.usuario.id,
            book_id=2
        )
        
        # Devolução
        loan_devolvido = self.loan_controller.registrar_devolucao(
            user_id=self.usuario.id,
            book_id=2
        )
        
        self.assertIsNotNone(loan_devolvido.returned_at)
        
        # Verificar estoque
        livro_atualizado = buscar_livro_por_id(2)
        self.assertEqual(livro_atualizado.estoque, 2)
    
    def test_relatorio_livros_mais_emprestados(self):
        """Testa relatório de livros mais emprestados"""
        # Cadastrar livros
        livro1 = Livro(id=10, titulo="Livro Popular", autor="Autor A", estoque=5)
        livro2 = Livro(id=11, titulo="Livro Menos", autor="Autor B", estoque=3)
        adicionar_livro(livro1)
        adicionar_livro(livro2)
        
        # Fazer empréstimos
        self.loan_controller.registrar_emprestimo(self.usuario.id, 10)
        self.loan_controller.registrar_emprestimo(self.usuario.id, 10)
        self.loan_controller.registrar_emprestimo(self.usuario.id, 11)
        
        # Gerar relatório
        relatorio = self.relatorio_service.gerar_relatorio_livros_mais_emprestados()
        
        self.assertGreater(len(relatorio), 0)
        self.assertEqual(relatorio[0]['totalEmprestimos'], 2)
    
    def test_relatorio_usuarios_mais_ativos(self):
        """Testa relatório de usuários mais ativos"""
        # Cadastrar livros
        livro = Livro(id=20, titulo="Livro", autor="Autor", estoque=10)
        adicionar_livro(livro)
        
        # Fazer empréstimos
        self.loan_controller.registrar_emprestimo(self.usuario.id, 20)
        self.loan_controller.registrar_emprestimo(self.usuario.id, 20)
        
        # Gerar relatório
        relatorio = self.relatorio_service.gerar_relatorio_usuarios_mais_ativos()
        
        self.assertGreater(len(relatorio), 0)
        self.assertEqual(relatorio[0]['totalEmprestimos'], 2)
    
    def test_status_acervo(self):
        """Testa relatório de status do acervo"""
        # Cadastrar livros
        livro1 = Livro(id=30, titulo="Livro 1", autor="Autor", estoque=1)  # Apenas 1 unidade
        livro2 = Livro(id=31, titulo="Livro 2", autor="Autor", estoque=1)  # Apenas 1 unidade
        adicionar_livro(livro1)
        adicionar_livro(livro2)
        
        # Emprestar um livro (agora estoque será 0 e status será "emprestado")
        self.loan_controller.registrar_emprestimo(self.usuario.id, 30)
        
        # Gerar relatório
        status = self.relatorio_service.contar_status_acervo()
        
        self.assertEqual(status['disponivel'], 1)  # livro 2 ainda disponível
        self.assertEqual(status['emprestado'], 1)  # livro 1 emprestado (estoque 0)
        self.assertEqual(status['total'], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)

