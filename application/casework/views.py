from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


casework_blueprint = Blueprint('casework_blueprint', __name__, template_folder='../frontend/templates', url_prefix='/sp')

# @casework_blueprint.route('/', defaults={'page': 'index'})
# @casework_blueprint.route('/<page>')
@casework_blueprint.route('/yo')
# def show(page):
def show():
    try:
        return render_template('success.html')
    except TemplateNotFound:
        abort(404)
