import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User, Feedback


@api.route('/sessions/<int:id>')
def get_session(id):
    session = Session.query.get_or_404(id)
    return jsonify(session.to_json())


@api.route('/sessions/<int:id>/feedbacks')
def get_session_feedbacks(id):
    feedbacks = Feedback.query.filter_by(session_id=id)
    return jsonify([f.to_json() for f in feedbacks])
