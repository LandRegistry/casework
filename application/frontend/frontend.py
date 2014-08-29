import logging
from sqlalchemy.exc import IntegrityError
from audit import Audit

from flask import render_template, request, redirect, flash
from flask_login import login_required

from application import app, Health, db
from application.frontend.forms import RegistrationForm
from application.frontend.title_number_generator import generate_title_number
from application.mint.mint import post_to_mint
from application.checks import service as check_service
from application.casework.service import get_casework_items, save_casework

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
    form = RegistrationForm(request.form)
    property_frontend_url = '%s/%s' % (app.config['PROPERTY_FRONTEND_URL'], 'property')
    created = request.args.get('created', None)

    if request.method == 'GET':
        form.title_number.data = generate_title_number()

    if request.method == 'POST' and form.validate():
        mint_data = form.to_dict()
        title_number = form.title_number.data

        try:
            response = post_to_mint(app.config['MINT_URL'], mint_data)
            if response.status_code == 400:
                return 'Failed to save to mint', 400
            else:
                return redirect('%s?created=%s' % ('/registration', title_number))
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
    check_items = check_service.get_check_items()

    return render_template("checks.html", checks=check_items)

@app.route('/checks', methods=['POST'])
def post_checks():
    try:
        check_service.save_checks(request.json)
    except IntegrityError:
        return 'Failed to save', 400
    except KeyError:
        return 'Invalid data', 400

    return 'OK', 200


@app.route('/casework', methods=['GET'])
@login_required
def get_casework():
    casework_items = get_casework_items()
    return render_template("casework.html", casework_items=casework_items)

@app.route('/casework', methods=['POST'])
def casework_post():
    try:
        save_casework(request.json)
    except IntegrityError:
        return 'Failed to save casework item.', 400
    except KeyError:
        return 'Invalid data', 400

    return 'OK', 200


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
