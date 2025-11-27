from flask import g, jsonify, request

from app.extensions import db
from ..models import Session, System, User
from . import api
from .authentication import auth


@api.route("/sites/<string:name>")
def get_site_info_by_name(name):
    """
    Retrieve site information by name
    ---
    tags:
        - Sites
    description: |
        Returns the sites identified by the site name.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: name
        schema:
          type: string
        required: true
        description: Name of the site.

    responses:
      200:
        description: Site information retrieved successfully.
        content:
          application/json:
            schema:
              type: object
              description: Serialized site object, including identifier and metadata.
      404:
        description: Site not found.
    """
    try:
        site = db.session.query(User).filter_by(username=name).first()
        return jsonify(site.serialize)
    except:
         return jsonify({"message": "Site not found"}), 404


@api.route("/sites/<int:id>/sessions", methods=["POST"])
@auth.login_required
def post_session(id):
    """
    Create a new session for a site
    ---
    tags:
        - Sites
    description: |
        Adds a new session entry in the database for the specified site.

        Only users with `role_id = 3` (Site users) are authorized.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the site.

      - in: formData
        name: session_fields
        schema:
          type: object
        required: true
        description: Key/value fields required to create a session.

    responses:
      200:
        description: Session successfully created.
        content:
          application/json:
            schema:
              type: object
              properties:
                session_id:
                  type: integer
                  description: ID of the newly created session.
      401:
        description: Unauthorized — only Site users may create sessions.
      404:
        description: Site not found.
    """
    try:
        if g.current_user.role_id != 3:  # Site
            return jsonify({"message": "Unauthorized"}), 401
        else:
            json_session = request.values
            session = Session.from_json(json_session)
            session.site_id = id
            db.session.add(session)
            db.session.commit()
            return jsonify({"session_id": session.id})
    except:
        return jsonify({"message": "Site not found."}), 404


@api.route("/sites/<int:id>/sessions")
def get_site_sessions(id):
    """
    Retrieve all sessions for a site
    ---
    tags:
        - Sites
    description: |
        Returns all sessions created under a specific site.

        **Internal endpoint used only by the Stella App.**

    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the site.

    responses:
      200:
        description: List of session objects.
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                description: Serialized session object.
      404:
        description: Site not found or no sessions associated.
    """
    try:
        sessions = db.session.query(Session).filter_by(site_id=id)
        return jsonify([s.to_json() for s in sessions])
    except:
        return jsonify({"message": "Site not found or no sessions associated."}), 404


@api.route("/sites/<int:id>/systems")
def get_site_systems(id):
    """
    Retrieve all systems deployed at a site
    ---
    tags:
        - Sites
    description: |
        Returns all experimental systems (ranking and recommendation) that are deployed
        at a specific site, identified by its ID.

        **Internal endpoint used only by the Stella App.**
    parameters:
      - in: path
        name: id
        schema:
          type: integer
        required: true
        description: Identifier of the site.

    responses:
      200:
        description: Dictionary of system IDs and their names deployed at the site.
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
                type: string
                description: System name
      404:
        description: System or session not found.
    """
    try:
        systems = db.session.query(System).filter_by(site=id).all()
        system_dict = {s.id: s.name for s in systems}
        return jsonify(system_dict)
    except:
        return jsonify({"message": "System or session not found."}), 404
