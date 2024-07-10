from fastapi import Depends
from sqlalchemy.orm import Session

from app.repositories.book import AbstractBookRepository, BookRepository
from app.schemas.book import BookCreate, Book, BookUpdate
from app.db.session import get_db


class BookService:
    def __init__(self, book_repository: AbstractBookRepository):
        self.book_repository = book_repository

    def get_all_books(self) -> list[Book]:
        return self.book_repository.get_all()

    def get_book_by_id(self, book_id: int) -> Book:
        return self.book_repository.get_by_id(book_id)

    def create_book(self, book: BookCreate) -> Book:
        return self.book_repository.create(book)

    def update_book(self, book_id: int, book_data: BookUpdate) -> Book:
        return self.book_repository.update(book_id, book_data)

    def delete_book(self, book_id: int) -> None:
        return self.book_repository.delete(book_id)


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    book_repository = BookRepository(db)
    return BookService(book_repository)
