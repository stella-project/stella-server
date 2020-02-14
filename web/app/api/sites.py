import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User


@api.route('/sites/<int:id>/sessions', methods=['POST'])
def post_session(id):
    json_session = request.values
    session = Session.from_json(json_session)
    session.site_id = id

    db.session.add(session)
    db.session.commit()

    return jsonify({'session_id': session.id})


@api.route('/sites/<string:name>')
def get_site_info_by_name(name):
    site = User.query.filter_by(username=name).first()
    return jsonify(site.serialize)


@api.route('/sites/<int:id>/sessions')
def get_site_sessions(id):
    sessions = Session.query.filter_by(site_id=id)
    return jsonify([s.to_json() for s in sessions])


@api.route('/sites/<int:id>/systems')
def get_site_systems(id):
    pass  #  TODO: return all systems deployed at site with id. return dictionary with ids as keys and names as values