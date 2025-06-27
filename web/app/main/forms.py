import re

from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    URLField,
    ValidationError,
)
from wtforms.fields import SelectField
from wtforms.validators import URL, DataRequired, Email, EqualTo, Length, Regexp, Optional

from ..models import System, User
from app.extensions import db


class Dropdown(FlaskForm):
    system = SelectField("", choices=[])
    submit = SubmitField("Show results")


class ChangeUsernameForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must have only letters, numbers, dots or " "underscores",
            ),
        ],
    )
    submit1 = SubmitField("change username")

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).first():
            raise ValidationError("Username already in use.")


class ChangeEmailForm(FlaskForm):
    email = StringField("E-Mail", validators=[DataRequired(), Length(1, 64), Email()])
    submit2 = SubmitField("change E-Mail")

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data.lower()).first():
            raise ValidationError("Email already registered.")


class ChangePassword(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must match."),
        ],
    )
    password2 = PasswordField("Confirm new Password", validators=[DataRequired()])
    submit3 = SubmitField("Change Password")


class SubmitSystem(FlaskForm):
    systemname = StringField(
        "System Name",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.-]*$",
                0,
                "Systemname must start with a letter, and can only include letters, numbers, underscores (_), hyphens (-), or dots (.)",
            ),
        ],
    )
    type = SelectField(
        "System type",
        choices=["Recommender", " Ranker"],
    )
    site = SelectField(
        "Site",
    )
    GitHubUrl = URLField(
        "URL",
        validators=[
            #DataRequired(message="Enter URL Please"),
            Optional(),
            URL(message="Enter Valid URL Please."),
        ],
    )

    def validate_systemname(self, field):
        if re.match("^[A-Za-z][A-Za-z0-9_.-]*$", field.data):
            if db.session.query(System).filter_by(name=field.data).first():
                flash("System name already in use.", "danger")
                raise ValidationError("System name already in use.")
        else:
            flash(
                "Systemname must start with a letter, and can only include letters, numbers, underscores (_), hyphens (-), or dots (.)",
                "danger",
            )

    submit = SubmitField("Submit")

    def __init__(self, sites=None, user_role_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.site.choices = sites or []

        if user_role_name == "Site":
            self.site.render_kw = {"disabled": "disabled"}

class SubmitRanking(FlaskForm):
    systemname = StringField(
        "System name",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.-]*$",
                0,
                "Systemname must start with a letter, and can only include letters, numbers, underscores (_), hyphens (-), or dots (.)",
            ),
        ],
    )
    site_type = SelectField(
        "Site & System type",
        choices=["Recommender", "Ranker"],
    )
    upload = FileField(
        "Run file",
        validators=[
            FileRequired(),
            FileAllowed(
                ["tar.xz", "tar.gz", "zip", "txt"],
                "Please upload a *.txt, *.tar.xz, or *.tar.gz file!",
            ),
        ],
    )

    def validate_systemname(self, field):
        if re.match("^[A-Za-z][A-Za-z0-9_.-]*$", field.data):
            if db.session.query(System).filter_by(name=field.data).first():
                flash("System name already in use.", "danger")
                raise ValidationError("System name already in use.")
        else:
            flash(
                "Systemname must start with a letter, and can only include letters, numbers, underscores (_), hyphens (-), or dots (.)",
                "danger",
            )

    submit2 = SubmitField("Submit")
