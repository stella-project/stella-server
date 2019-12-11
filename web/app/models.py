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
    start = db.Column(db.DateTime, unique=False)
    end = db.Column(db.DateTime, unique=False)
    rankings = db.relationship('Ranking', backref='session', lazy='dynamic')

    @property
    def serialize(self):
        return {'id': self.id,
                'start': self.start,
                'end': self.end,
                'rankings': self.get_rankings()
                }

    def get_rankings(self):
        return [r.id for r in self.rankings]


entities = db.Table('tags',
    db.Column('entity_id', db.Integer, db.ForeignKey('entities.id'), primary_key=True),
    db.Column('ranking_id', db.Integer, db.ForeignKey('rankings.id'), primary_key=True)
)


class Ranking(db.Model):
    __tablename__ = 'rankings'
    id = db.Column(db.Integer, primary_key=True)
    textquery = db.Column(db.String(64), unique=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    entities = db.relationship('Entity', secondary=entities, lazy='subquery',
                    backref=db.backref('rankings', lazy=True))

    @property
    def serialize(self):
        return {'ranking_id': self.id,
                'textquery': self.textquery,
                'session_id': self.session_id,
                'entities': self.get_entities()}

    def get_entities(self):
        return [e.id for e in self.entities]


class Entity(db.Model):
    __tablename__ = 'entities'
    id = db.Column(db.String(64), primary_key=True)
    author = db.Column(db.String(64), unique=False)
    content = db.Column(db.String(64), unique=False)
