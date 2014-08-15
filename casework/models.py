import datetime

from flask.ext.security import UserMixin, RoleMixin

from casework import db
from casework.validators import convert_to_bst


roles_users = db.Table('roles_users',
                       db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return str({
            'id': str(self.id),
            'email': str(self.email)
        })


class Casework(db.Model):
    __tablename__ = 'casework'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column(db.String(64), nullable=False)
    submitted_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    application_type = db.Column(db.String(50), nullable=False)

    @property
    def with_bst_time(self):
        return convert_to_bst(self.submitted_at)


class Check(db.Model):
    __tablename__ = 'checks'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column(db.String(64), nullable=False)
    submitted_at = db.Column(db.DateTime(), default=datetime.datetime.now)
    application_type = db.Column(db.String(50), nullable=False)

    @property
    def with_bst_time(self):
        return convert_to_bst(self.submitted_at)