from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'key'

# Simulating database
users_db = {}

salt='4c2@g34'

@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_db:
            return render_template('register.html', warning='Username already exists!')

        hashed_password = generate_password_hash(password+salt, method='sha256')
        # Write password to db using username as key
        users_db[username] = hashed_password
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users_db:
            return render_template('login.html', warning='Invalid username!')
        
        if not check_password_hash(users_db[username], password+salt):
            return render_template('login.html', warning='Invalid password!')

        session['user'] = username
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
