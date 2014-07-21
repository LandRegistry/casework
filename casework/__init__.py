import os, logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.from_object(os.environ.get('SETTINGS'))

CsrfProtect(app)

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.logger.info("\nConfiguration\n%s\n" % app.config)

# govuk_template asset path
@app.context_processor
def asset_path_context_processor():
    return {'asset_path': '/static/govuk_template/'}

db = SQLAlchemy(app)
