#!/usr/bin/env python3
"""
Teste básico para verificar se o código funciona
"""
print("Teste básico - Biblioteca")
print("=" * 30)

try:
    # Testar imports
    print("Testando imports...")
    from View_and_Interface.view import mock_db, User, Book, Loan
    print("✅ Imports funcionaram")

    # Testar dados mock
    print("\nTestando dados mock...")
    users = mock_db.get_users()
    books = mock_db.get_books()
    loans = mock_db.get_loans()

    print(f"Usuários: {len(users)}")
    print(f"Livros: {len(books)}")
    print(f"Empréstimos: {len(loans)}")

    # Testar empréstimos ativos
    emprestimos_ativos = {str(e.book_id).strip() for e in loans if e.return_date is None}
    print(f"Livros com empréstimos ativos: {emprestimos_ativos}")

    # Testar status dos livros
    print("\nStatus dos livros:")
    for book in books:
        if book.id and book.title:
            is_borrowed = str(book.id).strip() in emprestimos_ativos
            status = "EMPRESTADO" if is_borrowed else "DISPONÍVEL"
            print(f"  {book.title} (id={book.id}): {status}")

    print("\n✅ Teste básico passou!")

except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
