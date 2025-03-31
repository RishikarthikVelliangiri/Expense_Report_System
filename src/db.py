import sqlite3
import os

def get_db_connection():
    # Ensure the data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect("data/expenses.db")
    return conn

def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'user')) NOT NULL
    );
    """)

    # Create categories table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
    """)

    # Create payment_methods table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_methods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        method TEXT UNIQUE NOT NULL
    );
    """)

    # Create expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        tag TEXT,
        payment_method TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)

    # Insert default admin if not exists
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES ('admin', 'admin123', 'admin');
    """)

    conn.commit()
    conn.close()

# Initialize the database upon import
initialize_db()
