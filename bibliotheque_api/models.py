from database import get_connection


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                total_copies INTEGER NOT NULL,
                available_copies INTEGER NOT NULL
            )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        borrower_name TEXT NOT NULL,
        borrower_email TEXT NOT NULL,
        loan_date TEXT NOT NULL,
        return_date TEXT,
        status TEXT NOT NULL
        )
        """) 

def init_authors():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            )
        """)
