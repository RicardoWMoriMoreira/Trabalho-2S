from enum import Enum
from datetime import datetime
import re


class TipoUsuario(Enum):
    """Enum para tipos de usuário"""
    ALUNO = "ALUNO"
    PROFESSOR = "PROFESSOR"
    FUNCIONARIO = "FUNCIONARIO"


class StatusUsuario(Enum):
    """Enum para status do usuário"""
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"
    SUSPENSO = "SUSPENSO"


class Usuario:
    """Modelo de dados para Usuário"""
    
    _contador_id = 0
    
    def __init__(self, nome, matricula, tipo, email=None, status=None):
        # Validar nome
        if not nome or len(nome) < 1 or len(nome) > 100:
            raise ValueError("Nome deve ter entre 1 e 100 caracteres")
        
        # Validar matrícula
        if not matricula or len(matricula) < 5 or len(matricula) > 20:
            raise ValueError("Matrícula deve ter entre 5 e 20 caracteres")
        
        # Validar email (se fornecido)
        if email is not None and email != "":
            if not self._validar_email(email):
                raise ValueError("Email inválido")
        
        # Validar tipo
        if isinstance(tipo, str):
            tipo = TipoUsuario[tipo]
        
        # Gerar ID
        Usuario._contador_id += 1
        self.id = Usuario._contador_id
        
        # Atribuir valores
        self.nome = nome
        self.matricula = matricula
        self.tipo = tipo
        self.email = email
        self.dataRegistro = datetime.now().isoformat()
        self.status = status if status else StatusUsuario.ATIVO
    
    @staticmethod
    def _validar_email(email):
        """Valida formato de email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None
    
    def to_dict(self):
        """Serializa usuário para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'matricula': self.matricula,
            'tipo': self.tipo.value,
            'email': self.email,
            'dataRegistro': self.dataRegistro,
            'status': self.status.value
        }
    
    def __repr__(self):
        return f"Usuario(id={self.id}, nome='{self.nome}', matricula='{self.matricula}')"


class UsuarioService:
    """Serviço para gerenciar operações CRUD de usuários"""
    
    def __init__(self):
        self.usuarios = {}
        self.matriculas = set()
        self.emails = set()
        Usuario._contador_id = 0  # Reset para testes
    
    def cadastrar(self, nome, matricula, tipo, email=None):
        """Cadastra novo usuário"""
        # Verificar matrícula duplicada
        if matricula in self.matriculas:
            raise ValueError("Matrícula já cadastrada")
        
        # Verificar email duplicado (se fornecido)
        if email and email in self.emails:
            raise ValueError("Email já cadastrado")
        
        # Criar usuário
        usuario = Usuario(nome, matricula, tipo, email)
        
        # Armazenar
        self.usuarios[usuario.id] = usuario
        self.matriculas.add(matricula)
        if email:
            self.emails.add(email)
        
        return usuario
    
    def listar(self):
        """Lista todos os usuários"""
        return list(self.usuarios.values())
    
    def buscar_por_id(self, usuario_id):
        """Busca usuário por ID"""
        return self.usuarios.get(usuario_id)
    
    def buscar_por_matricula(self, matricula):
        """Busca usuário por matrícula"""
        for usuario in self.usuarios.values():
            if usuario.matricula == matricula:
                return usuario
        return None
    
    def atualizar(self, usuario_id, nome=None, email=None, status=None):
        """Atualiza dados de usuário existente"""
        usuario = self.buscar_por_id(usuario_id)
        
        if not usuario:
            raise ValueError("Usuário não encontrado")
        
        # Atualizar campos fornecidos
        if nome:
            if len(nome) < 1 or len(nome) > 100:
                raise ValueError("Nome deve ter entre 1 e 100 caracteres")
            usuario.nome = nome
        
        if email is not None:
            # Remover email antigo do conjunto
            if usuario.email:
                self.emails.discard(usuario.email)
            
            # Validar e adicionar novo email
            if email and not Usuario._validar_email(email):
                raise ValueError("Email inválido")
            
            if email and email in self.emails:
                raise ValueError("Email já cadastrado")
            
            usuario.email = email
            if email:
                self.emails.add(email)
        
        if status:
            if isinstance(status, str):
                status = StatusUsuario[status]
            usuario.status = status
        
        return usuario
    
    def remover(self, usuario_id):
        """Remove usuário por ID"""
        usuario = self.buscar_por_id(usuario_id)
        
        if not usuario:
            return False
        
        # Remover dos conjuntos
        self.matriculas.discard(usuario.matricula)
        if usuario.email:
            self.emails.discard(usuario.email)
        
        # Remover do dicionário
        del self.usuarios[usuario_id]
        
        return True

