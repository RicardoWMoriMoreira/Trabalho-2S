from typing import List, Dict, Optional
from datetime import datetime
from .loan import LoanController
from .usuario import UsuarioService
from . import livro


class RelatorioService:
    """Serviço para geração de relatórios do sistema de biblioteca"""
    
    def __init__(self, loan_controller: LoanController, usuario_service: UsuarioService):
        self.loan_controller = loan_controller
        self.usuario_service = usuario_service
    
    def gerar_relatorio_livros_mais_emprestados(self) -> List[Dict]:
        """Gera relatório dos livros mais emprestados"""
        emprestimos = self.loan_controller.listar_emprestimos()
        contagem = {}
        
        for emp in emprestimos:
            contagem[emp.book_id] = contagem.get(emp.book_id, 0) + 1
        
        relatorio = []
        for book_id, total in sorted(contagem.items(), key=lambda item: item[1], reverse=True):
            livro_obj = livro.buscar_livro_por_id(book_id)
            if livro_obj:
                relatorio.append({
                    'titulo': livro_obj.titulo,
                    'autor': livro_obj.autor,
                    'totalEmprestimos': total
                })
            else:
                relatorio.append({
                    'titulo': 'Livro Desconhecido',
                    'autor': 'N/A',
                    'totalEmprestimos': total
                })
        
        return relatorio
    
    def gerar_relatorio_usuarios_mais_ativos(self) -> List[Dict]:
        """Gera relatório dos usuários mais ativos"""
        emprestimos = self.loan_controller.listar_emprestimos()
        contagem = {}
        
        for emp in emprestimos:
            contagem[emp.user_id] = contagem.get(emp.user_id, 0) + 1
        
        relatorio = []
        for user_id, total in sorted(contagem.items(), key=lambda item: item[1], reverse=True):
            usuario = self.usuario_service.buscar_por_id(user_id)
            if usuario:
                relatorio.append({
                    'nome': usuario.nome,
                    'matricula': usuario.matricula,
                    'totalEmprestimos': total
                })
            else:
                relatorio.append({
                    'nome': 'Usuário Desconhecido',
                    'matricula': str(user_id),
                    'totalEmprestimos': total
                })
        
        return relatorio
    
    def filtrar_por_periodo(self, data_inicio: str, data_fim: str) -> List[Dict]:
        """Filtra empréstimos por período"""
        emprestimos = self.loan_controller.listar_emprestimos()
        filtrados = []
        
        for emp in emprestimos:
            emp_date = emp.borrowed_at.date().isoformat()
            if data_inicio <= emp_date <= data_fim:
                filtrados.append(emp.to_dict())
        
        return filtrados
    
    def contar_status_acervo(self) -> Dict[str, int]:
        """Conta status do acervo (disponível vs emprestado)"""
        livros_list = livro.listar_livros()
        disponivel = sum(1 for l in livros_list if l.status == 'disponível')
        emprestado = sum(1 for l in livros_list if l.status == 'emprestado')
        total = len(livros_list)
        
        return {
            'disponivel': disponivel,
            'emprestado': emprestado,
            'total': total
        }
    
    def relatorio_detalhado_emprestimos(self) -> List[Dict]:
        """Gera relatório detalhado de empréstimos com informações de usuário e livro"""
        emprestimos = self.loan_controller.listar_emprestimos()
        detalhes = []
        
        for emp in emprestimos:
            usuario = self.usuario_service.buscar_por_id(emp.user_id)
            livro_obj = livro.buscar_livro_por_id(emp.book_id)
            
            detalhes.append({
                'loan_id': emp.loan_id,
                'usuario': {
                    'id': usuario.id if usuario else emp.user_id,
                    'nome': usuario.nome if usuario else 'Usuário Desconhecido',
                    'matricula': usuario.matricula if usuario else 'N/A'
                },
                'livro': {
                    'id': livro_obj.id if livro_obj else emp.book_id,
                    'titulo': livro_obj.titulo if livro_obj else 'Livro Desconhecido',
                    'autor': livro_obj.autor if livro_obj else 'N/A'
                },
                'borrowed_at': emp.borrowed_at.isoformat(),
                'returned_at': emp.returned_at.isoformat() if emp.returned_at else None,
                'status': 'Devolvido' if emp.returned_at else 'Em curso'
            })
        
        return detalhes

