from pydantic import BaseModel
from datetime import datetime

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

class LoanCreate (BaseModel):
    book_id: int
    borrower_name: str
    borrower_email: str

class Loan (LoanCreate):
    id: int
    loan_date: datetime
    return_date: datetime | None
    status: str