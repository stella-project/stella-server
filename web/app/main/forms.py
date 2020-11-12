from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, URL, Email, EqualTo
from wtforms.fields.html5 import URLField
from wtforms.fields import SelectField
from wtforms import ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from ..models import User


class Dropdown(FlaskForm):
    system = SelectField(choices=[])
    site = SelectField(choices=[])
    submit = SubmitField('Display results')


class ChangeUsernameForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    submit1 = SubmitField('change username')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangeEmailForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit2 = SubmitField('change E-Mail')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')


class ChangePassword(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new Password', validators=[DataRequired()])
    submit3 = SubmitField('Change Password')


class SubmitSystem(FlaskForm):
    systemname = StringField('System Name', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Systemname must have only letters, numbers, dots or '
               'underscores')])
    site_type = SelectField('Site & System type', choices=['GESIS (Dataset recommender)', 'LIVIVO (Document ranker)'])
    GitHubUrl = URLField('URL', validators=[DataRequired(message="Enter URL Please"),
                                            URL(message="Enter Valid URL Please.")])

    submit = SubmitField('Submit')


class SubmitRanking(FlaskForm):
    systemname = StringField('System name', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Systemname must have only letters, numbers, dots or '
               'underscores')])
    site_type = SelectField('Site & System type', choices=['GESIS (Dataset recommender)', 'LIVIVO (Document ranker)'])
    upload = FileField('Run file', validators=[FileRequired(),
                                               FileAllowed(['out', 'txt'], 'Images only!')]
                       )

    submit2 = SubmitField('Submit')
