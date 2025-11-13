from collections import Counter
from typing import List, Dict, Any
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from Model.model import User, Book, Loan


class ReportService:
    
    def get_most_borrowed_books(self, loans: List[Loan], books: List[Book] = None) -> List[Dict[str, Any]]:
        if not loans or loans is None:
            return []
        
        book_counts = Counter(loan.book_id for loan in loans)
        books_dict = self._create_books_dict(books or [])
        
        return [
            self._format_book_report(book_id, count, books_dict)
            for book_id, count in book_counts.most_common()
        ]
    
    def _create_books_dict(self, books: List[Book]) -> Dict[str, Book]:
        return {book.id: book for book in books}
    
    def _format_book_report(self, book_id: str, count: int, books_dict: Dict[str, Book]) -> Dict[str, Any]:
        book = books_dict.get(book_id)
        if book:
            return {
                "title": book.title,
                "author": book.author,
                "loan_count": count
            }
        return {
            "book_id": book_id,
            "loan_count": count
        }
    
    def get_most_active_users(self, loans: List[Loan], users: List[User] = None) -> List[Dict[str, Any]]:
        if not loans or loans is None:
            return []
        
        user_counts = Counter(loan.user_id for loan in loans)
        users_dict = self._create_users_dict(users or [])
        
        return [
            self._format_user_report(user_id, count, users_dict)
            for user_id, count in user_counts.most_common()
        ]
    
    def _create_users_dict(self, users: List[User]) -> Dict[str, User]:
        return {user.id: user for user in users}
    
    def _format_user_report(self, user_id: str, count: int, users_dict: Dict[str, User]) -> Dict[str, Any]:
        user = users_dict.get(user_id)
        if user:
            return {
                "name": user.name,
                "email": user.email,
                "type": user.type,
                "loan_count": count
            }
        return {
            "user_id": user_id,
            "loan_count": count
        }
