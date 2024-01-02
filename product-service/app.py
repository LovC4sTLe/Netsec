from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv

load_dotenv()
app_product = Flask(__name__)
app_product.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI_PRODUCT")
app_product.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_product.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY_PRODUCT")  # Change this to a secure secret key
jwt_product = JWTManager(app_product)
db_product = SQLAlchemy(app_product)

class Product(db_product.Model):
    id = db_product.Column(db_product.Integer, primary_key=True)
    name = db_product.Column(db_product.String(50), nullable=False)
    price = db_product.Column(db_product.Float, nullable=False)

@app_product.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{'id': product.id, 'name': product.name, 'price': product.price} for product in products]
    return jsonify(products=product_list)

@app_product.route('/add_product', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()

    # Check if the user has the 'modder' role
    if current_user['role'] != 'modder':
        return jsonify({'message': 'You do not have permission to add a new product'}), 403

    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db_product.session.add(new_product)
    db_product.session.commit()

    return jsonify({'message': 'Product added successfully'}), 201


if __name__ == '__main__':
    db_product.create_all()
    app_product.run(host='0.0.0.0', port=5002, debug=True)