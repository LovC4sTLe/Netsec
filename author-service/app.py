# from datetime import datetime, timedelta
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_oauthlib.provider import OAuth2Provider

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authorization.db'  # Use a separate database for authorization
# app.config['SECRET_KEY'] = 'thisisasecretkey'

# db = SQLAlchemy(app)
# oauth = OAuth2Provider(app)

# class oauthclient(db.Model):
#     id = db.Column(db.String(40), primary_key=True)
#     name = db.Column(db.String(40))
#     user_id = db.Column(db.String(20), nullable=False)
#     user = db.relationship('User')  # Assuming you have a User model defined in your authentication service

# class oauthgrant(db.Model):
#     id = db.Column(db.String(40), primary_key=True)
#     user_id = db.Column(db.String(20), nullable=False)
#     client_id = db.Column(db.String(40), db.ForeignKey('oauthclient.id'), nullable=False)
#     client = db.relationship('OAuthClient')
# #bo vào 1 model
# class oauthtoken(db.Model):
#     id = db.Column(db.String(40), primary_key=True)
#     user_id = db.Column(db.String(20), nullable=False)
#     client_id = db.Column(db.String(40), db.ForeignKey('oauthclient.id'), nullable=False)
#     client = db.relationship('OAuthClient')
#     token_type = db.Column(db.String(40))
#     refresh_token = db.Column(db.String(40))
#     expires = db.Column(db.DateTime)

# @oauth.clientgetter
# def load_client(client_id):
#     return oauthclient.query.filter_by(id=client_id).first()

# @oauth.grantgetter
# def load_grant(client_id, code):
#     return oauthgrant.query.filter_by(client_id=client_id, id=code).first()

# @oauth.grantsetter
# def save_grant(client_id, code, request, *args, **kwargs):
#     expires = None
#     if 'expires_in' in request:
#         expires = datetime.utcnow() + timedelta(seconds=request['expires_in'])
#     grant = oauthgrant(
#         id=code,
#         client_id=client_id,
#         user_id=request.user.id,
#         expires=expires,
#     )
#     db.session.add(grant)
#     db.session.commit()
#     return grant

# @oauth.tokengetter
# def load_token(access_token=None, refresh_token=None):
#     if access_token:
#         return oauthtoken.query.filter_by(id=access_token).first()
#     elif refresh_token:
#         return oauthtoken.query.filter_by(refresh_token=refresh_token).first()

# @oauth.tokensetter
# def save_token(token, request, *args, **kwargs):
#     expires_in = token.get('expires_in')
#     expires = datetime.utcnow() + timedelta(seconds=expires_in)

#     token_entry = oauthtoken(
#         id=token['access_token'],
#         user_id=request.user.id,
#         client_id=request.client.client_id,
#         token_type=token['token_type'],
#         refresh_token=token['refresh_token'],
#         expires=expires,
#     )

#     db.session.add(token_entry)
#     db.session.commit()
#     return token_entry

# if __name__ == '__main__':
#     db.create_all()
#     app.run(host='0.0.0.0', port=6000,debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
db = SQLAlchemy(app)
oauth = OAuth2Provider(app)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Define your User model and any other necessary models for tokens, etc.



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

