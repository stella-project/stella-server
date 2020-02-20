from flask import jsonify, request
from . import api
from .. import db
from ..models import Session, System, User, Feedback


@api.route('/sessions/<int:id>/feedbacks', methods=['POST'])
def post_feedback(id):
    if request.method == 'POST':

        session = Session.query.get_or_404(id)
        json_feedback = request.values
        feedback = Feedback.from_json(json_feedback)
        feedback.session_id = id
        site = session.site_id
        feedback.site_id = site

        db.session.add(feedback)
        db.session.commit()

    return jsonify({'feedback_id': feedback.id})


@api.route('/feedbacks')
def get_feedbacks():
    feedbacks = Feedback.query.all()
    return jsonify([feedback.serialize for feedback in feedbacks])


@api.route('/feedbacks/<int:id>')
def get_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    return jsonify(feedback.to_json())


@api.route('/feedbacks/<int:id>', methods=['PUT'])
def edit_feedback(id):
    json_feedback = request.values
    feedback = Feedback.query.get_or_404(id)
    feedback.update(json_feedback)
    db.session.commit()


