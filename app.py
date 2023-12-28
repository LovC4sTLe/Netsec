from flask import Flask,render_template,send_from_directory,request, Response, redirect,session
from db import db_init, db
from models import Product
import os
import uuid
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.route('/')
def index():
    rows = Product.query.all()
    return render_template('index.html', rows=rows)

@app.route("/home", methods=["GET", "POST"], endpoint='home')
def home():
    if request.method == "POST":
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

    # Truy vấn tất cả sản phẩm không quan tâm đến user
    rows = Product.query.all()

    return render_template("home.html", rows=rows)

@app.route("/edit/<int:pro_id>", methods=["GET", "POST"], endpoint='edit')
def edit(pro_id):
    # select the editing product from db
    result = Product.query.all()

    if request.method == "POST":
        # update product information
        category = request.form.get("category")
        name = request.form.get("pro_name")
        description = request.form.get("description")
        price_range = request.form.get("price_range")
        comments = request.form.get("comments")

        # update product fields
        result.category = category
        result.name = name
        result.description = description
        result.comments = comments
        result.price_range = price_range

        # commit changes to the database
        db.session.commit()

        # fetch all products
        rows = Product.query.all()
        return render_template("home.html", rows=rows, message="Product edited")

    return render_template("edit.html", result=result)


if __name__ == "__main__":
    # init()
    app.run(debug=True)