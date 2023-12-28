# api_gateway.py
from flask import Flask, render_template, redirect, url_for, jsonify, request, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key

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
        response = requests.post('http://localhost:5001/login', json=data)

        if response.status_code == 200:
            # Redirect to the dashboard page after successful login
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')  # Use flash to display an error message
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {'username': form.username.data, 'password': form.password.data}
        response = requests.post('http://localhost:5001/register', json=data)

        if response.status_code == 201:
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form, error='Registration failed')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out', 'success')  # Use flash to display a success message
    return redirect(url_for('welcome'))

@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html')
    else:
        flash('You need to log in first', 'error')
        return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
