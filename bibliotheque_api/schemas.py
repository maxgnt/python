from pydantic import BaseModel, field_validator
from datetime import datetime
from datetime import date 

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

class AuthorCreate (BaseModel):
    first_name: str
    last_name: str
    birth_date: date

    @field_validator('birth_date')
    @classmethod
    def birth_date_not_future(cls, value):
        if value > date.today():
            raise ValueError("La date de naissance ne peut pas être dans le futur")
        return value

class BookCreate (BaseModel):
    title: str
    isbn: str
    year: int
    total_copies: int
    available_copies: int
    author_id: int
    
    @field_validator("year")
    @classmethod
    def validate_year(cls, value): 
        current_year = date.today().year
        if value < 1450 or value > current_year: 
            raise ValueError(
                f"L'année de publication doit être entre 1450 et {current_year}"
            )
        return value

class LoanCreate(BaseModel): 
    book_id: int
    borrower_name: str
    borrower_email: str
    loan_date: datetime

    @field_validator("loan_date")
    @classmethod
    def loan_date_not_future(cls, value): 
        if value and value > datetime.now(): 
            raise ValueError("La date d'emprunt ne peut pas être dans le futur")
        return value
    
    class Loan (BaseModel): 
        id: int
        book_id: int
        borrower_name: str
        borrower_email: str
        loan_date: datetime
        return_date: datetime | None
        status: str

        @field_validator("return_date")
        @classmethod
        def return_after_loan(cls, value, info): 
            loan_date = info.data.get("loan_date")
            if value and loan_date and value < loan_date: 
                raise ValueError("La date de retour doit être après la date d'emprunt"
                )
            return value
            