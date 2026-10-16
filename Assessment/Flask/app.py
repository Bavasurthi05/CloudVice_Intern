
import sqlite3
from pathlib import Path

from flask import (
    Flask,
    request,
    session,
    render_template,
    redirect,
    url_for
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

# Secret key for session handling
app.secret_key = "student_registration_secret_key"

# SQLite database path
DB_PATH = Path(app.root_path) / "students.db"


# Connect to database
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


# Create database and Student table
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


# Level 2: Display registration form
@app.route("/")
def home():
    return render_template("index.html")


# Level 2: Register student and save to SQLite
@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    age = request.form.get("age", "").strip()
    gender = request.form.get("gender", "").strip()
    course = request.form.get("course", "").strip()
    password = request.form.get("password", "")

    # Validate required fields
    if not all([name, email, age, gender, course, password]):
        return "All fields are required.", 400

    # Validate age
    try:
        age = int(age)
        if age <= 0:
            return "Age must be positive.", 400
    except ValueError:
        return "Age must be a number.", 400

    # Validate password
    if len(password) < 6:
        return "Password must be at least 6 characters.", 400

    con = None

    try:
        con = get_db()

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

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
            hashed_password
        ))

        con.commit()

    except sqlite3.IntegrityError:
        return "This email is already registered.", 400

    except sqlite3.Error as e:
        print("Database error:", e)
        return "Database insertion failed.", 500

    finally:
        if con is not None:
            con.close()

    return redirect(url_for("success", name=name))


# Level 2: Registration success page
@app.route("/success")
def success():
    name = request.args.get("name", "Student")
    return render_template("success.html", name=name)


# Level 3: Login using email and password
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        con = get_db()

        try:
            student = con.execute(
                "SELECT * FROM Student WHERE email = ?",
                (email,)
            ).fetchone()
        finally:
            con.close()

        # Verify password hash
        if student and check_password_hash(
            student["password"], password
        ):
            session.clear()
            session["student_id"] = student["id"]

            return redirect(url_for("profile"))

        return render_template(
            "login.html",
            error="Invalid email or password"
        ), 401

    return render_template("login.html")


# Level 3: Display logged-in student's profile
@app.route("/profile")
def profile():
    student_id = session.get("student_id")

    # Redirect if not logged in
    if student_id is None:
        return redirect(url_for("login"))

    con = get_db()

    try:
        student = con.execute("""
            SELECT id, name, email, age, course
            FROM Student
            WHERE id = ?
        """, (student_id,)).fetchone()
    finally:
        con.close()

    # Clear invalid session
    if student is None:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        student=student
    )


# Level 3: Logout and clear session
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# Run application
if __name__ == "__main__":
    init_db()
    app.run(
        debug=True,
        port=5001,
        use_reloader=False
    )
