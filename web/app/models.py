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

    def to_json(self):
        json_session = {
            'id': self.id,
            'start': self.start,
            'end': self.end,
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
    q_time = db.Column(db.DateTime, nullable=True)  # which datatype?
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

    def to_json(self):
        result_session = {
            'session_id': self.session_id,
            'system_id': self.system_id,
            'feedback_id': self.feedback_id,
            'site_id': self.site_id,
            'part_id': self.part_id,
            'type': self.type,
            'q': self.q,
            'q_date': self.q_date,
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

        q_time_raw = json_result.get('q_time', None)

        if q_time_raw is None:
            q_time = None
        else:
            q_time = datetime.strptime(q_time_raw, "%Y-%m-%d %H:%M:%S")

        part_name = json_result.get('part_name', None)

        if part_name is None:
            part_id = None
        else:
            part_id = User.query.filter_by(username=part_name).first().id

        num_found = json_result.get('num_found', None)
        page = json_result.get('page', None)
        rpp = json_result.get('rpp', None)
        items_raw = json_result.get('items', None)
        items = json.loads(items_raw)

        result = Result(q=q, q_date=q_date, q_time=q_time, part_id=part_id,
                        num_found=num_found, page=page, rpp=rpp,
                        items=items)

        return result


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    interleave = db.Column(db.Boolean)
    # refers to experimental and baseline ranking
    results = db.relationship('Result', backref='feedback', lazy='dynamic')
    # shown result list with clicks (click dates)
    clicks = db.Column(db.JSON)

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
            'start': self.start,
            'end': self.end,
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

