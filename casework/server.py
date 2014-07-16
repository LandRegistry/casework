from flask import render_template
from flask import request
from casework import app
from .mint import Mint

mint = Mint()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/new_title/', methods=['POST'])
def new_title():
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
