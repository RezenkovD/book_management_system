from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.services.book import BookService, get_book_service
from app.schemas.book import Book, BookCreate, BookUpdate

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/", response_model=list[Book])
def read_books(book_service: BookService = Depends(get_book_service)):
    books = book_service.get_all_books()
    return books


@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    try:
        db_book = book_service.get_book_by_id(book_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return db_book


@router.post("/", response_model=Book)
def create_book(
    book: BookCreate, book_service: BookService = Depends(get_book_service)
):
    try:
        return book_service.create_book(book)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book: BookUpdate,
    book_service: BookService = Depends(get_book_service),
):
    try:
        db_book = book_service.update_book(book_id, book)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return db_book


@router.delete("/{book_id}")
def delete_book(book_id: int, book_service: BookService = Depends(get_book_service)):
    try:
        book_service.delete_book(book_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
