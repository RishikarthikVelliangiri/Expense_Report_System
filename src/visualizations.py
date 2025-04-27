import matplotlib.pyplot as plt
from db import get_db_connection

def visualize_category_spending():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query to get total spending per category
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No expense data available for visualization.")
        return

    # Separate the query result into categories and their spending amounts
    categories = [row[0] for row in data]
    spending = [row[1] for row in data]

    # Plot a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(spending, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title('Category Spending Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
