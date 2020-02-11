import json
from flask import jsonify, request
from . import api
from .. import db
from datetime import datetime
from ..models import Session, System, User, Feedback

@api.route('/feedbacks', methods=['POST'])
def feedbacks():
    if request.method == 'POST':
        payload = request.values

        start_raw = payload.get('start', None)
        end_raw = payload.get('end', None)

        if start_raw is None:
            start = None
        else:
            start = datetime.strptime(start_raw, "%Y-%m-%d %H:%M:%S")

        if end_raw is None:
            end = None
        else:
            end = datetime.strptime(end_raw, "%Y-%m-%d %H:%M:%S")

        session_id = payload.get('session_id', None)
        site = payload.get('site', None)
        site_id = User.query.filter_by(username=site).first().id
        interleave = bool(payload.get('interleave', False))
        clicks_raw = payload.get('clicks')
        clicks = json.loads(clicks_raw)

        feedback = Feedback(
            start=start,
            end=end,
            session_id=session_id,
            site_id=site_id,
            interleave=interleave,
            clicks=clicks
        )

        db.session.add(feedback)
        db.session.commit()

        # 'start': '2019-11-04T00:06:23',
        # 'end': '2019-11-04T00:10:38',
        # 'session_id': 'rank_exp_a',
        # 'site': 'Site A',
        # 'interleave': True,
        # 'clicks': click_dict
    return jsonify({'feedback_id': feedback.id})
