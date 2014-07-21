from flask import render_template, redirect, url_for, flash, abort, request
from casework import app
from .mint import Mint
from flask_wtf import Form
from .generate_title_number import TitleNumber
from forms import RegistrationForm
import json

mint = Mint()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration', methods=['GET','POST'])
def registration():


    title_class = TitleNumber()
    form = RegistrationForm(request.form)
    success_url = None

    if request.method == 'POST' and form.validate():

        mint_data = form_to_json(form)
        title_number = form['title_number'].data
        try:
            response = mint.post(title_number, mint_data)
            app.logger.info('Created title number %s at the mint url %s: status code %d'
                            % (title_number, response.url, response.status_code))
            success_url = '%s/property/%s' % (app.config['PROPERTY_FRONTEND_URL'], title_number)
        except RuntimeError as e:
            app.logger.error('Failed to register title %s: Error %s' % (title_number, e))
            flash('Creation of title with number %s failed' % title_number)

    return render_template('registration.html', form=form, success_url=success_url, title_number=title_class.getTitleNumber())

def form_to_json(form):
    data = json.dumps({
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
          "postcode": form['postcode'].data
        },
        "tenure": form['property_tenure'].data,
        "class_of_title":  form['property_class'].data
      },
      "payment": {
        "price_paid": form['price_paid'].data,
        "titles":[
          form['title_number'].data
        ]
      }
    })
    return data

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
    response.headers.add('Content-Security-Policy', "default-src 'self' 'unsafe-inline' data:")
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
