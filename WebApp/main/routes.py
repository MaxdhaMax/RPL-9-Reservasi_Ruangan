from copy import Error
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from WebApp.model import Room
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
    if (keyword and form.validate()):
        flash(f"Searching for {keyword}", category='info')
        rooms = Room.query.filter(Room.name.like(keyword) | Room.location.like(
            keyword) | Room.room_type.like(keyword))
        hasCheckBooked = False
        try:
            check_in = form.check_in.data
            check_out = form.check_out.data
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
        except:
            pass
        return render_template("homepage.html", current_user=current_user, rooms=rooms, search=keyword, room_choice=room_choice, form=form, hasCheckBooked=hasCheckBooked)
    else:
        return render_template("homepage.html", current_user=current_user, room_choice=room_choice, form=form)


@ main.route("/about")
@ login_required
def about():
    return render_template('about.html')
