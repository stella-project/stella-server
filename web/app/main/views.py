import datetime
import json
import os
import re
import shutil

import plotly.offline
from flask import (
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required, login_user
from werkzeug.utils import secure_filename

from .. import db
from ..auth.forms import LoginForm
from ..dashboard import Dashboard
from ..models import Feedback, Result, Role, Session, System, User, load_user

# from ..core.bot import Bot
from ..util import (
    compress_file,
    create_precom_repo,
    create_stella_app_yaml,
    makeComposeFile,
    save_archive,
    save_file,
)
from . import main
from .forms import (
    ChangeEmailForm,
    ChangePassword,
    ChangeUsernameForm,
    SubmitRanking,
    SubmitSystem,
)


def get_systems(current_user):
    user_role = current_user.role_id

    if user_role == db.session.query(Role).filter_by(name="Admin").first().id:
        return db.session.query(System).filter_by().all()

    if user_role == db.session.query(Role).filter_by(name="Participant").first().id:
        return db.session.query(System).filter_by(participant_id=current_user.id).all()

    if user_role == db.session.query(Role).filter_by(name="Site").first().id:
        return db.session.query(System).filter_by(site=current_user.id).all()


@main.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid email or password.")
    return render_template("index.html", form=form)


@main.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if current_user.is_anonymous:
        return render_template("index.html")
    else:
        if request.method == "POST" and request.form.get("system") is not None:
            system_id = request.form.get("system")
            site_id = db.session.query(System).filter_by(id=system_id).first().site
            dashboard = Dashboard(current_user.id, system_id, site_id)
        else:
            dashboard = Dashboard(current_user.id)

        graphs = [
            dashboard.get_impressions(),
            dashboard.get_pie_chart(),
            dashboard.get_clicks(),
            dashboard.get_table(),
        ]

        return render_template(
            "dashboard.html",
            ids=["graph-{}".format(i) for i, _ in enumerate(graphs)],
            graphJSON=json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder),
            form=dashboard.dropdown(),
        )


@main.route("/systems", methods=["GET", "POST"])
@login_required
def systems():
    systems = get_systems(current_user)
    formContainer = SubmitSystem()
    formRanking = SubmitRanking()

    if formRanking.submit2.data and formRanking.validate():
        f = formRanking.upload.data
        filename = secure_filename(f.filename)
        systemname = formRanking.systemname.data.lower()
        subdir = None
        DELETE_UPLOAD = True  # move this to configs
        try:
            if filename.endswith(".txt"):
                subdir = save_file(f, systemname)
                tar_path = compress_file(subdir)

            if filename.endswith((".zip", ".xz", ".gz")):
                subdir = save_archive(f, systemname)
                tar_path = compress_file(subdir)

            type = (
                "REC"
                if formContainer.site_type.data == "GESIS (Dataset recommender)"
                else "RANK"
            )
            site = (
                db.session.query(User).filter_by(username="GESIS").first().id
                if type == "REC"
                else db.session.query(User).filter_by(username="LIVIVO").first().id
            )
            if current_app.config["AUTOMATOR_GH_KEY"]:
                gh_url = create_precom_repo(
                    token=current_app.config["AUTOMATOR_GH_KEY"],
                    repo_name=systemname,
                    run_tar_in=tar_path,
                    type=type,
                )
            else:
                gh_url = "http://github.com/stella-project"

            system = System(
                status="submitted",
                name=systemname,
                participant_id=current_user.id,
                type=type,
                submitted="TREC",
                url=gh_url,
                site=site,
                submission_date=datetime.datetime.now().date(),
            )
            db.session.add_all([system])
            db.session.commit()

            if subdir and DELETE_UPLOAD:
                shutil.rmtree(subdir)

            # automator.saveSplits(file, filename)

            flash("Run file submitted")
            return redirect(url_for("main.systems"))

        except Exception as e:
            if subdir and DELETE_UPLOAD:
                shutil.rmtree(subdir)
            flash(
                " ".join(
                    [
                        "Upload not possible. Use the following message for debugging:",
                        str(e),
                    ]
                ),
                "danger",
            )
            return redirect(url_for("main.systems"))

    if formContainer.submit.data and formContainer.validate():
        systemName = formContainer.systemname.data.lower()
        systemUrl = formContainer.GitHubUrl.data
        type = (
            "REC"
            if formContainer.site_type.data == "GESIS (Dataset recommender)"
            else "RANK"
        )
        site = (
            db.session.query(User).filter_by(username="GESIS").first().id
            if type == "REC"
            else db.session.query(User).filter_by(username="LIVIVO").first().id
        )
        system = System(
            status="submitted",
            name=systemName,
            participant_id=current_user.id,
            type=type,
            submitted="DOCKER",
            url=systemUrl,
            site=site,
            submission_date=datetime.datetime.now().date(),
        )
        db.session.add_all([system])
        db.session.commit()
        flash("Container submitted")
        return redirect(url_for("main.systems"))

    return render_template(
        "systems.html",
        systems=systems,
        formContainer=formContainer,
        formRanking=formRanking,
        current_user=current_user,
    )


@main.route("/administration")
@login_required
def administration():
    return render_template("administration.html", current_user=current_user)


@main.route("/uploads/<path:filename>", methods=["GET", "POST"])
def downloadTREC(filename):
    uploads = os.path.join(current_app.root_path, "../uploads")
    return send_from_directory(directory=uploads, filename=filename)


@main.route("/download/<system_id>")
@login_required
def download(system_id):
    if (
        current_user.id
        == db.session.query(System).filter_by(id=system_id).all()[0].participant_id
        or current_user.role_id == 1
        or (current_user.role_id == 3)
        and (
            db.session.query(System).filter_by(id=system_id).all()[0].site
            == current_user.id
        )
    ):

        system = db.session.query(System).filter_by(id=system_id).first()
        results = db.session.query(Result).filter_by(system_id=system_id).all()
        results = [
            result
            for result in results
            if "BASE" in [val["type"] for val in result.items.values()]
        ]
        feedbacks = [
            db.session.query(Feedback).filter(Feedback.id == r.feedback_id).first()
            for r in results
        ]
        queries = [
            db.session.query(Result).filter_by(feedback_id=f.id).first().q
            for f in feedbacks
        ]

        export = {
            system.name: [
                {
                    "clicks": f.clicks,
                    "start": f.start,
                    "end": f.end,
                    "interleave": f.interleave,
                    "query": q,
                }
                for f, q in zip(feedbacks, queries)
            ]
        }
        return jsonify(export)
    else:
        return render_template("404.html"), 404


@main.route("/downloadall")
@login_required
def downloadAll():
    if current_user.role_id == 1:  # Admin
        systems = db.session.query(System).all()
    if current_user.role_id == 2:  # Participant
        systems = (
            db.session.query(System).filter_by(participant_id=current_user.id).all()
        )
    if current_user.role_id == 3:  # Site
        systems = db.session.query(System).filter_by(site=current_user.id).all()

    export = {}
    for system in systems:
        if system.type == "REC":
            feedbacks = (
                db.session.query(Feedback)
                .join(Session, Session.id == Feedback.session_id)
                .join(System, System.id == Session.system_recommendation)
                .filter(System.id == system.id)
                .all()
            )
        else:
            feedbacks = (
                db.session.query(Feedback)
                .join(Session, Session.id == Feedback.session_id)
                .join(System, System.id == Session.system_ranking)
                .filter(System.id == system.id)
                .all()
            )

        queries = [
            db.session.query(Result).filter_by(feedback_id=f.id).first().q
            for f in feedbacks
        ]

        export[system.name] = [
            {
                "clicks": f.clicks,
                "start": f.start,
                "end": f.end,
                "interleave": f.interleave,
                "query": q,
            }
            for f, q in zip(feedbacks, queries)
        ]
    return jsonify(export)


"""
Multiple, prefilled forms in a single page workaround from: 
https://stackoverflow.com/questions/18290142/multiple-forms-in-a-single-page-using-flask-and-wtforms?answertab=votes#tab-top
"""


@main.route("/usersettings")
@login_required
def usersettings():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()
    return render_template(
        "userSettings.html",
        current_user=current_user,
        changeUsernameForm=changeUsernameForm,
        changePasswordForm=changePasswordForm,
        changeEmailForm=changeEmailForm,
    )


@main.route("/username", methods=["GET", "POST"])
@login_required
def username():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()

    if changeUsernameForm.validate_on_submit():
        user.username = changeUsernameForm.username.data
        db.session.commit()
        flash("Username changed.")

    return render_template(
        "userSettings.html",
        current_user=current_user,
        changeUsernameForm=changeUsernameForm,
        changePasswordForm=changePasswordForm,
        changeEmailForm=changeEmailForm,
    )


@main.route("/password", methods=["GET", "POST"])
@login_required
def password():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()

    if changePasswordForm.validate_on_submit():
        user.password = changePasswordForm.password.data
        db.session.commit()
        flash("Password changed.")

    return render_template(
        "userSettings.html",
        current_user=current_user,
        changeUsernameForm=changeUsernameForm,
        changePasswordForm=changePasswordForm,
        changeEmailForm=changeEmailForm,
    )


@main.route("/mail", methods=["GET", "POST"])
@login_required
def mail():
    user = load_user(current_user.id)
    changeUsernameForm = ChangeUsernameForm(obj=user)
    changeEmailForm = ChangeEmailForm(obj=user)
    changePasswordForm = ChangePassword()

    if changeEmailForm.validate_on_submit():
        user.email = changeEmailForm.email.data
        db.session.commit()
        flash("E-Mail changed.")

    return render_template(
        "userSettings.html",
        current_user=current_user,
        changeUsernameForm=changeUsernameForm,
        changePasswordForm=changePasswordForm,
        changeEmailForm=changeEmailForm,
    )


@main.route("/upload", methods=["POST"])
def upload_files():
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    if filename != "":
        file = uploaded_file.read().decode("utf-8").split("\n")[:-1]
        if all(
            [
                bool(re.match("^\d+\sQ0\s\w+\s\d*\s-?\d\.\d+\s\w+", line))
                for line in file
            ]
        ):
            print("RegEx validated")
            if all(
                [
                    (
                        True
                        if int(file[line].split(" ")[3])
                        == int(file[line - 1].split(" ")[3]) + 1
                        else False
                    )
                    for line in range(1, len(file))
                ]
            ):
                print("rank validated")
                if sorted([line.split(" ")[4] for line in file], reverse=True):
                    print("score validated")
                    uploaded_file.save(os.path.join("uploads", filename))
    return redirect(url_for("main.uploads"))


@main.route("/buildCompose")
def build():
    if makeComposeFile():
        flash('New "docker-compose.yaml" file created!')
    return render_template("index.html")


@main.route("/stella-app/update")
def update_stella_app():
    create_stella_app_yaml(type="all", token=current_app.config["AUTOMATOR_GH_KEY"])
    flash("Updated STELLA app!")
    return render_template("administration.html")


@main.route("/stella-app/update/gesis")
def update_stella_app_gesis():
    create_stella_app_yaml(type="rec", token=current_app.config["AUTOMATOR_GH_KEY"])
    flash("Updated STELLA app for GESIS!")
    return render_template("administration.html")


@main.route("/stella-app/update/livivo")
def update_stella_app_livivo():
    create_stella_app_yaml(type="rank", token=current_app.config["AUTOMATOR_GH_KEY"])
    flash("Updated STELLA app for LIVIVO!")
    return render_template("administration.html")


@main.route("/system/<int:id>/start")
def activate(id):
    flash("Started system.")
    user_role = current_user.role_id

    system = db.session.query(System).filter_by(id=id).first()
    system.status = "running"
    db.session.add_all([system])
    db.session.commit()

    return render_template(
        "systems.html",
        systems=get_systems(current_user),
        formContainer=SubmitSystem(),
        formRanking=SubmitRanking(),
        current_user=current_user,
    )


@main.route("/system/<int:id>/stop")
def deactivate(id):
    flash("Stopped system.")

    system = db.session.query(System).filter_by(id=id).first()
    system.status = "submitted"
    db.session.add_all([system])
    db.session.commit()

    return render_template(
        "systems.html",
        systems=get_systems(current_user),
        formContainer=SubmitSystem(),
        formRanking=SubmitRanking(),
        current_user=current_user,
    )


@main.route("/system/<int:id>/delete")
def delete(id):
    system = db.session.query(System).filter_by(id=id).first()

    if system.status == "submitted":
        db.session.delete(system)
        db.session.commit()
        flash("Deleted system")
    else:
        flash("Can only delete stopped systems", "danger")

    return redirect(url_for("main.systems"))
    # return render_template('systems.html',
    #                        systems=get_systems(current_user),
    #                        formContainer=SubmitSystem(),
    #                        formRanking=SubmitRanking(),
    #                        current_user=current_user)


@main.route("/statistics")
@login_required
def statistics():
    import pandas as pd

    systems = db.session.query(System).all()
    systems_sites = [(sys.id, sys.site) for sys in systems]
    data_dict = {}
    sessions_impressions_clicks = []
    idx_names = []
    for system_site in systems_sites:
        dash = Dashboard(
            current_user.id, system_id=system_site[0], site_id=system_site[1]
        )
        system_name = db.session.query(System).filter_by(id=dash.system_id).first().name
        data_dict[system_name] = [
            dash.win,
            dash.loss,
            dash.tie,
            dash.outcome,
            sum(dash.impressions.values()),
            sum(dash.impressions_results.values()),
            dash.num_clicks,
            dash.CTR,
        ]

        sessions_impressions_clicks.append(dash.impressions)
        sessions_impressions_clicks.append(dash.impressions_results)
        sessions_impressions_clicks.append(dash.clicks_exp)
        sessions_impressions_clicks.append(dash.clicks_base)
        idx_names.append("_".join([system_name, "sessions"]))
        idx_names.append("_".join([system_name, "impressions"]))
        idx_names.append("_".join([system_name, "clicks"]))
        idx_names.append("_".join([system_name, "clicks_base"]))

    pd.DataFrame(
        data=data_dict,
        index=[
            "win",
            "loss",
            "tie",
            "outcome",
            "sessions",
            "impressions",
            "clicks",
            "ctr",
        ],
    ).transpose().to_csv("overall_stats.csv")
    pd.DataFrame(
        data=sessions_impressions_clicks, index=idx_names, dtype=pd.Int64Dtype()
    ).to_csv("sessions_impressions.csv")

    return "CSV files dumped.", 200
