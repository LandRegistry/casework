from flask import render_template, redirect, url_for, flash, abort
from casework import app
from .mint import Mint
from registrationform import RegistrationForm
import json

mint = Mint()

@app.route('/', methods=('GET', 'POST'))
def index():
    form = RegistrationForm()
    return render_template("title_registration.html", form = form)

@app.route('/title', methods=['POST'])
def new_title():
    form = RegistrationForm()

    mint_data =  json.dumps({
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

    if form.validate_on_submit():
        title_number = form['title_number'].data
        response = mint.post(title_number, mint_data)
        if response.status_code == 200:
            flash('Succesfully created title with number %s'  % title_number)
            return redirect(url_for('index'))
        else:
            abort(response.status_code)
    else:
        return render_template('error.html', error = "validation error")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error = error), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error = error), 500

@app.route('/success')
@app.route('/success/<title_number>')
def success(title_number=None):
    return render_template("success.html", title_number = title_number)

#  Some useful headers to set to beef up the robustness of the app
# https://www.owasp.org/index.php/List_of_useful_HTTP_headers
@app.after_request
def after_request(response):
    response.headers.add('Content-Security-Policy', "default-src 'self' 'unsafe-inline' data:")
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
