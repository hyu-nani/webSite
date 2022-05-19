from email.policy import default
from enum import unique
from multiprocessing.pool import IMapUnorderedIterator

from pytz import timezone

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_data = db.Column(db.String(10000))
    note_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.email'))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('user.email'))
    order_title = db.Column(db.String(150))
    order_name = db.Column(db.String(150))
    order_password = db.Column(db.String(150))
    order_number = db.Column(db.String(150))
    order_data = db.Column(db.String(10000))
    order_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    notes = db.relationship('Note')
    orders = db.relationship('Order')

    #terms of user data
