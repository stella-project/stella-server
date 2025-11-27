from flask import g, jsonify, request

from app.extensions import db
from ..models import Feedback, Result, Session, System
from . import api


@api.route("/feedbacks/<int:id>/rankings", methods=["POST"])
def post_ranking(id):
    """
    Create a ranking for a specific feedback
    ---
    tags:
        - Rankings
    description: |
        Adds a new ranking associated with the given feedback ID and its parent session.
        Only users with role_id = 3 (Site) are authorized to create rankings.

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Identifier of the feedback.

      - in: formData
        name: system_id
        type: integer
        required: false
        description: Optional system identifier. Defaults to the session's system_ranking value.

      - in: formData
        name: other_fields
        type: string
        required: false
        description: Any additional fields required to construct a ranking object.

    responses:
      200:
        description: Ranking successfully created.
        schema:
          type: object
          properties:
            ranking_id:
              type: integer
              description: Identifier of the newly created ranking.

      401:
        description: Unauthorized. Only Site users may create rankings.

      404:
        description: Feedback or Session not found.
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
    Retrieve or update a specific ranking
    ---
    tags:
        - Rankings
    description: |
        GET returns the ranking and its associated fields.
        PUT updates the ranking with new values supplied in the request.

    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: Identifier of the ranking.

      - in: formData
        name: fields
        type: string
        required: false
        description: Fields to update (only used for PUT requests).

    responses:
      200:
        description: |
          GET – Returns the ranking as JSON.  
          PUT – Ranking updated successfully.
        schema:
          type: object
          properties:
            id:
              type: integer
            site_id:
              type: integer
            session_id:
              type: integer
            feedback_id:
              type: integer
            system_id:
              type: integer
            participant_id:
              type: integer
            type:
              type: string

      404:
        description: Ranking not found.
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
    List all ranking identifiers
    ---
    tags:
        - Rankings
    description: Returns the list of all ranking IDs stored in the database.
    responses:
      200:
        description: A list of ranking identifiers.
        schema:
          type: object
          properties:
            rids:
              type: array
              items:
                type: integer
              description: Ranking IDs.
    """
    results = db.session.query(Result).filter_by(type="RANK")
    return jsonify({"rids": [r.id for r in results]})
