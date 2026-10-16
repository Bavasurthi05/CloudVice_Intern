
import sqlite3
from pathlib import Path
from datetime import datetime

from flask import (
    Flask, request, session, render_template,
    redirect, url_for, jsonify
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)

app = Flask(__name__)
app.secret_key = "level4_student_dashboard_secret_key"

DB_PATH = Path(app.root_path) / "students.db"

COURSES = [
    "B.Tech IT",
    "B.Tech CSE",
    "B.E. ECE",
    "B.E. EEE",
    "B.Sc Computer Science",
    "MCA",
    "MBA"
]


def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


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


@app.route("/")
def home():
    if session.get("student_id"):
        return redirect(url_for("profile"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        age_text = request.form.get("age", "").strip()
        gender = request.form.get("gender", "").strip()
        course = request.form.get("course", "").strip()
        password = request.form.get("password", "")

        if not all([name, email, age_text, gender, course, password]):
            return render_template(
                "register.html",
                error="All fields are required.",
                courses=COURSES
            )

        try:
            age = int(age_text)
            if age <= 0:
                raise ValueError
        except ValueError:
            return render_template(
                "register.html",
                error="Enter a valid positive age.",
                courses=COURSES
            )

        if len(password) < 6:
            return render_template(
                "register.html",
                error="Password must contain at least 6 characters.",
                courses=COURSES
            )

        if course not in COURSES:
            return render_template(
                "register.html",
                error="Select a valid course.",
                courses=COURSES
            )

        con = get_db()
        try:
            con.execute("""
                INSERT INTO Student
                (name, email, age, gender, course, password)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                name, email, age, gender, course,
                generate_password_hash(password)
            ))
            con.commit()
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="This email is already registered.",
                courses=COURSES
            )
        finally:
            con.close()

        return redirect(url_for("login"))

    return render_template("register.html", courses=COURSES)


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

        if student and check_password_hash(
            student["password"], password
        ):
            session.clear()
            session["student_id"] = student["id"]
            return redirect(url_for("profile"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


@app.route("/profile")
def profile():
    student_id = session.get("student_id")

    if student_id is None:
        return redirect(url_for("login"))

    con = get_db()
    try:
        student = con.execute("""
            SELECT id, name, email, age, gender, course
            FROM Student
            WHERE id = ?
        """, (student_id,)).fetchone()
    finally:
        con.close()

    if student is None:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        student=student,
        courses=COURSES,
        current_time=datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )



@app.route("/update-course", methods=["POST"])
def update_course():
    student_id = session.get("student_id")

    if student_id is None:
        return jsonify({
            "success": False,
            "message": "Please log in again."
        }), 401

    data = request.get_json(silent=True) or {}
    course = data.get("course", "").strip()

    if course not in COURSES:
        return jsonify({
            "success": False,
            "message": "Please select a valid course."
        }), 400

    con = get_db()
    try:
        result = con.execute(
            "UPDATE Student SET course = ? WHERE id = ?",
            (course, student_id)
        )
        con.commit()

        if result.rowcount == 0:
            return jsonify({
                "success": False,
                "message": "Student record not found."
            }), 404
    finally:
        con.close()

    return jsonify({
        "success": True,
        "course": course,
        "message": f"Course updated to: {course}"
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5002, use_reloader=False)
