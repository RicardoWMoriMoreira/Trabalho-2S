from typing import List, Optional


class Livro:
	def __init__(self, id: int, titulo: str, autor: str, estoque: int, status: str = "disponível"):
		self.id = id
		self.titulo = titulo
		self.autor = autor
		self.estoque = estoque
		self.status = status

	def get_id(self) -> int:
		return self.id

	def get_titulo(self) -> str:
		return self.titulo

	def get_autor(self) -> str:
		return self.autor

	def get_estoque(self) -> int:
		return self.estoque

	def get_status(self) -> str:
		return self.status

	def set_status(self, novo_status: str) -> None:
		self.status = novo_status

	def emprestar(self) -> None:
		if self.estoque > 0:
			self.estoque -= 1
			if self.estoque == 0:
				self.status = "emprestado"
		else:
			raise ValueError("Livro indisponível para empréstimo")

	def devolver(self) -> None:
		self.estoque += 1
		self.status = "disponível"


_livros: List[Livro] = []


def adicionar_livro(livro: Livro) -> None:
	_livros.append(livro)


def listar_livros() -> List[Livro]:
	return _livros


def remover_livro(id: int) -> None:
	global _livros
	_livros = [l for l in _livros if l.get_id() != id]


def buscar_livro_por_id(id: int) -> Optional[Livro]:
	for livro in _livros:
		if livro.get_id() == id:
			return livro
	return None

