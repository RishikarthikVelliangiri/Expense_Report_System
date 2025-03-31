import csv
from db import get_db_connection

def import_expenses(file_path, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Skip header row
            for row in reader:
                # Expecting CSV order: Category,Amount,Date,Description,Tag,Payment Method
                if len(row) < 6:
                    print("Skipping invalid row:", row)
                    continue
                category, amount, date, description, tag, payment_method = row
                try:
                    amount = float(amount)
                except ValueError:
                    print("Invalid amount in row:", row)
                    continue
                cursor.execute("""
                    INSERT INTO expenses (user_id, category, amount, date, description, tag, payment_method)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, category, amount, date, description, tag, payment_method))
        conn.commit()
        print("CSV file imported successfully!")
    except Exception as e:
        print("Error importing CSV:", e)
    finally:
        conn.close()

def export_csv(file_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "User ID", "Category", "Amount", "Date", "Description", "Tag", "Payment Method"])
            writer.writerows(rows)
        print(f"Data exported to {file_path}")
    except Exception as e:
        print("Error exporting CSV:", e)
    finally:
        conn.close()
