
from pathlib import Path
import sqlite3

from flask import (
    Flask,
    request,
    session,
    render_template,
    redirect,
    url_for,
    jsonify
)

app = Flask(__name__)
app.secret_key = "my-secret"

DB_PATH = Path(app.root_path) / "tasks.db"


# Connect to the SQLite database
def get_db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


# Create the tasks table and update an existing table if necessary
def init_db():
    con = get_db()

    con.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    # Check which columns already exist
    columns = [
        row["name"]
        for row in con.execute("PRAGMA table_info(tasks)").fetchall()
    ]

    # Add status if the old database does not have it
    if "status" not in columns:
        con.execute("""
            ALTER TABLE tasks
            ADD COLUMN status TEXT NOT NULL DEFAULT 'Pending'
        """)

    con.commit()
    con.close()


# Login page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == "admin" and password == "1234":
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("tasks"))

        return render_template(
            "login.html",
            error="Invalid username or password"
        )

    if session.get("logged_in"):
        return redirect(url_for("tasks"))

    return render_template("login.html")


# Display all tasks
@app.route("/tasks", methods=["GET"])
def tasks():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    con = get_db()

    task_list = con.execute("""
        SELECT id, title, status
        FROM tasks
        ORDER BY id DESC
    """).fetchall()

    con.close()

    return render_template(
        "tasks.html",
        tasks=task_list,
        username=session.get("username", "admin")
    )


# Add a task using AJAX
@app.route("/add_task", methods=["POST"])
def add_task():
    if not session.get("logged_in"):
        return jsonify({
            "success": False,
            "error": "Please log in again."
        }), 401

    data = request.get_json(silent=True) or {}
    title = data.get("task", "")

    if not isinstance(title, str):
        title = ""

    title = title.strip()

    if not title:
        return jsonify({
            "success": False,
            "error": "Task cannot be empty."
        }), 400

    con = get_db()

    cursor = con.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (title,)
    )

    task_id = cursor.lastrowid

    con.commit()
    con.close()

    return jsonify({
        "success": True,
        "task": {
            "id": task_id,
            "title": title,
            "status": "Pending"
        }
    }), 201


# Logout
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("home"))


# Start the application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
