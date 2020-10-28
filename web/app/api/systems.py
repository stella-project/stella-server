from flask import jsonify, request
from . import api
from .. import db
from ..models import Session, System, User, Feedback


@api.route('/system/id/<string:name>')
def get_id(name):
    '''
    This endpoint is used to get the corresponding id for a specific system by its 'name'.
    Use the 'id' to get system specific click feedback.

    @param name: name of the system.
    @return: JSON/Dictionary with id of the system.
    '''
    system = System.query.filter_by(name=name).first()

    return jsonify({'system_id': system.id})


@api.route('/system/<int:id>/export')
def get_export(id):
    '''
    This endpoint is used to get an in depth export for a specific system by its 'id'.
    :param id: id of the system.
    :return: JSON/Dictionary with joined information about all sessions and clicks.
    '''

    export = {'Results': [{
        'clicks': r.clicks,
        'start': r.start,
        'end': r.end,
        'interleave': r.interleave
    } for r in Feedback.query.join(Session, Session.id == Feedback.session_id).join(
        System, System.id == Session.system_ranking).filter(System.id == id).all()]}

    return jsonify(export)
