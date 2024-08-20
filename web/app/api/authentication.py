from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from app.extensions import db
from ..models import User
from . import api

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    """
    Use this method to verify the password when user accesses the stella-server.

    @param email_or_token: Can be either the e-mail address of the user or a previously received token.
    @param password: Password in clear text.
    @return: Boolean indicating if password is correct.
    """
    if email_or_token == "":
        return False
    if password == "":
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = db.session.query(User).filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@api.route("/tokens", methods=["POST"])
@auth.login_required
def get_token():
    """

    @return: JSON/Dictionary containing the JSON Web Token (JWT) and information about the expiration,
             if user is authorized.
    """
    return jsonify(
        {
            "token": g.current_user.generate_auth_token(expiration=3600),
            "expiration": 3600,
        }
    )


@api.before_request
@auth.login_required
def before_request():
    """

    @return: JSON/Dictionary containing with 'forbidden' error and message about 'unconfirmed access'.
    """
    if g.current_user.is_anonymous:
        return jsonify({"error": "forbidden", "message": "Unconfirmed account"}), 403
