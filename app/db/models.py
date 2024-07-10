from sqlalchemy import Column, Integer, String, Date
from .base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_date = Column(Date, nullable=False)
    isbn = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
