from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from WebApp import db, bcrypt
from WebApp.model import User, Post
from WebApp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                RequestResetForm, ResetPasswordForm)
from WebApp.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if(request.method == "POST"):
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if("email" in session):
                email = session["email"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!", "info")
        return redirect(url_for("users.login"))


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            flash(
                f"Login successful, welcome {user.username}!", category='success')
            return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
        else:
            flash("Login Unsuccessful, please check your email and password", "danger")
    return render_template('login.html', title='Login', form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to login!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash("You has been logged out", "info")
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.datePosted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            pass
        else:
            send_reset_email(user)
        flash('If an email is exists with that email a recovery code will be sent', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashedPassword
        db.session.commit()
        flash("Your password has been updated! You are now able to login!", "success")
        return redirect(url_for("users.login"))
    return render_template('reset_token.html', title="Reset Password", form=form)
