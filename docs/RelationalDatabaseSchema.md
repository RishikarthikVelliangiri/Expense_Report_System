# Relational Schema Design for Expense Reporting System

## Entities

### 1. User
| Field    | Type      | Description                              |
| -------- | --------- | ---------------------------------------- |
| UserID   | INT (PK)  | Unique user id                           |
| Username | VARCHAR   | Username (unique)                        |
| Password | VARCHAR   | User password                            |
| Role     | VARCHAR   | User role (multi-valued: admin, user)    |

*Note:* The multi-valued attribute **Role** is stored in a separate table called **UserRole**.

---

### 1a. UserRole
| Field  | Type     | Description                             |
| ------ | -------- | --------------------------------------- |
| UserID | INT      | References User(UserID)                 |
| Role   | VARCHAR  | Role value (either 'admin' or 'user')   |

*Primary Key:* (UserID, Role)

---

### 2. Expense
| Field         | Type      | Description                                                      |
| ------------- | --------- | ---------------------------------------------------------------- |
| ExpenseID     | INT (PK)  | Unique expense id                                                |
| UserID        | INT (FK)  | References User(UserID); indicates which user recorded the expense |
| Category      | VARCHAR   | Expense category (stored as text; see relationship below for explicit relation) |
| Amount        | DECIMAL   | Expense amount                                                   |
| Date          | DATE      | Date of the expense (format: YYYY-MM-DD)                         |
| Tag           | VARCHAR   | Expense tag                                                      |
| Description   | VARCHAR   | Expense description (optional)                                   |
| Payment_Method| VARCHAR   | Payment method used (stored as text; see relationship below for explicit relation) |

---

### 3. Category
| Field      | Type      | Description                                |
| ---------- | --------- | ------------------------------------------ |
| CategoryID | INT (PK)  | Unique category id                         |
| Name       | VARCHAR   | Category name                              |

---

### 4. PaymentMethod
| Field           | Type      | Description                                 |
| --------------- | --------- | ------------------------------------------- |
| PaymentMethodID | INT (PK)  | Unique payment method id                    |
| Method          | VARCHAR   | Payment method name                         |

---

### 5. Budget
| Field    | Type      | Description                                                     |
| -------- | --------- | --------------------------------------------------------------- |
| BudgetID | INT (PK)  | Unique budget id                                                |
| Amount   | DECIMAL   | Budget amount                                                   |
| UserID   | INT (FK)  | References User(UserID); indicates which user set the budget      |
| Category | VARCHAR   | Budget category (stored as text; see relationship below for explicit relation) |
| Month    | VARCHAR   | Month for the budget (format: YYYY-MM)                          |

---

