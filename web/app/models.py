from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from datetime import datetime
import json


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property
    def serialize(self):
        return {'id': self.id,
                'username': self.username}

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=True)
    end = db.Column(db.DateTime, nullable=True)
    site_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    site_user = db.Column(db.String(64), index=True)
    system_ranking = db.Column(db.Integer, db.ForeignKey('systems.id'))
    system_recommendation = db.Column(db.Integer, db.ForeignKey('systems.id'))
    feedbacks = db.relationship('Feedback', backref='session', lazy='dynamic')

    @property
    def serialize(self):
        return {'sid': self.id,
                'site_id': self.site_id,
                'site_user': self.site_user,
                'system_ranking': self.system_ranking,
                'system_recommender': self.system_recommendation}

    def to_json(self):
        json_session = {
            'id': self.id,
            'start': self.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end': self.end.strftime('%Y-%m-%d %H:%M:%S'),
            'site_id': self.site_id,
            'site_user': self.site_user,
            'system_ranking': self.system_ranking,
            'system_recommendation': self.system_recommendation,
        }

        return json_session

    @staticmethod
    def from_json(json_session):
        # site_name = json_session.get('site_name', None)
        # site_id = User.query.filter_by(username=site_name).first().id
        site_user = json_session.get('site_user', None)
        start_raw = json_session.get('start', None)

        if start_raw is None:
            start = None
        else:
            start = datetime.strptime(start_raw, "%Y-%m-%d %H:%M:%S")

        end_raw = json_session.get('end', None)

        if end_raw is None:
            end = None
        else:
            end = datetime.strptime(end_raw, "%Y-%m-%d %H:%M:%S")

        system_ranking = json_session.get('system_ranking', None)
        system_ranking_id = System.query.filter_by(name=system_ranking).first().id
        system_recommendation = json_session.get('system_recommendation', None)
        system_recommendation_id = System.query.filter_by(name=system_recommendation).first().id

        session = Session(site_user=site_user,
                          start=start,
                          end=end,
                          system_ranking=system_ranking_id,
                          system_recommendation=system_recommendation_id)

        return session


class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedbacks.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    part_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(64), index=True)
    q = db.Column(db.String(64), index=True)
    q_date = db.Column(db.DateTime, nullable=True)
    q_time = db.Column(db.Integer)  # which datatype?
    num_found = db.Column(db.Integer)
    page = db.Column(db.Integer)
    rpp = db.Column(db.Integer)
    items = db.Column(db.JSON)

    @property
    def serialize(self):
        return {'ranking_id': self.id,
                'query': self.q,
                'query_date': self.q_date,
                'items': self.items}

    def update(self, data):
        session_id = data.get('session_id', None)
        system_id = data.get('system_id', None)
        feedback_id = data.get('feedback_id', None)
        site_id = data.get('site_id', None)
        part_id = data.get('part_id', None)
        type = data.get('type', None)
        q = data.get('q', None)
        q_time = data.get('q_time', None)
        q_date = data.get('q_date', None)
        num_found = data.get('num_found', None)
        rpp = data.get('rpp', None)
        page = data.get('page', None)
        items = data.get('items', None)

        if session_id is not None:
            self.session_id = session_id
        if system_id is not None:
            self.system_id = system_id
        if feedback_id is not None:
            self.feedback_id = feedback_id
        if site_id is not None:
            self.site_id = site_id
        if part_id is not None:
            self.part_id = part_id
        if type is not None:
            self.type = type
        if q is not None:
            self.q = q
        if q_time is not None:
            self.q_time = q_time
        if q_date is not None:
            self.q_date = datetime.strptime(q_date, "%Y-%m-%d %H:%M:%S")
        if num_found is not None:
            self.num_found = num_found
        if page is not None:
            self.page = page
        if rpp is not None:
            self.rpp = rpp
        if items is not None:
            self.items = items

    def to_json(self):
        result_session = {
            'session_id': self.session_id,
            'system_id': self.system_id,
            'feedback_id': self.feedback_id,
            'site_id': self.site_id,
            'part_id': self.part_id,
            'type': self.type,
            'q': self.q,
            'q_date': self.q_date.strftime('%Y-%m-%d %H:%M:%S'),
            'q_time': self.q_time,
            'num_found': self.num_found,
            'page': self.page,
            'rpp': self.rpp,
            'items': self.items
        }

        return result_session

    @staticmethod
    def from_json(json_result):
        q = json_result.get('q', None)
        q_date_raw = json_result.get('q_date', None)

        if q_date_raw is None:
            q_date = None
        else:
            q_date = datetime.strptime(q_date_raw, "%Y-%m-%d %H:%M:%S")

        q_time = json_result.get('q_time', None)
        num_found = json_result.get('num_found', None)
        page = json_result.get('page', None)
        rpp = json_result.get('rpp', None)
        items_raw = json_result.get('items', None)
        items = json.loads(items_raw)

        result = Result(q=q, q_date=q_date, q_time=q_time, num_found=num_found,
                        page=page, rpp=rpp, items=items)

        return result


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    interleave = db.Column(db.Boolean)
    results = db.relationship('Result', backref='feedback', lazy='dynamic')
    clicks = db.Column(db.JSON)

    @property
    def serialize(self):
        return {'feedback_id': self.id,
                'session_id': self.session_id,
                'site_id': self.site_id}

    def update(self, data):
        start = data.get('start', None)
        end = data.get('end', None)
        session_id = data.get('session_id', None)
        site_id = data.get('site_id', None)
        interleave = data.get('interleave', None)
        clicks = data.get('clicks', None)

        if start is not None:
            self.start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        if end is not None:
            self.end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
        if session_id is not None:
            self.session_id = session_id
        if site_id is not None:
            self.site_id = site_id
        if interleave is not None:
            self.interleave = bool(interleave)
        if clicks is not None:
            self.clicks = json.loads(clicks)

    @staticmethod
    def from_json(json_feedback):
        start_raw = json_feedback.get('start', None)
        end_raw = json_feedback.get('end', None)

        if start_raw is None:
            start = None
        else:
            start = datetime.strptime(start_raw, "%Y-%m-%d %H:%M:%S")

        if end_raw is None:
            end = None
        else:
            end = datetime.strptime(end_raw, "%Y-%m-%d %H:%M:%S")

        interleave = bool(json_feedback.get('interleave', False))
        clicks_raw = json_feedback.get('clicks')
        clicks = json.loads(clicks_raw)

        feedback = Feedback(
            start=start,
            end=end,
            interleave=interleave,
            clicks=clicks
        )

        return feedback

    def to_json(self):

        json_feedback = {
            'id': self.id,
            'start': self.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end': self.end.strftime('%Y-%m-%d %H:%M:%S'),
            'session_id': self.session_id,
            'site_id': self.site_id,
            'interleave': self.interleave,
            'clicks': self.clicks
        }

        return json_feedback


class System(db.Model):
    __tablename__ = 'systems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    participant_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type = db.Column(db.String(64), index=True)
    results = db.relationship('Result', backref='system', lazy='dynamic')

    @property
    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'participant_id': self.participant_id,
                'type': self.type}
