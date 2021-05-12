from copy import Error
from flask import Blueprint, render_template, url_for, flash, jsonify, redirect
from flask.globals import request
from flask_login import login_required, current_user
from WebApp.model import User, Room, Person_In_Charge, Booked
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date
from WebApp.rooms.utils import BookedSchema
from WebApp import db
import json
rooms = Blueprint('rooms', __name__)


@rooms.route("/room/<int:id>", methods=["GET", "POST"])
@login_required
def room(id):
    # user = current_user
    # print(user)
    # room = Room.query.filter_by(id=id).first()
    # print(room)
    # datenow = date(2001, 4, 20)
    # print(datenow)
    # booked = Booked(
    #     booked_by=user, room_booked=room,
    #     date=datenow, event="Silaturahmi",
    #     organization="IAAS")
    # booked_rooms = room.book_info
    # booked_date = [r.date.strftime("%Y/%m/%d") for r in booked_rooms]
    # db.session.add(booked)
    # db.session.commit()
    room = Room.query.filter_by(id=id).first()
    person_in_charge = room.person_in_charge[0]
    booked_rooms = room.book_info
    booked_date = [r.date.strftime("%Y/%m/%d") for r in booked_rooms]
    if(request.method == "POST"):
        try:
            selected_date = request.form["selectedDate"].split(" ")
            selected_date.pop(len(selected_date) - 1)
            for date in selected_date:
                dateobj = datetime.strptime(date, "%Y/%m/%d").date()
                booked = Booked(booked_by=current_user, room_booked=room,
                                date=dateobj, event="Belum Dipilih",
                                organization="Belum Dipilih", name="Belum Dipilih")
                db.session.add(booked)
            db.session.commit()
            print(selected_date)
            return redirect(url_for('rooms.room', id=id))
        except Error as e:
            print(e)
    # except SQLAlchemyError as e:
    #     error = str(e.__dict__['orig'])
    #     print(error)
    return render_template('info_ruangan.html', booked_date=booked_date, current_user=current_user, room=room, pic=person_in_charge)


@rooms.route("/calendar/<int:id>")
@login_required
def calendar(id):
    user = current_user
    print(user)
    room = Room.query.filter_by(id=id).first()
    print(room)
    booked_rooms = room.book_info
    booked_date = [r.date.strftime("%Y/%m/%d") for r in booked_rooms]
    print(booked_date)
    return render_template('calendar.html', booked_date=booked_date)


@rooms.route("/calendar/<int:id>/<string:date>", methods=["GET"])
def book_data(id, date):
    date = date.replace("-", "/")
    room = Room.query.filter_by(id=id).first()
    booked_schema = BookedSchema()
    print(date)
    try:
        booked_rooms = room.book_info
        datas = [d for d in booked_rooms if d.date.strftime(
            "%Y/%m/%d") == date]
        data = datas[0]
        output = booked_schema.dump(data)
        response = jsonify(output)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(e)
        pass
    return jsonify('Not Found')
