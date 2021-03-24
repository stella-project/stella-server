from flask import render_template, session, redirect, url_for, current_app, request, flash, jsonify, send_from_directory
from flask_login import current_user, login_user, login_required
from werkzeug.utils import secure_filename
from .. import db
import os
import re
import datetime
from . import main
import json
from .forms import SubmitSystem, ChangeUsernameForm, ChangePassword, ChangeEmailForm, SubmitRanking
from ..models import User, Session, System, Result, Feedback, Role, load_user
from ..dashboard import Dashboard
from ..auth.forms import LoginForm
import plotly.offline
from ..core.bot import Bot
from ..util import makeComposeFile
import shutil


def get_systems(current_user):
    user_role = current_user.role_id

    if user_role == Role.query.filter_by(name='Admin').first().id:
        return System.query.filter_by().all()

    if user_role == Role.query.filter_by(name='Participant').first().id:
        return System.query.filter_by(participant_id=current_user.id).all()

    if user_role == Role.query.filter_by(name='Site').first().id:
        return System.query.filter_by(site=current_user.id).all()


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
        if request.method == 'POST' and request.form.get('system') is not None:
            system_id = request.form.get('system')
            site_id = System.query.filter_by(id=system_id).first().site
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
    systems = get_systems(current_user)
    formContainer = SubmitSystem()
    formRanking = SubmitRanking()
    automator = Bot()

    if formRanking.submit2.data and formRanking.validate():
        f = formRanking.upload.data
        filename = secure_filename(f.filename)
        systemname = formRanking.systemname.data
        subdir = None
        DELETE_UPLOAD = True  # move this to configs
        try:
            if filename.endswith('.txt'):
                subdir = automator.saveFile(f, systemname)
                tar_path = automator.compressFile(subdir)

            if filename.endswith(('.zip', '.xz', '.gz')):
                subdir = automator.saveArchive(f, systemname)
                tar_path = automator.compressFile(subdir)

            type = 'REC' if formContainer.site_type.data == 'GESIS (Dataset recommender)' else 'RANK'
            site = User.query.filter_by(username='GESIS').first().id if type == 'REC' else User.query.filter_by(username='LIVIVO').first().id
            if current_app.config['AUTOMATOR_GH_KEY']:
                gh_url = automator.create_precom_repo(token=current_app.config['AUTOMATOR_GH_KEY'],
                                                      repo_name=systemname,
                                                      run_tar_in=tar_path,
                                                      type=type)
            else:
                gh_url = 'http://github.com/stella-project'

            system = System(status='submitted', name=systemname,
                            participant_id=current_user.id, type=type,
                            submitted='TREC', url=gh_url, site=site, submission_date=datetime.datetime.now().date())
            db.session.add_all([system])
            db.session.commit()

            if subdir and DELETE_UPLOAD:
                shutil.rmtree(subdir)

            # automator.saveSplits(file, filename)

            flash('Run file submitted')
            return redirect(url_for('main.systems'))

        except Exception as e:
            if subdir and DELETE_UPLOAD:
                shutil.rmtree(subdir)
            flash(' '.join(['Upload not possible. Use the following message for debugging:', str(e)]), 'danger')
            return redirect(url_for('main.systems'))

    if formContainer.submit.data and formContainer.validate():
        systemName = formContainer.systemname.data
        systemUrl = formContainer.GitHubUrl.data
        type = 'REC' if formContainer.site_type.data == 'GESIS (Dataset recommender)' else 'RANK'
        site = User.query.filter_by(username='GESIS').first().id if type == 'REC' else User.query.filter_by(username='LIVIVO').first().id
        system = System(status='submitted', name=systemName, participant_id=current_user.id, type=type,
                        submitted='DOCKER', url=systemUrl, site=site, submission_date=datetime.datetime.now().date())
        db.session.add_all([system])
        db.session.commit()
        flash('Container submitted')
        return redirect(url_for('main.systems'))

    return render_template('systems.html', systems=systems, formContainer=formContainer, formRanking=formRanking,
                           current_user=current_user)


@main.route('/administration')
@login_required
def administration():
    return render_template('administration.html', current_user=current_user)


@main.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def downloadTREC(filename):
    uploads = os.path.join(current_app.root_path, '../uploads')
    return send_from_directory(directory=uploads, filename=filename)


@main.route('/download/<system_id>')
@login_required
def download(system_id):
    if current_user.id == System.query.filter_by(id=system_id).all()[0].participant_id or current_user.role_id == 1 or (current_user.role_id == 3) and (System.query.filter_by(id=system_id).all()[0].site == current_user.id):

        system = System.query.filter_by(id=system_id).first()
        results = Result.query.filter_by(system_id=system_id).all()
        feedbacks = [Feedback.query.filter(Feedback.id == r.feedback_id).first() for r in results]
        queries = [Result.query.filter_by(feedback_id=f.id).first().q for f in feedbacks]

        export = {system.name: [{
            'clicks': f.clicks,
            'start': f.start,
            'end': f.end,
            'interleave': f.interleave,
            'query': q
        } for f, q in zip(feedbacks, queries)]}
        return jsonify(export)
    else:
        return render_template('404.html'), 404


@main.route('/downloadall')
@login_required
def downloadAll():
    if current_user.role_id == 1: # Admin
        systems = System.query.all()
    if current_user.role_id == 2:  # Participant
        systems = System.query.filter_by(participant_id=current_user.id).all()
    if current_user.role_id == 3:  # Site
        systems = System.query.filter_by(site=current_user.id).all()

    export = {}
    for system in systems:
        if system.type == 'REC':
            feedbacks = Feedback.query.join(Session, Session.id == Feedback.session_id).join(
                System, System.id == Session.system_recommendation).filter(System.id == system.id).all()
        else:
            feedbacks = Feedback.query.join(Session, Session.id == Feedback.session_id).join(
                System, System.id == Session.system_ranking).filter(System.id == system.id).all()

        queries = []
        for f in feedbacks:
            results = Result.query.filter_by(feedback_id=f.id)
            if results.first():
                queries.append(results.first().q)

        export[system.name] = [{
            'clicks': f.clicks,
            'start': f.start,
            'end': f.end,
            'interleave': f.interleave,
            'query': q
        } for f, q in zip(feedbacks, queries)]
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
            if all([True if int(file[line].split(' ')[3]) == int(file[line - 1].split(' ')[3]) + 1 else False for line
                    in range(1, len(file))]):
                print('rank validated')
                if sorted([line.split(' ')[4] for line in file], reverse=True):
                    print('score validated')
                    uploaded_file.save(os.path.join('uploads', filename))
    return redirect(url_for('main.uploads'))


# @main.route('/upload')
# @login_required
# def uploads():
#     return render_template('upload.html', current_user=current_user)


@main.route('/buildCompose')
def build():
    if makeComposeFile():
        flash('New "docker-compose.yaml" file created!')
    return render_template('index.html')


@main.route('/stella-app/update')
def update_stella_app():
    Bot.update_stella_app(type='all', token=current_app.config['AUTOMATOR_GH_KEY'])
    flash('Updated STELLA app!')
    return render_template('administration.html')


@main.route('/stella-app/update/gesis')
def update_stella_app_gesis():
    Bot.update_stella_app(type='rec', token=current_app.config['AUTOMATOR_GH_KEY'])
    flash('Updated STELLA app for GESIS!')
    return render_template('administration.html')


@main.route('/stella-app/update/livivo')
def update_stella_app_livivo():
    Bot.update_stella_app(type='rank', token=current_app.config['AUTOMATOR_GH_KEY'])
    flash('Updated STELLA app for LIVIVO!')
    return render_template('administration.html')


@main.route('/system/<int:id>/start')
def activate(id):
    flash('Started system.')
    user_role = current_user.role_id

    system = System.query.filter_by(id=id).first()
    system.status = 'running'
    db.session.add_all([system])
    db.session.commit()

    return render_template('systems.html',
                           systems=get_systems(current_user),
                           formContainer=SubmitSystem(),
                           formRanking=SubmitRanking(),
                           current_user=current_user)


@main.route('/system/<int:id>/stop')
def deactivate(id):
    flash('Stopped system.')

    system = System.query.filter_by(id=id).first()
    system.status = 'submitted'
    db.session.add_all([system])
    db.session.commit()

    return render_template('systems.html',
                           systems=get_systems(current_user),
                           formContainer=SubmitSystem(),
                           formRanking=SubmitRanking(),
                           current_user=current_user)


@main.route('/system/<int:id>/delete')
def delete(id):
    system = System.query.filter_by(id=id).first()

    if system.status == 'submitted':
        db.session.delete(system)
        db.session.commit()
        flash('Deleted system')
    else:
        flash('Can only delete stopped systems', 'danger')

    return redirect(url_for('main.systems'))
    # return render_template('systems.html',
    #                        systems=get_systems(current_user),
    #                        formContainer=SubmitSystem(),
    #                        formRanking=SubmitRanking(),
    #                        current_user=current_user)
