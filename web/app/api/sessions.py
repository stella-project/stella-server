import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User


@api.route('/sessions/<int:id>')
def get_session(id):
    session = Session.query.get_or_404(id)
    return jsonify(session.to_json())


@api.route('/sessions/<int:id>/feedbacks')
def get_session_feedbacks(id):
    pass  # TODO: return feedback data of session with id

# @api.route('/sessions', methods=['POST'])
# def post_session():
#     if request.method == 'POST':
#
#         json_session = request.values
#         session = Session.from_json(json_session)
#
#         db.session.add(session)
#         db.session.commit()
#
#         return jsonify({'session_id': session.id})
