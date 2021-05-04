from datetime import datetime
from WebApp import db, loginManager, search
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from WebApp.search import add_to_index, remove_from_index, query_index


@loginManager.user_loader
def loadUser(user_id):
    return User.query.get(int(user_id))


room_book = db.Table('room_book',
                     db.Column('user_id', db.Integer, db.ForeignKey(
                         'user.id'), primary_key=True),
                     db.Column('room_id', db.Integer, db.ForeignKey(
                         'room.id'), primary_key=True),
                     db.Column('tanggal', db.DateTime)
                     )


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.png")
    password = db.Column(db.String(60), nullable=False)
    rooms = db.relationship("Room", secondary=room_book, lazy="subquery",
                            backref=db.backref("rooms", lazy=True))
    mahasiswa = db.relationship(
        "Mahasiswa", backref="mhs", lazy=True)
    dosen = db.relationship(
        "Dosen", backref="dsn", lazy=True)
    staff = db.relationship(
        "Staff", backref="stf", lazy=True)

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


class Room(SearchableMixin, db.Model):
    __tablename__ = 'room'
    __searchable__ = ['name', 'location', 'room_type']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    information = db.Column(db.Text, nullable=False)
    person_in_charge = db.relationship(
        "Person_In_Charge", backref="room", lazy=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default="default.png")

    def __repr__(self):
        return f"Room('{self.name}', '{self.location}', '{self.room_type}')"


class Person_In_Charge(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.number}')"
