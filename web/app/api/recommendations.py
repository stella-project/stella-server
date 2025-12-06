from flask import g, jsonify, request, current_app
from flask_login import current_user, login_required, login_user

from app.extensions import db
from ..models import Feedback, Result, Session, System
from . import api


@api.route("/feedbacks/<int:id>/recommendations", methods=["POST"])
def post_recommendation(id):
    """
    Create a recommendation for a specific feedback
    --- 
    tags:
        - Recommendations
    description: |
        Creates a new recommendation entry associated with a feedback record and its session.

        **Internal endpoint used only by the Stella App.**
        Only users with `role_id = 3` (Site users) are authorized.

    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: Identifier of the feedback.

      - in: formData
        name: system_id
        required: false
        schema:
          type: integer
        description: Optional system ID. If omitted, defaults to `session.system_recommendation`.

      - in: formData
        name: recommendation_fields
        required: false
        schema:
          type: object
        description: Additional fields used to construct the recommendation.

    responses:
      200:
        description: Recommendation successfully created.
        schema:
          type: object
          properties:
            recommendation_id:
              type: integer
              description: ID of the created recommendation.

      401:
        description: Unauthorized — only Site users may submit recommendations.

      404:
        description: Feedback or Session not found.
    """
    if g.current_user.role_id != 3:  # Site
        return jsonify({"message": "Unauthorized"}), 401

    elif request.method == "POST":
        feedback = db.get_or_404(Feedback, id)
        site = feedback.site_id
        session = db.get_or_404(Session, feedback.session_id)
        json_recommendation = request.values
        recommendation = Result.from_json(json_recommendation)
        recommendation.site_id = site
        recommendation.session_id = session.id
        recommendation.feedback_id = id
        
        recommendation.system_id = (
            json_recommendation.get("system_id")
            if json_recommendation.get("system_id")
            else session.system_recommendation
        )
        recommendation.participant_id = db.get_or_404(
            System, session.system_recommendation
        ).participant_id
        
        recommendation.type = "REC"
        db.session.add(recommendation)
        db.session.commit()

    return jsonify({"recommendation_id": recommendation.id})


@api.route("/recommendations/<int:id>", methods=["GET", "PUT"])
def recommendation(id):
    """
    Retrieve or update a specific recommendation
    ---
    tags:
        - Recommendations
    description: |
        GET returns the full recommendation object.  
        PUT updates the recommendation using the provided form fields.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: Identifier of the recommendation.

      - in: formData
        name: recommendation_fields
        required: false
        schema:
          type: object
        description: Fields to update (only for PUT requests).

    responses:
      200:
        description: |
          GET – Recommendation retrieved.  
          PUT – Recommendation updated successfully.
        schema:
          type: object
          description: Serialized recommendation object.

      404:
        description: Recommendation not found.
    """
    if request.method == "GET":
        recommendation = db.get_or_404(Result, id)
        return jsonify(recommendation.to_json())
    if request.method == "PUT":
        json_recommendation = request.values
        recommendation = db.get_or_404(Result, id)
        recommendation.update(json_recommendation)
        db.session.commit()
        return jsonify(recommendation.to_json())


@api.route("/recommendations")
def get_recommendations():
    """
    Retrieve all recommendation IDs
    ---
    tags:
        - Recommendations
    description: |
        Returns all recommendation identifiers stored in the database.

        **Internal endpoint used only by the Stella App.**

        Note: This endpoint is **not currently protected**, even though it should be.
        Consider adding authentication.

    responses:
      200:
        description: List of recommendation IDs.
        schema:
          type: object
          properties:
            rids:
              type: array
              items:
                type: integer
              description: Recommendation IDs.
    """
    """
    TODO: This endpoint is protected. But where?
    Tested: True
    @return: JSON/Dictionary with identifiers of all recommendations in database.
    """
    results = db.session.query(Result).filter_by(type="REC")
    return jsonify({"rids": [r.id for r in results]})
