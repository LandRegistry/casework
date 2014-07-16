from flask import render_template
from flask import request
from casework import app
from .mint import Mint
from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

mint = Mint()

@app.route('/', methods=('GET', 'POST'))
def index():
    form = IndexForm()
    return render_template("index.html", form = form)

@app.route('/new_title/', methods=['POST'])
def new_title():
    form = IndexForm()
    if form.validate_on_submit():
        return 'its ok '#'redirect('/success/' + request.form['titleNumber'])
    mint_string = request.form['titleNumber'] + ':' + request.form['titleJSON']
    response = mint.post({"title_number" : request.form['titleNumber'], "foo":"bar"})
    print "RESPONSE", response
    return mint_string

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error = error), 404

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

class IndexForm(Form):
    titleNumber = TextField('titleNumber', validators=[DataRequired()])
