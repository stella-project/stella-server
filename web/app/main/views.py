from flask import render_template, session, redirect, url_for, current_app
from flask_login import current_user
from . import main
from .forms import NameForm

from dev import visualise

from ..models import User, Session, System, Feedback

import json


@main.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


@main.route('/dashboard')
def dashboard():
    # test = visualise.makeJson()
    # ids = test[0]
    # graphJSON = test[1]

    if current_user.is_anonymous:
        return render_template('index.html')
    else:

        # get first ranker of participant
        ranker = System.query.filter_by(participant_id=current_user.id, type='RANK').first()
        # get first site at which ranker is deployed
        site = Session.query.with_entities(Session.site_id).distinct().filter_by(system_ranking=ranker.id).first()
        # get all session id with ranker at site
        sessions = Session.query.filter_by(system_ranking=ranker.id, site_id=site[0]).all()
        sids = [s.id for s in sessions]
        feedbacks = Feedback.query.filter(Feedback.session_id.in_(sids)).all()

        impressions = {}
        for s in sessions:
            date = s.start.strftime('%Y-%m-%d')
            if impressions.get(date) is None:
                impressions.update({date: 1})
            else:
                impressions[date] = impressions[date] + 1

        clicks_base = {}
        clicks_exp = {}

        win = 0
        loss = 0
        tie = 0

        for f in feedbacks:
            clicks = f.clicks
            cnt_base = 0
            cnt_exp = 0
            for c in clicks.values():
                if c.get('clicked') and c.get('system') == 'EXP':
                    date = c.get('date')[:10]
                    if clicks_exp.get(date) is None:
                        clicks_exp.update({date: 1})
                    else:
                        clicks_exp[date] = clicks_exp[date] + 1
                    cnt_exp += 1
                if c.get('clicked') and c.get('system') == 'BASE':
                    date = c.get('date')[:10]
                    if clicks_base.get(date) is None:
                        clicks_base.update({date: 1})
                    else:
                        clicks_base[date] = clicks_base[date] + 1
                    cnt_base += 1
                if cnt_exp > cnt_base:
                    win += 1
                if cnt_exp < cnt_base:
                    loss += 1
                if cnt_exp == cnt_base:
                    tie += 1

            outcome = win / (win + tie)
            ctr = len(clicks_exp) / len(impressions)

            test = visualise.makeJson()
            ids = test[0]
            graphJSON = json.loads(test[1])

            # bar plot - impressions
            graphJSON[0]['data'][0]['x'] = list(impressions.keys())
            graphJSON[0]['data'][0]['y'] = list(impressions.values())

            # bar plot - clicks (exp vs. base)
            graphJSON[2]['data'][0]['x'] = list(clicks_base.keys())
            graphJSON[2]['data'][0]['y'] = list(clicks_base.values())

            graphJSON[2]['data'][1]['x'] = list(clicks_exp.keys())
            graphJSON[2]['data'][1]['y'] = list(clicks_exp.values())

            # pie chart
            graphJSON[1]['data'][0]['values'] = [win, loss, tie]

            # table
            graphJSON[3]['data'][0]['cells']['values'][1] = [win, loss, tie, outcome, ctr]


        return render_template('dashboard.html', ids=ids, graphJSON=json.dumps(graphJSON))
