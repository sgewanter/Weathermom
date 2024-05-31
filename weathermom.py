import sqlite3
from flask import Flask, render_template, request, redirect, flash, url_for, session
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'weathermom'

def get_db_connection():
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('weathermom'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('UserLogin.html', form=form)

@app.route('/weathermom.html', methods=['POST', 'GET'])
def weathermom():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    username = session.get('username', 'Guest')
    return render_template('weathermom.html', username=username)

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        city = form.city.data
        zip_code = form.zip_code.data
        phone_number = form.phone_number.data

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password, first_name, last_name, city, zip_code, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (username, password, first_name, last_name, city, zip_code, phone_number))
        conn.commit()
        conn.close()
        return redirect('/weathermom.html')
    
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
