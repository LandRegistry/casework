import logging
import requests
from audit import Audit

from flask import render_template, request, redirect, flash
from flask_login import login_required

from application import app, Health, db
from application.frontend.forms import RegistrationForm
from application.frontend.title_number_generator import generate_title_number
from application.mint.mint import post_to_mint
from application.cases import get_cases, complete_case

Health(app, checks=[db.health])
Audit(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    form = RegistrationForm(request.form, country='GB')
    property_frontend_url = '%s/%s' % (app.config['PROPERTY_FRONTEND_URL'], 'property')
    created = request.args.get('created', None)

    if request.method == 'GET':
        form.title_number.data = generate_title_number()

    if request.method == 'POST' and form.validate():
        mint_data = form.to_dict()
        title_number = form.title_number.data

        try:
            response = post_to_mint(app.config['MINT_URL'], mint_data)
            response.raise_for_status()

            return redirect('%s?created=%s' % ('/registration', title_number))
        except requests.exceptions.HTTPError as e:
            app.logger.error("HTTP Error %s", e)
            raise e
        except requests.exceptions.ConnectionError as e:
            app.logger.error("Error %s", e)
            raise e

        except RuntimeError as e:
            app.logger.error('Failed to register title %s: Error %s' % (title_number, e))
            flash('Creation of title with number %s failed' % title_number)

    return render_template('registration.html',
                           form=form,
                           property_frontend_url=property_frontend_url,
                           title_number=form.title_number.data,
                           created=created)

@app.route('/checks', methods=['GET'])
@login_required
def get_checks():
    checks = get_cases('check')
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

# @app.before_request()
# def log_request():
#     log the request

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
