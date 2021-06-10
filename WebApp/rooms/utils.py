from datetime import date, timedelta
from WebApp import ma
from WebApp.model import Transaction
from flask import current_app
from flask_login import current_user
import os
from PIL import Image
import secrets


class BookedSchema(ma.Schema):
    class Meta:
        fields = ('date', 'event', 'organization', 'name',
                  'booked_by.username', 'room_booked.name')


def ListBetweenTwoDates(first_date: date, second_date: date):
    delta = second_date - first_date
    dateBetween = []
    for i in range(delta.days + 1):
        day = first_date + timedelta(days=i)
        daystr = day.strftime("%Y-%m-%d")
        dateBetween.append(daystr)
    return dateBetween


def PaymentParameters(payment: str, name: str, email: str, phone: str, price: int, transID: str):
    if(payment == "BCA"):
        param = {
            "payment_type": "bank_transfer",
            "customer_details": {
                "first_name": name.split()[0],
                "last_name": " ".join((name).split()[1:]),
                "email": email,
                "phone": phone
            },
            "transaction_details": {
                "order_id": transID,
                "gross_amount": price
            },
            "bank_transfer": {
                "bank": "bca"
            },
            "custom_expiry": {
                "expiry_duration": 60 * 6,
                "unit": "minute"
            }
        }
    elif(payment == "BNI"):
        param = {
            "payment_type": "bank_transfer",
            "customer_details": {
                "first_name": name.split()[0],
                "last_name": " ".join((name).split()[1:]),
                "email": email,
                "phone": phone
            },
            "transaction_details": {
                "order_id": transID,
                "gross_amount": price
            },
            "bank_transfer": {
                "bank": "bni"
            },
            "custom_expiry": {
                "expiry_duration": 60 * 6,
                "unit": "minute"
            }
        }
    elif(payment == "BRI"):
        param = {
            "payment_type": "bank_transfer",
            "customer_details": {
                "first_name": name.split()[0],
                "last_name": " ".join((name).split()[1:]),
                "email": email,
                "phone": phone
            },
            "transaction_details": {
                "order_id": transID,
                "gross_amount": price
            },
            "bank_transfer": {
                "bank": "bri"
            },
            "custom_expiry": {
                "expiry_duration": 60 * 6,
                "unit": "minute"
            }
        }
    elif(payment == "GOPAY"):
        param = {
            "payment_type": "gopay",
            "customer_details": {
                "first_name": name.split()[0],
                "last_name": " ".join((name).split()[1:]),
                "email": email,
                "phone": phone
            },
            "transaction_details": {
                "gross_amount": price,
                "order_id": transID,
            },
            "custom_expiry": {
                "expiry_duration": 60 * 6,
                "unit": "minute"
            }
        }
    return param


def SavePictures(form_pictures, room_id):
    picture_filenames = []
    for picture in form_pictures:
        random_hex = secrets.token_hex(2)
        _, file_ext = os.path.splitext(picture.filename)
        picture_filename = room_id + "-" + random_hex + file_ext
        picture_filenames.append(picture_filename)
        picture_path = os.path.join(
            current_app.root_path, 'static', 'images', picture_filename)
        i = Image.open(picture)
        i.save(picture_path)
    return picture_filenames
