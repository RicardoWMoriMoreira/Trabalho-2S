import pytest
from datetime import datetime
from Model.model import User, Book, Loan


def test_user_creation():
    user = User("123", "João Silva", "joao@email.com", "Estudante")
    assert user.id == "123"
    assert user.name == "João Silva"
    assert user.email == "joao@email.com"
    assert user.type == "Estudante"


def test_book_creation():
    book = Book("456", "Python Programming", "John Doe", "123456789", True)
    assert book.id == "456"
    assert book.title == "Python Programming"
    assert book.author == "John Doe"
    assert book.isbn == "123456789"
    assert book.available == True


def test_loan_creation():
    loan_date = datetime(2024, 1, 15)
    loan = Loan("789", "123", "456", loan_date)
    assert loan.id == "789"
    assert loan.user_id == "123"
    assert loan.book_id == "456"
    assert loan.loan_date == loan_date
    assert loan.return_date is None
