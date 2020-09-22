from flask import render_template, session, redirect, url_for, current_app, request, flash
from flask_login import current_user, login_user, login_required
from werkzeug.utils import secure_filename

import os
import re

from . import main
import json

from .forms import SubmitSystem

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
@login_required
def systems():
    systems = System.query.filter().distinct().all()
    # systems = System.query.filter_by(participant_id=current_user.id).all()
    form = SubmitSystem()
    return render_template('systems.html', systems=systems, form=form, current_user=current_user)


@main.route('/usersettings', methods=['GET', 'POST'])
@login_required
def usersettings():
    # form = RegistrationForm()

    return render_template('userSettings.html', current_user=current_user)


@main.route('/upload', methods=['POST'])
def upload_files():

    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file = uploaded_file.read().decode("utf-8").split('\n')[:-1]
        if all([bool(re.match('^\d+\sQ0\s\w+\s\d*\s-?\d\.\d+\s\w+', line)) for line in file]):
            print('RegEx validated')
            if all([True if int(file[line].split(' ')[3]) == int(file[line-1].split(' ')[3])+1 else False for line in range(1, len(file))]):
                print('rank validated')
                if sorted([line.split(' ')[4] for line in file], reverse=True):
                    print('score validated')
                    uploaded_file.save(os.path.join('uploads', filename))
    return redirect(url_for('main.uploads'))


@main.route('/upload')
@login_required
def uploads():
    return render_template('upload.html', current_user=current_user)
