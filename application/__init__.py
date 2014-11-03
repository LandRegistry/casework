from flask.ext.basicauth import BasicAuth
from flask.ext.login import LoginManager
from flask.ext.security import SQLAlchemyUserDatastore, Security
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask_wtf import CsrfProtect
from raven.contrib.flask import Sentry
import logging
import os
from application.health import Health
from lrutils import dateformat, datetimeformat
from application.casework.views import casework_blueprint
from application.checks.views import checks_blueprint


app = Flask('application.frontend')
app.config.from_object(os.environ.get('SETTINGS'))

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['dateformat'] = dateformat

app.register_blueprint(casework_blueprint)
app.register_blueprint(checks_blueprint)

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

app.logger.debug("\nConfiguration\n%s\n" % app.config)


def health(self):
    try:
        with self.engine.connect() as c:
            c.execute('select 1=1').fetchall()
            return True, 'DB'
    except:
        return False, 'DB'

db = SQLAlchemy(app)
SQLAlchemy.health = health

from application.frontend.login_model import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


