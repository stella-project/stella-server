from flask import g, jsonify, request

from app.extensions import db
from ..models import Feedback, Result, Session, System
from . import api


@api.route("/feedbacks/<int:id>/rankings", methods=["POST"])
def post_ranking(id):
    """
    Use this endpoint to add a ranking for a specific feedback and the corresponding session.

    @param id: Identifier of the feedback.
    @return: JSON/Dictionary with id of the ranking.
    """

    if g.current_user.role_id != 3:  # Site
        return jsonify({"message": "Unauthorized"}), 401

    elif request.method == "POST":
        feedback = db.get_or_404(Feedback, id)
        site = feedback.site_id
        session = db.get_or_404(Session, feedback.session_id)
        json_ranking = request.values
        ranking = Result.from_json(json_ranking)
        ranking.site_id = site
        ranking.session_id = session.id
        ranking.feedback_id = id
        ranking.system_id = (
            json_ranking.get("system_id")
            if json_ranking.get("system_id")
            else session.system_ranking
        )
        ranking.participant_id = db.get_or_404(
            System, session.system_ranking
        ).participant_id

        ranking.type = "RANK"
        db.session.add(ranking)
        db.session.commit()

    return jsonify({"ranking_id": ranking.id})


@api.route("/rankings/<int:id>", methods=["GET", "PUT"])
def ranking(id):
    """
    Use this endpoint either to get information about a specific ranking (GET) or to update the information (PUT).

    @param id: Identifier of the ranking.
    @return: GET - JSON/Dictionary with ranking and corresponding items.
             PUT - Update ranking with specified identifier 'id'.
    """
    if request.method == "GET":
        ranking = db.get_or_404(Result, id)
        return jsonify(ranking.to_json())
    if request.method == "PUT":
        json_ranking = request.values
        ranking = db.get_or_404(Result, id)
        ranking.update(json_ranking)
        db.session.commit()
        return 200


@api.route("/rankings")
def get_rankings():
    """

    @return: JSON/Dictionary with identifiers of all rankings in database.
    """
    results = db.session.query(Result).filter_by(type="RANK")
    return jsonify({"rids": [r.id for r in results]})
