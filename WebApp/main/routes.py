from flask import Blueprint, render_template, request
from flask_login import login_required
from WebApp.model import Post

main = Blueprint('main', __name__)


@main.route("/")
def landing_page():
    return render_template('landing.html')


@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.datePosted.desc()).paginate(page=page, per_page=5)
    return render_template("index.html", posts=posts)


@main.route("/about")
@login_required
def about():
    return render_template('about.html')
