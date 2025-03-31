from db import get_db_connection

def add_user(username, password, role):
    if role not in ['admin', 'user']:
        print("Invalid role! Choose 'admin' or 'user'.")
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        print(f"User '{username}' added successfully!")
    except Exception as e:
        print("Error adding user:", e)
    finally:
        conn.close()

def list_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
