from flask import Flask, render_template, send_from_directory, request, jsonify, redirect, url_for
from db import db_init, db
from models import Product
import os
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route("/product", methods=["GET"])
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

@app.route("/product", methods=["POST"])
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
        db.session.add(new_pro)
        db.session.commit()

        status = {"success": True, "message": "Product added successfully."}
        return jsonify(status)
    except Exception as e:
        # Handle exceptions appropriately
        status = {"success": False, "message": str(e)}
        return jsonify(status)
    
@app.route("/edit/<int:pro_id>", methods=['POST'])
def edit(pro_id):
    try:
        result = Product.query.filter_by(pro_id=pro_id).first()
        if result:
            result.category = request.form.get("category")
            result.name = request.form.get("pro_name")
            result.description = request.form.get("description")
            result.price_range = request.form.get("price_range")
            result.comments = request.form.get("comments")
            db.session.commit()
            return jsonify({"success": True, "message": "Product edited successfully"})
        else:
            return jsonify({"success": False, "message": "Product not found"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)
