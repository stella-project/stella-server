from flask import render_template, session, redirect, url_for, current_app, request, flash
from flask_login import current_user, login_user
from . import main
import json

from ..models import User, Session, System, Feedback

from ..dashboard import Dashboard
from .. auth.forms import LoginForm
import plotly.offline

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('index.html', form=form)


@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_anonymous:
        return render_template('index.html')
    else:
        if request.method == 'POST' and request.form.get('system') is not None and request.form.get('site') is not None:
            system_id = request.form.get('system')
            site_id = request.form.get('site')
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


@main.route('/systems', methods=['GET', 'POST'])
def systems():
    systems = System.query.filter().distinct().all()
    # systems = System.query.filter_by(participant_id=current_user.id).all()
    return render_template('systems.html', systems=systems)
