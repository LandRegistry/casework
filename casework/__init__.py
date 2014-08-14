from flask.ext.basicauth import BasicAuth
from flask.ext.login import LoginManager
from flask.ext.security import SQLAlchemyUserDatastore, Security
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from raven.contrib.flask import Sentry
import logging
import os


app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

login_manager = LoginManager()
login_manager.init_app(app)

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

if app.config.get('BASIC_AUTH_USERNAME'):
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)

# Sentry exception reporting
if 'SENTRY_DSN' in os.environ:
    sentry = Sentry(app, dsn=os.environ['SENTRY_DSN'])

csrf = CsrfProtect()
csrf.init_app(app)

app.logger.info("\nConfiguration\n%s\n" % app.config)


def health(self):
    try:
        with self.engine.connect() as c:
            c.execute('select 1=1').fetchall()
            return True, 'DB'
    except:
        return False, 'DB'

db = SQLAlchemy(app)
SQLAlchemy.health = health

from .models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

