from db import get_db_connection

def top_expenses(n, date_range):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT * FROM expenses
        WHERE date BETWEEN ? AND ?
        ORDER BY amount DESC LIMIT ?
        """, (date_range[0], date_range[1], n))
        results = cursor.fetchall()
    except Exception as e:
        print("Error generating top expenses report:", e)
        results = []
    finally:
        conn.close()
    return results

def category_spending(category):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
        total = cursor.fetchone()[0]
    except Exception as e:
        print("Error calculating category spending:", e)
        total = 0
    finally:
        conn.close()
    return total if total else 0

def above_average_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT e.*
        FROM expenses e
        JOIN (
            SELECT category, AVG(amount) as avg_amount
            FROM expenses
            GROUP BY category
        ) a ON e.category = a.category
        WHERE e.amount > a.avg_amount
        """)
        results = cursor.fetchall()
    except Exception as e:
        print("Error generating above average expenses report:", e)
        results = []
    finally:
        conn.close()
    return results

def monthly_category_spending():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT strftime('%Y-%m', date) as month, category, SUM(amount)
        FROM expenses
        GROUP BY month, category
        ORDER BY month
        """)
        results = cursor.fetchall()
    except Exception as e:
        print("Error generating monthly category spending report:", e)
        results = []
    finally:
        conn.close()
    return results

def highest_spender_per_month():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT month, user_id, MAX(total) FROM (
            SELECT strftime('%Y-%m', date) as month, user_id, SUM(amount) as total
            FROM expenses
            GROUP BY month, user_id
        )
        GROUP BY month
        """)
        results = cursor.fetchall()
    except Exception as e:
        print("Error generating highest spender per month report:", e)
        results = []
    finally:
        conn.close()
    return results

def frequent_category():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT category, COUNT(*) as freq
        FROM expenses
        GROUP BY category
        ORDER BY freq DESC LIMIT 1
        """)
        result = cursor.fetchone()
    except Exception as e:
        print("Error generating frequent category report:", e)
        result = None
    finally:
        conn.close()
    return result[0] if result else "None"

def payment_method_usage():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT payment_method, SUM(amount)
        FROM expenses
        GROUP BY payment_method
        """)
        results = cursor.fetchall()
    except Exception as e:
        print("Error generating payment method usage report:", e)
        results = []
    finally:
        conn.close()
    return results

def tag_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT tag, COUNT(*)
        FROM expenses
        GROUP BY tag
        """)
        results = cursor.fetchall()
    except Exception as e:
        print("Error generating tag expenses report:", e)
        results = []
    finally:
        conn.close()
    return results
