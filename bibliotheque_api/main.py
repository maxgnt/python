from fastapi import FastAPI, HTTPException
from database import get_connection
from models import init_db
from schemas import BookCreate, Book
from schemas import AuthorCreate, Author

app = FastAPI(title="API Bibliothèque")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "API Bibliothèque opérationnelle"}


@app.post("/books", response_model=Book)
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


@app.get("/books", response_model=list[Book])
def list_books():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT id, title, isbn, year, total_copies, available_copies
            FROM books
        """)
        rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "title": row[1],
            "isbn": row[2],
            "year": row[3],
            "total_copies": row[4],
            "available_copies": row[5]
        }
        for row in rows
    ]

@app.post("/authors", response_model=Author)
def create_author(author: AuthorCreate):
    with get_connection() as conn: 
        cursor = conn.execute ("""
        INSERT INTO authors (first_name, last_name)
        VALUES (?, ?)
        """, (author.first_name, author.last_name))
        author_id = cursor.lastrowid
        return {**author.dict(), "id": author_id}

@app.get("/authors", response_model=list[Author])
def list_authors(): 
    with get_connection() as conn: 
        cursor = conn.execute ("""
        SELECT id, first_name, last_name FROM authors
        """)
        rows = cursosr.fetchall()

        return [
            {
                "id":row[0],
                "first_name": row[1],
                "last_name": row[2]
            }
            for row in rows
        ]