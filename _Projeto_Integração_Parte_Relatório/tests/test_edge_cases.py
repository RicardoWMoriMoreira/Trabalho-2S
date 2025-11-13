import pytest
from datetime import datetime
from Model.model import User, Book, Loan
from src.report_service import ReportService


def test_report_service_with_none_inputs():
    service = ReportService()
    assert service.get_most_borrowed_books(None) == []
    assert service.get_most_active_users(None) == []


def test_report_service_with_empty_books_list():
    loans = [Loan("1", "user1", "book1", datetime.now())]
    service = ReportService()
    result = service.get_most_borrowed_books(loans, [])
    assert len(result) == 1
    assert "book_id" in result[0]
    assert result[0]["book_id"] == "book1"


def test_report_service_with_empty_users_list():
    loans = [Loan("1", "user1", "book1", datetime.now())]
    service = ReportService()
    result = service.get_most_active_users(loans, [])
    assert len(result) == 1
    assert "user_id" in result[0]
    assert result[0]["user_id"] == "user1"


def test_user_with_empty_fields():
    user = User("", "", "", "")
    assert user.id == ""
    assert user.name == ""
    assert user.email == ""
    assert user.type == ""


def test_book_with_empty_fields():
    book = Book("", "", "", "", False)
    assert book.id == ""
    assert book.title == ""
    assert book.author == ""
    assert book.isbn == ""
    assert book.available == False


def test_loan_with_return_date():
    loan_date = datetime(2024, 1, 15)
    return_date = datetime(2024, 2, 15)
    loan = Loan("1", "user1", "book1", loan_date, return_date)
    assert loan.return_date == return_date


def test_multiple_loans_same_book():
    loans = [
        Loan("1", "user1", "book1", datetime.now()),
        Loan("2", "user2", "book1", datetime.now()),
        Loan("3", "user3", "book1", datetime.now()),
    ]
    books = [Book("book1", "Popular Book", "Author", "123", True)]
    
    service = ReportService()
    result = service.get_most_borrowed_books(loans, books)
    
    assert len(result) == 1
    assert result[0]["loan_count"] == 3


def test_multiple_loans_same_user():
    loans = [
        Loan("1", "user1", "book1", datetime.now()),
        Loan("2", "user1", "book2", datetime.now()),
        Loan("3", "user1", "book3", datetime.now()),
    ]
    users = [User("user1", "Active User", "user@email.com", "Student")]
    
    service = ReportService()
    result = service.get_most_active_users(loans, users)
    
    assert len(result) == 1
    assert result[0]["loan_count"] == 3


def test_report_ordering():
    loans = [
        Loan("1", "user1", "book1", datetime.now()),
        Loan("2", "user2", "book2", datetime.now()),
        Loan("3", "user2", "book2", datetime.now()),
        Loan("4", "user3", "book3", datetime.now()),
        Loan("5", "user3", "book3", datetime.now()),
        Loan("6", "user3", "book3", datetime.now()),
    ]
    books = [
        Book("book1", "Book A", "Author A", "111", True),
        Book("book2", "Book B", "Author B", "222", True),
        Book("book3", "Book C", "Author C", "333", True),
    ]
    
    service = ReportService()
    result = service.get_most_borrowed_books(loans, books)
    
    assert len(result) == 3
    assert result[0]["title"] == "Book C"
    assert result[0]["loan_count"] == 3
    assert result[1]["title"] == "Book B"
    assert result[1]["loan_count"] == 2
    assert result[2]["title"] == "Book A"
    assert result[2]["loan_count"] == 1
