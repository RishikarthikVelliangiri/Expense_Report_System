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

    # Create User table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL,
        Role TEXT CHECK(Role IN ('admin', 'user')) NOT NULL
    );
    """)

    # Create Category table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Category (
        CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT UNIQUE NOT NULL
    );
    """)

    # Create Payment_Method table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment_Method (
        PaymentMethodID INTEGER PRIMARY KEY AUTOINCREMENT,
        Method TEXT UNIQUE NOT NULL
    );
    """)

    # Create Expense table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Expense (
        ExpenseID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        -- Instead of storing category as text, ideally we would use a relationship table.
        -- However, for simplicity, we'll keep the Expense table as is.
        Category TEXT,
        Amount REAL NOT NULL,
        Date TEXT NOT NULL,
        Description TEXT,
        Tag TEXT,
        Payment_Method TEXT,
        FOREIGN KEY(UserID) REFERENCES User(UserID)
    );
    """)

    # Create Budget table with a foreign key to Category
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Budget (
        BudgetID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        CategoryID INTEGER,
        Month TEXT,  -- Format: YYYY-MM
        Amount REAL NOT NULL,
        FOREIGN KEY(UserID) REFERENCES User(UserID),
        FOREIGN KEY(CategoryID) REFERENCES Category(CategoryID)
    );
    """)

    # Insert default admin user if not exists
    cursor.execute("""
    INSERT OR IGNORE INTO User (Username, Password, Role)
    VALUES ('admin', 'admin123', 'admin');
    """)

    conn.commit()
    conn.close()

# Initialize the database on import
initialize_db()
