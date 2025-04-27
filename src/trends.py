import matplotlib.pyplot as plt
from db import get_db_connection

def visualize_expense_trends(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT strftime('%Y-%m', date) AS month, SUM(amount)
            FROM expenses
            WHERE user_id = ?
            GROUP BY month
            ORDER BY month
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT strftime('%Y-%m', date) AS month, SUM(amount)
            FROM expenses
            GROUP BY month
            ORDER BY month
        """)
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No expense data available to display trends.")
        return

    months = [row[0] for row in data]
    totals = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(months, totals, marker='o', linestyle='-', color='b')
    plt.title("Monthly Expense Trends")
    plt.xlabel("Month")
    plt.ylabel("Total Expense")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
