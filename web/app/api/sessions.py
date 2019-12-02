from flask import jsonify
from . import api
from .authentication import auth


@api.route('/sessions/', methods=['GET', 'POST'])
def get_sessions():
    return 'TODO: return all sessions'


@api.route('/sessions/<int:id>', methods=['GET', 'PUT'])
@auth.login_required
def get_session(id):
    # TODO: implement Session Role with multiple rankings

    # toy data
    session = {
                "sid": "ssoar-s33127",
                "qid": "ssoar-q588",
                "time": "2017-08-02T00:23:53.348+0200",
                "ranking": [
                            {"docid": "ssoar-d23667", "clicked": True, "team": "site"},
                            {"docid": "ssoar-d23664", "clicked": False, "team": "participant"},
                            {"docid": "ssoar-d7941", "clicked": False, "team": "site"},
                            {"docid": "ssoar-d22395", "clicked": False, "team": "participant"},
                            {"docid": "ssoar-d23669", "clicked": False, "team": "site"},
                           ]
                }

    return jsonify(session)
