from flask import request, jsonify
from . import api
from .. import db
from ..models import Result, Feedback, Session, System


@api.route('/feedbacks/<int:id>/rankings', methods=['POST'])
def post_ranking(id):
    if request.method == 'POST':

        feedback = Feedback.query.get_or_404(id)
        site = feedback.site_id
        session = Session.query.get_or_404(feedback.session_id)

        json_ranking = request.values
        ranking = Result.from_json(json_ranking)
        ranking.site_id = site
        ranking.session_id = session.id
        ranking.feedback_id = id
        ranking.system_id = session.system_ranking
        ranking.part_id = System.query.get_or_404(session.system_ranking).participant_id
        ranking.type = 'RANK'

        db.session.add(ranking)
        db.session.commit()

    return jsonify({'ranking_id': ranking.id})


@api.route('/rankings/<int:id>', methods=['GET', 'PUT'])
def ranking(id):
    if request.method == 'GET':
        ranking = Result.query.get_or_404(id)
        return jsonify(ranking.to_json())
    if request.method == 'PUT':
        json_ranking = request.values
        ranking = Result.query.get_or_404(id)
        ranking.update(json_ranking)
        db.session.commit()
        return 200


@api.route('/rankings')
def get_rankings():
    results = Result.query.filter_by(type='RANK')
    return jsonify({"rids": [r.id for r in results]})

