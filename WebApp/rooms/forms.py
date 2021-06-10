from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, MultipleFileField
from flask_wtf.file import FileAllowed
from wtforms.fields.core import SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from WebApp.model import User
import email_validator
from datetime import datetime


class SearchForm(FlaskForm):
    ruangan = StringField("Ruangan", validators=[
        Optional()])
    check_in = DateField("Check-in", format='%Y-%m-%d',
                         validators=[Optional()])
    check_out = DateField("Check-out", format='%Y-%m-%d',
                          validators=[Optional()])
    submit = SubmitField("Find")

    def validate_check_in(self, check_in):
        if(not self.check_in.data and self.check_out.data):
            raise ValidationError(
                'Please fill the Check-in form')
        if(self.check_in.data and not self.check_out.data):
            raise ValidationError(
                'Please fill the Check-out form')
        if(self.check_in.data > self.check_out.data):
            raise ValidationError(
                'Check-in is larger than Check-out')

    def validate_check_out(self, check_out):
        if(self.check_in.data and not self.check_out.data):
            raise ValidationError(
                'Please fill the Check-out form')
        if(not self.check_in.data and self.check_out.data):
            raise ValidationError(
                'Please fill the Check-in form')
        if(self.check_in.data > self.check_out.data):
            raise ValidationError(
                'Check-out is smaller than Check-in')


class BookForm(FlaskForm):
    name = StringField("Full Name", validators=[
        DataRequired()])
    number = StringField("Phone Number", validators=[
        DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    event_name = StringField("Event Name", validators=[
        DataRequired()])
    event_organizer = StringField("Event Organizer", validators=[
        DataRequired()])
    payment = SelectField("Payment", validators=[DataRequired()],
                          choices=[("BCA", "Transfer BCA"), ("BNI", "Transfer BNI"), ("BRI", "Transfer BRI"), ("GOPAY", "Gopay")])
    submit = SubmitField("Pesan")

    def validate_number(self, number):
        if(number.data[0] != "+"):
            raise ValidationError(
                'Masukan nomor telephone diawali dengan +')
        if(len(number.data) < 10):
            raise ValidationError(
                'Please enter a valid number')


class EditRoomForm(FlaskForm):
    name = StringField("Room Name", validators=[DataRequired()])
    location = StringField("Room Location", validators=[DataRequired()])
    room_type = StringField("Room Type", validators=[DataRequired()])
    capacity = IntegerField("Room Capacity", validators=[DataRequired()])
    information = TextAreaField("Room Information")
    picture = MultipleFileField('Upload room pictures', validators=[
        FileAllowed(['jpg', 'png', 'jpeg']), Optional()])
    submit = SubmitField("Edit Informasi")
