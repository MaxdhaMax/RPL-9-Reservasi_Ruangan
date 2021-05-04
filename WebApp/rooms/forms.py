from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flask_login import current_user
from WebApp.model import User
import email_validator
from datetime import datetime


class SearchForm(FlaskForm):
    ruangan = StringField("Ruangan", validators=[
        DataRequired()])
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
