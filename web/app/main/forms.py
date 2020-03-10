from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class Dropdown(FlaskForm):
    system = SelectField(choices=[])
    site = SelectField(choices=[])
    submit = SubmitField('Display results')

