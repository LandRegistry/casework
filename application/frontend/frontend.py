import logging

from flask import render_template
from flask_login import login_required

from application import app, Health, db
from datetime import datetime

Health(app, checks=[db.health])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

# a few date-related Jinja2 filters until until date transport and storage type can be established
def format_time(dt):
    norm = datetime.fromtimestamp(dt)
    return datetime.strftime(norm, '%d-%m-%Y')

def country_lookup_filter(iso):
    from datatypes.validators.iso_country_code_validator import countries
    country = countries.get(alpha2=iso).name
    return country

app.jinja_env.filters['country_lookup'] = lambda iso : country_lookup_filter(iso)
app.jinja_env.filters['format_time'] = lambda dt : format_time(dt)

@app.route('/')
@login_required
def index():
    return render_template("index.html")