from os import abort
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from WebApp import db, bcrypt
from WebApp.model import Booked, User
from WebApp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                RequestResetForm, ResetPasswordForm)
from WebApp.users.utils import save_picture, send_reset_email
from datetime import timedelta,datetime 

users = Blueprint('users', __name__)


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


@users.route("/history")
@login_required
def history():
    user = current_user
    trans = user.transaction
    pending_trans = [t for t in trans if t.status == "pending"]
    for t in pending_trans:
        t.formatted_price = f'Rp {t.price:,}'.replace(",", ".") + ',00'
        t.expire = (t.time + timedelta(hours=6)).strftime("%d/%m/%Y, %H:%M:%S") + " WIB"
    print(pending_trans)
    booked = user.book_info
    booked_and_payed = [o for o in booked if o.transaction.status == "capture" or o.transaction.status== "settlement"]
    booked_and_payed.sort(key=lambda x: x.date, reverse=True)
    return render_template("history.html", booked=booked_and_payed, pending_trans=pending_trans)

@users.route("/history/<string:book_id>")
@login_required
def book_detail(book_id):
    user = current_user
    book_info = Booked.query.filter_by(id=book_id).first_or_404()
    if book_info.booked_by != current_user:
        abort(403)
    date = book_info.date
    room = book_info.room_booked
    return render_template("book_detail.html", book_info=book_info, room=room, date=date)

@users.route("/history/<string:book_id>/cancel")
@login_required
def book_detail_cancel(book_id):
    user = current_user
    book_info = Booked.query.filter_by(id=book_id).first_or_404()
    if book_info.booked_by != current_user:
        abort(403)
    try:
        db.session.delete(book_info)
        db.session.commit()
    except:
        pass
    flash(f"Your booking has been canceled", "info")
    return redirect(url_for('users.history'))

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
