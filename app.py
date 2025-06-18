from flask import Flask, session, redirect, request, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route('/')
def home():
    return redirect('/login')

# Student Login Page
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
            return "Invalid login. <a href='/login'>Try again</a>"

    return render_template('login.html')

# Placeholder for forgot password
@app.route('/forgot-password')
def forgot_password():
    return "<h3>Forgot Password functionality coming soon.</h3><a href='/login'>Back to login</a>"

# Example protected page
@app.route('/scan')
def scan():
    if 'student_id' not in session:
        return redirect('/login')
    return f"<h2>Welcome, {session['student_name']}!</h2><p>You are now on the scan page.</p>"

# Logout (optional)
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
