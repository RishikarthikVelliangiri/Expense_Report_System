from db import get_db_connection

def top_expenses(n, date_range, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT * FROM expenses 
            WHERE user_id = ? AND date BETWEEN ? AND ?
            ORDER BY amount DESC LIMIT ?
        """, (user_id, date_range[0], date_range[1], n))
    else:
        cursor.execute("""
            SELECT * FROM expenses 
            WHERE date BETWEEN ? AND ?
            ORDER BY amount DESC LIMIT ?
        """, (date_range[0], date_range[1], n))
    results = cursor.fetchall()
    conn.close()
    return results

def category_spending(category, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND category = ?", (user_id, category))
    else:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def above_average_expenses(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT e.*
            FROM expenses e
            JOIN (
                SELECT category, AVG(amount) AS avg_amount
                FROM expenses
                WHERE user_id = ?
                GROUP BY category
            ) a ON e.category = a.category
            WHERE e.amount > a.avg_amount AND e.user_id = ?
        """, (user_id, user_id))
    else:
        cursor.execute("""
            SELECT e.*
            FROM expenses e
            JOIN (
                SELECT category, AVG(amount) AS avg_amount
                FROM expenses
                GROUP BY category
            ) a ON e.category = a.category
            WHERE e.amount > a.avg_amount
        """)
    results = cursor.fetchall()
    conn.close()
    return results

def monthly_category_spending(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT strftime('%Y-%m', date) AS month, category, SUM(amount)
            FROM expenses
            WHERE user_id = ?
            GROUP BY month, category
            ORDER BY month
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT strftime('%Y-%m', date) AS month, category, SUM(amount)
            FROM expenses
            GROUP BY month, category
            ORDER BY month
        """)
    results = cursor.fetchall()
    conn.close()
    return results

def highest_spender_per_month(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        # When a user is specified, only that user's spending is relevant.
        cursor.execute("""
            SELECT strftime('%Y-%m', date) AS month, user_id, SUM(amount) AS total
            FROM expenses
            WHERE user_id = ?
            GROUP BY month
            ORDER BY month
        """, (user_id,))
    else:
        # For all users, determine the highest spender per month.
        cursor.execute("""
            SELECT month, user_id, MAX(total)
            FROM (
                SELECT strftime('%Y-%m', date) AS month, user_id, SUM(amount) AS total
                FROM expenses
                GROUP BY month, user_id
            )
            GROUP BY month
        """)
    results = cursor.fetchall()
    conn.close()
    return results

def frequent_category(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT category, COUNT(*) AS freq
            FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY freq DESC LIMIT 1
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT category, COUNT(*) AS freq
            FROM expenses
            GROUP BY category
            ORDER BY freq DESC LIMIT 1
        """)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "None"

def payment_method_usage(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT payment_method, SUM(amount)
            FROM expenses
            WHERE user_id = ?
            GROUP BY payment_method
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT payment_method, SUM(amount)
            FROM expenses
            GROUP BY payment_method
        """)
    results = cursor.fetchall()
    conn.close()
    return results

def tag_expenses(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT tag, COUNT(*)
            FROM expenses
            WHERE user_id = ?
            GROUP BY tag
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT tag, COUNT(*)
            FROM expenses
            GROUP BY tag
        """)
    results = cursor.fetchall()
    conn.close()
    return results
