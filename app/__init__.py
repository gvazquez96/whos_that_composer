import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from app.routes import blueprints
from app.models import db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"  # Store session data in files
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    session = Session(app)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    db.init_app(app)
    return app, session
