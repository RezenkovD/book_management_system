from datetime import date

import factory
from factory.fuzzy import FuzzyInteger
from sqlalchemy.orm import scoped_session

from tests.conftest import TestingSessionLocal
from app.db.models import Book


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = scoped_session(TestingSessionLocal)
        sqlalchemy_session_persistence = "commit"


class BookFactory(BaseFactory):
    title = factory.Faker("word")
    author = factory.Faker("word")
    published_date = date.today()
    isbn = FuzzyInteger(1, 50)
    pages = FuzzyInteger(1, 50)

    class Meta:
        model = Book
