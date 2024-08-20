from flask import g, jsonify, request
from flask_login import current_user, login_required, login_user

from app.extensions import db
from ..models import Feedback, Result, Session, System
from . import api


@api.route("/feedbacks/<int:id>/recommendations", methods=["POST"])
def post_recommendation(id):
    """
    Use this endpoint to add a recommendation for a specific feedback and the corresponding session.
    tested: true

    @param id: Identifier of the feedback.
    @return: JSON/Dictionary with id of the recommendation.
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
    Use this endpoint either to get information about a specific recommendation (GET) or to update the information (PUT)

    @param id: Identifier of the recommendation.
    @return: GET - JSON/Dictionary with recommendation and corresponding items.
             PUT - Update recommendation with specified identifier 'id'.
    """
    if request.method == "GET":
        recommendation = db.get_or_404(Session, id)
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
    TODO: This endpoint is protected. But where?
    Tested: True
    @return: JSON/Dictionary with identifiers of all recommendations in database.
    """
    results = db.session.query(Result).filter_by(type="REC")
    return jsonify({"rids": [r.id for r in results]})
