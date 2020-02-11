from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


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


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    site = db.Column(db.Integer, db.ForeignKey('users.id'))
    interleave = db.Column(db.Boolean)
    # refers to experimental and baseline ranking
    results = db.relationship('Result', backref='feedback', lazy='dynamic')
    # shown result list with clicks (click dates)
    clicks = db.Column(db.JSON)


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

