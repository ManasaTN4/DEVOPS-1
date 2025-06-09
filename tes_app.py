from flask import Flask, request, session, redirect, render_template_string

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'admin@example.com' and password == 'admin123':
            session['admin_logged_in'] = True
            return "Admin logged in!"
        else:
            return "Invalid admin login"
    return render_template_string('''
        <form method="post">
            Email: <input name="email"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
