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


# class Session(db.Model):
#     __tablename__ = 'sessions'
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.String(64), unique=False)
#     length = db.Column(db.Float, unique=False)
#
#
# class Results(db.Model):
#     __tablename__ = 'results'
#     id = db.Column(db.Integer, primary_key=True)
#     ranker_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
#
#
# class System(db.Model):
#     __tablename__ = 'systems'
#     id = db.Column(db.Integer, primary_key=True)
#
#
# class Entity(db.Model):
#     __tablename__ = 'entities'
#     id = db.Column(db.Integer, primary_key=True)
#
#
# class TextQuery(db.Model):
#     __tablename__ = 'textqueries'
#     id = db.Column(db.Integer, primary_key=True)
#
#
# class SiteUser(db.Model):
#     __tablename__ = 'siteusers'
#     id = db.Column(db.Integer, primary_key=True)

