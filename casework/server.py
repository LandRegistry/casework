from flask import render_template
from flask import request

from casework import app


# govuk_template asset path
@app.context_processor
def asset_path_context_processor():
    return {'asset_path': '/static/govuk_template/'}

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/new_title/', methods=['POST'])
def new_title():

  if request.method == 'POST':
    mint_string = request.form['titleNumber'] + ':' + request.form['titleJSON']
    return mint_string



#  Some useful headers to set to beef up the robustness of the app
# https://www.owasp.org/index.php/List_of_useful_HTTP_headers
@app.after_request
def after_request(response):
    response.headers.add('Content-Security-Policy', "default-src 'self' 'unsafe-inline' data:")
    response.headers.add('X-Frame-Options', 'deny')
    response.headers.add('X-Content-Type-Options', 'nosniff')
    response.headers.add('X-XSS-Protection', '1; mode=block')
    return response
