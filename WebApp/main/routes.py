from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from WebApp.model import Post, Room
from WebApp import search

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
    username = current_user.username
    p_image = current_user.image_file
    if (request.method == "POST"):
        keyword = request.form.get('ruangan')
        rooms, total = Room.search(keyword, 1, 100)
        rooms = rooms.all()
        return render_template("homepage.html", current_user=current_user, rooms=rooms, search=keyword)
    else:
        print(p_image)
        return render_template("homepage.html", current_user=current_user)


@main.route("/about")
@login_required
def about():
    return render_template('about.html')
