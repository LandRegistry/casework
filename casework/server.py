from sqlalchemy.exc import IntegrityError
from flask.ext.security import login_required
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from audit import Audit

import models
from casework import csrf
from casework import app
from casework import db
from casework.title_number_generator import generate_title_number
from .health import Health
from .mint import Mint
from forms import RegistrationForm


mint = Mint(app.config['MINT_URL'])
Health(app, checks=[db.health])
Audit(app)


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/casework', methods=['POST'])
def casework_post():
    data = request.json
    casework_model = models.Casework()

    try:
        casework_model.title_number = data['title_number']
        casework_model.application_type = data['application_type']
    except KeyError:
        return 'Could not find expected keys in data', 400

    try:
        db.session.add(casework_model)
        db.session.commit()
    except IntegrityError:
        return 'Failed to save', 400

    return 'OK', 200


@app.route('/casework', methods=['GET'])
@login_required
@csrf.exempt
def casework_get():
   casework_items = models.Casework.query.order_by(models.Casework.submitted_at).all()
   return render_template("casework.html", casework_items=casework_items)

@app.route('/checks', methods=['POST'])
def checks_post():
    data = request.json
    check = models.Check()

    try:
        check.title_number = data['title_number']
        check.application_type = data['application_type']
    except KeyError:
        return 'Could not find expected keys in data', 400

    try:
        db.session.add(check)
        db.session.commit()
    except IntegrityError:
        return 'Failed to save', 400

    return 'OK', 200


@csrf.exempt
@app.route('/checks', methods=['GET'])
@login_required
def checks_get():
    return render_template("checks.html", checks=(models.Check.query.order_by(models.Check.submitted_at).all()))


@app.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    form = RegistrationForm(request.form)
    property_frontend_url = '%s/%s' % (app.config['PROPERTY_FRONTEND_URL'], 'property')
    created = request.args.get('created', None)

    if request.method == 'GET':
        form.title_number.data = generate_title_number()

    if request.method == 'POST' and form.validate():
        mint_data = form.to_json()
        title_number = form['title_number'].data

        try:
            mint.post(title_number, mint_data)
            return redirect('%s?created=%s' % (url_for('registration'), title_number))
        except RuntimeError as e:
            app.logger.error('Failed to register title %s: Error %s' % (title_number, e))
            flash('Creation of title with number %s failed' % title_number)

    return render_template('registration.html',
                           form=form,
                           property_frontend_url=property_frontend_url,
                           title_number=form.title_number.data,
                           created=created)


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
