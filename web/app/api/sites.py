from flask import g, jsonify, request

from app.extensions import db
from ..models import Session, System, User
from . import api
from .authentication import auth


@api.route("/sites/<string:name>")
def get_site_info_by_name(name):
    """Get the user ID of a user by its username
    Tested: True

    @param name: Name of the site.
    @return: JSON/Dictionary containing information (also the identifier) about the site specified by 'name'.
    """
    site = db.session.query(User).filter_by(username=name).first()
    return jsonify(site.serialize)


@api.route("/sites/<int:id>/sessions", methods=["POST"])
@auth.login_required
def post_session(id):
    """
    Use this endpoint to make a new database entry for a new session.
    Tested: True

    @param id: Identifier of the site.
    @return: JSON/Dictionary with the identifier of the session that was created.
    """
    if g.current_user.role_id != 3:  # Site
        return jsonify({"message": "Unauthorized"}), 401
    else:
        json_session = request.values
        session = Session.from_json(json_session)
        session.site_id = id
        db.session.add(session)
        db.session.commit()
        return jsonify({"session_id": session.id})


@api.route("/sites/<int:id>/sessions")
def get_site_sessions(id):
    """Get all sessions from a site by its user ID

    tested: True
    TODO: This uses a different authentication as the above. Why?
    @param id: Identifier of the site.
    @return: JSON/Dictionary with information about all sessions from the site specified by the identifier.
    """
    sessions = db.session.query(Session).filter_by(site_id=id)
    return jsonify([s.to_json() for s in sessions])


@api.route("/sites/<int:id>/systems")
def get_site_systems(id):
    """
    TODO: test this function
    @param id: Identifier of the site.
    @return: JSON/Dictionary with information about all the systems that are deployed at the site.
    """
    system_dict = {}
    systems = (
        db.session.query(Session)
        .with_entities(Session.system_ranking)
        .distinct()
        .filter_by(site_id=id)
        .all()
    )
    for s in systems:
        system_dict.update({s.system_ranking: db.get_or_404(System, s).name})
    return jsonify(system_dict)
