from flask import request, jsonify
from . import api
from .. import db
from ..models import Result, Feedback, Session


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
        ranking.type = 'RANK'

        db.session.add(ranking)
        db.session.commit()

    return jsonify({'ranking_id': ranking.id})


@api.route('/rankings/<int:id>')
def get_ranking(id):
    ranking = Session.query.get_or_404(id)
    return jsonify(ranking.to_json())


@api.route('rankings/<int:id>', methods=['PUT'])
def edit_ranking(id):
    pass  # TODO: update ranking with id


@api.route('/rankings')
def get_rankings():
    pass  # TODO: return all rankings. does this make sense?