from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, URL
from wtforms.fields.html5 import URLField
from wtforms import ValidationError
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
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class SubmitSystem(FlaskForm):
    systemname = StringField('System Name', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Systemname must have only letters, numbers, dots or '
               'underscores')])
    GitHubUrl = URLField('URL', validators=[DataRequired(message="Enter URL Please"),
        URL(message="Enter Valid URL Please.")])

    submit = SubmitField('Submit')