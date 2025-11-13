import pytest
import json
from datetime import datetime
from Model.model import User, Book, Loan
from src.report_service import ReportService


def test_user_serialization_contract():
    user = User("123", "João Silva", "joao@email.com", "Estudante")
    user_dict = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "type": user.type
    }
    
    assert "id" in user_dict
    assert "name" in user_dict
    assert "email" in user_dict
    assert "type" in user_dict
    assert isinstance(user_dict["id"], str)
    assert isinstance(user_dict["name"], str)
    assert isinstance(user_dict["email"], str)
    assert isinstance(user_dict["type"], str)


def test_book_serialization_contract():
    book = Book("456", "Python Programming", "John Doe", "123456789", True)
    book_dict = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "available": book.available
    }
    
    assert "id" in book_dict
    assert "title" in book_dict
    assert "author" in book_dict
    assert "isbn" in book_dict
    assert "available" in book_dict
    assert isinstance(book_dict["id"], str)
    assert isinstance(book_dict["title"], str)
    assert isinstance(book_dict["author"], str)
    assert isinstance(book_dict["isbn"], str)
    assert isinstance(book_dict["available"], bool)


def test_loan_serialization_contract():
    loan_date = datetime(2024, 1, 15)
    loan = Loan("789", "123", "456", loan_date)
    loan_dict = {
        "id": loan.id,
        "user_id": loan.user_id,
        "book_id": loan.book_id,
        "loan_date": loan.loan_date.isoformat(),
        "return_date": loan.return_date.isoformat() if loan.return_date else None
    }
    
    assert "id" in loan_dict
    assert "user_id" in loan_dict
    assert "book_id" in loan_dict
    assert "loan_date" in loan_dict
    assert "return_date" in loan_dict
    assert isinstance(loan_dict["id"], str)
    assert isinstance(loan_dict["user_id"], str)
    assert isinstance(loan_dict["book_id"], str)
    assert isinstance(loan_dict["loan_date"], str)


def test_report_output_contract_books():
    loans = [Loan("1", "user1", "book1", datetime.now())]
    books = [Book("book1", "Test Book", "Test Author", "123", True)]
    
    service = ReportService()
    result = service.get_most_borrowed_books(loans, books)
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    report_item = result[0]
    assert isinstance(report_item, dict)
    assert "title" in report_item
    assert "author" in report_item
    assert "loan_count" in report_item
    assert isinstance(report_item["title"], str)
    assert isinstance(report_item["author"], str)
    assert isinstance(report_item["loan_count"], int)


def test_report_output_contract_users():
    loans = [Loan("1", "user1", "book1", datetime.now())]
    users = [User("user1", "Test User", "test@email.com", "Student")]
    
    service = ReportService()
    result = service.get_most_active_users(loans, users)
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    report_item = result[0]
    assert isinstance(report_item, dict)
    assert "name" in report_item
    assert "email" in report_item
    assert "type" in report_item
    assert "loan_count" in report_item
    assert isinstance(report_item["name"], str)
    assert isinstance(report_item["email"], str)
    assert isinstance(report_item["type"], str)
    assert isinstance(report_item["loan_count"], int)
