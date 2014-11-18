#!/usr/bin/python
import os

from flask_security.utils import encrypt_password

from flask.ext.script import Manager
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand
from application import app
from application import db
from application import user_datastore

app.config.from_object(os.environ['SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.option('--email', dest='email')
@manager.option('--password', dest='password')
@manager.option('--active', dest='active')
def create_user(email, password, active):
    if not user_datastore.find_user(email=email):
        user_datastore.create_user(email=email,
            password=encrypt_password(password), active=active)
        db.session.commit()


if __name__ == '__main__':
    manager.run()
