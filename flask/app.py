
import sqlite3
from flask import (
    Flask, render_template, request,
    redirect, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'change-this-secret-key'

def get_db():
    con = sqlite3.connect('users.db')
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_db()
    con.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    con.commit()
    con.close()

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_user():
    name = request.form['name'].strip()
    username = request.form['username'].strip()
    password = request.form['password']

    if not name or not username or not password:
        return 'All fields are required!', 400

    con = get_db()
    try:
        con.execute(
            'INSERT INTO accounts (name, username, password) VALUES (?, ?, ?)',
            (name, username, generate_password_hash(password))
        )
        con.commit()
    except sqlite3.IntegrityError:
        con.close()
        return 'Username already exists. Please choose another.', 400

    con.close()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        con = get_db()
        user = con.execute(
            'SELECT * FROM accounts WHERE username = ?',
            (username,)
        ).fetchone()
        con.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))

        return render_template(
            'login.html', error='Invalid username or password'
        )

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    con = get_db()
    user = con.execute(
        'SELECT id, name, username FROM accounts WHERE id = ?',
        (session['user_id'],)
    ).fetchone()
    con.close()

    if user is None:
        session.clear()
        return redirect(url_for('login'))

    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
