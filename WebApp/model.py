from datetime import datetime, timedelta

from sqlalchemy.orm import backref
from WebApp import db, loginManager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from uuid import uuid4
from random import randint


@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.String(19), primary_key=True)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.String(5), db.ForeignKey('room.id'), nullable=False)
    book_info = db.relationship("Booked", backref="transaction", lazy=True)
    status = db.Column(db.String(20))
    payment_type = db.Column(db.String(10))
    time = db.Column(
        db.DateTime, default=datetime.utcnow() + timedelta(hours=7))
    data = db.Column(db.Text)

    def __repr__(self):
        return f"Transaction('{self.id}', '{self.payment_type}', '{self.time}', '{self.status}')"


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.png")
    password = db.Column(db.String(60), nullable=False)
    transaction = db.relationship("Transaction", backref="user", lazy=True)
    active = db.Column(db.Boolean, nullable=False, default=False)

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Room(db.Model):
    __tablename__ = 'room'
    __searchable__ = ['name', 'location', 'room_type']

    id = db.Column(db.String(5), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, default=100, nullable=False)
    information = db.Column(db.Text, nullable=False)
    person_in_charge = db.relationship(
        "Person_In_Charge", backref="room", lazy="select")
    image_file = db.relationship(
        "Room_Image_File", backref="room", lazy="select")
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, location, room_type, capacity, information, person_in_charge, image_file, price):
        self.name = name
        self.location = location
        self.room_type = room_type
        self.capacity = capacity
        self.information = information
        self.person_in_charge = person_in_charge
        self.image_file = image_file
        self.price = price
        self.id = uuid4().hex[:5]

    def __repr__(self):
        return f"Room('{self.name}', '{self.location}', '{self.room_type}')"


class Room_Image_File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    room_id = db.Column(db.String(5), db.ForeignKey('room.id'), nullable=False)


class Person_In_Charge(User):
    id = db.Column("id", db.Integer, db.ForeignKey(
        'user.id'), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    room_id = db.Column(db.String(5), db.ForeignKey('room.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.number}')"


class Booked(db.Model):
    __tablename__ = 'booked'
    id = db.Column(db.String(17), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.String(5), db.ForeignKey('room.id'))
    date = db.Column(db.Date)
    event = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    booked_by = db.relationship("User", backref="book_info", lazy="select")
    room_booked = db.relationship("Room", backref="book_info", lazy="select")
    transaction_id = db.Column(db.String(19), db.ForeignKey('transaction.id'))

    def __init__(self, date, event, organization, name, email, phone, booked_by, room_booked, transaction_id=None):
        self.date = date
        self.event = event
        self.organization = organization
        self.name = name
        self.email = email
        self.phone = phone
        self.booked_by = booked_by
        self.room_booked = room_booked
        self.transaction_id = transaction_id
        self.id = "br-" + uuid4().hex[:14]
