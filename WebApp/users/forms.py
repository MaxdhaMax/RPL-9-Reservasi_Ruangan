from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from WebApp.model import User
import email_validator


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirmation = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if (user):
            raise ValidationError(
                'That username is taken, please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if (user):
            raise ValidationError(
                'That email is taken, please choose another one.')


class RegistrationTypeForm(FlaskForm):
    choice = ["Mahasiswa", "Dosen", "Staff"]
    user_type = SelectField("Siapakah Anda", validators=[
                            DataRequired()], choices=choice)
    submit = SubmitField("Pilih")


class MahasiswaRegistrationForm(FlaskForm):
    nim = StringField("NIM", validators=[
        DataRequired(), Length(max=12)])
    nama = StringField("NIM", validators=[
        DataRequired(), Length(min=2, max=30)])
    departemen = StringField("Departemen", validators=[
        DataRequired(), Length(min=2, max=30)])
    fakultas = StringField("Fakultas", validators=[
        DataRequired(), Length(min=2, max=30)])
    angkatan = IntegerField("Angkatan", validators=[
        DataRequired()])
    submit = SubmitField("Pilih")


class DosenRegistrationForm(FlaskForm):
    nik = StringField("NIK", validators=[
        DataRequired(), Length(max=12)])
    nama = StringField("NIM", validators=[
        DataRequired(), Length(min=2, max=30)])
    departemen = StringField("Departemen", validators=[
        DataRequired(), Length(min=2, max=30)])
    fakultas = StringField("Fakultas", validators=[
        DataRequired(), Length(min=2, max=30)])
    submit = SubmitField("Pilih")


class StaffRegistrationForm(FlaskForm):
    nik = StringField("NIK", validators=[
        DataRequired(), Length(max=12)])
    nama = StringField("NIM", validators=[
        DataRequired(), Length(min=2, max=30)])
    submit = SubmitField("Pilih")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if (user):
                raise ValidationError(
                    'That username is taken, please choose another one.')


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if (user) is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    passwordConfirmation = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
