from flask import g, jsonify, request
from . import api
from .. import db
from ..models import Session, System, User
from .authentication import auth


@api.route('/sites/<int:id>/sessions', methods=['POST'])
@auth.login_required
def post_session(id):
    '''
    Use this endpoint to make a new database entry for a new session.

    @param id: Identifier of the site.
    @return: JSON/Dictionary with the identifier of the session that was created.
    '''
    if g.current_user.role_id != 3:  # Site
        return jsonify({'message': 'Unauthorized'}), 401
    else:
        json_session = request.values
        session = Session.from_json(json_session)
        session.site_id = id
        db.session.add(session)
        db.session.commit()
        return jsonify({'session_id': session.id})


@api.route('/sites/<string:name>')
def get_site_info_by_name(name):
    '''

    @param name: Name of the site.
    @return: JSON/Dictionary containing information (also the identifier) about the site specified by 'name'.
    '''
    site = User.query.filter_by(username=name).first()
    return jsonify(site.serialize)


@api.route('/sites/<int:id>/sessions')
def get_site_sessions(id):
    '''

    @param id: Identifier of the site.
    @return: JSON/Dictionary with information about all sessions from the site specified by the identifier.
    '''
    sessions = Session.query.filter_by(site_id=id)
    return jsonify([s.to_json() for s in sessions])


@api.route('/sites/<int:id>/systems')
def get_site_systems(id):
    '''

    @param id: Identifier of the site.
    @return: JSON/Dictionary with information about all the systems that are deployed at the site.
    '''
    system_dict = {}
    systems = Session.query.with_entities(Session.system_ranking).distinct().filter_by(site_id=id).all()
    for s in systems:
        system_dict.update({s.system_ranking: System.query.get_or_404(s).name})
    return jsonify(system_dict)
