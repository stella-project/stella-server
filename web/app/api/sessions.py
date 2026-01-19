import json
from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from ..models import Feedback, Session, System, User
from . import api


@api.route("/sessions/<int:id>")
def get_session(id):
    """
    Retrieve a session by ID
    ---
    tags:
        - Sessions
    description: |
        Returns detailed information for a specific session, including all
        stored attributes.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the session.

    responses:
      200:
        description: Session object retrieved successfully.
        content:
          application/json:
            schema:
              type: object
              description: Serialized session data.
      404:
        description: Session not found.
    """
    try:    
        session = db.session.query(Session).get_or_404(id)
        return jsonify(session.to_json())
    except:
        return jsonify({"message": "Session not found."}), 404

@api.route("/sessions/<int:id>/feedbacks")
def get_session_feedbacks(id):
    """
    Retrieve all feedback for a session
    ---
    tags:
        - Sessions
    description: |
        Returns a list of all feedback entries associated with a specific session.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the session.

    responses:
      200:
        description: List of feedback objects.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                description: Serialized feedback entry.
      404:
        description: Session not found.
    """
    feedbacks = db.session.query(Feedback).filter_by(session_id=id)
    return jsonify([f.to_json() for f in feedbacks])


@api.route("/sessions/<int:id>/systems")
def get_session_systems(id):
    """
    Retrieve system names for a session
    ---
    tags:
        - Sessions  
    description: |
        Returns the names of the ranking and recommendation systems used in a session.
        If a system ID is missing, the value will be `null`.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the session.

    responses:
      200:
        description: Names of the ranking and recommendation systems.
        content:
          application/json:
            schema:
              type: object
              properties:
                RANK:
                  type: string
                  nullable: true
                  description: Name of the ranking system.
                REC:
                  type: string
                  nullable: true
                  description: Name of the recommendation system.
      404:
        description: Session or system not found.
    """
    try:
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
    except:
        return jsonify({"message": "Session or system not found."}), 404
