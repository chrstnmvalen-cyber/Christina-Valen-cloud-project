from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(128), nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    price = db.Column(db.Float, nullable=False)

    stock = db.Column(db.Integer, default=0)

    image_url = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, nullable=False)

    product_name = db.Column(db.String(200), nullable=False)
   
    price = db.Column(db.Float, nullable=False)
 
    quantity = db.Column(db.Integer, nullable=False)

    total = db.Column(db.Float, nullable=False)
