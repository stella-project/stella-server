from flask import render_template, session, redirect, url_for, current_app, request
from flask_login import current_user
from . import main
import json

from dev import visualise

from ..models import User, Session, System, Feedback

from ..dashboard import Dashboard
import plotly.offline


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_anonymous:
        return render_template('index.html')
    else:
        if request.method == 'POST' and request.form.get('system') is not None and request.form.get('site') is not None:
            system_id = request.form.get('system')
            site_id =  request.form.get('site')
            dashboard = Dashboard(current_user.id, system_id, site_id)
        else:
            dashboard = Dashboard(current_user.id)

        graphs = [dashboard.get_impressions(),
                  dashboard.get_pie_chart(),
                  dashboard.get_clicks(),
                  dashboard.get_table()]

        return render_template('dashboard.html',
                               ids=['graph-{}'.format(i) for i, _ in enumerate(graphs)],
                               graphJSON=json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder),
                               form=dashboard.dropdown())
