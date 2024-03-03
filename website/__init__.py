from flask import Flask
import pyrebase
from firebase_admin import credentials,initialize_app

cred = credentials.Certificate("website/pristupDatabaze.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = ''

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    return app
