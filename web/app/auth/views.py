from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from ..commands import register_user
from ..models import User
from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid email or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            register_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                role="Participant",
            )
        except ValueError as e:
            flash(str(e), "danger")
        else:
            flash("You can now login.")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)
