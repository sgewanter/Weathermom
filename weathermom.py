import mysql.connector
from flask import Flask, render_template, request, redirect, flash, url_for, session
from forms import RegistrationForm, LoginForm, UserProfileForm, UpdateProfileForm
from finalWeather import fetch_weather_forecast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'weathermom'

def get_db_connection():
    conn = mysql.connector.connect(
        user='admin', 
        password='12345678',
        host='database-2.c9ik0cgcw0hi.us-east-1.rds.amazonaws.com',
        database='test'
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('weathermom', form=form))
        else:
            flash('Invalid username or password', 'danger')
   
    return render_template('UserLogin.html', form=form)

@app.route('/weathermom.html', methods=['POST', 'GET'])
def weathermom():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    # Check if the user exists
    if user is None:
        flash('User not found', 'danger')
        return redirect(url_for('index'))
    
    form = UserProfileForm(data=user)

    # Handle the case where zip_code might be None
    zip_code = form.zip_code.data
    if zip_code:
        address = zip_code + ", USA"
        forecast, advice = fetch_weather_forecast(address)
    else:
        forecast, advice = None, None

    return render_template('weathermom.html', username=user['username'], form=form, user=user, forecast=forecast, advice=advice)


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
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (username, password, first_name, last_name, city, zip_code, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (username, password, first_name, last_name, city, zip_code, phone_number)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/weathermom.html')
   
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
   
    form = UpdateProfileForm()
    if form.validate():
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()

        if user:
            if user['username'] != form.username.data:
                cursor.execute('UPDATE users SET username = %s WHERE id = %s', (form.username.data, user_id))
            if user['first_name'] != form.first_name.data:
                cursor.execute('UPDATE users SET first_name = %s WHERE id = %s', (form.first_name.data, user_id))
            if user['last_name'] != form.last_name.data:
                cursor.execute('UPDATE users SET last_name = %s WHERE id = %s', (form.last_name.data, user_id))
            if user['city'] != form.city.data:
                cursor.execute('UPDATE users SET city = %s WHERE id = %s', (form.city.data, user_id))
            if user['zip_code'] != form.zip_code.data:
                cursor.execute('UPDATE users SET zip_code = %s WHERE id = %s', (form.zip_code.data, user_id))
            if user['phone_number'] != form.phone_number.data:
                cursor.execute('UPDATE users SET phone_number = %s WHERE id = %s', (form.phone_number.data, user_id))

            conn.commit()
        cursor.close()
        conn.close()
        
        flash('Profile updated successfully', 'success')
        return redirect(url_for('weathermom'))
    else:
        flash('Form validation failed', 'danger')
        return redirect(url_for('weathermom'))

if __name__ == '__main__':
    app.run(debug=True)
