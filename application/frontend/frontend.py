from sqlite3 import IntegrityError
from audit import Audit

from flask import current_app, render_template, request, redirect, flash
from flask_login import login_required

from application import app, Health, db
from application.frontend.forms import RegistrationForm
from application.frontend.title_number_generator import generate_title_number
from application.mint.mint import post_to_mint
from application.checks import service as check_service
from application.casework.service import get_casework_items, save_casework

Health(app, checks=[db.health])
Audit(app)

@app.route('/')
# TODO: Figure out how to login from the tests
@login_required
def index():
    return render_template("index.html")


@app.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    form = RegistrationForm(request.form)
    property_frontend_url = '%s/%s' % (current_app.config['PROPERTY_FRONTEND_URL'], 'property')

    if request.method == 'GET':
        form.title_number.data = generate_title_number()

    if form.validate_on_submit():
        mint_data = form.to_dict()
        try:
            post_to_mint(current_app.config['MINT_URL'], mint_data)
            return redirect('%s?created=%s' % ('/registration', mint_data['title_number']))
        except RuntimeError as e:
            current_app.logger.error('Failed to register title %s: Error %s' % (mint_data['title_number'], e))
            flash('Creation of title with number %s failed' % mint_data['title_number'])

    return render_template('registration.html',
                           form=form,
                           property_frontend_url=property_frontend_url,
                           title_number=form.title_number.data,
                           created=request.args.get('created', None))

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
        save_casework(request.data)
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

