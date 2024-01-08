from db import db

class Product(db.Model):
	pro_id = db.Column(db.Integer, primary_key=True)
	category= db.Column(db.String(50), nullable=False)
	name = db.Column(db.String(100), nullable=False)
	description= db.Column(db.String(250), nullable=True)
	price_range= db.Column(db.String(200), nullable=False)
	comments= db.Column(db.String(200), nullable=True)
	filename = db.Column(db.Text, nullable=False, unique=True)
	username = db.Column(db.String(50), nullable=True)
	def __repr__(self):
		return '<Name %r>' % self.name