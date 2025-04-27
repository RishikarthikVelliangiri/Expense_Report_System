# Expense Reporting System

## Project Overview

The Expense Reporting System is a command-line application built with Python and SQLite. It allows users to log, manage, and analyze their expenses while enforcing relational database principles and using SQL queries. The system supports multi-user authentication with role-based access control (RBAC), advanced expense management, CSV import/export, reporting, data visualization, budget tracking, and expense trend analysis.

## Features

### 1. User Management & Role-Based Access Control (RBAC)
- **Multi-User Authentication:**  
  - Users can log in with a username and password.
  - Roles are multi-valued (e.g., `admin`, `user`) and stored in the `UserRole` table.
- **Admin-Only Functions:**  
  - Only users with the admin role can create new users, add new expense categories, and list all users.

### 2. Expense Management
- **CRUD Operations on Expenses:**  
  - Users can add, update, delete, and list their own expenses.
  - Each expense includes details such as amount, date, description, tag, category, and payment method.
- **Relationship Handling:**  
  - The relationship between User and Expense is explicitly modeled using the `Records` table.

### 3. Category and Payment Method Management
- **Categories:**  
  - Admins can add and list expense categories.
- **Payment Methods:**  
  - Admins can add and list payment methods.
- **Explicit Relationships:**  
  - The relationship between Expense and Category is modeled in the `ExpenseCategory` table.
  - The relationship between Expense and PaymentMethod is modeled in the `ExpensePayment` table.

### 4. Budget Tracking
- **Set and View Budgets:**  
  - Users can set a monthly budget for a specific category.
  - Budgets can only be set if the category exists in the `Category` table.
  - The `Budget` table stores a foreign key (`CategoryID`) to ensure budgets reference valid categories.
- **Relationship:**  
  - The relationship between Budget and Category is explicitly represented by the `AppliesTo` table.
  - Users can view their budgets along with current spending to monitor adherence to their budget.

### 5. CSV Import & Export
- **Import Expenses:**  
  - Users can bulk import expenses from a CSV file.  
  - Data is validated before insertion.
- **Export Expenses:**  
  - Users can export expenses to a CSV file, with the option to sort on a specified field.

### 6. Reporting & Visualization
- **Reports:**  
  - Generate reports such as top expenses, category spending, above average expenses, monthly spending per category, highest spender per month, most frequent category, payment method usage, and tag-based expense counts.
  - Reporting functions are filtered so that non-admin users only see their own data.
- **Data Visualization:**  
  - Visualize expense data using Matplotlib.  
  - Commands include displaying a pie chart for category spending and a line chart for expense trends over time.

## Database Schema & ER Diagram Overview

### Entities:
1. **User** `(UserID, Username, Password, Role)`  
2. **Expense** `(ExpenseID, UserID, Amount, Date, Description, Tag)`  
3. **Category** `(CategoryID, Name)`  
4. **PaymentMethod** `(PaymentMethodID, Method)`  
5. **Budget** `(BudgetID, Amount, UserID, CategoryID, Month)`

### Relationships:
1. **Records**: User – Expense (One-to-Many)
2. **ExpenseCategory**: Expense – Category (Many-to-One)
3. **ExpensePayment**: Expense – PaymentMethod (Many-to-One)
4. **SetsBudget**: User – Budget (One-to-Many)
5. **AppliesTo**: Budget – Category (Many-to-One)

*Note:* Although our relational schema uses foreign keys to enforce relationships, we have also explicitly created relationship tables (e.g., `Records`, `ExpenseCategory`, `ExpensePayment`, `SetsBudget`, and `AppliesTo`) to name the relationships between entities.

## Getting Started

### Prerequisites
- **Python 3.x**
- **SQLite**
- **Required Python Libraries:**  
  Install dependencies with:
  ```sh
  pip install matplotlib


# File Structure
ExpenseReportingSystem/
├── src/
│   ├── main.py
│   ├── cli.py
│   ├── db.py
│   ├── auth.py
│   ├── user.py
│   ├── expense.py
│   ├── budget.py
│   ├── reports.py
│   ├── trends.py
│   ├── visualizations.py
│   └── utils.py
├── data/
│   ├── expenses.db
│   └── sample_expenses.csv
├── docs/
│   ├── ER_Diagram.txt
│   ├── RelationalSchema.sql
│   └── README.md (this file)
└── requirements.txt


# Authors
## By:

Rishikarthik Velliangiri

Karmandeep Singh

Liam Shaw

Paarth Gala