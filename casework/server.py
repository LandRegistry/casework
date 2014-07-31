from flask import render_template, request, flash, redirect, url_for, request_started
from casework import app
from .mint import Mint
from forms import RegistrationForm
import simplejson
import random
from healthcheck import HealthCheck
from flask.ext.login import current_user

mint = Mint(app.config['MINT_URL'])
HealthCheck(app, '/health')


def audit(sender, **extra):
    id = current_user.get_id()
    if id:
        sender.logger.info('Audit: user=[%s], request=[%s]' % (id, request))
    else:
        sender.logger.info('Audit: user=[anon], request=[%s]' % request)

request_started.connect(audit, app)

def generate_title_number():
    return 'TEST%d' % random.randint(1, 9999)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration', methods=['GET','POST'])
def registration():

    form = RegistrationForm(request.form)
    property_frontend_url = '%s/%s' % (app.config['PROPERTY_FRONTEND_URL'], 'property')
    created = request.args.get('created', None)

    if  request.method == 'GET':
      #put the title number into the form's hidden field
      form.title_number.data = generate_title_number()

    if request.method == 'POST' and form.validate():
        mint_data = form_to_json(form)
        title_number = form['title_number'].data
        try:
            response = mint.post(title_number, mint_data)
            app.logger.info('Created title number %s at the mint url %s: status code %d'
                            % (title_number, response.url, response.status_code))

            return redirect('%s?created=%s' % (url_for('registration'), title_number))

        except RuntimeError as e:
            app.logger.error('Failed to register title %s: Error %s' % (title_number, e))
            flash('Creation of title with number %s failed' % title_number)

    return render_template('registration.html', form=form, property_frontend_url=property_frontend_url,
              title_number=form.title_number.data, created=created)

def form_to_json(form):
    data = simplejson.dumps({
      "title_number": form['title_number'].data,
      "proprietors":[
        {
          "first_name": form['first_name1'].data,
          "last_name": form['surname1'].data #can we sort names out please? not have last_name and surname2?
        },
        {
          "first_name": form['first_name2'].data,
          "last_name": form['surname2'].data
        }
      ],
      "property":{

        "address": {
          "house_number": form['house_number'].data,
          "road": form['road'].data,
          "town": form['town'].data,
          "postcode": _format_postcode(form['postcode'].data)
        },
        "tenure": form['property_tenure'].data,
        "class_of_title":  form['property_class'].data
      },
      "payment": {
        "price_paid": form['price_paid'].data,
        "titles":[
          form['title_number'].data
        ]
      },
      "extent": form['extent'].data
    })
    return data

def _format_postcode(postcode):
    out = postcode.upper()
    if ' ' not in postcode:
        i = len(postcode) - 3
        out = out[:i] + ' ' + out[i:]

    return out


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error = error), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error = error), 500

#  Some useful headers to set to beef up the robustness of the app
# https://www.owasp.org/index.php/List_of_useful_HTTP_headers
@app.after_request
def after_request(response):
    response.headers.add('Content-Security-Policy', "default-src 'self' 'unsafe-inline' data: http://maxcdn.bootstrapcdn.com")
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
