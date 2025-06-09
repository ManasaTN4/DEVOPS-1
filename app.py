from flask import Flask, session, redirect, request, render_template_string
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'any-secret-key-you-want'

# Initialize DB and create tables if not exist
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        session_id TEXT,
                        timestamp TEXT)''')
    # Add a test student (only if not already there)
    cursor.execute("INSERT OR IGNORE INTO students (name, email, password) VALUES (?, ?, ?)",
                   ("Test Student", "test@example.com", "1234"))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM students WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['student_id'] = user[0]
            session['student_name'] = user[1]
            return redirect('/scan?session=abc123')
        else:
            return "Invalid login"
    
    # Simple login form
    return '''
        <h2>Student Login</h2>
        <form method="post">
            Email: <input name="email"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/scan')
def scan():
    student_id = session.get('student_id')
    session_id = request.args.get('session', 'default123')
    if not student_id:
        return redirect('/login')
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, session_id, timestamp) VALUES (?, ?, ?)",
                   (student_id, session_id, timestamp))
    conn.commit()
    conn.close()
    
    return render_template_string('''
        <h2>Attendance Recorded</h2>
        <p>Student: {{ name }}</p>
        <p>Session: {{ session_id }}</p>
        <p>Time: {{ time }}</p>
    ''', name=session.get('student_name'), session_id=session_id, time=timestamp)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@example.com' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect('/dashboard')
        else:
            return "Invalid admin login"
    return render_template_string('''
        <h2>Admin Login</h2>
        <form method="post">
            Email: <input name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect('/admin-login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.name, a.session_id, a.timestamp
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        ORDER BY a.timestamp DESC
    ''')
    records = cursor.fetchall()
    conn.close()

    return render_template_string('''
        <h2>Attendance Dashboard</h2>
        <table border="1">
            <tr><th>Student Name</th><th>Session ID</th><th>Timestamp</th></tr>
            {% for name, session_id, timestamp in records %}
            <tr>
                <td>{{ name }}</td>
                <td>{{ session_id }}</td>
                <td>{{ timestamp }}</td>
            </tr>
            {% endfor %}
        </table>
        <a href="/admin-login">Logout</a>
    ''', records=records)

if __name__ == '__main__':
    print("Flask app is starting...")
    init_db()
    app.run(debug=True)
