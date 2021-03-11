import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from WebApp import mail


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

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename


def send_reset_email(user):
    token = user.getlogin_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@apps.ipb.ac.id', recipients=[user.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('users.reset_token',token=token, _external = True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.send(msg)
