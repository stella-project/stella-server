from flask import request, jsonify
from . import api
from ..models import Ranking


@api.route('/rankings')
def rankings():
    return jsonify([i.serialize for i in Ranking.query.all()])


@api.route('/rankings/<int:id>', methods=['GET'])
def ranking(id):
    if request.method == 'GET':
        ranking = Ranking.query.get(id)
        return jsonify(ranking.serialize)