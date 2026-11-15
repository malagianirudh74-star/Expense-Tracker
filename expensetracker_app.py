# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import datetime


# ============================================================
# 2. CREATE THE FLASK APPLICATION
# ============================================================

app = Flask(__name__)

# Secret key is required for Flask flash messages.
app.secret_key = "expense_tracker_secret_key"


# ============================================================
# 3. DATABASE CONNECTION
# ============================================================

def get_db_connection():

    # Connect to the SQLite database.
    connection = sqlite3.connect("expenses.db")

    # Allows us to access database columns using their names.
    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# 4. CREATE DATABASE TABLE
# ============================================================

def create_table():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL

        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# 5. HOME PAGE
# ============================================================

@app.route("/")
def home():

    connection = get_db_connection()

    # Retrieve all expenses.
    expenses = connection.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    # Calculate total expenses.
    total = connection.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()[0]

    if total is None:
        total = 0

    # Count the number of transactions.
    count = connection.execute(
        "SELECT COUNT(*) FROM expenses"
    ).fetchone()[0]

    # Calculate category-wise expenses.
    categories = connection.execute("""
        SELECT category, SUM(amount) AS category_total
        FROM expenses
        GROUP BY category
        ORDER BY category_total DESC
    """).fetchall()

    connection.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        count=count,
        categories=categories
    )

# ============================================================
# CALCULATE TOTAL EXPENSES
# ============================================================

@app.route("/total")
def calculate_total():

    connection = get_db_connection()

    # Calculate the total amount spent.
    total = connection.execute(
        "SELECT SUM(amount) FROM expenses"
    ).fetchone()[0]

    if total is None:
        total = 0

    # Count the total number of transactions.
    count = connection.execute(
        "SELECT COUNT(*) FROM expenses"
    ).fetchone()[0]

    # Calculate category-wise expenses.
    categories = connection.execute("""
        SELECT category, SUM(amount) AS category_total
        FROM expenses
        GROUP BY category
        ORDER BY category_total DESC
    """).fetchall()

    connection.close()

    return render_template(
        "total.html",
        total=total,
        count=count,
        categories=categories
    )


# ============================================================
# 6. ADD EXPENSE
# ============================================================

@app.route("/add", methods=["POST"])
def add_expense():

    description = request.form.get("description", "").strip()
    amount = request.form.get("amount", "").strip()
    category = request.form.get("category", "").strip()

    # Check whether the description is empty.
    if not description:

        flash("Please enter an expense description.", "error")
        return redirect(url_for("home"))

    # Check whether the amount is a valid number.
    try:
        amount = float(amount)

    except ValueError:

        flash("Please enter a valid amount.", "error")
        return redirect(url_for("home"))

    # Expense amount must be positive.
    if amount <= 0:

        flash("Amount must be greater than zero.", "error")
        return redirect(url_for("home"))

    # Check whether a valid category was selected.
    allowed_categories = [
        "Food",
        "Travel",
        "Shopping",
        "Education",
        "Entertainment",
        "Other"
    ]

    if category not in allowed_categories:

        flash("Please select a valid category.", "error")
        return redirect(url_for("home"))

    # Get the current date.
    date = datetime.datetime.now().strftime("%d-%b-%Y")

    connection = get_db_connection()

    # Insert the expense into the database.
    connection.execute("""
        INSERT INTO expenses (description, amount, category, date)
        VALUES (?, ?, ?, ?)
    """, (description, amount, category, date))

    connection.commit()
    connection.close()

    flash("Expense added successfully!", "success")

    return redirect(url_for("home"))


# ============================================================
# 7. DELETE EXPENSE
# ============================================================

@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):

    connection = get_db_connection()

    # Delete the expense with the given ID.
    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()

    flash("Expense deleted successfully!", "success")

    return redirect(url_for("home"))


# ============================================================
# 8. RUN THE APPLICATION
# ============================================================

if __name__ == "__main__":

    # Create the database table before starting Flask.
    create_table()

    app.run(debug=True)
