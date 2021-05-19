from copy import Error
from operator import and_
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from WebApp.model import Booked, Room
from WebApp.rooms.forms import SearchForm
from WebApp.rooms.utils import ListBetweenTwoDates

main = Blueprint('main', __name__)


@main.route("/")
def landing_page():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    return render_template('landing.html')


@main.route("/home", methods=["POST", "GET"])
@login_required
def home():
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(
    #     Post.datePosted.desc()).paginate(page=page, per_page=5)
    form = SearchForm(request.args)
    all_room = Room.query.order_by(Room.name).all()
    room_choice = list()
    for room in all_room:
        room_choice.append(room.name)
        room_choice.append(room.location)
        room_choice.append(room.room_type)
    room_choice = list(dict.fromkeys(room_choice))
    keyword = form.ruangan.data
    page = request.args.get('page', 1, type=int)
    if(keyword):
        flash(f"Searching for {keyword}", category='info')
        rooms = Room.query.filter(Room.name.like(keyword) | Room.location.like(
            keyword) | Room.room_type.like(keyword))
    else:
        flash(f"Searching All Room", category='info')
        rooms = Room.query
    hasCheckBooked = False
    check_in = form.check_in.data
    check_out = form.check_out.data
    tersediaFilter = request.args.get("tersediaFilter")
    try:
        if(check_in and check_out):
            hasCheckBooked = True
            for room in rooms:
                room_bd = room.book_info
                isBooked = list(filter(
                    lambda x: x.date.strftime("%Y-%m-%d") in ListBetweenTwoDates(check_in, check_out), room_bd))
                if(isBooked):
                    room.available = False
                else:
                    room.available = True
            if(tersediaFilter):
                rooms = rooms.filter(~Room.book_info.any(
                    (Booked.date.in_(ListBetweenTwoDates(check_in, check_out)))))
        else:
            if(tersediaFilter):
                flash(
                    "Untuk memfilter ruangan yang tersedia, harap cantumkan tanggal check-in dan check-out", category="danger")
    except Error as e:
        print(e)
        pass
    rooms = rooms.paginate(page=page, per_page=4)
    return render_template("homepage.html", current_user=current_user, rooms=rooms, search=keyword, room_choice=room_choice, form=form,
                           hasCheckBooked=hasCheckBooked, check_in=check_in, check_out=check_out, tersediaFilter=tersediaFilter)


@ main.route("/about")
@ login_required
def about():
    return render_template('about.html')
