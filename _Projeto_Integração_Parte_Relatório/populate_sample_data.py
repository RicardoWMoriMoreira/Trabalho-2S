#!/usr/bin/env python3
"""
Script para popular o banco MongoDB com dados ricos de exemplo
para testar a aplicação da Biblioteca Universitária
"""

from datetime import datetime, timedelta
from config.database import db_config
from Model.model import User, Book, Loan
import random

def create_sample_users():
    """Cria uma coleção rica de usuários de exemplo (~50 usuários)"""
    print("🏗️  Criando usuários de exemplo...")

    sample_users = [
        # Estudantes (30)
        User("u001", "João Silva Santos", "joao.santos@email.com", "Estudante"),
        User("u002", "Maria Fernandes Costa", "maria.costa@email.com", "Estudante"),
        User("u003", "Pedro Oliveira Lima", "pedro.lima@email.com", "Estudante"),
        User("u004", "Ana Paula Rodrigues", "ana.rodrigues@email.com", "Estudante"),
        User("u005", "Lucas Pereira Alves", "lucas.alves@email.com", "Estudante"),
        User("u006", "Carolina Souza Mendes", "carolina.mendes@email.com", "Estudante"),
        User("u007", "Rafael Barbosa Gomes", "rafael.gomes@email.com", "Estudante"),
        User("u008", "Beatriz Castro Silva", "beatriz.silva@email.com", "Estudante"),
        User("u009", "Gabriel Martins Rocha", "gabriel.rocha@email.com", "Estudante"),
        User("u010", "Isabela Moreira Pinto", "isabela.pinto@email.com", "Estudante"),
        User("u021", "Thiago Santos Ribeiro", "thiago.ribeiro@email.com", "Estudante"),
        User("u022", "Juliana Alves Cardoso", "juliana.cardoso@email.com", "Estudante"),
        User("u023", "Fernando Costa Martins", "fernando.martins@email.com", "Estudante"),
        User("u024", "Amanda Silva Ferreira", "amanda.ferreira@email.com", "Estudante"),
        User("u025", "Bruno Oliveira Santos", "bruno.santos@email.com", "Estudante"),
        User("u026", "Camila Rodrigues Lima", "camila.lima@email.com", "Estudante"),
        User("u027", "Diego Pereira Alves", "diego.alves@email.com", "Estudante"),
        User("u028", "Eduarda Mendes Castro", "eduarda.castro@email.com", "Estudante"),
        User("u029", "Felipe Barbosa Rocha", "felipe.rocha@email.com", "Estudante"),
        User("u030", "Gabriela Moreira Pinto", "gabriela.pinto@email.com", "Estudante"),
        User("u031", "Henrique Silva Santos", "henrique.santos@email.com", "Estudante"),
        User("u032", "Ingrid Fernandes Costa", "ingrid.costa@email.com", "Estudante"),
        User("u033", "João Pedro Lima", "joao.pedro@email.com", "Estudante"),
        User("u034", "Karla Rodrigues Alves", "karla.alves@email.com", "Estudante"),
        User("u035", "Leonardo Mendes Gomes", "leonardo.gomes@email.com", "Estudante"),
        User("u036", "Mariana Castro Silva", "mariana.silva@email.com", "Estudante"),
        User("u037", "Nicolas Martins Rocha", "nicolas.rocha@email.com", "Estudante"),
        User("u038", "Olivia Moreira Pinto", "olivia.pinto@email.com", "Estudante"),
        User("u039", "Paulo Santos Ribeiro", "paulo.ribeiro@email.com", "Estudante"),
        User("u040", "Quenia Alves Cardoso", "quenia.cardoso@email.com", "Estudante"),

        # Professores (10)
        User("u011", "Prof. Dr. Carlos Eduardo Santos", "carlos.santos@universidade.edu", "Professor"),
        User("u012", "Profª. Dra. Helena Cristina Lima", "helena.lima@universidade.edu", "Professor"),
        User("u013", "Prof. Dr. Roberto Fernandes", "roberto.fernandes@universidade.edu", "Professor"),
        User("u014", "Profª. Dra. Sandra Regina Alves", "sandra.alves@universidade.edu", "Professor"),
        User("u015", "Prof. Dr. Antonio Marcos Silva", "antonio.silva@universidade.edu", "Professor"),
        User("u041", "Prof. Dr. Marcos Vinicius Costa", "marcos.costa@universidade.edu", "Professor"),
        User("u042", "Profª. Dra. Patricia Regina Sousa", "patricia.sousa@universidade.edu", "Professor"),
        User("u043", "Prof. Dr. Ricardo Almeida Santos", "ricardo.santos@universidade.edu", "Professor"),
        User("u044", "Profª. Dra. Silvia Cristina Lima", "silvia.lima@universidade.edu", "Professor"),
        User("u045", "Prof. Dr. Thiago Rodrigues Alves", "thiago.alves@universidade.edu", "Professor"),

        # Funcionários (10)
        User("u016", "José Roberto Oliveira", "jose.oliveira@universidade.edu", "Funcionário"),
        User("u017", "Maria Clara Pereira", "maria.pereira@universidade.edu", "Funcionário"),
        User("u018", "Antonio Carlos Mendes", "antonio.mendes@universidade.edu", "Funcionário"),
        User("u019", "Rosa Helena Castro", "rosa.castro@universidade.edu", "Funcionário"),
        User("u020", "Fernando Luiz Barbosa", "fernando.barbosa@universidade.edu", "Funcionário"),
        User("u046", "Cristina Santos Lima", "cristina.lima@universidade.edu", "Funcionário"),
        User("u047", "Daniel Costa Rodrigues", "daniel.rodrigues@universidade.edu", "Funcionário"),
        User("u048", "Elaine Silva Mendes", "elaine.mendes@universidade.edu", "Funcionário"),
        User("u049", "Fabio Alves Castro", "fabio.castro@universidade.edu", "Funcionário"),
        User("u050", "Gisele Moreira Barbosa", "gisele.barbosa@universidade.edu", "Funcionário"),
    ]

    return sample_users

def create_sample_books():
    """Cria uma coleção rica de livros de exemplo (~50 livros)"""
    print("📚 Criando livros de exemplo...")

    sample_books = [
        # Programação e Tecnologia (15 livros)
        Book("b001", "Python para Ciência de Dados", "Luciano Ramalho", "978-8575227594", True),
        Book("b002", "Algoritmos: Teoria e Prática", "Thomas H. Cormen", "978-8535236999", True),
        Book("b003", "Estruturas de Dados e Algoritmos em Java", "Robert Lafore", "978-8576052232", True),
        Book("b004", "Clean Code: Código Limpo", "Robert C. Martin", "978-8576082672", True),
        Book("b005", "Design Patterns", "Gang of Four", "978-8573076103", True),
        Book("b006", "Machine Learning: Uma Abordagem Prática", "Peter Harrington", "978-8575223374", True),
        Book("b007", "Inteligência Artificial: Uma Abordagem Moderna", "Stuart Russell", "978-8595159907", True),
        Book("b051", "JavaScript: O Guia Definitivo", "David Flanagan", "978-8575227198", True),
        Book("b052", "React: Desenvolvimento de Interfaces Web", "Cássio de Sousa Santos", "978-8550814894", True),
        Book("b053", "Node.js na Prática", "Alexandre Gaussman", "978-8575225378", True),
        Book("b054", "Programação Orientada a Objetos", "Pablo Dall'Oglio", "978-8575222940", True),
        Book("b055", "Git e GitHub para Iniciantes", "Rafael Rosa Fu", "978-8550814115", True),
        Book("b056", "Docker: Containers para Desenvolvedores", "Rafael Gomes", "978-8575225293", True),
        Book("b057", "Microserviços com Spring Boot", "Daniel Alves", "978-8550816010", True),
        Book("b058", "TypeScript na Prática", "Lucas Santos", "978-8550817123", True),

        # Banco de Dados (8 livros)
        Book("b008", "Sistemas de Banco de Dados", "Abraham Silberschatz", "978-8543025001", True),
        Book("b009", "MongoDB: Guia Prático", "Shannon Bradshaw", "978-8575225361", True),
        Book("b010", "SQL para Análise de Dados", "Cathy Tanimura", "978-8550814481", True),
        Book("b011", "NoSQL Essencial", "Pramod J. Sadalage", "978-8575225361", True),
        Book("b059", "PostgreSQL: Guia do Desenvolvedor", "Regina Obe", "978-8575225460", True),
        Book("b060", "Redis: Guia Essencial", "Josiah Carlson", "978-8575225477", True),
        Book("b061", "Modelagem de Dados", "Carlos Alberto Heuser", "978-8573073659", True),
        Book("b062", "Data Warehousing", "Ralph Kimball", "978-8543020129", True),

        # Matemática e Estatística (8 livros)
        Book("b012", "Cálculo: Volume 1", "James Stewart", "978-8522123414", True),
        Book("b013", "Álgebra Linear e Suas Aplicações", "Gilbert Strang", "978-8521630309", True),
        Book("b014", "Probabilidade e Estatística", "Morris H. DeGroot", "978-8565837317", True),
        Book("b015", "Matemática Discreta com Aplicações", "Susanna S. Epp", "978-8543020358", True),
        Book("b063", "Cálculo: Volume 2", "James Stewart", "978-8522123421", True),
        Book("b064", "Estatística Básica", "Pedro A. Morettin", "978-8524401377", True),
        Book("b065", "Geometria Analítica", "João Santos", "978-8522123455", True),
        Book("b066", "Equações Diferenciais", "Dennis Zill", "978-8522123486", True),

        # Engenharia de Software (6 livros)
        Book("b016", "Engenharia de Software Moderna", "Marco Tulio Valente", "978-6599027004", True),
        Book("b017", "Scrum: A Arte de Fazer o Dobro na Metade do Tempo", "Jeff Sutherland", "978-8544100625", True),
        Book("b018", "Refatoração", "Martin Fowler", "978-8575227242", True),
        Book("b019", "Test Driven Development", "Kent Beck", "978-8575222360", True),
        Book("b067", "XP Explained", "Kent Beck", "978-8575222377", True),
        Book("b068", "Domain-Driven Design", "Eric Evans", "978-8575227242", True),

        # Ciência da Computação (5 livros)
        Book("b020", "Arquitetura de Computadores", "Andrew S. Tanenbaum", "978-8575224081", True),
        Book("b021", "Redes de Computadores", "Andrew S. Tanenbaum", "978-8575224081", True),
        Book("b022", "Sistemas Operacionais Modernos", "Andrew S. Tanenbaum", "978-8575224081", True),
        Book("b023", "Compiladores: Princípios, Técnicas e Ferramentas", "Alfred V. Aho", "978-8576050467", True),
        Book("b069", "Teoria da Computação", "Michael Sipser", "978-8575224081", True),

        # Livros de Ficção e Literatura (4 livros)
        Book("b024", "1984", "George Orwell", "978-8535914849", True),
        Book("b025", "Dom Casmurro", "Machado de Assis", "978-8525408033", True),
        Book("b026", "O Pequeno Príncipe", "Antoine de Saint-Exupéry", "978-8595080808", True),
        Book("b027", "Harry Potter e a Pedra Filosofal", "J.K. Rowling", "978-8532530783", True),

        # Livros Técnicos Diversos (4 livros)
        Book("b029", "Gestão de Projetos", "Harold Kerzner", "978-8573930507", True),
        Book("b030", "Segurança da Informação", "Andrew S. Tanenbaum", "978-8575224081", True),
        Book("b031", "Interface Humano-Computador", "Alan Dix", "978-8575224081", True),
        Book("b032", "Computação em Nuvem", "Rajkumar Buyya", "978-8575224081", True),
    ]

    return sample_books

def create_sample_loans(users, books):
    """Cria empréstimos de exemplo baseados nos usuários e livros (~50 empréstimos)"""
    print("📖 Criando empréstimos de exemplo...")

    # IDs dos usuários e livros disponíveis
    user_ids = [u.id for u in users]
    book_ids = [b.id for b in books]

    sample_loans = []

    # Empréstimos ativos (sem data de devolução) - cerca de 15
    active_loans_data = [
        ("u001", "b001", 2),   # João - Python para Ciência de Dados
        ("u002", "b008", 5),   # Maria - Sistemas de Banco de Dados
        ("u003", "b016", 1),   # Pedro - Engenharia de Software Moderna
        ("u011", "b004", 7),   # Prof. Carlos - Clean Code
        ("u012", "b020", 3),   # Prof. Helena - Arquitetura de Computadores
        ("u013", "b014", 10),  # Prof. Roberto - Probabilidade e Estatística
        ("u015", "b023", 4),   # Prof. Antonio - Compiladores
        ("u016", "b029", 6),   # José - Gestão de Projetos
        ("u021", "b051", 1),   # Thiago - JavaScript
        ("u022", "b052", 3),   # Juliana - React
        ("u041", "b005", 2),   # Prof. Marcos - Design Patterns
        ("u042", "b067", 5),   # Prof. Patricia - XP Explained
        ("u043", "b068", 8),   # Prof. Ricardo - Domain-Driven Design
        ("u044", "b061", 4),   # Prof. Silvia - Modelagem de Dados
        ("u045", "b069", 6),   # Prof. Thiago - Teoria da Computação
    ]

    loan_id_counter = 1
    for user_id, book_id, days_ago in active_loans_data:
        loan_date = datetime.now() - timedelta(days=days_ago)
        loan = Loan(f"l{loan_id_counter:03d}", user_id, book_id, loan_date)
        sample_loans.append(loan)
        loan_id_counter += 1

    # Empréstimos finalizados (com data de devolução) - cerca de 35
    completed_loans_data = [
        # Empréstimos recentes finalizados
        ("u001", "b002", 45, 35),   # João devolveu Algoritmos
        ("u002", "b003", 50, 40),   # Maria devolveu Estruturas de Dados
        ("u003", "b005", 40, 30),   # Pedro devolveu Design Patterns
        ("u004", "b012", 55, 45),   # Ana devolveu Cálculo
        ("u005", "b018", 35, 25),   # Lucas devolveu Refatoração
        ("u011", "b007", 60, 50),   # Prof. Carlos devolveu IA
        ("u012", "b013", 70, 60),   # Prof. Helena devolveu Álgebra Linear
        ("u013", "b021", 65, 55),   # Prof. Roberto devolveu Redes
        ("u014", "b024", 30, 20),   # Prof. Sandra devolveu 1984
        ("u015", "b027", 25, 15),   # Prof. Antonio devolveu Harry Potter
        ("u016", "b030", 75, 65),   # José devolveu Segurança da Informação
        ("u017", "b031", 80, 70),   # Maria Clara devolveu IHC
        ("u001", "b025", 90, 80),   # João devolveu Dom Casmurro
        ("u003", "b026", 85, 75),   # Pedro devolveu Pequeno Príncipe
        ("u007", "b028", 95, 85),   # Rafael devolveu Senhor dos Anéis
        ("u009", "b006", 100, 90),  # Gabriel devolveu Machine Learning
        ("u010", "b009", 110, 100), # Isabela devolveu MongoDB
        ("u004", "b015", 120, 110), # Ana devolveu Matemática Discreta
        ("u008", "b017", 130, 120), # Beatriz devolveu Scrum
        ("u006", "b019", 140, 130), # Carolina devolveu TDD

        # Mais empréstimos finalizados para aumentar o histórico
        ("u021", "b053", 150, 140), # Thiago devolveu Node.js
        ("u022", "b054", 145, 135), # Juliana devolveu POO
        ("u023", "b055", 160, 150), # Fernando devolveu Git
        ("u024", "b056", 155, 145), # Amanda devolveu Docker
        ("u025", "b057", 170, 160), # Bruno devolveu Spring Boot
        ("u026", "b058", 165, 155), # Camila devolveu TypeScript
        ("u027", "b059", 180, 170), # Diego devolveu PostgreSQL
        ("u028", "b060", 175, 165), # Eduarda devolveu Redis
        ("u029", "b062", 190, 180), # Felipe devolveu Data Warehousing
        ("u030", "b063", 185, 175), # Gabriela devolveu Cálculo Vol. 2
        ("u031", "b064", 200, 190), # Henrique devolveu Estatística Básica
        ("u032", "b065", 195, 185), # Ingrid devolveu Geometria Analítica
        ("u033", "b066", 210, 200), # João Pedro devolveu Equações Diferenciais
        ("u034", "b010", 205, 195), # Karla devolveu SQL
        ("u035", "b011", 220, 210), # Leonardo devolveu NoSQL
    ]

    for user_id, book_id, loan_days_ago, return_days_ago in completed_loans_data:
        loan_date = datetime.now() - timedelta(days=loan_days_ago)
        return_date = datetime.now() - timedelta(days=return_days_ago)
        loan = Loan(f"l{loan_id_counter:03d}", user_id, book_id, loan_date, return_date)
        sample_loans.append(loan)
        loan_id_counter += 1

    # Empréstimos adicionais aleatórios para completar ~50 empréstimos
    random.seed(42)  # Para reprodutibilidade
    additional_loans = []

    # Gerar empréstimos aleatórios para aumentar o volume
    for _ in range(10):
        user_id = random.choice(user_ids)
        # Evitar livros já emprestados ativamente
        active_book_ids = {loan.book_id for loan in sample_loans if loan.return_date is None}
        available_books = [b_id for b_id in book_ids if b_id not in active_book_ids]

        if available_books:
            book_id = random.choice(available_books)
            days_ago = random.randint(30, 300)  # Até 10 meses atrás
            loan_date = datetime.now() - timedelta(days=days_ago)

            # 80% chance de já ter sido devolvido
            if random.random() < 0.8:
                return_days = random.randint(1, days_ago-1)
                return_date = datetime.now() - timedelta(days=return_days)
                loan = Loan(f"l{loan_id_counter:03d}", user_id, book_id, loan_date, return_date)
            else:
                loan = Loan(f"l{loan_id_counter:03d}", user_id, book_id, loan_date)

            additional_loans.append(loan)
            loan_id_counter += 1

    sample_loans.extend(additional_loans)

    # Atualizar status dos livros baseado nos empréstimos ativos
    active_book_ids = {loan.book_id for loan in sample_loans if loan.return_date is None}
    for book in books:
        if book.id in active_book_ids:
            book.available = False

    return sample_loans

def populate_database():
    """Popula o banco de dados com dados de exemplo ricos"""
    print("🚀 Iniciando população do banco de dados com dados de exemplo...")
    print("=" * 60)

    # Conectar ao banco
    if not db_config.connect():
        print("❌ ERRO: Não foi possível conectar ao MongoDB!")
        return False

    try:
        # Limpar dados existentes
        print("🧹 Limpando dados existentes...")
        db_config.users_collection.delete_many({})
        db_config.books_collection.delete_many({})
        db_config.loans_collection.delete_many({})
        print("✅ Dados existentes removidos")

        # Criar dados de exemplo
        users = create_sample_users()
        books = create_sample_books()
        loans = create_sample_loans(users, books)

        # Inserir usuários
        print(f"\n👥 Inserindo {len(users)} usuários...")
        users_inserted = 0
        for user in users:
            try:
                result = db_config.users_collection.insert_one(user.to_dict())
                users_inserted += 1
            except Exception as e:
                print(f"❌ ERRO ao inserir usuário {user.name}: {e}")

        print(f"✅ {users_inserted} usuários inseridos com sucesso")

        # Inserir livros
        print(f"\n📚 Inserindo {len(books)} livros...")
        books_inserted = 0
        for book in books:
            try:
                result = db_config.books_collection.insert_one(book.to_dict())
                books_inserted += 1
            except Exception as e:
                print(f"❌ ERRO ao inserir livro '{book.title}': {e}")

        print(f"✅ {books_inserted} livros inseridos com sucesso")

        # Inserir empréstimos
        print(f"\n📖 Inserindo {len(loans)} empréstimos...")
        loans_inserted = 0
        active_loans = 0
        completed_loans = 0

        for loan in loans:
            try:
                result = db_config.loans_collection.insert_one(loan.to_dict())
                loans_inserted += 1
                if loan.return_date is None:
                    active_loans += 1
                else:
                    completed_loans += 1
            except Exception as e:
                print(f"❌ ERRO ao inserir empréstimo {loan.id}: {e}")

        print(f"✅ {loans_inserted} empréstimos inseridos com sucesso")
        print(f"   📋 Empréstimos ativos: {active_loans}")
        print(f"   ✅ Empréstimos finalizados: {completed_loans}")

        print("\n" + "=" * 60)
        print("SISTEMA DE GESTA DE BIBLIOTECA")
        print("=" * 60)
        print("\n📊 RESUMO DOS DADOS:")
        print(f"👥 Usuários: {users_inserted} ({len([u for u in users if u.type == 'Estudante'])} estudantes, {len([u for u in users if u.type == 'Professor'])} professores, {len([u for u in users if u.type == 'Funcionário'])} funcionários)")
        print(f"📚 Livros: {books_inserted} ({len([b for b in books if not b.available])} emprestados, {len([b for b in books if b.available])} disponíveis)")
        print(f"📖 Empréstimos: {loans_inserted} ({active_loans} ativos, {completed_loans} finalizados)")

        print("\n🚀 Agora você pode executar a aplicação e ver os dados!")
        print("   Use: python simple_server.py")
        print("   Ou: python -m http.server 8080 (se usar o server.js)")

        return True

    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        db_config.disconnect()

if __name__ == "__main__":
    print("🏛️  POPULADOR DE DADOS - Biblioteca Universitária")
    print("Script para criar dados ricos de exemplo no MongoDB")
    print("=" * 60)

    success = populate_database()

    if success:
        print("\nSISTEMA DE GESTA DE BIBLIOTECA")
        print("\n💡 DICAS PARA TESTAR:")
        print("• Execute a aplicação: python simple_server.py")
        print("• Acesse: http://localhost:8000")
        print("• Navegue pelas seções: Usuários, Livros, Empréstimos, Relatórios")
        print("• Nos relatórios, você verá estatísticas reais baseadas nos empréstimos!")
    else:
        print("\n❌ PROCESSO FALHOU!")
        print("Verifique se o MongoDB está rodando e tente novamente.")
