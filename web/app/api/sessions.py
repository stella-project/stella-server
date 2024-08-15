import json
from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from ..models import Feedback, Session, System, User
from . import api


@api.route("/sessions/<int:id>")
def get_session(id):
    """
    @param id: Identifier of the session.
    @return: JSON/Dictionary with session and corresponding information.
    """
    session = db.session.query(Session).get_or_404(id)
    return jsonify(session.to_json())


@api.route("/sessions/<int:id>/feedbacks")
def get_session_feedbacks(id):
    """
    @param id: Identifier of the session.
    @return: JSON/Dictionary with all feedbacks corresponding to the specified session.
    """
    feedbacks = db.session.query(Feedback).filter_by(session_id=id)
    return jsonify([f.to_json() for f in feedbacks])


@api.route("/sessions/<int:id>/systems")
def get_session_systems(id):
    """
    @param id: Identifier of the session.
    @return: JSON/Dictionary with the names of the experimental ranking and recommendation systems corresponding to
             the specified session.
    """
    session = db.session.query(Session).filter_by(id=id).first()
    json_session = session.to_json()

    ranker_name = (
        json_session.get("system_ranking")
        if json_session.get("system_ranking") is None
        else db.session.query(System)
        .get_or_404(json_session.get("system_ranking"))
        .name
    )

    recommender_name = (
        json_session.get("system_recommendation")
        if json_session.get("system_recommendation") is None
        else db.session.query(System)
        .get_or_404(json_session.get("system_recommendation"))
        .name
    )

    return jsonify({"RANK": ranker_name, "REC": recommender_name})
