from flask import Blueprint, render_template, url_for, flash
from flask_login import login_required, current_user
from WebApp.model import User, Room, Person_In_Charge, Booked
from WebApp import db
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date

rooms = Blueprint('rooms', __name__)


@rooms.route("/book/<int:id>")
@login_required
def book(id):
    user = current_user
    print(user)
    room = Room.query.filter_by(id=id).first()
    print(room)
    datenow = date(2001, 4, 20)
    print(datenow)
    booked = Booked(
        booked_by=user, room_booked=room,
        date=datenow, event="Silaturahmi",
        organization="IAAS")
    b = user.book_info[0].room_booked
    print(b)
    db.session.add(booked)
    db.session.commit()
    # except SQLAlchemyError as e:
    #     error = str(e.__dict__['orig'])
    #     print(error)
    return render_template('home.html')
