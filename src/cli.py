import shlex
from auth import login
from user import add_user, list_users
from expense import add_expense, update_expense, delete_expense, list_expenses
from reports import (top_expenses, category_spending, above_average_expenses, 
                     monthly_category_spending, highest_spender_per_month, frequent_category, 
                     payment_method_usage, tag_expenses)
from utils import import_expenses, export_csv
from visualizations import visualize_category_spending
from trends import visualize_expense_trends
from budget import set_budget as set_budget_func, check_budget as check_budget_func

# Global variable to hold the currently logged-in user info
current_user = None

def print_welcome_banner():
    banner = """
***************************************************************
*                                                             *
*    Welcome to the Expense Reporting System!                 *
*                                                             *
*    Developed by:                                            *
*       Rishikarthik Velliangiri                              *
*       Karmandeep Singh                                      *
*       Liam Shaw                                             *
*       Paarth Gala                                           *
*                                                             *
*    Class: CSIT222                                           *
*                                                             *
***************************************************************
    """
    print(banner)

def print_help():
    help_text = """
Available commands:
  help
    Display this help message.
    
  login <username> <password>
    Authenticate a user.
    
  logout
    End the current user session.
    
  add_user <username> <password> <role>
    (Admin-only) Create a new user (role must be 'admin' or 'user').
    
  list_users
    (Admin-only) List all users with their roles.
    
  add_category <category_name>
    (Admin-only) Add a new expense category.
    
  list_categories
    List all available expense categories.
    
  add_payment_method <method_name>
    Add a new payment method.
    
  list_payment_methods
    List all available payment methods.
    
  add_expense <amount> <category> <payment_method> <date> <description> <tag>
    Add a new expense record.
    
  update_expense <expense_id> <field> <new_value>
    Update an existing expense.
    
  delete_expense <expense_id>
    Delete an expense.
    
  list_expenses
    List all expenses for the current user.
    
  import_expenses <file_path>
    Import expenses from a CSV file.
    
  export_csv <file_path> sort-on <field>
    Export expenses to a CSV file sorted by the specified field.
    
  report top_expenses <N> <start_date> <end_date>
    Show the top N highest expenses within a date range.
    
  report category_spending <category>
    Show total spending for a specific category.
    
  report above_average_expenses
    List expenses that exceed the average spending of their category.
    
  report monthly_category_spending
    Present the total spending per category for each month.
    
  report highest_spender_per_month
    Show the user with the highest spending for each month.
    
  report frequent_category
    Show the most frequently used expense category.
    
  report payment_method_usage
    Provide a breakdown of spending by payment method.
    
  report tag_expenses
    Display the count of expenses for each tag.
    
  report visualize_category_spending
    Display a pie chart of spending per category.
    
  report expense_trends
    Display a line chart of monthly expense trends.
    
  set_budget <category> <month: YYYY-MM> <amount>
    Set or update your budget for a category (must exist in the category table) and month.
    
  view_budget <category> <month: YYYY-MM>
    View your budget and current spending for a category.
    
  exit
    Exit the application.
"""
    print(help_text)

def main():
    global current_user
    # Print a fun, engaging welcome banner with our names and class info.
    print_welcome_banner()
    print("Expense Reporting System CLI. Type 'help' for available commands.")
    
    while True:
        try:
            command_input = input(">> ").strip()
            if not command_input:
                continue
            args = shlex.split(command_input)
            command = args[0].lower()

            if command == "help":
                print_help()

            elif command == "login":
                if len(args) != 3:
                    print("Usage: login <username> <password>")
                    continue
                user = login(args[1], args[2])
                if user:
                    current_user = user
                    print(f"Logged in as {args[1]} with role {user['role']}.")
                else:
                    print("Invalid credentials.")

            elif command == "logout":
                if current_user:
                    print("User logged out.")
                    current_user = None
                else:
                    print("No user is currently logged in.")

            elif command == "add_user":
                if not current_user or current_user['role'] != 'admin':
                    print("Only admin users can add new users.")
                    continue
                if len(args) != 4:
                    print("Usage: add_user <username> <password> <role>")
                    continue
                add_user(args[1], args[2], args[3])

            elif command == "list_users":
                if not current_user or current_user['role'] != 'admin':
                    print("Only admin users can list users.")
                    continue
                users = list_users()
                if users:
                    for user in users:
                        print(f"ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")
                else:
                    print("No users found.")

            elif command == "add_category":
                if not current_user or current_user['role'] != 'admin':
                    print("Only admin users can add categories.")
                    continue
                if len(args) != 2:
                    print("Usage: add_category <category_name>")
                    continue
                from db import get_db_connection
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO Category (Name) VALUES (?)", (args[1],))
                    conn.commit()
                    print(f"Category '{args[1]}' added successfully.")
                except Exception as e:
                    print("Error adding category:", e)
                finally:
                    conn.close()

            elif command == "list_categories":
                from db import get_db_connection
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Category")
                categories = cursor.fetchall()
                conn.close()
                if categories:
                    for cat in categories:
                        print(f"ID: {cat[0]}, Name: {cat[1]}")
                else:
                    print("No categories found.")

            elif command == "add_payment_method":
                if len(args) != 2:
                    print("Usage: add_payment_method <method_name>")
                    continue
                from db import get_db_connection
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO Payment_Method (Method) VALUES (?)", (args[1],))
                    conn.commit()
                    print(f"Payment method '{args[1]}' added successfully.")
                except Exception as e:
                    print("Error adding payment method:", e)
                finally:
                    conn.close()

            elif command == "list_payment_methods":
                from db import get_db_connection
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Payment_Method")
                methods = cursor.fetchall()
                conn.close()
                if methods:
                    for method in methods:
                        print(f"ID: {method[0]}, Method: {method[1]}")
                else:
                    print("No payment methods found.")

            elif command == "add_expense":
                if not current_user:
                    print("Please login to add an expense.")
                    continue
                if len(args) < 7:
                    print("Usage: add_expense <amount> <category> <payment_method> <date> <description> <tag>")
                    continue
                try:
                    amount = float(args[1])
                except ValueError:
                    print("Invalid amount.")
                    continue
                # Order: amount, category, payment_method, date, description, tag
                add_expense(current_user['id'], args[2], amount, args[4], args[5], args[6], args[3])

            elif command == "update_expense":
                if not current_user:
                    print("Please login to update an expense.")
                    continue
                if len(args) != 4:
                    print("Usage: update_expense <expense_id> <field> <new_value>")
                    continue
                update_expense(args[1], args[2], args[3])

            elif command == "delete_expense":
                if not current_user:
                    print("Please login to delete an expense.")
                    continue
                if len(args) != 2:
                    print("Usage: delete_expense <expense_id>")
                    continue
                delete_expense(args[1])

            elif command == "list_expenses":
                if not current_user:
                    print("Please login to view expenses.")
                    continue
                expenses = list_expenses(current_user['id'])
                if expenses:
                    for expense in expenses:
                        print(expense)
                else:
                    print("No expenses found.")

            elif command == "import_expenses":
                if not current_user:
                    print("Please login to import expenses.")
                    continue
                if len(args) != 2:
                    print("Usage: import_expenses <file_path>")
                    continue
                import_expenses(args[1], current_user['id'])

            elif command == "export_csv":
                if not current_user:
                    print("Please login to export expenses.")
                    continue
                if len(args) != 4 or args[2].lower() != "sort-on":
                    print("Usage: export_csv <file_path> sort-on <field>")
                    continue
                export_csv(args[1])

            elif command == "report":
                if not current_user:
                    print("Please login to generate reports.")
                    continue
                if len(args) < 2:
                    print("Usage: report <report_type> [additional parameters]")
                    continue
                # For non-admin users, pass their ID to filter reports.
                filter_user = current_user['id'] if current_user['role'] != 'admin' else None
                report_type = args[1].lower()
                if report_type == "top_expenses":
                    if len(args) != 5:
                        print("Usage: report top_expenses <N> <start_date> <end_date>")
                        continue
                    results = top_expenses(int(args[2]), (args[3], args[4]), filter_user)
                    for r in results:
                        print(r)
                elif report_type == "category_spending":
                    if len(args) != 3:
                        print("Usage: report category_spending <category>")
                        continue
                    total = category_spending(args[2], filter_user)
                    print(f"Total spending for {args[2]}: {total}")
                elif report_type == "above_average_expenses":
                    results = above_average_expenses(filter_user)
                    for r in results:
                        print(r)
                elif report_type == "monthly_category_spending":
                    results = monthly_category_spending(filter_user)
                    for r in results:
                        print(r)
                elif report_type == "highest_spender_per_month":
                    results = highest_spender_per_month(filter_user)
                    for r in results:
                        print(r)
                elif report_type == "frequent_category":
                    result = frequent_category(filter_user)
                    print(f"Most frequent category: {result}")
                elif report_type == "payment_method_usage":
                    results = payment_method_usage(filter_user)
                    for r in results:
                        print(r)
                elif report_type == "tag_expenses":
                    results = tag_expenses(filter_user)
                    for r in results:
                        print(r)
                elif report_type == "visualize_category_spending":
                    visualize_category_spending()
                elif report_type == "expense_trends":
                    visualize_expense_trends(filter_user)
                else:
                    print("Unknown report type.")

            elif command == "set_budget":
                if not current_user:
                    print("Please login to set a budget.")
                    continue
                if len(args) != 4:
                    print("Usage: set_budget <category> <month: YYYY-MM> <amount>")
                    continue
                try:
                    budget_amount = float(args[3])
                except ValueError:
                    print("Invalid amount.")
                    continue
                message = set_budget_func(current_user['id'], args[1], args[2], budget_amount)
                print(message)

            elif command == "view_budget":
                if not current_user:
                    print("Please login to view a budget.")
                    continue
                if len(args) != 3:
                    print("Usage: view_budget <category> <month: YYYY-MM>")
                    continue
                budget_amount, spending = check_budget_func(current_user['id'], args[1], args[2])
                if budget_amount is None:
                    print(f"No budget set for category '{args[1]}' in {args[2]}. Current spending: {spending}")
                else:
                    print(f"Budget for {args[1]} in {args[2]}: {budget_amount}. Current spending: {spending}")
                    if spending >= budget_amount:
                        print("Alert: You have exceeded your budget!")
                    elif spending >= 0.9 * budget_amount:
                        print("Warning: You are close to exceeding your budget.")

            elif command == "exit":
                print("Exiting the application.")
                break

            else:
                print("Unknown command. Type 'help' to see available commands.")

        except Exception as e:
            print("Error processing command:", e)

if __name__ == "__main__":
    main()
