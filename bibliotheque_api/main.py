from fastapi import FastAPI, HTTPException
from database import get_connection
from models import init_db
from schemas import BookCreate, Book
from schemas import AuthorCreate, Author
from schemas import LoanCreate, Loan
from datetime import datetime

app = FastAPI(title="API Bibliothèque")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API Bibliothèque opérationnelle"}


@app.post("/books", response_model=Book, tags=["Livres"])
def create_book(book: BookCreate):
    if book.available_copies > book.total_copies:
        raise HTTPException(
            status_code=400,
            detail="Les exemplaires disponibles ne peuvent pas dépasser le total"
        )

    try:
        with get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO books (title, isbn, year, total_copies, available_copies)
                VALUES (?, ?, ?, ?, ?)
            """, (
                book.title,
                book.isbn,
                book.year,
                book.total_copies,
                book.available_copies
            ))
            book_id = cursor.lastrowid
    except Exception:
        raise HTTPException(status_code=400, detail="ISBN déjà existant")

    return {**book.dict(), "id": book_id}


@app.get("/books/{book_id}", response_model=Book, tags=["Livres"])
def get_book(book_id: int):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, title, isbn, year, total_copies, available_copies
            FROM books WHERE id = ?
        """, (book_id,)).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Livre introuvable")

    return {
        "id": row[0],
        "title": row[1],
        "isbn": row[2],
        "year": row[3],
        "total_copies": row[4],
        "available_copies": row[5]
    }


@app.post("/authors", response_model=Author, tags=["Auteurs"])
def create_author(author: AuthorCreate):
    with get_connection() as conn: 
        cursor = conn.execute ("""
        INSERT INTO authors (first_name, last_name)
        VALUES (?, ?)
        """, (author.first_name, author.last_name))
        author_id = cursor.lastrowid
        return {**author.dict(), "id": author_id}

@app.get("/authors/{author_id}", response_model=Author, tags=["Auteurs"])
def get_author(author_id: int):
    with get_connection() as conn:
        row = conn.execute("""
            SELECT id, first_name, last_name
            FROM authors WHERE id = ?
        """, (author_id,)).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Auteur introuvable")

    return {
        "id": row[0],
        "first_name": row[1],
        "last_name": row[2]
    }


@app.post("/loans", response_model=Loan, tags=["Emprunts"])
def create_loan(loan: LoanCreate):
    with get_connection() as conn:
        book = conn.execute(
            "SELECT available_copies FROM books WHERE id = ?",
            (loan.book_id,)
        ).fetchone()

        if not book:
            raise HTTPException(status_code=404, detail="Livre non trouvé")

        if book[0] <= 0:
            raise HTTPException(status_code=400, detail="Indisponible pour le moment")

        count = conn.execute("""
            SELECT COUNT(*) FROM loans
            WHERE borrower_email = ? AND status = 'active'
        """, (loan.borrower_email,)).fetchone()[0]

        if count >= 5:
            raise HTTPException(
                status_code=400,
                detail="Limite de 5 emprunts atteinte"
            )

        cursor = conn.execute("""
            INSERT INTO loans (
                book_id, borrower_name, borrower_email,
                loan_date, status
            )
            VALUES (?, ?, ?, ?, 'active')
        """, (
            loan.book_id,
            loan.borrower_name,
            loan.borrower_email,
            datetime.utcnow().isoformat()
        ))

        conn.execute("""
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE id = ?
        """, (loan.book_id,))

        loan_id = cursor.lastrowid

    return {
        "id": loan_id,
        **loan.dict(),
        "loan_date": datetime.now(),
        "return_date": None,
        "status": "active"
    }



@app.post("/loans/{loan_id}/return", tags=["Emprunts"])
def return_loan(loan_id: int):
    with get_connection() as conn:
        loan = conn.execute("""
            SELECT book_id, status FROM loans WHERE id = ?
        """, (loan_id,)).fetchone()

        if not loan:
            raise HTTPException(status_code=404, detail="Emprunt introuvable")

        if loan[1] != "active":
            raise HTTPException(status_code=400, detail="Emprunt déjà retourné")

        conn.execute("""
            UPDATE loans
            SET status = 'returned',
                return_date = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), loan_id))

    
        conn.execute("""
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE id = ?
        """, (loan[0],))

    return {"message": "Livre retourné avec succès"}
    

@app.get("/loans", response_model=list[Loan], tags=["Emprunts"])
def list_loans():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, book_id, borrower_name, borrower_email,
                   loan_date, return_date, status
            FROM loans
        """).fetchall()

    return [
        {
            "id": row[0],
            "book_id": row[1],
            "borrower_name": row[2],
            "borrower_email": row[3],
            "loan_date": row[4],
            "return_date": row[5],
            "status": row[6]
        }
        for row in rows
    ]
