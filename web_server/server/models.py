"""
models.py
Author: Umar Qureshi

The purpose of this class is to provide models for database and user accounts and transactions
"""

from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    account_no = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cards = db.relationship('Cards', backref='author', lazy=True)
    # transactions = db.relationship('Transactions', backref='trans', lazy=True)


    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}', '{self.image_file}')"


# Cards Table
class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    funds = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.card_name}', '{self.date_created}')"


# Transactions Table
class Transactions(db.Model):
    transaction_id = db.Column(db.String(255), primary_key=True)
    account_no = db.Column(db.Integer, nullable=False)
    location_no = db.Column(db.Integer, nullable=False, default=1)
    transaction_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    transaction_value = db.Column(db.Float, nullable=False)




    # return {
    #   "transaction_id": self.transaction_id,
    #   "account_no": self.account_no,
    #   "location_no": self.location_no,
    #   "transaction_time": str(self.transaction_time),
    #   "transaction_value": self.transaction_value
    # }




    def __repr__(self):
        return f"Transaction('{self.transaction_id}', '{self.history}')"
