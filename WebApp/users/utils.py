from enum import Flag
import os
import secrets
from PIL import Image
from flask import url_for, current_app, request
from flask_mail import Message
from flask_login import current_user
from WebApp import mail
import qrcode
from itsdangerous import JSONWebSignatureSerializer as Serializer


def save_picture(form_picture):
    pref_picture = os.path.join(
        current_app.root_path, "static", "images", current_user.image_file)
    if os.path.exists(pref_picture) and os.path.basename(pref_picture) != 'default.jpg':
        os.remove(pref_picture)
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(
        current_app.root_path, 'static', 'images', picture_filename)

    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_filename


def generate_book_qr(image_path, book_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    s = Serializer(current_app.config['SECRET_KEY'])
    qr.add_data(url_for('users.book_detail_validation', book_id=book_id,
                token=s.dumps({'book_id': book_id}).decode('utf-8'), _external=True))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img.save(image_path)


def validate_book(book_id, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        book_id_token = s.loads(token)['book_id']
    except:
        return False
    if(book_id == book_id_token):
        return True
    else:
        return False


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@apps.ipb.ac.id', recipients=[user.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('users.reset_token',token=token, _external = True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.send(msg)


def send_activate_email(user):
    token = user.get_reset_token()
    msg = Message('Activate Your Account',
                  sender='noreply@apps.ipb.ac.id', recipients=[user.email])
    msg.body = f'''To activate your account, click the following link:
{url_for('users.activate_account',token=token, _external = True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.send(msg)
