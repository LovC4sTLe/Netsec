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
    
@app.route('/product')
def show_products():
    # Check if the user is logged in and has an access token
    if session.get('logged_in') and 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        response = requests.get('http://localhost:5003/product', headers=headers)
    
        if response.status_code == 200:
            products = response.json().get('data')

            # Ensure 'filename' is present in each product
            for product in products:
                if 'filename' not in product:
                    product['filename'] = ''  # Set a default value or handle it appropriately

            return render_template('index.html', products=products)
        else:
            flash('You need to log in and authorize access', 'error')
            return redirect(url_for('login'))
    else:
        flash('You need to log in and authorize access', 'error')
        return redirect(url_for('login'))


@app.route('/options', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            # Logic to add a new product
            data = {
                'category': request.form.get('category'),
                'pro_name': request.form.get('pro_name'),
                'description': request.form.get('description'),
                'price_range': request.form.get('price_range'),
                'comments': request.form.get('comments'),
            }

            files = {'image': request.files['image']}
            headers = {'Authorization': 'Bearer ' + session.get('access_token', '')}

            response = requests.post('http://localhost:5003/product', data=data, files=files, headers=headers)

            if response.status_code == 200:
                flash('Product added successfully', 'success')
            else:
                flash('Failed to add product', 'error')
        except Exception as e:
            flash('An error occurred while processing the request', 'error')

    return render_template('product.html')

@app.route('/edit/<int:pro_id>', methods=['GET', 'POST'])
def edit(pro_id):
    if request.method == 'POST':
        try:
            data = {
                "category": request.form.get("category"),
                "pro_name": request.form.get("pro_name"),
                "description": request.form.get("description"),
                "price_range": request.form.get("price_range"),
                "comments": request.form.get("comments"),
            }

            headers = {'Authorization': 'Bearer ' + session.get('access_token', '')}

            files = {'image': request.files['image']}
            response = requests.post(f'http://localhost:5003/edit/{pro_id}', data=data, files=files, headers=headers)
            if response.status_code == 200:
                flash('Product edited successfully', 'success')
            else:
                flash('Failed to edit product', 'error')

        except Exception as e:
            flash('An error occurred while processing the request', 'error')
    return render_template('edit.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)