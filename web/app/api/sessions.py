import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User


@api.route('/sessions', methods=['POST'])
def sessions():
    if request.method == 'POST':
        site_name = request.values.get('site_name', None)
        site_id = User.query.filter_by(username=site_name).first().id
        site_user = request.values.get('site_user', None)
        start = request.values.get('start', None)
        end = request.values.get('start', None)
        system_ranking = request.values.get('system_ranking', None)
        system_ranking_id = System.query.filter_by(name=system_ranking).first().id
        system_recommendation = request.values.get('system_recommendation', None)
        system_recommendation_id = System.query.filter_by(name=system_recommendation).first().id

        session = Session(site_id=site_id,
                          site_user=site_user,
                          start=start,
                          end=end,
                          system_ranking=system_ranking_id,
                          system_recommendation=system_recommendation_id)

        db.session.add_all([
            session
        ])

        db.session.commit()
        return jsonify({'session_id': session.id})



# import json
# from flask import jsonify, request
# from . import api
# from .. import db
# from datetime import datetime
# from ..models import Session, Ranking, Entity
#
#
# @api.route('/sessions', methods=['GET', 'POST'])
# # @auth.login_required
# def sessions():
#     if request.method == 'POST':
#         data_dict = json.loads(request.data)
#         try:
#             assert data_dict.get('start') is not None and data_dict.get('end') is not None
#             start = datetime.strptime(data_dict.get('start'), '%Y-%m-%d %H:%M:%S')
#             end = datetime.strptime(data_dict.get('end'), '%Y-%m-%d %H:%M:%S')
#         except AssertionError as e:
#             start = datetime.now()
#             end = None
#
#         session = Session(start=start, end=end)
#         db.session.add(session)
#         db.session.commit()
#         return "<h1> Session added with start time: " + str(start)
#
#     if request.method == 'GET':
#         return jsonify([i.serialize for i in Session.query.all()])
#
#
# @api.route('/sessions/<int:id>', methods=['GET', 'PUT'])
# def session(id):
#     if request.method == 'GET':
#         session = Session.query.get(id)
#         return jsonify(session.serialize)
#
#
# @api.route('/sessions/<int:id>/rankings', methods=['GET', 'POST', 'PUT'])
# def session_rankings(id):
#     if request.method == 'GET':
#         session = Session.query.get(id)
#         return jsonify({'ranking ids': session.get_rankings()})
#
#     if request.method == 'POST':
#         data_dict = json.loads(request.data)
#         query_text = data_dict.get('query')
#         entities_dict = data_dict.get('entities')
#         ranking = Ranking(textquery=query_text)
#         ranking.session_id = id
#         db.session.add(ranking)
#
#         for ent_id in entities_dict:
#             ent = Entity.query.get(ent_id)
#             if ent is None:
#                 ent = Entity(id=ent_id)
#             # ent.rankings.append(ranking.id)
#             ranking.entities.append(ent)
#             db.session.add(ent)
#
#         db.session.commit()
#
#         return 'Added ranking'
