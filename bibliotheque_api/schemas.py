from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    isbn: str
    year: int
    total_copies: int
    available_copies: int


class Book(BookCreate):
    id: int
