from starlette import status

from app.db.models import Book
from book_factory import BookFactory


def test_read_books(client):
    book = BookFactory()
    response = client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == book.title


def test_read_book(client):
    book = BookFactory()
    response = client.get(f"/books/{book.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == book.title
    assert data["author"] == book.author


def test_create_book(client, db_session):
    book_data = {
        "title": "New Book",
        "author": "New Author",
        "published_date": "2024-01-01",
        "isbn": "12345",
        "pages": 100,
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]

    db_session.commit()
    db_book = db_session.query(Book).filter_by(id=data["id"]).one()
    assert db_book.title == book_data["title"]
    assert db_book.author == book_data["author"]


def test_update_book(client, db_session):
    book = BookFactory()
    update_data = {
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "published_date": "2024-01-01",
        "isbn": "12345",
        "pages": 200,
    }
    response = client.put(f"/books/{book.id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["author"] == update_data["author"]
    assert data["pages"] == update_data["pages"]

    db_session.commit()
    db_book = db_session.query(Book).get(book.id)
    assert db_book.title == update_data["title"]
    assert db_book.author == update_data["author"]
    assert db_book.pages == update_data["pages"]


def test_delete_book(client, db_session):
    book = BookFactory()
    response = client.delete(f"/books/{book.id}")
    assert response.status_code == status.HTTP_200_OK

    db_session.commit()
    db_book = db_session.query(Book).get(book.id)
    assert db_book is None


def test_read_nonexistent_book(client):
    response = client.get("/books/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_book_invalid_data(client):
    invalid_data = {
        "title": "Book",
        "author": "Author",
        "published_date": "invalid-date",
        "isbn": "12345",
        "pages": 200,
    }
    response = client.post("/books/", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_book_invalid_data(client):
    book = BookFactory()
    invalid_data = {
        "title": "Book",
        "author": "Author",
        "published_date": "invalid-date",
        "isbn": "12345",
        "pages": 200,
    }
    response = client.put(f"/books/{book.id}", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_book(client):
    update_data = {
        "title": "Updated Book",
        "author": "Updated Author",
        "published_date": "2024-01-01",
        "isbn": "12345",
        "pages": 150,
    }
    response = client.put("/books/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_nonexistent_book(client):
    response = client.delete("/books/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
