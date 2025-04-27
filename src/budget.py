from db import get_db_connection

def set_budget(user_id, category_name, month, amount):
    """
    Set or update the budget for a given user, category, and month.
    The category must exist in the Category table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the given category exists
    cursor.execute("SELECT CategoryID FROM Category WHERE Name = ?", (category_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return f"Error: Category '{category_name}' does not exist. Please add it using 'add_category <category_name>'."
    
    category_id = row[0]
    
    # Check if a budget entry already exists for this user, category, and month
    cursor.execute("SELECT BudgetID FROM Budget WHERE UserID = ? AND CategoryID = ? AND Month = ?", (user_id, category_id, month))
    existing = cursor.fetchone()
    
    if existing:
        # Update existing budget
        cursor.execute("UPDATE Budget SET Amount = ? WHERE BudgetID = ?", (amount, existing[0]))
        message = "Budget updated successfully."
    else:
        # Insert new budget record
        cursor.execute("INSERT INTO Budget (UserID, CategoryID, Month, Amount) VALUES (?, ?, ?, ?)", (user_id, category_id, month, amount))
        message = "Budget set successfully."
    
    conn.commit()
    conn.close()
    return message

def check_budget(user_id, category_name, month):
    """
    Retrieve the budget and current spending for a given user, category (by name), and month.
    Returns a tuple (budget_amount, current_spending).
    If the category does not exist, returns (None, current_spending) with an error message.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Look up the category in the Category table
    cursor.execute("SELECT CategoryID FROM Category WHERE Name = ?", (category_name,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None, 0  # Category doesn't exist; caller should handle this case.
    
    category_id = row[0]
    
    # Get the budget amount for this user, category, and month
    cursor.execute("SELECT Amount FROM Budget WHERE UserID = ? AND CategoryID = ? AND Month = ?", (user_id, category_id, month))
    budget_row = cursor.fetchone()
    budget_amount = budget_row[0] if budget_row else None
    
    # Calculate current spending from the Expense table for this user, category, and month.
    # For simplicity, here we assume that the Expense table stores category as text.
    # In a fully normalized design, we would store a CategoryID in Expense.
    cursor.execute("SELECT SUM(Amount) FROM Expense WHERE UserID = ? AND Category = ? AND strftime('%Y-%m', Date) = ?", (user_id, category_name, month))
    spending_row = cursor.fetchone()
    spending = spending_row[0] if spending_row[0] is not None else 0.0
    
    conn.close()
    return budget_amount, spending
