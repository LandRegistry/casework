import logging

from flask import render_template, abort
from flask_login import login_required
from functools import wraps

from application import app, Health, db
from application.cases import get_cases, complete_case
from datetime import datetime
from lrutils.audit import Audit
from lrutils.errorhandler.errorhandler_utils import ErrorHandler, eh_after_request

Health(app, checks=[db.health])
Audit(app)
ErrorHandler(app)
app.after_request(eh_after_request)
# app.errorhandler(eh_error_handler)

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
