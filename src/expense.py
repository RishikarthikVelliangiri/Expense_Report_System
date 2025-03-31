from db import get_db_connection

def add_expense(user_id, category, amount, date, description, tag, payment_method):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO expenses (user_id, category, amount, date, description, tag, payment_method)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, category, amount, date, description, tag, payment_method))
        conn.commit()
        print("Expense added successfully!")
    except Exception as e:
        print("Error adding expense:", e)
    finally:
        conn.close()

def list_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def update_expense(expense_id, field, new_value):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if field not in ['category', 'amount', 'date', 'description', 'tag', 'payment_method']:
            print("Invalid field! Choose from: category, amount, date, description, tag, payment_method.")
            return
        query = f"UPDATE expenses SET {field} = ? WHERE id = ?"
        cursor.execute(query, (new_value, expense_id))
        conn.commit()
        print("Expense updated successfully!")
    except Exception as e:
        print("Error updating expense:", e)
    finally:
        conn.close()

def delete_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        print("Expense deleted successfully!")
    except Exception as e:
        print("Error deleting expense:", e)
    finally:
        conn.close()
