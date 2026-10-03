from flask_sqlalchemy import SQLAlchemy

""" Creates db object """
db = SQLAlchemy()


class User(db.Model):
    """ Creates valid attributes for each user """
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(30), unique=True, nullable=False)
    password: bytes = db.Column(
        db.LargeBinary(60), unique=False, nullable=False)
    max_streak: int = db.Column(db.Integer, nullable=True)
