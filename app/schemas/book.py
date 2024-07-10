from datetime import date

from .base_model import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    published_date: date
    isbn: str
    pages: int


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int
