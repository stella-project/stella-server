from flask import request, jsonify
from . import api
from .. import db
from ..models import Result, Feedback, Session


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
        recommendation.type = 'REC'

        db.session.add(recommendation)
        db.session.commit()

    return jsonify({'recommendation_id': recommendation.id})


@api.route('/recommendations/<int:id>')
def get_recommendation(id):
    recommendation = Session.query.get_or_404(id)
    return jsonify(recommendation.to_json())