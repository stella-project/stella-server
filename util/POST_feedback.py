import requests as req
import json

'''
rank_exp_a
rank_exp_b
rec_exp_a
rec_exp_b
rank_base_a
rank_base_b
rec_base_a
rec_base_b
'''

HOST = 'http://0.0.0.0:8000'


def main():

    click_dict = {
        "doc1": None,
        "doc11": '2019-11-04T00:08:15',
        "doc2": None,
        "doc12": '2019-11-04T00:06:23',
        "doc3": None,
        "doc13": None,
        "doc4": None,
        "doc14": None,
        "doc5": None,
        "doc15": None,
    }

    # post new session
    payload = {
        'start': '2019-11-04 00:06:23',
        'end': '2019-11-04 00:10:38',
        'session_id': 'rank_exp_a',
        'site': 'Site A',
        'interleave': True,
        'clicks': json.dumps(click_dict)
               }

    r = req.post(HOST + '/stella/api/v1/feedbacks', data=payload)
    r_text = json.loads(r.text)
    feedback_id = r_text.get('feedback_id')
    print(feedback_id)

    '''
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    site = db.Column(db.Integer, db.ForeignKey('users.id'))
    interleave = db.Column(db.Boolean)
    # refers to experimental and baseline ranking
    results = db.relationship('Result', backref='feedback', lazy='dynamic')
    # shown result list with clicks (click dates)
    clicks = db.Column(db.JSON)
    '''


if __name__ == '__main__':
    main()
