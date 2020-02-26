import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User


@api.route('/participants/<int:id>/systems')
def get_participant_systems(id):
    systems = System.query.filter_by(participant_id=id)
    return jsonify([sys.serialize for sys in systems])


@api.route('/participants/<int:id>/sessions')
def get_participant_sessions(id):
    systems = System.query.filter_by(participant_id=id)
    systems_id = tuple([sys.id for sys in systems])
    ranking_sessions = db.session.query(Session).filter(Session.system_ranking.in_(systems_id)).all()
    recommendation_sessions = db.session.query(Session).filter(Session.system_recommendation.in_(systems_id)).all()

    return jsonify([s.serialize for s in ranking_sessions + recommendation_sessions])