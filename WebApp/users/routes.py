import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app, Markup
from flask_login import login_user, current_user, logout_user, login_required
from WebApp import db, bcrypt
from WebApp.model import Booked, User
from WebApp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                RequestResetForm, ResetPasswordForm)
from WebApp.users.utils import save_picture, send_activate_email, send_reset_email, generate_book_qr, validate_book
from datetime import timedelta, datetime

users = Blueprint('users', __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.active == True:
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            flash(
                f"Login successful, welcome {user.username}!", category='success')
            return redirect(nextPage) if nextPage else redirect(url_for('main.home'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and user.active == False:
            flash(Markup(
                f"Please activate your account, we have sent an activation code to your email,<a href=\"{url_for('users.sent_activate_token', username=user.username)}\" class=\"ms-1 me-1\">click here</a>to send them again"), "danger")
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
                    email=form.email.data, password=hashedPassword, active=False)
        db.session.add(user)
        db.session.commit()
        send_activate_email(user)
        flash("Please activate your account, an activation link has been sent to your email", "info")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/register/sent-activation-link/<string:username>")
def sent_activate_token(username):
    user = User.query.filter_by(username=username).first()
    if(user):
        send_activate_email(user)
        flash("An activation link has been sent to your email", "info")
        return redirect(url_for('users.login'))
    else:
        os.abort(403)


@users.route("/register/<string:token>")
def activate_account(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('users.register'))
    user.active = True
    db.session.commit()
    flash("Your account has been activated, now you're able to login", "success")
    return redirect(url_for('users.login'))


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
        t.expire = (t.time + timedelta(hours=6)
                    ).strftime("%d/%m/%Y, %H:%M:%S") + " WIB"
    print(pending_trans)
    booked = user.book_info
    booked_and_payed = [o for o in booked if o.transaction.status ==
                        "capture" or o.transaction.status == "settlement"]
    booked_and_payed.sort(key=lambda x: x.date, reverse=True)
    return render_template("history.html", booked=booked_and_payed, pending_trans=pending_trans)


@users.route("/history/<string:book_id>")
@login_required
def book_detail(book_id):
    user = current_user
    book_info = Booked.query.filter_by(id=book_id).first_or_404()
    if book_info.booked_by != current_user:
        os.abort(403)
    image_name = f"qr_{book_id}.png"
    image_path = os.path.join(
        current_app.root_path, "static", "images", image_name)
    if not os.path.exists(image_path):
        generate_book_qr(image_path, book_id)
    date = book_info.date
    room = book_info.room_booked
    return render_template("book_detail.html", book_info=book_info, room=room, date=date, image_name=image_name)


@users.route("/history/<string:book_id>/<string:token>")
def book_detail_validation(book_id, token):
    booked = Booked.query.filter_by(id=book_id).first_or_404()
    if(validate_book(book_id, token)):
        return render_template("book_confirmation_success.html", booked=booked)
    else:
        return render_template("book_confirmation_failed.html", booked=booked)


@users.route("/history/<string:book_id>/cancel")
@login_required
def book_detail_cancel(book_id):
    user = current_user
    book_info = Booked.query.filter_by(id=book_id).first_or_404()
    if book_info.booked_by != current_user:
        os.abort(403)
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
        print(form.picture.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        if form.password.data:
            if bcrypt.check_password_hash(current_user.password, form.oldPassword.data):
                pass
            else:
                flash("Your current password is incorrect", category="danger")
                return redirect(url_for('users.account'))
            hashedPassword = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            current_user.password = hashedPassword
        db.session.commit()
        flash("Your account has been updated", category='success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' +
                         current_user.image_file)
    return render_template('profil.html', title="Account", image_file=image_file, form=form)


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
        flash('Your reset password request has been sent to your email', 'success')
        return redirect(url_for('users.login'))
    return render_template('forgot_password.html', form=form)


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
    return render_template('reset_password.html', form=form, user=user)
