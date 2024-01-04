from db import db


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=True, unique=True)
    user_password = db.Column(db.String(255), nullable=True)
    histories = db.relationship('History', backref="user", lazy=True)
