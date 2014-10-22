import logging
from audit import Audit

from flask import render_template
from flask_login import login_required

from application import app, Health, db
from application.cases import get_cases, complete_case
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


@app.route('/checks', methods=['GET'])
@login_required
def get_checks():
    checks = get_cases('checks')
    logging.info("check_items:: %s" % checks)
    return render_template("checks.html", checks=checks)


@app.route('/casework', methods=['GET'])
@login_required
def get_casework():
    casework_items = get_cases('casework')
    return render_template("casework.html", casework_items=casework_items)

@app.route("/complete-case/<case_id>", methods=['POST'])
def complete_case_item(case_id):
    logging.info("POST complete-case:"+case_id)
    response = complete_case(case_id)
    if response.status_code == 200:
        return get_casework()
    else:
       return response

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
