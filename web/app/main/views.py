from flask import render_template, session, redirect, url_for, current_app, request, flash, jsonify, send_from_directory
from flask_login import current_user, login_user, login_required
from werkzeug.utils import secure_filename
from .. import db

import os
import re

from . import main
import json

from .forms import SubmitSystem, ChangeUsernameForm, ChangePassword, ChangeEmailForm, SubmitRanking

from ..models import User, Session, System, Feedback, load_user, Result

from ..dashboard import Dashboard
from .. auth.forms import LoginForm
import plotly.offline

from ..core.validator import Validator

from ..util import makeComposeFile

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
    systems = System.query.filter_by(participant_id=current_user.id).all()

    formContainer = SubmitSystem()
    formRanking = SubmitRanking()

    if formRanking.submit2.data and formRanking.validate():
        f = formRanking.upload.data
        filename = secure_filename(f.filename)
        file = f.read().decode("utf-8")

        if Validator().validate(file):

            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            with open(os.path.join('uploads', filename), 'w') as outfile:
                outfile.write(file)

            systemname = formRanking.systemname.data
            system = System(status='submitted', name=systemname, participant_id=current_user.id, type='RANK',
                            submitted='TREC', url=filename)
            db.session.add_all([system])
            db.session.commit()

            flash('Ranking submitted')
            return redirect(url_for('main.systems'))
        else:
            flash('Validation failed')
            return redirect(url_for('main.systems'))

    if formContainer.submit.data and formContainer.validate():
        systemName = formContainer.systemname.data
        systemUrl = formContainer.GitHubUrl.data
        system = System(status='submitted', name=systemName, participant_id=current_user.id, type='RANK',
                          submitted='DOCKER', url=systemUrl)
        db.session.add_all([system])
        db.session.commit()
        flash('Container submitted')
        return redirect(url_for('main.systems'))

    return render_template('systems.html', systems=systems, formContainer=formContainer, formRanking=formRanking, current_user=current_user)


@main.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def downloadTREC(filename):
    uploads = os.path.join(current_app.root_path, '../uploads')
    return send_from_directory(directory=uploads, filename=filename)


@main.route('/download/<system>')
@login_required
def download(system):
    if current_user.id == System.query.filter_by(id=system).all()[0].participant_id:
        export = {'Results' : [r.serialize for r in Result.query.filter_by(system_id=system).all()]}
        return jsonify(export)
    else:
        return render_template('404.html'), 404


@main.route('/downloadall')
@login_required
def downloadAll():
    systems = System.query.filter_by(participant_id=current_user.id).all()
    export = {}
    for system in systems:
        export[system.name] = [r.serialize for r in Result.query.filter_by(system_id=system.id).all()]
    return jsonify(export)


"""
Multiple, prefilled forms in a single page workaround from: 
https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms?answertab=votes#tab-top
"""
@main.route('/usersettings')
@login_required
def usersettings():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()
    return render_template('userSettings.html', current_user=current_user, changeUsernameForm=changeUsernameForm,
                           changePasswordForm=changePasswordForm, changeEmailForm=changeEmailForm)


@main.route('/username', methods=['GET', 'POST'])
@login_required
def username():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()

    if changeUsernameForm.validate_on_submit():
        user.username = changeUsernameForm.username.data
        db.session.commit()
        flash('Username changed.')

    return render_template('userSettings.html', current_user=current_user, changeUsernameForm=changeUsernameForm,
                           changePasswordForm=changePasswordForm, changeEmailForm=changeEmailForm)


@main.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()

    if changePasswordForm.validate_on_submit():
        user.password = changePasswordForm.password.data
        db.session.commit()
        flash('Password changed.')

    return render_template('userSettings.html', current_user=current_user, changeUsernameForm=changeUsernameForm,
                           changePasswordForm=changePasswordForm, changeEmailForm=changeEmailForm)


@main.route('/mail', methods=['GET', 'POST'])
@login_required
def mail():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()

    if changeEmailForm.validate_on_submit():
        user.email = changeEmailForm.email.data
        db.session.commit()
        flash('E-Mail changed.')

    return render_template('userSettings.html', current_user=current_user, changeUsernameForm=changeUsernameForm,
                           changePasswordForm=changePasswordForm, changeEmailForm=changeEmailForm)


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


@main.route('/buildCompose')
def build():
    if makeComposeFile():
        flash('New "docker-compose.yaml" file created!')
    return render_template('index.html')