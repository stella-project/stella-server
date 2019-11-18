from flask import render_template, session, redirect, url_for, current_app
from . import main
from .forms import NameForm

from dev import visualise


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
    traffic = visualise.traffic()

    return render_template('dashboard.html', traffic=traffic)