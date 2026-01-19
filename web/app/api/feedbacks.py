from flask import g, jsonify, request

from app.extensions import db
from ..models import Feedback, Session
from . import api
from .authentication import auth


@api.route("/sessions/<int:id>/feedbacks", methods=["POST"])
@auth.login_required
def post_feedback(id):
    """
    Create feedback for a session
    ---
    tags:
        - Feedback
    description: |
        Creates a new feedback entry for a specific session identified by `id`.

        **Internal endpoint used only by the Stella App.**
        Only users with `role_id = 3` (Site users) may create feedback.

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the session.

      - in: formData
        name: feedback_fields
        schema:
          type: object
        description: Key/value fields representing feedback data.

    responses:
      200:
        description: Feedback successfully created.
        schema:
          type: object
          properties:
            feedback_id:
              type: integer
              description: Identifier of the created feedback.

      401:
        description: Unauthorized – Only Site users may create feedback.

      404:
        description: Session not found.
    """
    try:
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
    except:
        return jsonify({"message": "Session not found."}), 404


@api.route("/feedbacks")
def get_feedbacks():
    """
    Retrieve all feedback entries
    ---
    tags:
        - Feedback
    description: |
        Returns an array of all feedback entries stored in the database.

        **Internal endpoint used only by the Stella App.**

    responses:
      200:
        description: List of feedback entries.
        schema:
          type: array
          items:
            type: object
            description: Serialized feedback object.
    """
    feedbacks = Feedback.query.all()
    return jsonify([feedback.serialize for feedback in feedbacks])


@api.route("/feedbacks/<int:id>")
def get_feedback(id):
    """
    Retrieve a specific feedback entry
    ---
    tags:
        - Feedback
    description: |
        Returns a single feedback entry by its identifier.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the feedback entry.

    responses:
      200:
        description: Feedback object retrieved successfully.
        schema:
          type: object
          description: Serialized feedback data.

      404:
        description: Feedback not found.
    """
    feedback = db.get_or_404(Feedback, id)
    return jsonify(feedback.to_json())


@api.route("/feedbacks/<int:id>", methods=["PUT"])
def edit_feedback(id):
    """
    Update a feedback entry
    ---
    tags:
        - Feedback
    description: |
        Updates an existing feedback entry using the provided key/value fields.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the feedback entry to update.

      - in: formData
        name: feedback_fields
        schema:
          type: object
        description: Fields to update in the feedback entry.

    responses:
      200:
        description: Feedback updated successfully.
        schema:
          type: object
          description: Updated feedback data.

      404:
        description: Feedback not found.
    """
    json_feedback = request.values
    feedback = db.get_or_404(Feedback, id)
    feedback.update(json_feedback)
    db.session.commit()

    return jsonify(feedback.to_json())
