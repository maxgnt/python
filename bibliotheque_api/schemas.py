from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    isbn: str
    year: int
    total_copies: int
    available_copies: int


class Book(BookCreate):
    id: int

class AuthorCreate(BaseModel):
    first_name: str
    last_name: str

class Author(AuthorCreate):
    id: int