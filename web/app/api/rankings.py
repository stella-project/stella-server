from flask import g, request, jsonify
from . import api
from .. import db
from ..models import Result, Feedback, Session, System


@api.route('/feedbacks/<int:id>/rankings', methods=['POST'])
def post_ranking(id):
    '''
    Use this endpoint to add a ranking for a specific feedback and the corresponding session.

    @param id: Identifier of the feedback.
    @return: JSON/Dictionary with id of the ranking.
    '''

    if g.current_user.role_id != 3:  # Site
        return jsonify({'message': 'Unauthorized'}), 401

    elif request.method == 'POST':
        feedback = Feedback.query.get_or_404(id)
        site = feedback.site_id
        session = Session.query.get_or_404(feedback.session_id)
        json_ranking = request.values
        ranking = Result.from_json(json_ranking)
        ranking.site_id = site
        ranking.session_id = session.id
        ranking.feedback_id = id
        ranking.system_id = json_ranking.get('system_id') if json_ranking.get('system_id') else session.system_ranking
        ranking.participant_id = System.query.get_or_404(session.system_ranking).participant_id
        ranking.type = 'RANK'
        db.session.add(ranking)
        db.session.commit()

    return jsonify({'ranking_id': ranking.id})


@api.route('/rankings/<int:id>', methods=['GET', 'PUT'])
def ranking(id):
    '''
    Use this endpoint either to get information about a specific ranking (GET) or to update the information (PUT).

    @param id: Identifier of the ranking.
    @return: GET - JSON/Dictionary with ranking and corresponding items.
             PUT - Update ranking with specified identifier 'id'.
    '''
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
    '''

    @return: JSON/Dictionary with identifiers of all rankings in database.
    '''
    results = Result.query.filter_by(type='RANK')
    return jsonify({"rids": [r.id for r in results]})

