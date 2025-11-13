import pytest
from datetime import datetime
from Model.model import User, Book, Loan
from src.report_service import ReportService


def test_most_borrowed_books_empty_data():
    service = ReportService()
    result = service.get_most_borrowed_books([])
    assert result == []


def test_most_borrowed_books_with_data():
    loans = [
        Loan("1", "user1", "book1", datetime.now()),
        Loan("2", "user2", "book1", datetime.now()),
        Loan("3", "user3", "book2", datetime.now()),
    ]
    books = [
        Book("book1", "Python Guide", "Author A", "123", True),
        Book("book2", "Java Basics", "Author B", "456", True),
    ]
    
    service = ReportService()
    result = service.get_most_borrowed_books(loans, books)
    
    assert len(result) == 2
    assert result[0]["title"] == "Python Guide"
    assert result[0]["loan_count"] == 2
    assert result[1]["title"] == "Java Basics"
    assert result[1]["loan_count"] == 1


def test_most_active_users_empty_data():
    service = ReportService()
    result = service.get_most_active_users([])
    assert result == []


def test_most_active_users_with_data():
    loans = [
        Loan("1", "user1", "book1", datetime.now()),
        Loan("2", "user1", "book2", datetime.now()),
        Loan("3", "user2", "book1", datetime.now()),
    ]
    users = [
        User("user1", "João Silva", "joao@email.com", "Estudante"),
        User("user2", "Maria Santos", "maria@email.com", "Professor"),
    ]
    
    service = ReportService()
    result = service.get_most_active_users(loans, users)
    
    assert len(result) == 2
    assert result[0]["name"] == "João Silva"
    assert result[0]["loan_count"] == 2
    assert result[1]["name"] == "Maria Santos"
    assert result[1]["loan_count"] == 1
