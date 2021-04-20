from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from WebApp.model import Post

main = Blueprint('main', __name__)


@main.route("/")
def landing_page():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    return render_template('landing.html')


@main.route("/home")
@login_required
def home():
    # page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(
    #     Post.datePosted.desc()).paginate(page=page, per_page=5)
    username = current_user.username
    p_image = current_user.image_file
    print(p_image)
    return render_template("homepage.html", username=username, p_image=p_image)


@main.route("/about")
@login_required
def about():
    return render_template('about.html')
