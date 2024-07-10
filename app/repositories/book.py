from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.schemas.book import Book, BookCreate, BookUpdate
from app.db.models import Book as BookModel


class AbstractBookRepository(ABC):

    @abstractmethod
    def get_all(self) -> list[Book]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Book:
        pass

    @abstractmethod
    def create(self, item: BookCreate) -> Book:
        pass

    @abstractmethod
    def update(self, item_id: int, item: BookUpdate) -> Book:
        pass

    @abstractmethod
    def delete(self, item_id: int) -> None:
        pass


class BookRepository(AbstractBookRepository):
    def __init__(self, session: Session) -> None:
        self._session: Session = session

    def get_all(self) -> list[Book]:
        books = self._session.query(BookModel).all()
        return [Book(**book.__dict__) for book in books]

    def get_by_id(self, item_id: int) -> Book:
        book = self._session.query(BookModel).filter_by(id=item_id).one()
        return Book(**book.__dict__)

    def create(self, item: BookCreate) -> Book:
        book_model = BookModel(**item.model_dump())
        try:
            self._session.add(book_model)
            self._session.commit()
            self._session.refresh(book_model)
        except Exception as e:
            self._session.rollback()
            raise e
        return Book(**book_model.__dict__)

    def update(self, item_id: int, item: BookUpdate) -> Book:
        existing_item = self._session.query(BookModel).filter_by(id=item_id).one()
        try:
            for key, value in item.model_dump().items():
                setattr(existing_item, key, value)
            self._session.commit()
            self._session.refresh(existing_item)
        except Exception as e:
            self._session.rollback()
            raise e
        return Book(**existing_item.__dict__)

    def delete(self, item_id: int) -> None:
        item = self._session.query(BookModel).filter_by(id=item_id).one()
        self._session.delete(item)
        self._session.commit()
