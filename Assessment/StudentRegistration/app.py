
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash

app = Flask(__name__)

DB_PATH = Path(app.root_path) / "students.db"


# Database connection
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


# Create Student table
def init_db():
    con = get_db()

    con.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            course TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()


# Registration page
@app.route("/")
def home():
    return render_template("index.html")


# Handle form submission
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    age = request.form.get("age", "").strip()
    gender = request.form.get("gender", "")
    course = request.form.get("course", "")
    password = request.form.get("password", "")

    # Required field validation
    if not all([name, email, age, gender, course, password]):
        return "All fields are required.", 400

    # Age validation
    try:
        age = int(age)
        if age <= 0:
            return "Age must be a positive number.", 400
    except ValueError:
        return "Age must be numeric.", 400

    # Password validation
    if len(password) < 6:
        return "Password must contain at least 6 characters.", 400

    con = None

    try:
        con = get_db()

        # Insert registration data using SQL
        con.execute("""
            INSERT INTO Student
            (name, email, age, gender, course, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            age,
            gender,
            course,
            generate_password_hash(password)
        ))

        con.commit()

        # Redirect to success page
        return redirect(url_for("success", name=name))

    except sqlite3.IntegrityError:
        return "This email is already registered.", 400

    except sqlite3.Error as e:
        print("Database error:", e)
        return "Registration failed due to a database error.", 500

    finally:
        if con is not None:
            con.close()


# Success page
@app.route("/success")
def success():
    name = request.args.get("name", "Student")
    return render_template("success.html", name=name)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
