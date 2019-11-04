from flask import jsonify
from . import api


@api.route('/site/feedback/')
def feedback():

    result = {
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

    return jsonify(result)

