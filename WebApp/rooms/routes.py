from copy import Error
from flask import Blueprint, render_template, url_for, flash, jsonify, redirect, session, abort, Markup, request
from flask_login import login_required, current_user
from WebApp.model import User, Room, Transaction, Booked, Room_Image_File
from WebApp.rooms.forms import BookForm, EditRoomForm
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date, timedelta
from WebApp.rooms.utils import BookedSchema, PaymentParameters, SavePictures
from WebApp.myscheduler import CheckTransactionStatus
from WebApp import db
import midtransclient
from uuid import uuid4
import json
rooms = Blueprint('rooms', __name__)


@rooms.route("/room/<string:id>", methods=["GET", "POST"])
@login_required
def room(id):
    room = Room.query.filter_by(id=id).first_or_404()
    room.information = Markup(room.information.replace("\n", "<br>"))
    person_in_charge = room.person_in_charge[0]
    booked_rooms = room.book_info
    booked_date = [r.date.strftime("%Y/%m/%d") for r in booked_rooms]
    if(request.method == "POST"):
        try:
            selected_date = request.form["selectedDate"].split(" ")
            selected_date.pop(len(selected_date) - 1)
            session['date'] = selected_date
            return redirect(url_for('rooms.room_book', id=id))
        except Error as e:
            print(e)
    return render_template('info_ruangan.html', booked_date=booked_date, current_user=current_user, room=room, pic=person_in_charge)


@rooms.route("/room/<string:id>/edit", methods=["GET", "POST"])
@login_required
def room_edit(id):
    room = Room.query.filter_by(id=id).first_or_404()
    person_in_charge = room.person_in_charge[0]
    form = EditRoomForm()
    if(current_user.id != person_in_charge.id):
        abort(403)
    if(form.validate_on_submit()):
        print("masuk")
        room.name = form.name.data
        room.location = form.location.data
        room.room_type = form.room_type.data
        room.capacity = form.capacity.data
        room.information = form.information.data
        if(form.picture.data):
            pics = request.files.getlist(form.picture.name)
            pictures_name = SavePictures(pics, id)
            for im in room.image_file:
                db.session.delete(im)
            list_image_file = []
            for p_name in pictures_name:
                image_file = Room_Image_File(name=p_name)
                list_image_file.append(image_file)
            room.image_file = list_image_file
        db.session.commit()
        flash("Informasi ruangan telah diedit", category="success")
        return redirect(url_for('rooms.room', id=id))
    elif(request.method == 'GET'):
        print("masuk")
        form.name.data = room.name
        form.location.data = room.location
        form.room_type.data = room.room_type
        form.capacity.data = room.capacity
        form.information.data = room.information
    return render_template('info_ruangan_edit.html', current_user=current_user, room=room, pic=person_in_charge, form=form)


@rooms.route("/room/<string:id>/book", methods=["GET", "POST"])
@login_required
def room_book(id):
    try:
        selected_date = session['date']
    except:
        return redirect(url_for('rooms.room', id=id))
    room = Room.query.filter_by(id=id).first_or_404()
    form = BookForm()

    price = room.price * len(selected_date)
    price_formatted = f'Rp {price:,}'.replace(",", ".") + ',00'
    if(form.validate_on_submit()):
        name = form.name.data
        email = form.email.data
        phone = form.number.data
        event = form.event_name.data
        organizer = form.event_organizer.data
        payment = form.payment.data
        print(payment)
        try:
            transID = "tr-" + str(uuid4().hex)[:16]
            trans = Transaction(id=transID, price=price,
                                user_id=current_user.id, room_id=room.id, status="pending")
            db.session.add(trans)
            for date in selected_date:
                dateobj = datetime.strptime(date, "%Y/%m/%d").date()
                isBooked = Booked.query.filter_by(
                    room_booked=room, date=dateobj).first()
                if(isBooked):
                    flash(
                        f"Ruangan {room.name} sudah terbooking pada tanggal {dateobj}", "danger")
                    return redirect(url_for('rooms.room', id=id))
                booked = Booked(booked_by=current_user, room_booked=room,
                                date=dateobj, event=event,
                                organization=organizer, name=name, email=email, phone=phone,
                                transaction_id=transID)
                print(booked.id, booked.transaction_id)
                db.session.add(booked)
            core_api = midtransclient.CoreApi(
                is_production=False,
                server_key='SB-Mid-server-UKoo4wuXPkpkoOx8dFWla_BS',
                client_key='SB-Mid-client-BfoyzFWFCAh_9V25'
            )
            param = PaymentParameters(
                payment, name, email, phone, price, transID)
            charge_response = core_api.charge(param)
            trans.data = json.dumps(charge_response)
            trans.payment_type = payment
            print(charge_response)
            db.session.commit()
            return redirect(url_for('rooms.room_book_transaction',
                                    id=id, transID=transID))
        except Error as e:
            print(e)
            pass
    return render_template("fill-data.html", room=room, current_user=current_user, form=form, selected_date=selected_date, price=price_formatted)


@rooms.route("/room/<string:id>/book/<string:transID>")
@login_required
def room_book_transaction(id, transID):
    room = Room.query.filter_by(id=id).first_or_404()
    trans = Transaction.query.filter_by(id=transID).first_or_404()
    if(current_user != trans.user):
        abort(403)
    CheckTransactionStatus(trans)
    if(trans.status in ["capture", "settlement"]):
        flash("Your transaction is successfull, successfully booked your room",
              category="success")
        return redirect(url_for('users.history'))
    elif(trans.status in ["deny", "cancel", "expire"]):
        if(trans.status == "deny"):
            flash(
                "[FAILED] This transaction has been denied and no longer available", category="danger")
        elif(trans.status == "cancel"):
            flash(
                "[FAILED] This transaction has been canceled and no longer available", category="danger")
        elif(trans.status == "expire"):
            flash(
                "[FAILED] This transaction has been expired and no longer available", category="danger")
        return redirect(url_for('rooms.room', id=id))
    selected_date = [book.date for book in trans.book_info]
    book_info = trans.book_info[0]
    priceFormatted = f'Rp {room.price:,}'.replace(",", ".") + ',00'
    priceSum = room.price * len(selected_date)
    priceSumFormatted = f'Rp {priceSum:,}'.replace(
        ",", ".") + ',00'
    trans_data = json.loads(trans.data)
    expire = (trans.time + timedelta(hours=6)
              ).strftime("%d/%m/%Y, %H:%M:%S") + " WIB"
    print(trans_data)
    if(trans.payment_type in ["BNI", "BCA", "BRI"]):
        va_numbers = trans_data["va_numbers"][0]["va_number"]
        va_numbers = " ".join(
            [va_numbers[:len(va_numbers) // 2], va_numbers[len(va_numbers) // 2:]])
        status = trans.status
        return render_template("payment.html", current_user=current_user, selected_date=selected_date, room=room,
                               trans=trans, book_info=book_info, priceFormatted=priceFormatted, priceSumFormatted=priceSumFormatted,
                               expire=expire, va_numbers=va_numbers, payment_type=trans.payment_type, status=status)
    elif(trans.payment_type == "GOPAY"):
        status = trans.status
        qrURL = trans_data["actions"][0]["url"]
        return render_template("payment.html", current_user=current_user, selected_date=selected_date, room=room,
                               trans=trans, book_info=book_info, priceFormatted=priceFormatted, priceSumFormatted=priceSumFormatted,
                               expire=expire, payment_type=trans.payment_type, status=status, qrURL=qrURL)


@rooms.route("/room/<string:id>/book/<string:transID>/cancel")
@login_required
def room_book_cancel(id, transID):
    room = Room.query.filter_by(id=id).first_or_404()
    trans = Transaction.query.filter_by(id=transID).first_or_404()
    if(current_user != trans.user):
        abort(403)
    book_info = trans.book_info
    try:
        db.session.delete(trans)
        for book in book_info:
            db.session.delete(book)
        db.session.commit()
    except:
        pass
    flash(f"Your order has been canceled", "info")
    return redirect(url_for("rooms.room", id=id))


@ rooms.route("/calendar/<string:id>")
@ login_required
def calendar(id):
    user = current_user
    print(user)
    room = Room.query.filter_by(id=id).first()
    print(room)
    booked_rooms = room.book_info
    booked_date = [r.date.strftime("%Y/%m/%d") for r in booked_rooms]
    print(booked_date)
    return render_template('calendar.html', booked_date=booked_date)


@ rooms.route("/calendar/<string:id>/<string:date>", methods=["GET"])
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
        return response
    except Exception as e:
        print(e)
        pass
    return jsonify('Not Found')


@rooms.route("/notification-handling", methods=["GET", "POST"])
def notification():
    try:
        core = midtransclient.CoreApi(
            is_production=False,
            server_key='SB-Mid-server-UKoo4wuXPkpkoOx8dFWla_BS',
            client_key='SB-Mid-client-BfoyzFWFCAh_9V25'
        )
        request_json = request.get_json()
        transaction_status_dict = core.transactions.notification(request_json)

        order_id = request_json['order_id']
        trans = Transaction.query.filter_by(id=order_id).first()
        CheckTransactionStatus(trans)
    except:
        pass
    return jsonify("NOPE")
