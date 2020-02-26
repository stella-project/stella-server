from flask import request, jsonify
from . import api
from .. import db
from ..models import Result, Feedback, Session, System


@api.route('/feedbacks/<int:id>/recommendations', methods=['POST'])
def post_recommendation(id):
    if request.method == 'POST':
        feedback = Feedback.query.get_or_404(id)
        site = feedback.site_id
        session = Session.query.get_or_404(feedback.session_id)
        json_recommendation = request.values
        recommendation = Result.from_json(json_recommendation)
        recommendation.site_id = site
        recommendation.session_id = session.id
        recommendation.feedback_id = id
        recommendation.system_id = session.system_ranking
        recommendation.participant_id = System.query.get_or_404(session.system_recommendation).participant_id
        recommendation.type = 'REC'
        db.session.add(recommendation)
        db.session.commit()

    return jsonify({'recommendation_id': recommendation.id})


@api.route('/recommendations/<int:id>', methods=['GET', 'PUT'])
def recommendation(id):
    if request.method == 'GET':
        recommendation = Session.query.get_or_404(id)
        return jsonify(recommendation.to_json())
    if request.method == 'PUT':
        json_recommendation = request.values
        recommendation = Result.query.get_or_404(id)
        recommendation.update(json_recommendation)
        db.session.commit()
        return 200


@api.route('/recommendations')
def get_recommendations():
    results = Result.query.filter_by(type='REC')
    return jsonify({"rids": [r.id for r in results]})
