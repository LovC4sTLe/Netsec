from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv
import uuid

load_dotenv()
app_product = Flask(__name__)
app_product.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI_PRODUCT")
app_product.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app_product.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY_PRODUCT")  # Change this to a secure secret key
jwt_product = JWTManager(app_product)
db_product = SQLAlchemy(app_product)



class Product(db_product.Model):
	pro_id = db_product.Column(db_product.Integer, primary_key=True)
	category= db_product.Column(db_product.String(50), nullable=False)
	name = db_product.Column(db_product.String(100), nullable=False)
	description= db_product.Column(db_product.String(250), nullable=True)
	price_range= db_product.Column(db_product.String(200), nullable=False)
	comments= db_product.Column(db_product.String(200), nullable=True)
	filename = db_product.Column(db_product.Text, nullable=False, unique=True)
	username = db_product.Column(db_product.String(50), nullable=True)

@app_product.route("/product", methods=["GET"])
def get_products():
    try:
        # Retrieve all products from the database
        products = Product.query.all()
        products_list = [{"category": product.category, "name": product.name, "description": product.description,
                          "price_range": product.price_range, "comments": product.comments} for product in products]
        return jsonify({"success": True, "data": products_list})
    except Exception as e:
        # Handle exceptions appropriately
        status = {"success": False, "message": str(e)}
        return jsonify(status)

@app_product.route("/product", methods=["POST"])
def add_product():
    try:
        image = request.files['image']
        filename = str(uuid.uuid1()) + os.path.splitext(image.filename)[1]
        image.save(os.path.join("static/images", filename))

        category = request.form.get("category")
        name = request.form.get("pro_name")
        description = request.form.get("description")
        price_range = request.form.get("price_range")
        comments = request.form.get("comments")

        new_pro = Product(category=category, name=name, description=description, price_range=price_range, comments=comments, filename=filename)
        db_product.session.add(new_pro)
        db_product.session.commit()

        status = {"success": True, "message": "Product added successfully."}
        return jsonify(status)
    except Exception as e:
        # Handle exceptions appropriately
        status = {"success": False, "message": str(e)}
        return jsonify(status)
    
@app_product.route("/edit/<int:pro_id>", methods=['POST'])
def edit(pro_id):
    try:
        result = Product.query.filter_by(pro_id=pro_id).first()
        if result:
            result.category = request.form.get("category")
            result.name = request.form.get("pro_name")
            result.description = request.form.get("description")
            result.price_range = request.form.get("price_range")
            result.comments = request.form.get("comments")
            db_product.session.commit()
            return jsonify({"success": True, "message": "Product edited successfully"})
        else:
            return jsonify({"success": False, "message": "Product not found"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})



if __name__ == '__main__':
    db_product.create_all()
    app_product.run(host='0.0.0.0', port=5003, debug=True)