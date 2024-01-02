from flask import Flask, render_template, redirect, url_for, jsonify, request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # Change this to a secure secret key

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, message='Username must be at least 4 characters')])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, message='Password must be at least 20 characters')])
    submit = SubmitField('Register')

@app.route('/')
def welcome():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = {'username': form.username.data, 'password': form.password.data}
        response = requests.post('http://127.0.0.1:5001/login', json=data)

        if response.status_code == 200:
            # Store the access token in the session
            session['access_token'] = response.json().get('access_token')
            session['logged_in'] = True
            print("Access Token:", session['access_token'])
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {'username': form.username.data, 'password': form.password.data}
        response = requests.post('http://127.0.0.1:5001/register', json=data)

        if response.status_code == 201:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form, error='Registration failed')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('welcome'))

@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html')
    else:
        flash('You need to log in first', 'error')
        return redirect(url_for('login'))
    
@app.route('/products')
def product():
    # Check if the user is logged in and has an access token
    if session.get('logged_in') and 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        response = requests.get('http://127.0.0.1:5002/products', headers=headers)

        if response.status_code == 200:
            products = response.json().get('products', [])
            return render_template('products.html', products=products)
        else:
            flash('Error fetching products', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('You need to log in and authorize access', 'error')
        return redirect(url_for('login'))

@app.route('/add_product', methods=['POST'])
def add_product():
    # Check if the user is logged in and has an access token
    if session.get('logged_in') and 'access_token' in session:
        # Get the user's role from the session
        user_role = session.get('user_role')

        # Check if the user has the 'modder' role
        if user_role == 'modder':
            # Forward the request to the product service
            headers = {'Authorization': 'Bearer ' + session['access_token']}
            data = request.get_json()
            response = requests.post('http://127.0.0.1:5002/add_product', json=data, headers=headers)

            if response.status_code == 201:
                flash('Product added successfully', 'success')
            else:
                flash('Error adding product', 'error')

            return redirect(url_for('dashboard'))
        else:
            flash('You do not have permission to add a new product', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('You need to log in and authorize access', 'error')
        return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)