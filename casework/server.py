from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
from casework import app
from .mint import Mint
from flask_wtf import Form
from registrationform import RegistrationForm
from json import JSONEncoder
from .generate_title_number import TitleNumber

mint = Mint()

@app.route('/', methods=('GET', 'POST'))
def index():
    form = RegistrationForm()
    title_class = TitleNumber()
    return render_template("index.html", form = form, title_number =
      title_class.getTitleNumber() )

@app.route('/new_title/', methods=['POST'])
def new_title():
    form = RegistrationForm()
    mint_JSON =  JSONEncoder().encode({
      "title_id":request.form['titleNumber'],
      "proprietors":[
        {
          "first_name":request.form['firstName1'],
          "last_name":request.form['surname1']
        },
        {
          "first_name":request.form['firstName2'],
          "last_name":request.form['surname2']
        }
      ],
      "property":{
        "address": {
          "house_number": request.form['houseNumber'],
          "road": request.form['road'],
          "town": request.form['town'],
          "postcode": request.form['postcode']
        },
        "tenure": request.form['tenure'],
        "class_of_title": request.form['class']
      },
      "payment": {
        "price_paid": request.form['pricePaid'],
        "titles":[
          request.form['titleNumber']
        ]
      }
    })

    if form.validate_on_submit():
      response = mint.post(mint_JSON)
      if response.status_code == 200:
        return redirect(url_for('success', title_number = request.form['titleNumber']))
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
