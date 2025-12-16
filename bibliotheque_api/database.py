import sqlite3

DB_NAME = "bibliotheque.db"


def get_connection():
    return sqlite3.connect(DB_NAME)
