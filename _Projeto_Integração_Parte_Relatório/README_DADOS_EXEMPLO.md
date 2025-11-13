# 🏗️ Dados de Exemplo - Biblioteca Universitária

Este documento explica como popular o banco MongoDB com dados ricos de exemplo para testar a aplicação da Biblioteca Universitária.

## 📊 Visão Geral dos Dados

O script `populate_sample_data.py` cria aproximadamente:
- **50 usuários** (30 estudantes + 10 professores + 10 funcionários)
- **50 livros** de diferentes categorias (programação, bancos de dados, matemática, etc.)
- **50 empréstimos** (15 ativos + 35 finalizados) com histórico realista

## 🚀 Como Usar

### Pré-requisitos

1. **MongoDB instalado e rodando**
   - Windows: Instalar via [MongoDB Community](https://www.mongodb.com/try/download/community)
   - Linux: `sudo apt install mongodb`
   - macOS: `brew install mongodb-community`

2. **Dependências Python instaladas**
   ```bash
   pip install pymongo
   ```

### Passos para Popular o Banco

#### Opção 1: Script Batch (Recomendado para Windows)
```bash
POPULAR_DADOS.bat
```

#### Opção 2: Script PowerShell
```powershell
.\Popular_Dados.ps1
```

#### Opção 3: Execução Direta
```bash
python populate_sample_data.py
# ou
python3 populate_sample_data.py
```

## 📈 Dados Criados

### 👥 Usuários (50 total)

**Estudantes (30):**
- IDs: `u001` até `u040`
- Exemplos: João Silva, Maria Fernandes, Pedro Oliveira, etc.
- Emails: `nome.sobrenome@email.com`

**Professores (10):**
- IDs: `u011`, `u012`, `u013`, `u014`, `u015`, `u041` até `u045`
- Exemplos: Prof. Dr. Carlos Eduardo Santos, Profª. Dra. Helena Cristina Lima, etc.
- Emails: `nome.sobrenome@universidade.edu`

**Funcionários (10):**
- IDs: `u016` até `u020`, `u046` até `u050`
- Exemplos: José Roberto Oliveira, Maria Clara Pereira, etc.
- Emails: `nome.sobrenome@universidade.edu`

### 📚 Livros (50 total)

**Distribuição por categoria:**
- **Programação/Tecnologia** (15 livros): Python, JavaScript, React, Docker, etc.
- **Bancos de Dados** (8 livros): MongoDB, PostgreSQL, SQL, Redis, etc.
- **Matemática/Estatística** (8 livros): Cálculo, Álgebra Linear, Probabilidade, etc.
- **Engenharia de Software** (6 livros): Scrum, TDD, Refatoração, etc.
- **Ciência da Computação** (5 livros): Arquitetura, Redes, SO, Compiladores, etc.
- **Literatura/Ficção** (4 livros): 1984, Dom Casmurro, Harry Potter, etc.
- **Técnicos Diversos** (4 livros): Gestão, Segurança, IHC, Computação em Nuvem

**Status dos livros:**
- Alguns livros marcados como **emprestados** (não disponíveis)
- Outros marcados como **disponíveis** para empréstimo

### 📖 Empréstimos (50 total)

**Empréstimos Ativos (15):**
- Livros atualmente emprestados (sem data de devolução)
- Exemplos: João com "Python para Ciência de Dados", Maria com "Sistemas de Banco de Dados", etc.

**Empréstimos Finalizados (35):**
- Empréstimos com datas de empréstimo e devolução
- Histórico de até 10 meses atrás
- Permite análise estatística nos relatórios

## 📊 Funcionalidades de Teste

Após executar o script, você pode testar:

### 📋 Listar Usuários
- Visualizar todos os 50 usuários cadastrados
- Ver diferentes tipos: Estudantes, Professores, Funcionários
- Cada usuário tem nome, email e tipo

### 📚 Listar Livros
- Visualizar catálogo completo de 50 livros
- Ver status: **Disponível** ou **Emprestado**
- Livros emprestados estão marcados com 🔒

### 📋 Listar Empréstimos
- Visualizar empréstimos ativos (15 registros)
- Ver quem pegou qual livro e quando
- Status: "Em andamento"

### 📊 Relatórios

**Livros Mais Emprestados:**
- Ranking baseado no histórico de empréstimos
- Mostra os livros mais populares da biblioteca

**Usuários Mais Ativos:**
- Ranking de usuários que mais fazem empréstimos
- Mostra estudantes e professores mais assíduos

## 🔧 Personalização

Para modificar os dados de exemplo, edite o arquivo `populate_sample_data.py`:

```python
# Para adicionar mais usuários
sample_users.append(User("u051", "Novo Usuário", "novo@email.com", "Estudante"))

# Para adicionar mais livros
sample_books.append(Book("b070", "Novo Livro", "Autor", "ISBN", True))

# Para ajustar quantidade de empréstimos
for _ in range(20):  # Mais empréstimos
    # ... lógica de criação
```

## 🐛 Troubleshooting

### Erro de Conexão MongoDB
```
ERRO: Falha ao conectar ao MongoDB
```
**Solução:** Verifique se o MongoDB está rodando:
```bash
# Windows
net start MongoDB

# Linux/macOS
sudo systemctl start mongod
# ou
mongod
```

### Erro de Dependências
```
ModuleNotFoundError: No module named 'pymongo'
```
**Solução:** Instale as dependências:
```bash
pip install pymongo
```

### Dados Não Aparecem na Aplicação
1. Execute o script de população
2. Reinicie a aplicação
3. Verifique se o MongoDB está conectado

## 📝 Notas Técnicas

- **IDs únicos:** Usuários (`u001-u050`), Livros (`b001-b070`), Empréstimos (`l001-l050+`)
- **Datas realistas:** Empréstimos com datas variando dos últimos 10 meses
- **Consistência:** Livros emprestados são marcados como não disponíveis
- **Reprodutibilidade:** Dados gerados com seed fixo para consistência

---

🎯 **Próximo passo:** Execute `POPULAR_DADOS.bat` e depois inicie a aplicação com `python simple_server.py`!
