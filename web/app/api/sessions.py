import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User, Feedback


@api.route('/sessions/<int:id>')
def get_session(id):
    '''

    @param id: Identifier of the session.
    @return: JSON/Dictionary with session and corresponding information.
    '''
    session = Session.query.get_or_404(id)
    return jsonify(session.to_json())


@api.route('/sessions/<int:id>/feedbacks')
def get_session_feedbacks(id):
    '''

    @param id: Identifier of the session.
    @return: JSON/Dictionary with all feedbacks corresponding to the specified session.
    '''
    feedbacks = Feedback.query.filter_by(session_id=id)
    return jsonify([f.to_json() for f in feedbacks])


@api.route('/sessions/<int:id>/systems')
def get_session_systems(id):
    '''

    @param id: Identifier of the session.
    @return: JSON/Dictionary with the names of the experimental ranking and recommendation systems corresponding to
             the specified session.
    '''
    session = Session.query.filter_by(id=id).first()
    json_session = session.to_json()

    ranker_name = System.query.get_or_404(json_session.get('system_ranking')).name
    recommender_name = System.query.get_or_404(json_session.get('system_recommendation')).name

    return jsonify({'RANK': ranker_name,
                    'REC': recommender_name})
