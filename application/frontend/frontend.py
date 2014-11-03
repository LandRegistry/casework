import logging
from audit import Audit

from flask import render_template
from flask_login import login_required

from application import app, Health, db
from datetime import datetime

Health(app, checks=[db.health])
Audit(app)

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


@app.errorhandler(Exception)
def catch_all_exceptions(error):
    return render_template('error.html', error=error), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error=error), 500


# Some useful headers to set to beef up the robustness of the app
# https://www.owasp.org/index.php/List_of_useful_HTTP_headers
@app.after_request
def after_request(response):
    response.headers.add('Content-Security-Policy',
                         "default-src 'self' 'unsafe-inline' data: http://maxcdn.bootstrapcdn.com")
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
