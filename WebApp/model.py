from datetime import datetime
from WebApp import db, loginManager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.String(19), primary_key=True)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    book_info = db.relationship("Booked", backref="transaction", lazy=True)
    status = db.Column(db.String(20))
    payment_type = db.Column(db.String(10))
    time = db.Column(db.DateTime, default=datetime.now)
    data = db.Column(db.Text)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.png")
    password = db.Column(db.String(60), nullable=False)
    mahasiswa = db.relationship(
        "Mahasiswa", backref="usr", lazy=True)
    dosen = db.relationship(
        "Dosen", backref="usr", lazy=True)
    staff = db.relationship(
        "Staff", backref="usr", lazy=True)
    transaction = db.relationship("Transaction", backref="user", lazy=True)

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


class Mahasiswa(User):
    id = db.Column("id", db.Integer, db.ForeignKey(User.id), primary_key=True)
    nim = db.Column(db.String(12), nullable=False)
    nama = db.Column(db.String(30), nullable=False)
    departemen = db.Column(db.String(30), nullable=False)
    fakultas = db.Column(db.String(30), nullable=False)
    angkatan = db.Column(db.Integer, nullable=False)


class Dosen(User):
    id = db.Column("id", db.Integer, db.ForeignKey(User.id), primary_key=True)
    nik = db.Column(db.String(12), nullable=False)
    nama = db.Column(db.String(30), nullable=False)
    departemen = db.Column(db.String(30), nullable=False)
    fakultas = db.Column(db.String(30), nullable=False)


class Staff(User):
    id = db.Column("id", db.Integer, db.ForeignKey(User.id), primary_key=True)
    nik = db.Column(db.String(12), nullable=False)
    nama = db.Column(db.String(30), nullable=False)


class Post(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"


class Room(db.Model):
    __tablename__ = 'room'
    __searchable__ = ['name', 'location', 'room_type']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, default=100, nullable=False)
    information = db.Column(db.Text, nullable=False)
    person_in_charge = db.relationship(
        "Person_In_Charge", backref="room", lazy="select")
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.png")
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Room('{self.name}', '{self.location}', '{self.room_type}')"


class Person_In_Charge(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.number}')"


class Booked(db.Model):
    __tablename__ = 'booked'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    date = db.Column(db.Date)
    event = db.Column(db.String(50), nullable=False)
    organization = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    booked_by = db.relationship("User", backref="book_info", lazy="select")
    room_booked = db.relationship("Room", backref="book_info", lazy="select")
    transaction_id = db.Column(db.String(19), db.ForeignKey('transaction.id'))
