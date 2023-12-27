from flask import Flask
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
oauth = OAuth2Provider()

def create_app():
    app = Flask(__name__)
    oauth.init_app(app)
    return app