from flask import g, jsonify, request

from app.extensions import db
from ..models import Feedback, Session
from . import api
from .authentication import auth


@api.route("/sessions/<int:id>/feedbacks", methods=["POST"])
@auth.login_required
def post_feedback(id):
    """
    This endpoint is used to make a feedback entry for a specific session identified by 'id'.
    Use the 'id' to post further click feedback.

    @param id: Identifier of the session.
    @return: JSON/Dictionary with identifier of the feedback.
    """
    if g.current_user.role_id != 3:  # Site
        return jsonify({"message": "Unauthorized"}), 401

    elif request.method == "POST":

        session = db.get_or_404(Session, id)
        json_feedback = request.values
        feedback = Feedback.from_json(json_feedback)
        feedback.session_id = id
        site = session.site_id
        feedback.site_id = site

        db.session.add(feedback)
        db.session.commit()

    return jsonify({"feedback_id": feedback.id})


@api.route("/feedbacks")
def get_feedbacks():
    """

    @return: JSON/Dictionary containing the entire feedback data.
    """
    feedbacks = db.query(Feedback).all()
    return jsonify([feedback.serialize for feedback in feedbacks])


@api.route("/feedbacks/<int:id>")
def get_feedback(id):
    """

    @param id: Identifier of the feedback database entry.
    @return: JSON/Dictionary containing the feedback.
    """
    feedback = db.get_or_404(Feedback, id)
    return jsonify(feedback.to_json())


@api.route("/feedbacks/<int:id>", methods=["PUT"])
def edit_feedback(id):
    """
    Updates the feedback by the specified identifier.

    @param id:  Identifier of the feedback database entry.
    @return: -
    """
    json_feedback = request.values
    feedback = db.get_or_404(Feedback, id)
    feedback.update(json_feedback)
    db.session.commit()
