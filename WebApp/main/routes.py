from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from WebApp.model import Post, Room
from WebApp.rooms.forms import SearchForm
from WebApp import search
import json

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
    form = SearchForm()
    all_room = Room.query.order_by(Room.name).all()
    room_choice = list()
    for room in all_room:
        room_choice.append(room.name)
        room_choice.append(room.location)
        room_choice.append(room.room_type)
    room_choice = list(dict.fromkeys(room_choice))
    if (form.validate_on_submit()):
        keyword = form.ruangan.data
        try:
            check_in = form.check_in.data.strftime('%Y-%m-%d')
            check_out = form.check_out.data.strftime('%Y-%m-%d')
        except:
            pass
        flash(f"Searching for {keyword}", category='info')
        rooms, total = Room.search(keyword, 1, 100)
        rooms = rooms.all()
        return render_template("homepage.html", current_user=current_user, rooms=rooms, search=keyword, room_choice=room_choice, form=form)
    else:
        return render_template("homepage.html", current_user=current_user, room_choice=room_choice, form=form)


@main.route("/about")
@login_required
def about():
    return render_template('about.html')
