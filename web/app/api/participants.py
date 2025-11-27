import json
from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from ..models import Session, System, User
from . import api


@api.route("/participants/<int:id>/systems")
def get_participant_systems(id):
    """
    Get all systems submitted by a participant
    ---
    tags:
        - Participants
    description: |
        Returns all systems associated with a participant (identified by `id`).

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the participant.

    responses:
      200:
        description: List of systems submitted by the participant.
        schema:
          type: array
          items:
            type: object
            description: Serialized system object.

      404:
        description: Participant not found or no systems associated.
    """
    systems = db.session.query(System).filter_by(participant_id=id)
    return jsonify([sys.serialize for sys in systems])


@api.route("/participants/<int:id>/sessions")
def get_participant_sessions(id):
    """
    Get all sessions associated with a participant's systems
    ---
    tags:
        - Participants
    description: |
        Retrieves all sessions in which any system created by the participant took part.
        This includes:
          - Ranking sessions (matching `system_ranking`)
          - Recommendation sessions (matching `system_recommendation`)

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the participant.

    responses:
      200:
        description: List of session objects associated with the participant.
        schema:
          type: array
          items:
            type: object
            description: Serialized session object.

      404:
        description: Participant not found or no sessions associated.
    """
    systems = db.session.query(System).filter_by(participant_id=id)
    systems_id = tuple([sys.id for sys in systems])
    ranking_sessions = (
        db.session.query(Session).filter(Session.system_ranking.in_(systems_id)).all()
    )
    recommendation_sessions = (
        db.session.query(Session)
        .filter(Session.system_recommendation.in_(systems_id))
        .all()
    )

    return jsonify([s.serialize for s in ranking_sessions + recommendation_sessions])
